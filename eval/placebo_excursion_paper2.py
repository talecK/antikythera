#!/usr/bin/env python3
"""Paper 2: targeted placebo on the two excursion windows (post-registration
robustness check, no registered bar touched; disclosed as such).

Question: in the exact data regime of the 2020Q4-2021Q2 excursion (extreme
densification, 500K+ eval docs), can the registered machinery manufacture a
large POSITIVE segregation z when truth is null by construction?

Design (R1 pattern, run_robustness.py, adapted to the window statistic):
for each excursion cell (B=4, k=3 and k=4; WSB/union; EXCLUDED_TICKERS
applied), build-window eligibility is computed from the REAL build data
(unchanged), then each placebo replicate p:
  1. outer shuffle: permute the eval incidence ticker column once
     (default_rng(20260901000 + p) — per-replicate seed, documented here),
     destroying any real pair structure -> truth null by construction;
  2. run the FULL registered statistic on the placebo eval (obs total vs
     inner R=100 shuffle null, inner seed 20260831 as registered) -> z_p,
     formed_p.
20 replicates per window, parallelized (fork). Honest machinery in this
regime => placebo z distribution centered ~0 with sd ~1, formed ~1% floor;
the real excursion (+28.6/+30.9, formed 24/61) must be far outside it.
"""
import multiprocessing as mp
import os
import sys
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_gate import (  # noqa: E402
    build_docs, E_MIN, F_DEFAULT, R, SHUFFLE_SEED, EXCLUDED_TICKERS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENTIONS = os.path.join(ROOT, "data", "paper2", "ticker_mentions.parquet")
B, EVAL_Q = 4, 2
WINDOWS = (3, 4)          # k: eval 2020Q4..2021Q1 and 2021Q1..2021Q2
REPS = 20
OUTER_SEED_BASE = 20260901000


def qdate(k: int) -> datetime:
    y = 2019 + k // 4
    return datetime(y, (k % 4) * 3 + 1, 1)


def prepare(rows, k):
    """Real build eligibility + real eval incidences for window k."""
    bs, be, ee = qdate(k), qdate(k + B), qdate(k + B + EVAL_Q)
    bdocs, edocs = build_docs(rows, bs, be), build_docs(rows, be, ee)
    bfreq = defaultdict(set)
    for d, s in bdocs.items():
        for t in s:
            bfreq[t].add(d)
    fs = {t for t, v in bfreq.items() if len(v) >= F_DEFAULT}
    Nb = len(bdocs)
    co = set()
    for d, s in bdocs.items():
        ss = sorted(s & fs)
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                co.add((ss[i], ss[j]))
    fl = sorted(fs, key=lambda t: -len(bfreq[t]))
    eligible = []
    for i, a in enumerate(fl):
        fa = len(bfreq[a])
        for b2 in fl[i + 1:]:
            if fa * len(bfreq[b2]) / max(Nb, 1) < E_MIN:
                break
            key = (min(a, b2), max(a, b2))
            if key not in co:
                eligible.append(key)
    inc_doc, inc_tok = [], []
    for d in sorted(edocs):                       # determinism clause
        for t in sorted(edocs[d] & fs):
            inc_doc.append(d)
            inc_tok.append(t)
    return fs, eligible, inc_doc, np.array(inc_tok, dtype=object)


def stat_on(inc_doc, inc_tok_arr, fs, eligible):
    """Registered statistic on an incidence list (obs vs inner null)."""
    idx = {p: j for j, p in enumerate(eligible)}
    n = len(eligible)

    def pair_counts(docmap):
        counts = np.zeros(n, dtype=np.int32)
        docs_of = defaultdict(set)
        for d, s in docmap.items():
            ss = sorted(s)
            for i in range(len(ss)):
                for j in range(i + 1, len(ss)):
                    j2 = idx.get((ss[i], ss[j]))
                    if j2 is not None:
                        counts[j2] += 1
                        docs_of[(ss[i], ss[j])].add(d)
        return counts, docs_of

    docmap = defaultdict(set)
    for d, t in zip(inc_doc, inc_tok_arr):
        docmap[d].add(t)
    obs, docs_of = pair_counts(docmap)
    rng = np.random.default_rng(SHUFFLE_SEED)     # inner null, as registered
    null = np.zeros((R, n), dtype=np.int32)
    for r in range(R):
        perm = rng.permutation(inc_tok_arr)
        sh = defaultdict(set)
        for d, t in zip(inc_doc, perm):
            sh[d].add(t)
        null[r], _ = pair_counts(sh)
    p99 = np.percentile(null, 99, axis=0)
    formed = 0
    for pr, j in idx.items():
        if obs[j] > p99[j] and obs[j] >= 2 and \
           len({d[0] for d in docs_of.get(pr, set())}) >= 2:
            formed += 1
    totals = null.sum(axis=1)
    z = (obs.sum() - totals.mean()) / max(totals.std(), 1e-9)
    return float(z), int(formed), int(obs.sum())


_G = {}


def worker(args):
    k, rep = args
    fs, eligible, inc_doc, inc_tok = _G[k]
    rng = np.random.default_rng(OUTER_SEED_BASE + rep)
    placebo_tok = rng.permutation(inc_tok)        # outer shuffle: truth null
    z, formed, obs = stat_on(inc_doc, placebo_tok, fs, eligible)
    print(f"PLACEBO k={k} rep={rep}: z={z:+.2f} formed={formed} obs={obs}",
          flush=True)
    return k, rep, z, formed


def main() -> None:
    reg = os.path.join(ROOT, "preregistration_paper2.md")
    assert "STATUS: REGISTERED" in open(reg).read()
    con = duckdb.connect()
    rows = [r for r in con.sql(f"""
        SELECT author, time, ticker FROM '{MENTIONS}'
        WHERE subreddit IN ('wallstreetbets',)
    """).fetchall() if r[2] not in EXCLUDED_TICKERS]
    for k in WINDOWS:
        _G[k] = prepare(rows, k)
        print(f"window k={k}: eligible={len(_G[k][1])} "
              f"incidences={len(_G[k][2])}", flush=True)
    tasks = [(k, rep) for k in WINDOWS for rep in range(REPS)]
    with mp.get_context("fork").Pool(6) as pool:
        results = pool.map(worker, tasks)
    print("\n== PLACEBO SUMMARY (real excursion: k=3 z=+28.63 formed=24; "
          "k=4 z=+30.86 formed=61)")
    for k in WINDOWS:
        zs = [z for kk, _, z, _ in results if kk == k]
        fm = [f for kk, _, _, f in results if kk == k]
        print(f"k={k}: reps={len(zs)} z mean={np.mean(zs):+.3f} "
              f"sd={np.std(zs):.3f} min={min(zs):+.2f} max={max(zs):+.2f} "
              f"formed mean={np.mean(fm):.1f} max={max(fm)}")
    print("PLACEBO DONE", flush=True)


if __name__ == "__main__":
    main()
