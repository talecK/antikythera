#!/usr/bin/env python3
"""Paper 2 REGISTERED eval: rolling-window segregation on WSB + DD control.

Refuses to run unless preregistration_paper2.md reads STATUS: REGISTERED.

Per window (build [k, k+B) quarters, eval [k+B, k+B+2)), per stratum and
lens: eligibility exactly as the gate (F>=20, E>=2, zero build co-mention,
hub guard via run_gate.build_docs), then the run-8 statistic — total obs
eval co-mention docs over eligible pairs vs the label-shuffle null total
(R=100, numpy default_rng seed 20260831), z. Formation counts secondary
(obs > per-pair p99 AND >=2 docs AND >=2 authors).

The eval block below replicates run_gate.analyse's registered machinery
line-for-line (registration determinism clause): every incidence list is
sorted() before feeding the seeded RNG; a fresh default_rng(SHUFFLE_SEED)
per cell, exactly as the gate uses one per analyse() call.

Order: primary cells first (B=4 WSB/union, then B=4 DD/union), then the
remaining sensitivity/descriptive cells. Emits reports/paper2_windows_z.tsv
progressively; scoring (onset rule, P1/P2/P3, step fit) is computed by
this script at the end from the primary cells alone.
"""
import os
import sys
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_gate import (  # noqa: E402
    build_docs, E_MIN, F_DEFAULT, R, SHUFFLE_SEED, EXCLUDED_TICKERS)
from run_eval8 import binom_sf_ge  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENTIONS = "/Volumes/1TB NVME 1/antikythera/data/paper2/ticker_mentions.parquet"
OUT_TSV = os.path.join(ROOT, "reports", "paper2_windows_z.tsv")
DD_SUBS = ("SecurityAnalysis", "ValueInvesting", "StockMarket", "stocks",
           "investing")
WSB_SUBS = ("wallstreetbets",)
B_PRIMARY, B_SENS = 4, (6, 8)
EVAL_Q = 2
Q0, NQ = (2019, 0), 24
CASHTAG_UNINF = 20      # registered: <20 eligible -> UNINFORMATIVE
ONSET_Z, DEEP_Z = -3.0, -5.0


def qdate(k: int) -> datetime:
    y = Q0[0] + (Q0[1] + k) // 4
    q = (Q0[1] + k) % 4
    return datetime(y, q * 3 + 1, 1)


def qlabel(k: int) -> str:
    y = Q0[0] + (Q0[1] + k) // 4
    q = (Q0[1] + k) % 4
    return f"{y}Q{q + 1}"


def window_stat(rows, bs, be, ee, F=F_DEFAULT):
    """run_gate.analyse's registered eval machinery, window-parameterized."""
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
    eligible = []
    for i, a in enumerate(fl):
        fa = len(bfreq[a])
        for b in fl[i + 1:]:
            if fa * len(bfreq[b]) / max(Nb, 1) < E_MIN:
                break
            key = (min(a, b), max(a, b))
            if key not in co:
                eligible.append(key)
    out = {"build_docs": Nb, "eval_docs": len(edocs), "n_eligible": len(eligible)}
    idx = {p: j for j, p in enumerate(eligible)}
    n = len(eligible)
    if n == 0:
        out.update({"obs_total": 0, "null_mean": 0.0, "null_sd": 0.0,
                    "z_seg": 0.0, "formed": 0, "binom_p": 1.0})
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
    # sorted(): registration determinism clause (gate review finding 1.2)
    for d in sorted(edocs):
        for t in sorted(edocs[d] & fs):
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
    formed = 0
    for pr, j in idx.items():
        if obs[j] > p99[j] and obs[j] >= 2 and \
           len({d[0] for d in docs_of.get(pr, set())}) >= 2:
            formed += 1
    totals = null.sum(axis=1)
    z_seg = (obs.sum() - totals.mean()) / max(totals.std(), 1e-9)
    out.update({"obs_total": int(obs.sum()),
                "null_mean": float(totals.mean()),
                "null_sd": float(totals.std()),
                "z_seg": float(z_seg), "formed": formed,
                "binom_p": float(binom_sf_ge(formed, n, 0.01)) if formed else 1.0})
    return out


def onset_window(zs):
    """Registered onset rule: earliest w with z<=-3 whose every later
    window is z<=-3, allowing at most one later exception."""
    for w in range(len(zs)):
        if zs[w] <= ONSET_Z:
            later = zs[w + 1:]
            if sum(1 for z in later if z > ONSET_Z) <= 1:
                return w
    return None


def step_fit(zs):
    """Registered secondary: one-break two-mean least-squares fit; point
    estimate + the set of breaks with SSE within 10% of minimum."""
    best, sses = None, {}
    for b in range(1, len(zs)):
        l, r = zs[:b], zs[b:]
        sse = sum((z - sum(l) / len(l)) ** 2 for z in l) + \
              sum((z - sum(r) / len(r)) ** 2 for z in r)
        sses[b] = sse
        if best is None or sse < sses[best]:
            best = b
    near = sorted(b for b, s in sses.items() if s <= sses[best] * 1.10)
    return best, near


def main() -> None:
    reg = os.path.join(ROOT, "preregistration_paper2.md")
    assert os.path.exists(reg) and "STATUS: REGISTERED" in open(reg).read(), \
        "paper-2 registration not frozen — refusing to run eval"
    con = duckdb.connect()
    data = {}
    for stratum, subs in (("WSB", WSB_SUBS), ("DD", DD_SUBS)):
        for lens in ("union", "cashtag"):
            unit = "" if lens == "union" else "AND unit_type = 'cashtag'"
            data[(stratum, lens)] = [
                r for r in con.sql(f"""
                    SELECT author, time, ticker FROM '{MENTIONS}'
                    WHERE subreddit IN {subs!r} {unit}
                """).fetchall() if r[2] not in EXCLUDED_TICKERS]

    cells = []
    for stratum in ("WSB", "DD"):                       # primary B first
        for k in range(0, NQ - B_PRIMARY - EVAL_Q + 1):
            cells.append((B_PRIMARY, k, stratum, "union"))
    for B in B_SENS:                                    # sensitivity B
        for stratum in ("WSB", "DD"):
            for k in range(0, NQ - B - EVAL_Q + 1):
                cells.append((B, k, stratum, "union"))
    for B in (B_PRIMARY, *B_SENS):                      # cashtag last
        for stratum in ("WSB", "DD"):
            for k in range(0, NQ - B - EVAL_Q + 1):
                cells.append((B, k, stratum, "cashtag"))

    cols = ["B", "window", "eval_start", "eval_end", "stratum", "lens",
            "build_docs", "eval_docs", "n_eligible", "obs_total",
            "null_mean", "null_sd", "z_seg", "formed", "binom_p",
            "uninformative"]
    results = {}
    with open(OUT_TSV, "w") as f:
        f.write("\t".join(cols) + "\n")
        for B, k, stratum, lens in cells:
            bs, be, ee = qdate(k), qdate(k + B), qdate(k + B + EVAL_Q)
            st = window_stat(data[(stratum, lens)], bs, be, ee)
            uninf = int(lens == "cashtag" and st["n_eligible"] < CASHTAG_UNINF)
            rec = {"B": B, "window": k, "eval_start": qlabel(k + B),
                   "eval_end": qlabel(k + B + EVAL_Q - 1),
                   "stratum": stratum, "lens": lens, **st,
                   "uninformative": uninf}
            results[(B, k, stratum, lens)] = rec
            f.write("\t".join(str(rec[c]) for c in cols) + "\n")
            f.flush()
            print(f"B={B} {rec['eval_start']}..{rec['eval_end']} "
                  f"{stratum}/{lens}: n={st['n_eligible']} "
                  f"obs={st['obs_total']} null={st['null_mean']:.1f} "
                  f"z={st['z_seg']:+.2f} formed={st['formed']}"
                  f"{' UNINFORMATIVE' if uninf else ''}", flush=True)

    # ---- registered scoring, primary cells only ----
    nw = NQ - B_PRIMARY - EVAL_Q + 1
    wsb = [results[(B_PRIMARY, k, "WSB", "union")] for k in range(nw)]
    dd = [results[(B_PRIMARY, k, "DD", "union")] for k in range(nw)]
    zs = [r["z_seg"] for r in wsb]
    ow = onset_window(zs)
    print("\n== REGISTERED SCORING (primary: B=4, union) ==")
    print("WSB z series:", " ".join(f"{r['eval_start']}:{r['z_seg']:+.1f}"
                                    for r in wsb))
    print("DD  z series:", " ".join(f"{r['eval_start']}:{r['z_seg']:+.1f}"
                                    for r in dd))
    if ow is None:
        print("ONSET: none (no window satisfies the onset rule)")
        p1 = False
    else:
        pre = [i for i in range(ow) if abs(zs[i]) < 3]
        pre_ok = any(pre[i] + 1 == pre[i + 1] for i in range(len(pre) - 1)) \
            if len(pre) >= 2 else False
        deep = [i for i in range(ow, nw) if zs[i] <= DEEP_Z]
        deep_ok = any(deep[i] + 1 == deep[i + 1] for i in range(len(deep) - 1)) \
            if len(deep) >= 2 else False
        p1 = pre_ok and deep_ok
        onset_time = qdate(ow + B_PRIMARY)
        print(f"ONSET window: {ow} (eval {wsb[ow]['eval_start']}.."
              f"{wsb[ow]['eval_end']}, onset time {onset_time.date()})")
        print(f"P1 (>=2 consec |z|<3 before onset: {pre_ok}; "
              f">=2 consec z<=-5 at/after: {deep_ok}) -> "
              f"{'PASS' if p1 else 'FAIL'}")
        p2 = datetime(2021, 1, 1) <= onset_time <= datetime(2021, 12, 31)
        print(f"P2 (onset in 2021): {'PASS' if p2 else 'FAIL'}")
    ddz = [r["z_seg"] for r in dd]
    p3_viol = [k for k in range(nw - 1)
               if ddz[k] > -3 and ddz[k + 1] <= -5
               and datetime(2020, 1, 1) <= qdate(k + 1 + B_PRIMARY)
               and qdate(k + 1 + B_PRIMARY) <= datetime(2022, 12, 31)]
    print(f"P3 (no DD cliff in 2020-2022): "
          f"{'PASS' if not p3_viol else 'FAIL at windows ' + str(p3_viol)}")
    b, near = step_fit(zs)
    print(f"STEP FIT (secondary): break before window {b} "
          f"(eval {wsb[b]['eval_start']}), near-ties (SSE<=1.1*min): "
          f"{[wsb[x]['eval_start'] for x in near]}")
    print(f"\nresults: {OUT_TSV}")


if __name__ == "__main__":
    main()
