#!/usr/bin/env python3
"""Pilot 0 registry builder: claims -> embeddings -> incremental clustering
-> idea registry. Run under .venv-ml (arm64: torch/MPS + faiss).

Stages (each cached, resume-safe):
  collect  — gather per-doc claims from the extraction cache -> claims.parquet
  embed    — encode unique claim texts (BGE-small-en-v1.5, 384-dim, L2-normed)
             -> embeddings.npy (+ claim_texts.json order)
  cluster  — time-ordered incremental clustering vs registry centroids.
             cos >= auto_hi: merge (alias). cos in [gray_lo, auto_hi): GRAY —
             logged for adjudication (Pilot 0: counted + sampled, adjudication
             wiring lands before any registry is called final). Else: new idea.
  report   — registry stats + samples for the sanity eyeball.

Registry semantics: idea_id = first claim (by doc time) that started the
cluster; centroid = running mean of member embeddings (re-normed).
Polarity caveat (logged): embedding cosine cannot distinguish negation;
auto_hi merges may join opposite-polarity claims. Pilot 0 measures the rate
(gray + auto samples in the report); the fix (adjudicate-all-merges) is a
Pilot 1 gate, not a Pilot 0 blocker.
"""
import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("REGISTRY_OUT", os.path.join(ROOT, "data", "registry", "pilot0"))
EXTRACTOR_ID = os.environ.get("REGISTRY_EXTRACTOR", "deepseek-v4-flash-nothink_ptitles1_svt1")
EMBED_MODEL = "BAAI/bge-small-en-v1.5"   # 2023 release; predates all eval windows
AUTO_HI = 0.95
GRAY_LO = 0.85

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def stage_collect() -> None:
    import duckdb
    import glob
    out = os.path.join(OUT, "claims.parquet")
    if os.path.exists(out):
        print("collect: cached")
        return
    import re
    fence = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)

    def rec_claims(rec: dict) -> list[str]:
        if "claims" in rec:                      # titles-conveyor shape
            return rec["claims"]
        m = fence.match(rec.get("raw", ""))      # doc-conveyor shape: parse raw
        try:
            data = json.loads(m.group(1) if m else rec["raw"])
        except (json.JSONDecodeError, KeyError):
            return []
        out = []
        for c in data.get("claims", []) if isinstance(data, dict) else []:
            if isinstance(c, dict) and isinstance(c.get("claim"), str):
                out.append(c["claim"])           # lenient: extras/null quotes ignored
        return out

    rows = []
    shards = glob.glob(os.path.join(ROOT, "data", "extractions", EXTRACTOR_ID, "*", "*.json"))
    print(f"collect: {len(shards)} cached docs ({EXTRACTOR_ID})")
    for path in shards:
        rec = json.load(open(path))
        for c in rec_claims(rec):
            rows.append((rec["doc_id"], c))
    import pyarrow as pa
    import pyarrow.parquet as pq
    con = duckdb.connect()
    t = pa.table({"doc_id": [r[0] for r in rows], "claim": [r[1] for r in rows]})
    con.register("claims_raw", t)
    years = os.environ.get("REGISTRY_YEARS", "")  # e.g. "2015,2016,2017"; empty = all
    year_filter = f"AND year(d.time) IN ({years})" if years else ""
    times = con.sql(f"""
        SELECT c.doc_id, c.claim, d.time FROM claims_raw c
        JOIN read_parquet('{ROOT}/data/docs/docs_*.parquet') d ON c.doc_id = d.doc_id
        WHERE 1=1 {year_filter}
        ORDER BY d.time, c.doc_id
    """).arrow()
    if hasattr(times, "read_all"):
        times = times.read_all()
    pq.write_table(times, out, compression="zstd")
    print(f"collect: {times.num_rows} claims from {len(shards)} docs")


def stage_embed(batch_size: int = 256) -> None:
    import pyarrow.parquet as pq
    emb_path = os.path.join(OUT, "embeddings.npy")
    txt_path = os.path.join(OUT, "claim_texts.json")
    if os.path.exists(emb_path):
        print("embed: cached")
        return
    claims = pq.read_table(os.path.join(OUT, "claims.parquet"))["claim"].to_pylist()
    uniq = list(dict.fromkeys(claims))  # preserve first-seen order
    print(f"embed: {len(uniq)} unique texts of {len(claims)} claims")
    from sentence_transformers import SentenceTransformer
    import torch
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer(EMBED_MODEL, device=device)
    vecs = model.encode(uniq, batch_size=batch_size, normalize_embeddings=True,
                        show_progress_bar=True)
    with open(emb_path + ".tmp", "wb") as f:  # atomic: partial write never caches
        np.save(f, vecs.astype(np.float32))
    os.replace(emb_path + ".tmp", emb_path)
    json.dump(uniq, open(txt_path, "w"))
    print(f"embed: {vecs.shape} saved")


def stage_cluster() -> None:
    import faiss
    import pyarrow.parquet as pq
    reg_path = os.path.join(OUT, "registry.json")
    if os.path.exists(reg_path):
        print("cluster: cached")
        return
    vecs = np.load(os.path.join(OUT, "embeddings.npy"))
    texts = json.load(open(os.path.join(OUT, "claim_texts.json")))
    vec_of = {t: i for i, t in enumerate(texts)}
    table = pq.read_table(os.path.join(OUT, "claims.parquet"))
    doc_ids = table["doc_id"].to_pylist()
    claims = table["claim"].to_pylist()
    times = table["time"].to_pylist()

    dim = vecs.shape[1]
    if os.environ.get("CLUSTER_INDEX", "flat") == "hnsw":
        # approximate: ~N log N. Certify against an exact run before trusting
        # a registry built this way (recall misses compound sequentially).
        index = faiss.IndexHNSWFlat(dim, 32, faiss.METRIC_INNER_PRODUCT)
        index.hnsw.efConstruction = 200
        index.hnsw.efSearch = 64
        print("cluster: HNSW index (approximate)", flush=True)
    else:
        index = faiss.IndexFlatIP(dim)      # exact search; rebuilt-free adds
    centroids: list[np.ndarray] = []        # running sums (unnormalized)
    counts: list[int] = []
    ideas: list[dict] = []                  # idea_id -> canonical, first_seen, n
    assign: list[int] = []                  # per claim row -> idea_id
    gray: list[tuple[int, int, float]] = [] # (claim_row, idea_id, cos)

    batch_size = int(os.environ.get("CLUSTER_BATCH", "1"))

    def found_idea(row: int, claim: str, t, v: np.ndarray) -> int:
        idea = len(ideas)
        ideas.append({"idea_id": idea, "canonical": claim,
                      "first_seen": str(t), "n": 0})
        centroids.append(v.copy())
        counts.append(0)
        return idea

    if batch_size > 1:
        # Batched variant — semantics IDENTICAL to sequential: every claim is
        # matched against exactly the founders that precede it (frozen index
        # for prior batches + in-batch founders created before it). Batch
        # searches use all cores via faiss's internal OpenMP.
        # Resumable: atomic checkpoint every ~100K claims; status.json is the
        # live progress interface (cat it for row/rate/eta).
        import time as _time
        ckpt_path = os.path.join(OUT, "cluster_ckpt.npz")
        ckpt_ideas = os.path.join(OUT, "cluster_ckpt_ideas.json")
        status_path = os.path.join(OUT, "status.json")
        resume_row = 0
        if os.path.exists(ckpt_path):
            ck = np.load(ckpt_path, allow_pickle=False)
            assign.extend(int(x) for x in ck["assign"])
            gray.extend((int(a), int(b), float(c)) for a, b, c in ck["gray"])
            ideas.extend(json.load(open(ckpt_ideas)))
            resume_row = int(ck["next_row"])
            index.add(np.stack([vecs[vec_of[i["canonical"]]] for i in ideas]))
            centroids.extend(np.zeros(dim) for _ in ideas)  # accumulators only
            counts.extend(0 for _ in ideas)
            print(f"cluster: RESUMED at row {resume_row} "
                  f"({len(ideas)} ideas, {len(gray)} gray)", flush=True)

        def checkpoint(next_row: int) -> None:
            np.savez(ckpt_path + ".tmp.npz",
                     assign=np.array(assign, dtype=np.int64),
                     gray=np.array(gray, dtype=np.float64).reshape(len(gray), 3)
                     if gray else np.zeros((0, 3)),
                     next_row=np.int64(next_row))
            os.replace(ckpt_path + ".tmp.npz", ckpt_path)
            json.dump(ideas, open(ckpt_ideas + ".tmp", "w"))
            os.replace(ckpt_ideas + ".tmp", ckpt_ideas)

        t0 = _time.time()
        done0 = resume_row

        def write_status(row_now: int) -> None:
            rate = (row_now - done0) / max(_time.time() - t0, 1e-9)
            remaining = len(doc_ids) - row_now
            json.dump({"row": row_now, "total": len(doc_ids),
                       "ideas": len(ideas), "gray": len(gray),
                       "claims_per_sec": round(rate, 1),
                       "eta_min": round(remaining / max(rate, 1e-9) / 60, 1)},
                      open(status_path + ".tmp", "w"))
            os.replace(status_path + ".tmp", status_path)

        rows = list(zip(doc_ids, claims, times))
        for start in range(resume_row, len(rows), batch_size):
            chunk = rows[start:start + batch_size]
            V = np.stack([vecs[vec_of[c]] for _, c, _ in chunk])
            if index.ntotal:
                D, NN = index.search(V, 1)
            else:
                D = np.full((len(chunk), 1), -1.0, dtype=np.float32)
                NN = np.full((len(chunk), 1), -1, dtype=np.int64)
            new_vecs = []          # founders created in this batch
            new_ids = []
            for k, (doc_id, claim, t) in enumerate(chunk):
                row = start + k
                cos, nn = float(D[k, 0]), int(NN[k, 0])
                # also consider in-batch founders created before this claim
                if new_vecs:
                    sims = np.asarray(new_vecs) @ V[k]
                    j = int(np.argmax(sims))
                    if float(sims[j]) > cos:
                        cos, nn = float(sims[j]), new_ids[j]
                idea = -1
                if nn >= 0 and cos >= AUTO_HI:
                    idea = nn
                elif nn >= 0 and cos >= GRAY_LO:
                    gray.append((row, nn, round(cos, 4)))
                if idea < 0:
                    idea = found_idea(row, claim, t, V[k])
                    new_vecs.append(V[k])
                    new_ids.append(idea)
                else:
                    centroids[idea] += V[k]
                    counts[idea] += 1
                ideas[idea]["n"] += 1
                assign.append(idea)
            if new_vecs:
                index.add(np.stack(new_vecs))
            if start and start % 50_000 < batch_size:
                write_status(start + len(chunk))
                print(f"cluster: {start + len(chunk)} claims -> {len(ideas)} ideas, "
                      f"{len(gray)} gray", flush=True)
            if start and start % 100_000 < batch_size:
                checkpoint(start + len(chunk))
        checkpoint(len(rows))
        write_status(len(rows))
    else:
        for row, (doc_id, claim, t) in enumerate(zip(doc_ids, claims, times)):
            v = vecs[vec_of[claim]]
            idea = -1
            if index.ntotal:
                cos, nn = index.search(v[None, :], 1)
                cos, nn = float(cos[0, 0]), int(nn[0, 0])
                if cos >= AUTO_HI:
                    idea = nn
                elif cos >= GRAY_LO:
                    gray.append((row, nn, round(cos, 4)))
            if idea < 0:
                idea = found_idea(row, claim, t, v)
                index.add(v[None, :])
            else:
                centroids[idea] += v
                counts[idea] += 1
            ideas[idea]["n"] += 1
            assign.append(idea)
            if row and row % 50_000 == 0:
                print(f"cluster: {row} claims -> {len(ideas)} ideas, {len(gray)} gray",
                      flush=True)  # flush: piped runs must not go blind (2026-08-29)

    json.dump(ideas, open(reg_path, "w"))
    np.save(os.path.join(OUT, "assignments.npy"), np.array(assign, dtype=np.int64))
    json.dump(gray, open(os.path.join(OUT, "gray_pairs.json"), "w"))
    print(f"cluster: {len(claims)} claims -> {len(ideas)} ideas, "
          f"{len(gray)} gray-zone pairs")


def stage_report() -> None:
    ideas = json.load(open(os.path.join(OUT, "registry.json")))
    gray = json.load(open(os.path.join(OUT, "gray_pairs.json")))
    ns = sorted((i["n"] for i in ideas), reverse=True)
    total = sum(ns)
    singletons = sum(1 for n in ns if n == 1)
    print(f"ideas: {len(ideas)} | claim instances: {total}")
    print(f"singleton ideas: {singletons} ({singletons / len(ideas):.0%})")
    print(f"top-10 idea sizes: {ns[:10]}")
    print(f"gray-zone pairs (adjudication backlog): {len(gray)}")
    print("\n-- top ideas by frequency --")
    for i in sorted(ideas, key=lambda x: -x["n"])[:25]:
        print(f"  [{i['n']:5d}] {i['canonical'][:100]}")


STAGES = {"collect": stage_collect, "embed": stage_embed,
          "cluster": stage_cluster, "report": stage_report}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stages", nargs="*", default=list(STAGES))
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    stages = args.stages or list(STAGES)
    # torch (embed) and faiss (cluster) crash macOS when loaded in one
    # process (duplicate libomp) — the crash is silent behind a pipe. Run
    # each stage in its own subprocess when more than one was requested.
    if len(stages) > 1:
        import subprocess
        for s in stages:
            subprocess.run([sys.executable, os.path.abspath(__file__), s],
                           check=True, env=os.environ)
        return
    for s in stages:
        STAGES[s]()


if __name__ == "__main__":
    main()
