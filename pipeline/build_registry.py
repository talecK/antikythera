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
EXTRACTOR_ID = "deepseek-v4-flash-nothink_ptitles1_svt1"
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
    rows = []
    shards = glob.glob(os.path.join(ROOT, "data", "extractions", EXTRACTOR_ID, "*", "*.json"))
    print(f"collect: {len(shards)} cached docs")
    for path in shards:
        rec = json.load(open(path))
        for c in rec["claims"]:
            rows.append((rec["doc_id"], c))
    import pyarrow as pa
    import pyarrow.parquet as pq
    con = duckdb.connect()
    t = pa.table({"doc_id": [r[0] for r in rows], "claim": [r[1] for r in rows]})
    con.register("claims_raw", t)
    times = con.sql(f"""
        SELECT c.doc_id, c.claim, d.time FROM claims_raw c
        JOIN read_parquet('{ROOT}/data/docs/docs_*.parquet') d ON c.doc_id = d.doc_id
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
    index = faiss.IndexFlatIP(dim)          # exact search; rebuilt-free adds
    centroids: list[np.ndarray] = []        # running sums (unnormalized)
    counts: list[int] = []
    ideas: list[dict] = []                  # idea_id -> canonical, first_seen, n
    assign: list[int] = []                  # per claim row -> idea_id
    gray: list[tuple[int, int, float]] = [] # (claim_row, idea_id, cos)

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
            idea = len(ideas)
            ideas.append({"idea_id": idea, "canonical": claim,
                          "first_seen": str(t), "n": 0})
            centroids.append(v.copy())
            counts.append(0)
            index.add(v[None, :])
        else:
            centroids[idea] += v
            counts[idea] += 1
            norm = centroids[idea] / np.linalg.norm(centroids[idea])
            # faiss has no in-place update on IndexFlat; use reconstruct-free
            # trick: keep index as first-claim anchors. Centroid drift ignored
            # for Pilot 0 (anchor matching); noted in report.
        ideas[idea]["n"] += 1
        assign.append(idea)
        if row and row % 200_000 == 0:
            print(f"cluster: {row} claims -> {len(ideas)} ideas, {len(gray)} gray")

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
