#!/usr/bin/env python3
"""Pilot 1 eval: gap ranking vs baselines, precision-at-k on edge formation.

Inputs (from REGISTRY_OUT, built over build+eval years):
  claims.parquet (doc_id, claim, time), assignments.npy, registry.json,
  embeddings.npy + claim_texts.json (for idea centroids / affinity)
Plus docs parquet for per-doc author lists.

All ranker inputs are computed from docs with time < eval_start (leakage
guard asserts). Edge formation is computed only in [eval_start, eval_end).

Parameters come from preregistration.md — run with --prereg to assert the
file's REGISTERED marker is present before any eval output is produced.

Definitions (pre-registered):
- Idea frequency: distinct docs mentioning the idea in the build window,
  exponentially decayed with half-life H days to eval_start.
- Eligible pair: both ideas' RAW distinct-doc counts >= F in build window;
  never co-mentioned in ANY build-window doc; centroid cosine >= A.
- z-score: for pair (i,j): expected co-doc count E = N * p_i * p_j over
  build docs; z = (obs - E) / sqrt(E). Gaps have obs=0 -> z = -sqrt(E).
- Gap score: decayed_freq_i * decayed_freq_j * affinity * |z|.
- Edge forms: >= M docs in eval window co-mention the pair, with >= M
  distinct story authors among those docs (independent-author adoption).
- P@k over the pre-registered k values, all rankers on the SAME eligible set.
"""
import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("REGISTRY_OUT", os.path.join(ROOT, "data", "registry", "pilot1"))

# ---- pre-registered parameters (mirror preregistration.md) ----
EVAL_START = "2017-01-01"
EVAL_END = "2018-01-01"
HALF_LIFE_DAYS = 365.0
FREQ_FLOOR = 10          # F: min distinct build docs per idea
AFFINITY_MIN = 0.55      # A: min centroid cosine
MIN_ADOPTERS = 2         # M: co-mentioning docs AND distinct story authors
K_VALUES = [50, 200, 1000]
RNG_SEED = 20260829


def load_doc_ideas():
    con = duckdb.connect()
    t = con.sql(f"""
        SELECT c.doc_id, c.time, d."by" AS author
        FROM read_parquet('{OUT}/claims.parquet') c
        JOIN (SELECT doc_id, any_value(authors[1]) AS "by"
              FROM read_parquet('{ROOT}/data/docs/docs_*.parquet') GROUP BY doc_id) d
          ON c.doc_id = d.doc_id
    """).fetchall()
    assign = np.load(os.path.join(OUT, "assignments.npy"))
    rows = defaultdict(set)          # doc_id -> idea set
    doc_time, doc_author = {}, {}
    for (doc_id, ts, author), idea in zip(t, assign):
        rows[doc_id].add(int(idea))
        doc_time[doc_id] = ts
        doc_author[doc_id] = author
    return rows, doc_time, doc_author


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prereg", action="store_true",
                    help="require REGISTERED marker in preregistration.md")
    args = ap.parse_args()
    prereg = open(os.path.join(ROOT, "preregistration.md")).read()
    if args.prereg and "STATUS: REGISTERED" not in prereg:
        raise SystemExit("preregistration.md not marked REGISTERED — refusing to run eval")

    eval_start = datetime.fromisoformat(EVAL_START)
    eval_end = datetime.fromisoformat(EVAL_END)
    doc_ideas, doc_time, doc_author = load_doc_ideas()

    build_docs = {d for d, t in doc_time.items() if t < eval_start}
    eval_docs = {d for d, t in doc_time.items() if eval_start <= t < eval_end}
    assert build_docs and eval_docs, "empty window"
    print(f"build docs: {len(build_docs)}, eval docs: {len(eval_docs)}")

    # ---- build-window statistics (leakage guard: build_docs only) ----
    raw_count = defaultdict(int)
    decayed = defaultdict(float)
    growth_early, growth_late = defaultdict(int), defaultdict(int)
    mid = datetime.fromisoformat("2016-01-01")
    co_docs = defaultdict(int)
    for d in build_docs:
        ideas = doc_ideas[d]
        age_days = (eval_start - doc_time[d]).total_seconds() / 86400
        w = 0.5 ** (age_days / HALF_LIFE_DAYS)
        for i in ideas:
            raw_count[i] += 1
            decayed[i] += w
            (growth_late if doc_time[d] >= mid else growth_early)[i] += 1
        ideas_l = sorted(ideas)
        for a in range(len(ideas_l)):
            for b in range(a + 1, len(ideas_l)):
                co_docs[(ideas_l[a], ideas_l[b])] += 1

    frequent = [i for i, n in raw_count.items() if n >= FREQ_FLOOR]
    print(f"ideas over freq floor ({FREQ_FLOOR}): {len(frequent)}")

    # centroids over build-window claims only
    vecs = np.load(os.path.join(OUT, "embeddings.npy"))
    texts = json.load(open(os.path.join(OUT, "claim_texts.json")))
    vec_of = {t: k for k, t in enumerate(texts)}
    con = duckdb.connect()
    cl = con.sql(f"SELECT doc_id, claim FROM read_parquet('{OUT}/claims.parquet')").fetchall()
    assign = np.load(os.path.join(OUT, "assignments.npy"))
    cent = defaultdict(lambda: np.zeros(vecs.shape[1], dtype=np.float64))
    fset = set(frequent)
    for (doc_id, claim), idea in zip(cl, assign):
        if doc_id in build_docs and int(idea) in fset:
            cent[int(idea)] += vecs[vec_of[claim]]
    ids = sorted(cent)
    C = np.stack([cent[i] / np.linalg.norm(cent[i]) for i in ids])

    # eligible pairs: affinity >= A, zero build co-occurrence
    N = len(build_docs)
    sims = C @ C.T
    eligible = []
    for x in range(len(ids)):
        for y in range(x + 1, len(ids)):
            i, j = ids[x], ids[y]
            if sims[x, y] < AFFINITY_MIN or co_docs.get((min(i, j), max(i, j)), 0) > 0:
                continue
            E = N * (raw_count[i] / N) * (raw_count[j] / N)
            z = -np.sqrt(E)                        # obs = 0
            score = decayed[i] * decayed[j] * sims[x, y] * abs(z)
            g_i = growth_late[i] / max(growth_early[i], 1)
            g_j = growth_late[j] / max(growth_early[j], 1)
            eligible.append({"i": i, "j": j, "affinity": float(sims[x, y]),
                             "z": float(z), "gap": float(score),
                             "growth": float(g_i * g_j)})
    print(f"eligible gap pairs: {len(eligible)}")

    # ---- edge formation in eval window ----
    formed = set()
    pair_docs = defaultdict(list)
    for d in eval_docs:
        ideas_l = sorted(doc_ideas[d] & fset)
        for a in range(len(ideas_l)):
            for b in range(a + 1, len(ideas_l)):
                pair_docs[(ideas_l[a], ideas_l[b])].append(d)
    for pair, docs in pair_docs.items():
        if len(docs) >= MIN_ADOPTERS and \
           len({doc_author[d] for d in docs}) >= MIN_ADOPTERS:
            formed.add(pair)
    key = lambda p: (min(p["i"], p["j"]), max(p["i"], p["j"]))
    base_rate = sum(1 for p in eligible if key(p) in formed) / max(len(eligible), 1)
    print(f"edges formed among eligible: {base_rate:.4%} "
          f"({sum(1 for p in eligible if key(p) in formed)}/{len(eligible)})")

    # ---- rankers ----
    rng = np.random.default_rng(RNG_SEED)
    rankers = {
        "gap_score": sorted(eligible, key=lambda p: -p["gap"]),
        "affinity_only": sorted(eligible, key=lambda p: -p["affinity"]),
        "freq_growth": sorted(eligible, key=lambda p: -p["growth"]),
        "random": list(rng.permutation(np.array(eligible, dtype=object))),
    }
    results = {}
    for name, ranked in rankers.items():
        results[name] = {k: sum(1 for p in ranked[:k] if key(p) in formed) / k
                         for k in K_VALUES}
    print(f"\n{'ranker':<15}" + "".join(f"P@{k:<8}" for k in K_VALUES))
    for name, r in results.items():
        print(f"{name:<15}" + "".join(f"{r[k]:<10.4f}" for k in K_VALUES))

    json.dump({"params": {"eval_start": EVAL_START, "eval_end": EVAL_END,
                          "half_life": HALF_LIFE_DAYS, "freq_floor": FREQ_FLOOR,
                          "affinity_min": AFFINITY_MIN, "min_adopters": MIN_ADOPTERS,
                          "k": K_VALUES},
               "n_eligible": len(eligible), "base_rate": base_rate,
               "results": results},
              open(os.path.join(OUT, "eval_results.json"), "w"), indent=1)
    print(f"\nsaved {OUT}/eval_results.json")


if __name__ == "__main__":
    main()
