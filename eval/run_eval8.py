#!/usr/bin/env python3
"""Registered run 8: shuffle-calibrated formation (preregistration_run8.md).

Per-pair empirical null: R=100 eval-window label shuffles; pair forms iff
observed co-mention doc count > per-pair p99 AND >=2 docs AND >=2 authors.
Spaces: --author (run-5 universe) | --thread (run-3 universe).
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from itertools import combinations

import duckdb
import numpy as np
from numpy import log, exp
from math import lgamma


def binom_sf_ge(k, n, p):
    """P(X >= k), X ~ Binomial(n, p); exact via log-space summation."""
    if k <= 0:
        return 1.0
    hi = min(n, k + 10000)
    js = np.arange(k, hi + 1, dtype=np.float64)
    lg = (lgamma(n + 1) - np.array([lgamma(j + 1) + lgamma(n - j + 1) for j in js])
          + js * log(p) + (n - js) * log(1 - p))
    return float(np.clip(exp(lg).sum(), 0.0, 1.0))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AC = os.path.join(ROOT, "data", "registry", "run5_author", "author_concepts.parquet")
PC = os.path.join(ROOT, "data", "registry", "pilot1_concepts")
F = 20
E_MIN = 2.0
HUB_MAX = 100
R = 100
SEED = 20260831
FOLDS = [("fold1", datetime(2017, 1, 1), datetime(2018, 1, 1)),
         ("fold2", datetime(2016, 1, 1), datetime(2017, 1, 1))]
BUILD_START = datetime(2015, 1, 1)


def author_universe(be, ee):
    con = duckdb.connect()
    rows = con.sql(f"SELECT author, time, concept FROM read_parquet('{AC}')").fetchall()
    bdoc, edoc = defaultdict(set), defaultdict(set)
    for author, ts, concept in rows:
        if BUILD_START <= ts < be:
            bdoc[(author, ts.year, (ts.month - 1) // 3)].add(concept)
        elif be <= ts < ee:
            edoc[(author, ts.year, (ts.month - 1) // 3)].add(concept)
    bdoc = {k: v for k, v in bdoc.items() if len(v) <= HUB_MAX}
    edoc = {k: v for k, v in edoc.items() if len(v) <= HUB_MAX}
    return bdoc, edoc, lambda d: d[0]


def thread_universe(be, ee):
    con = duckdb.connect()
    rows = con.sql(f"""
        SELECT c.doc_id, c.claim, c.time, d."by" AS author
        FROM read_parquet('{PC}/claims.parquet') c
        JOIN (SELECT doc_id, min(authors[1]) AS "by"
              FROM read_parquet('{ROOT}/data/docs/docs_*.parquet') GROUP BY doc_id) d
          ON c.doc_id = d.doc_id""").fetchall()
    bdoc, edoc = defaultdict(set), defaultdict(set)
    author_of = {}
    for did, concept, ts, by in rows:
        author_of[did] = by
        if ts < be:
            bdoc[did].add(concept)
        elif ts < ee:
            edoc[did].add(concept)
    return bdoc, edoc, lambda d: author_of.get(d)


def eligible_set(bdoc):
    bfreq = defaultdict(int)
    for s in bdoc.values():
        for c in s:
            bfreq[c] += 1
    fs = {c for c, n in bfreq.items() if n >= F}
    Nb = len(bdoc)
    co = set()
    for s in bdoc.values():
        ss = sorted(s & fs)
        for pr in combinations(ss, 2):
            co.add(pr)
    fl = sorted(fs, key=lambda c: -bfreq[c])
    eligible = []
    for i, a in enumerate(fl):
        fa = bfreq[a]
        for b in fl[i + 1:]:
            if fa * bfreq[b] / Nb < E_MIN:
                break
            key = (min(a, b), max(a, b))
            if key not in co:
                eligible.append(key)
    return fs, eligible


def pair_doc_counts(edoc, fs, eligible_idx):
    counts = np.zeros(len(eligible_idx), dtype=np.int32)
    docs_of = defaultdict(set)
    for d, s in edoc.items():
        ss = sorted(s & fs)
        for pr in combinations(ss, 2):
            j = eligible_idx.get(pr)
            if j is not None:
                counts[j] += 1
                docs_of[pr].add(d)
    return counts, docs_of


def run_space(space, rng):
    out = {}
    for name, be, ee in FOLDS:
        bdoc, edoc, author_fn = (author_universe if space == "author"
                                 else thread_universe)(be, ee)
        fs, eligible = eligible_set(bdoc)
        idx = {p: j for j, p in enumerate(eligible)}
        n = len(eligible)
        obs, docs_of = pair_doc_counts(edoc, fs, idx)
        print(f"{space} {name}: build docs {len(bdoc)} eval docs {len(edoc)} "
              f"F>=20 {len(fs)} eligible {n} | obs co-mention total {obs.sum()}",
              flush=True)

        inc_doc, inc_con = [], []
        # sorted(): unsorted set iteration is hash-order nondeterministic and
        # feeds rng.permutation — the seed pins nothing without it
        # (adversarial review 2026-08-31, finding 1.2)
        for d in edoc:
            for c in sorted(edoc[d] & fs):
                inc_doc.append(d)
                inc_con.append(c)
        inc_con = np.array(inc_con, dtype=object)
        null = np.zeros((R, n), dtype=np.int32)
        for r in range(R):
            perm = rng.permutation(inc_con)
            sh = defaultdict(set)
            for d, c in zip(inc_doc, perm):
                sh[d].add(c)
            null[r], _ = pair_doc_counts(sh, fs, idx)
            if (r + 1) % 20 == 0:
                print(f"  {space} {name} rep {r+1}/{R}", flush=True)

        p99 = np.percentile(null, 99, axis=0)
        formed = []
        for j, p in enumerate(eligible):
            if obs[j] > p99[j] and obs[j] >= 2 and \
               len({author_fn(d) for d in docs_of.get(p, set())}) >= 2:
                formed.append((p, int(obs[j]), float(p99[j])))
        k = len(formed)
        pval = binom_sf_ge(k, n, 0.01) if k else 1.0
        totals = null.sum(axis=1)
        zt = (obs.sum() - totals.mean()) / max(totals.std(), 1e-9)
        print(f"RUN8 {space} {name}: calibrated formed {k}/{n} "
              f"(floor {0.01*n:.1f}, binomial one-sided p={pval:.4g}) | "
              f"co-mention total obs {obs.sum()} vs null {totals.mean():.0f} "
              f"(sd {totals.std():.0f}) z={zt:+.1f}", flush=True)
        for p, o, t in sorted(formed, key=lambda x: -x[1]):
            print(f"    obs={o} p99={t:.1f}  '{p[0]}' <-> '{p[1]}'", flush=True)
        out[name] = {"eligible": n, "formed": k, "binom_p": pval,
                     "obs_total": int(obs.sum()),
                     "null_total_mean": float(totals.mean()),
                     "null_total_sd": float(totals.std()),
                     "z_total": float(zt),
                     "formed_pairs": [(list(p), o, t) for p, o, t in formed]}
    return out


def main():
    reg = open(os.path.join(ROOT, "preregistration_run8.md")).read()
    assert "Run 8 registration" in reg
    rng = np.random.default_rng(SEED)  # one stream: author-f1, -f2, thread-f1, -f2
    out_a = run_space("author", rng)
    json.dump(out_a, open(os.path.join(ROOT, "data", "registry", "run5_author",
                                       "run8_author.json"), "w"), indent=1)
    out_t = run_space("thread", rng)
    json.dump(out_t, open(os.path.join(PC, "run8_thread.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
