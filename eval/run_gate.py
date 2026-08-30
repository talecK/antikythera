#!/usr/bin/env python3
"""Variant gate: author-space suppressed-pair census on Reddit finance discourse.

Same formulation as runs 5/6 (validated on HN), units = tickers:
  document        = (author, calendar quarter)
  eligible pair   = E_build >= 2 AND zero build co-mentions ("suppressed")
  formation       = shuffle-calibrated (registered amendment, run 8): obs
                    eval co-mention docs > per-pair label-shuffle p99
                    (R=100, seed 20260831) AND >= 2 docs AND >= 2 authors
  segregation     = CO-PRIMARY (Q1b): total obs co-mention over eligible
                    pairs vs shuffle-null total, as z

The null is imported from eval/run_eval8.py so the HN and Reddit numbers are
identical by construction, not by reimplementation.

Modes:
  --census   outcome-blind structure only (for the registration)
  (default)  full eval; refuses to run unless the registration is committed

Strata: DD (SecurityAnalysis, ValueInvesting, StockMarket, stocks, investing)
vs MEME (wallstreetbets) vs ALL — the registered mechanism test.
Unit lenses: union (cashtag + stoplisted bare) and cashtag-only.
"""
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

import duckdb
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_eval8 import binom_sf_ge  # noqa: E402  (registered null, run 8)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENTIONS = "/Volumes/1TB NVME 1/antikythera/data/reddit_gate/ticker_mentions.parquet"
DD_SUBS = {"SecurityAnalysis", "ValueInvesting", "StockMarket", "stocks",
           "investing"}
MEME_SUBS = {"wallstreetbets"}
FOLDS = {  # name: (build_start, build_end/eval_start, eval_end)
    "A": ("2017-01-01", "2019-01-01", "2020-01-01"),
    "B": ("2022-01-01", "2024-01-01", "2025-01-01"),
}
F_DEFAULT = 20
E_MIN = 2.0
HUB_MAX = 50          # author-quarters with more distinct tickers are dropped
SEED = 20260830
R = 100               # shuffle reps, matching run 8
SHUFFLE_SEED = 20260831


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def quarter(ts: int) -> tuple[int, int]:
    d = datetime.fromtimestamp(ts, tz=timezone.utc)
    return (d.year, (d.month - 1) // 3)


def build_docs(rows, lo: datetime, hi: datetime) -> dict:
    docs = defaultdict(set)
    for author, ts, ticker in rows:
        t = datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None)
        if lo <= t < hi:
            y, q = quarter(ts)
            docs[(author, y, q)].add(ticker)
    return {k: v for k, v in docs.items() if len(v) <= HUB_MAX}


def analyse(rows, fold: str, stratum: str, lens: str, census: bool,
            F: int = F_DEFAULT) -> dict:
    bs, be, ee = (datetime.fromisoformat(x) for x in FOLDS[fold])
    bdocs, edocs = build_docs(rows, bs, be), build_docs(rows, be, ee)
    bfreq = defaultdict(set)
    for d, s in bdocs.items():
        for t in s:
            bfreq[t].add(d)
    fs = {t for t, v in bfreq.items() if len(v) >= F}
    Nb = len(bdocs)
    co, neigh = set(), defaultdict(set)
    for d, s in bdocs.items():
        ss = sorted(s & fs)
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                co.add((ss[i], ss[j]))
                neigh[ss[i]].add(ss[j])
                neigh[ss[j]].add(ss[i])
    fl = sorted(fs, key=lambda t: -len(bfreq[t]))
    eligible = []
    for i, a in enumerate(fl):
        fa = len(bfreq[a])
        for b in fl[i + 1:]:
            if fa * len(bfreq[b]) / max(Nb, 1) < E_MIN:
                break
            key = (min(a, b), max(a, b))
            if key not in co:
                eligible.append(key)
    out = {"fold": fold, "stratum": stratum, "lens": lens, "F": F,
           "build_docs": Nb, "eval_docs": len(edocs),
           "frequent_tickers": len(fs), "co_pairs": len(co),
           "eligible_suppressed": len(eligible)}
    if census:
        return out

    # --- registered criterion (run-8 amendment): per-pair shuffle null ---
    idx = {p: j for j, p in enumerate(eligible)}
    n = len(eligible)
    if n == 0:
        out.update({"formed": 0, "binom_p": 1.0, "z_seg": 0.0,
                    "obs_total": 0, "formed_pairs": []})
        return out

    def pair_counts(docmap):
        counts = np.zeros(n, dtype=np.int32)
        docs_of = defaultdict(set)
        for d, s in docmap.items():
            ss = sorted(s & fs)
            for i in range(len(ss)):
                for j in range(i + 1, len(ss)):
                    j2 = idx.get((ss[i], ss[j]))
                    if j2 is not None:
                        counts[j2] += 1
                        docs_of[(ss[i], ss[j])].add(d)
        return counts, docs_of

    obs, docs_of = pair_counts(edocs)
    inc_doc, inc_tok = [], []
    for d in edocs:
        for t in edocs[d] & fs:
            inc_doc.append(d)
            inc_tok.append(t)
    inc_tok = np.array(inc_tok, dtype=object)
    rng = np.random.default_rng(SHUFFLE_SEED)
    null = np.zeros((R, n), dtype=np.int32)
    for r in range(R):
        perm = rng.permutation(inc_tok)
        sh = defaultdict(set)
        for d, t in zip(inc_doc, perm):
            sh[d].add(t)
        null[r], _ = pair_counts(sh)

    p99 = np.percentile(null, 99, axis=0)
    formed = []
    for pr, j in idx.items():
        if obs[j] > p99[j] and obs[j] >= 2 and \
           len({d[0] for d in docs_of.get(pr, set())}) >= 2:
            formed.append((pr, int(obs[j]), float(p99[j])))
    k = len(formed)
    pval = binom_sf_ge(k, n, 0.01) if k else 1.0
    totals = null.sum(axis=1)
    z_seg = (obs.sum() - totals.mean()) / max(totals.std(), 1e-9)
    lo, hi = wilson(k, n)
    out.update({"formed": k, "rate": k / n, "ci95": [lo, hi],
                "floor": 0.01 * n, "binom_p": float(pval),
                "obs_total": int(obs.sum()),
                "null_total_mean": float(totals.mean()),
                "null_total_sd": float(totals.std()),
                "z_seg": float(z_seg),
                "formed_pairs": [(list(pr), o, t) for pr, o, t in
                                 sorted(formed, key=lambda x: -x[1])]})
    return out


def main() -> None:
    census = "--census" in sys.argv
    if not census:
        reg = os.path.join(ROOT, "preregistration_gate.md")
        assert os.path.exists(reg) and "STATUS: REGISTERED" in open(reg).read(), \
            "gate registration not frozen — refusing to run eval"
    con = duckdb.connect()
    all_rows = con.sql(f"""
        SELECT author, time, ticker, subreddit, unit_type
        FROM read_parquet('{MENTIONS}')""").fetchall()
    print(f"mentions: {len(all_rows)}", flush=True)
    results = []
    for fold in FOLDS:
        for stratum, subs in (("ALL", None), ("DD", DD_SUBS), ("MEME", MEME_SUBS)):
            for lens in ("union", "cashtag"):
                rows = [(a, t, k) for a, t, k, s, u in all_rows
                        if (subs is None or s in subs)
                        and (lens == "union" or u == "cashtag")]
                r = analyse(rows, fold, stratum, lens, census)
                results.append(r)
                extra = "" if census else \
                    f" | Q1 formed {r['formed']}/{r['eligible_suppressed']} " \
                    f"(floor {r.get('floor', 0):.1f}, p={r.get('binom_p', 1):.3g})" \
                    f" | Q1b seg z={r.get('z_seg', 0):+.1f} " \
                    f"(obs {r.get('obs_total', 0)} vs null " \
                    f"{r.get('null_total_mean', 0):.0f})"
                print(f"fold {fold} {stratum:5s} {lens:8s}: "
                      f"docs {r['build_docs']:>7}/{r['eval_docs']:<7} "
                      f"tickers {r['frequent_tickers']:>4} "
                      f"co-pairs {r['co_pairs']:>7} "
                      f"suppressed {r['eligible_suppressed']:>6}{extra}",
                      flush=True)
    tag = "census" if census else "eval"
    json.dump(results, open(f"{ROOT}/data/registry/gate_{tag}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
