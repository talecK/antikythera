#!/usr/bin/env python3
"""Paper 2 Part A: provenance-hardened fold-B endpoint rebuild.

Registered in preregistration_paper2.md (REGISTERED 99ffd9e): recompute
the gate's WSB-dependent fold-B cells with the Pushshift-era dump months
replaced by API months — i.e. run the FROZEN gate criterion on the
paper-2 single-era API corpus. The statistic is run_gate.analyse itself
(imported, not reimplemented): same folds, same F/E/hub rules, same
shuffle null (R=100, seed 20260831), same formation floor.

Cells: fold B x {MEME, ALL, DD} x {union, cashtag}. MEME and ALL are the
registered targets (they contain WSB); DD is reported as a consistency
check (its gate value was already API-sourced). Registered expectation:
MEME fold-B segregation z stays <= -3.

Gate reference values (commit 1386fc0 table): fold B union z — ALL
-17.6, MEME -8.7, DD -16.3.
"""
import os
import sys

import duckdb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_gate import analyse  # noqa: E402  (frozen criterion, verbatim)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENTIONS = "/Volumes/1TB NVME 1/antikythera/data/paper2/ticker_mentions.parquet"
DD_SUBS = ("SecurityAnalysis", "ValueInvesting", "StockMarket", "stocks",
           "investing")
MEME_SUBS = ("wallstreetbets",)
ALL_SUBS = DD_SUBS + MEME_SUBS
GATE_REF = {("ALL", "union"): -17.6, ("MEME", "union"): -8.7,
            ("DD", "union"): -16.3}


def main() -> None:
    reg = os.path.join(ROOT, "preregistration_paper2.md")
    assert "STATUS: REGISTERED" in open(reg).read(), \
        "paper-2 registration not frozen — refusing to run"
    con = duckdb.connect()
    for stratum, subs in (("MEME", MEME_SUBS), ("ALL", ALL_SUBS),
                          ("DD", DD_SUBS)):
        for lens in ("union", "cashtag"):
            unit = "" if lens == "union" else "AND unit_type = 'cashtag'"
            rows = con.sql(f"""
                SELECT author, time, ticker FROM '{MENTIONS}'
                WHERE subreddit IN {subs!r} {unit}
            """).fetchall()
            r = analyse(rows, "B", stratum, lens, census=False)
            ref = GATE_REF.get((stratum, lens))
            print(f"PARTA fold B {stratum}/{lens}: n_eligible="
                  f"{r['eligible_suppressed']} obs={r['obs_total']} "
                  f"z={r['z_seg']:+.2f} formed={r['formed']} "
                  f"binom_p={r['binom_p']:.4f}"
                  + (f"  [gate mixed-provenance ref z={ref:+.1f}]"
                     if ref is not None else ""), flush=True)
    print("PARTA DONE", flush=True)


if __name__ == "__main__":
    main()
