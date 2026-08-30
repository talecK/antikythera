#!/usr/bin/env python3
"""Variant gate: author-space suppressed-pair census on Reddit finance discourse.

Same formulation as runs 5/6 (validated on HN), units = tickers:
  document        = (author, calendar quarter)
  eligible pair   = E_build >= 2 AND zero build co-mentions ("suppressed")
  formation       = >= 2 eval docs, >= 2 distinct authors, eval z >= 2

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

    epair, efreq = defaultdict(set), defaultdict(int)
    for d, s in edocs.items():
        ss = sorted(s & fs)
        for t in ss:
            efreq[t] += 1
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                epair[(ss[i], ss[j])].add(d)
    Ne = len(edocs)
    formed = set()
    for pair, dd in epair.items():
        a, b = pair
        E = efreq[a] * efreq[b] / max(Ne, 1)
        if len(dd) >= 2 and len({x[0] for x in dd}) >= 2 and \
           (len(dd) - E) / max(math.sqrt(E), 1e-9) >= 2.0:
            formed.add(pair)
    hits = [p for p in eligible if p in formed]
    lo, hi = wilson(len(hits), len(eligible))
    out.update({"formed": len(hits), "rate": len(hits) / max(len(eligible), 1),
                "ci95": [lo, hi],
                "top_hits": [list(p) for p in sorted(
                    hits, key=lambda p: -len(neigh[p[0]] & neigh[p[1]]))[:15]]})
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
                    f" | formed {r['formed']} ({r['rate']:.2%}, " \
                    f"CI {r['ci95'][0]:.2%}-{r['ci95'][1]:.2%})"
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
