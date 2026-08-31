#!/usr/bin/env python3
"""Paper 2: OUTCOME-BLIND per-window census (registration gate).

Computes, for every rolling window and every candidate build length B,
per stratum and lens: build docs, eval docs, frequent tickers, observed
build co-mention pairs, and ELIGIBLE SUPPRESSED PAIRS. Nothing else.

This file deliberately CANNOT compute the study's statistic: it never
counts eval co-mentions over eligible pairs and never runs the shuffle
null. That is the point — the B-ladder decision and the LOW-POWER window
marking must be made from these counts alone, before any z exists.

Doc construction, hub guard, frequency floor and eligibility are IMPORTED
from eval/run_gate.py so they are identical to the registered gate by
construction (which itself imports the run-8 null machinery).

Windows: quarterly step over 2019Q1..2024Q4; window k has build =
quarters [k, k+B) and eval = quarters [k+B, k+B+2).

Usage: census_paper2.py            (writes TSV + summary to stdout)
"""
import os
import sys
from datetime import datetime

import duckdb

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from run_gate import build_docs, E_MIN, F_DEFAULT  # noqa: E402
from collections import defaultdict  # noqa: E402

MENTIONS = "/Volumes/1TB NVME 1/antikythera/data/paper2/ticker_mentions.parquet"
DD_SUBS = ("SecurityAnalysis", "ValueInvesting", "StockMarket", "stocks",
           "investing")
WSB_SUBS = ("wallstreetbets",)
B_LADDER = (4, 6, 8)     # candidate build lengths, in quarters
EVAL_Q = 2               # eval length, in quarters (fixed)
Q0, NQ = (2019, 0), 24   # 2019Q1 .. 2024Q4


def qdate(k: int) -> datetime:
    """Start datetime of the k-th quarter after Q0."""
    y = Q0[0] + (Q0[1] + k) // 4
    q = (Q0[1] + k) % 4
    return datetime(y, q * 3 + 1, 1)


def qlabel(k: int) -> str:
    y = Q0[0] + (Q0[1] + k) // 4
    q = (Q0[1] + k) % 4
    return f"{y}Q{q + 1}"


def census(rows, bs: datetime, be: datetime, ee: datetime,
           F: int = F_DEFAULT) -> dict:
    """Eligibility structure only — mirrors run_gate.analyse(census=True)."""
    bdocs, edocs = build_docs(rows, bs, be), build_docs(rows, be, ee)
    bfreq = defaultdict(set)
    for d, s in bdocs.items():
        for t in s:
            bfreq[t].add(d)
    fs = {t for t, v in bfreq.items() if len(v) >= F}
    Nb = len(bdocs)
    co = set()
    for d, s in bdocs.items():
        ss = sorted(s & fs)
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                co.add((ss[i], ss[j]))
    fl = sorted(fs, key=lambda t: -len(bfreq[t]))
    eligible = 0
    for i, a in enumerate(fl):
        fa = len(bfreq[a])
        for b in fl[i + 1:]:
            if fa * len(bfreq[b]) / max(Nb, 1) < E_MIN:
                break
            if (min(a, b), max(a, b)) not in co:
                eligible += 1
    return {"build_docs": Nb, "eval_docs": len(edocs),
            "frequent_tickers": len(fs), "co_pairs": len(co),
            "eligible": eligible}


def main() -> None:
    con = duckdb.connect()
    data = {}
    for stratum, subs in (("WSB", WSB_SUBS), ("DD", DD_SUBS)):
        for lens in ("union", "cashtag"):
            unit = "" if lens == "union" else "AND unit_type = 'cashtag'"
            data[(stratum, lens)] = con.sql(f"""
                SELECT author, time, ticker FROM '{MENTIONS}'
                WHERE subreddit IN {subs!r} {unit}
            """).fetchall()
            print(f"loaded {stratum}/{lens}: {len(data[(stratum, lens)])} "
                  f"mentions", flush=True)

    out = []
    for B in B_LADDER:
        for k in range(0, NQ - B - EVAL_Q + 1):
            bs, be, ee = qdate(k), qdate(k + B), qdate(k + B + EVAL_Q)
            for (stratum, lens), rows in data.items():
                c = census(rows, bs, be, ee)
                rec = {"B": B, "window": k, "build_start": qlabel(k),
                       "eval_start": qlabel(k + B),
                       "eval_end": qlabel(k + B + EVAL_Q - 1),
                       "stratum": stratum, "lens": lens, **c}
                out.append(rec)
                print(f"B={B} k={k:2d} {rec['eval_start']}..{rec['eval_end']} "
                      f"{stratum}/{lens}: bdocs={c['build_docs']} "
                      f"edocs={c['eval_docs']} freq={c['frequent_tickers']} "
                      f"elig={c['eligible']}", flush=True)

    cols = ["B", "window", "build_start", "eval_start", "eval_end", "stratum",
            "lens", "build_docs", "eval_docs", "frequent_tickers", "co_pairs",
            "eligible"]
    tsv = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "reports", "paper2_window_census.tsv")
    with open(tsv, "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in out:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")

    print("\n== B-LADDER (registered rule: shortest B whose MEDIAN eligible "
          "count in WSB/union is >= 100)")
    import statistics
    choice = None
    for B in B_LADDER:
        vals = sorted(r["eligible"] for r in out
                      if r["B"] == B and r["stratum"] == "WSB"
                      and r["lens"] == "union")
        med = statistics.median(vals) if vals else 0
        lo = min(vals) if vals else 0
        hi = max(vals) if vals else 0
        n_low = sum(1 for v in vals if v < 30)
        print(f"B={B}q: windows={len(vals)} median_eligible={med} "
              f"min={lo} max={hi} LOW_POWER(<30)={n_low}")
        if choice is None and med >= 100:
            choice = B
    print(f"\nB-LADDER CHOICE: {'B=' + str(choice) + ' quarters' if choice else 'NONE MEETS THE BAR — registration requires an amendment before eval'}")
    print(f"census written: {tsv}")


if __name__ == "__main__":
    main()
