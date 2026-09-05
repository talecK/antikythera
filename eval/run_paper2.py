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

2026-09-04 additions (critique response; see preregistration_nulls.md):
  --workers N   run cells in a process pool. Cells are independent (a
                fresh generator per cell), so the registered output is
                byte-identical in any worker count. Workers load their
                own rows from the parquet; the parent writes rows in
                the registered cell order.
  --null KIND   label (registered) | stratified (labels permuted within
                the document's calendar quarter). Anything other than
                the registered null at R=100 requires the nulls
                amendment to read STATUS: REGISTERED, writes to a
                separate TSV, and adds the wide columns (ratio, Monte
                Carlo p, null range, margin-drift diagnostic).
  --R N         replicates (default 100, registered).
  --headline    the eight headline cells named in the amendment.
  --cells ...   explicit cell list "B:k:stratum:lens,...".
  --drift N     margin-drift diagnostic on the first N replicates
                (default 10 for non-registered runs, 0 for registered).
"""
import argparse
import multiprocessing as mp
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

import duckdb
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_gate import (  # noqa: E402
    build_docs, E_MIN, F_DEFAULT, R, SHUFFLE_SEED, EXCLUDED_TICKERS)
from run_eval8 import binom_sf_ge  # noqa: E402
from nulls import (label_shuffle, label_shuffle_stratified, margin_drift,  # noqa: E402
                   null_summary, drift_mean)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENTIONS = os.path.join(ROOT, "data", "paper2", "ticker_mentions.parquet")
OUT_TSV = os.path.join(ROOT, "reports", "paper2_windows_z.tsv")
NULLS_REG = os.path.join(ROOT, "preregistration_nulls.md")
DD_SUBS = ("SecurityAnalysis", "ValueInvesting", "StockMarket", "stocks",
           "investing")
WSB_SUBS = ("wallstreetbets",)
B_PRIMARY, B_SENS = 4, (6, 8)
EVAL_Q = 2
Q0, NQ = (2019, 0), 24
CASHTAG_UNINF = 20      # registered: <20 eligible -> UNINFORMATIVE
ONSET_Z, DEEP_Z = -3.0, -5.0
NULL_KINDS = ("label", "stratified")

REG_COLS = ["B", "window", "eval_start", "eval_end", "stratum", "lens",
            "build_docs", "eval_docs", "n_eligible", "obs_total",
            "null_mean", "null_sd", "z_seg", "formed", "binom_p",
            "uninformative"]
WIDE_COLS = ["null_kind", "R", "ratio", "null_min", "null_max",
             "mc_p_lo", "mc_p_hi", "mc_p_2s", "drift_reps", "inc_before",
             "inc_after", "collapsed_frac", "docs_changed", "toks_changed"]
# Headline cells (preregistration_nulls.md): the two chance windows before
# the onset, the two excursion windows, the onset window, the last window,
# and the two DD windows bracketing the control's 2021Q2 step.
HEADLINE = [(4, k, "WSB", "union") for k in (1, 2, 3, 4, 5, 18)] + \
           [(4, k, "DD", "union") for k in (4, 5)]


def qdate(k: int) -> datetime:
    y = Q0[0] + (Q0[1] + k) // 4
    q = (Q0[1] + k) % 4
    return datetime(y, q * 3 + 1, 1)


def qlabel(k: int) -> str:
    y = Q0[0] + (Q0[1] + k) // 4
    q = (Q0[1] + k) % 4
    return f"{y}Q{q + 1}"


def window_stat(rows, bs, be, ee, F=F_DEFAULT, null_kind="label", R=R,
                drift_reps=0):
    """run_gate.analyse's registered eval machinery, window-parameterized.

    With null_kind="label", R=100 the registered keys are computed by the
    registered lines, unchanged; the wide keys are added alongside."""
    assert null_kind in NULL_KINDS, null_kind
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
    out = {"build_docs": Nb, "eval_docs": len(edocs), "n_eligible": len(eligible),
           "null_kind": null_kind, "R": R, "drift_reps": drift_reps}
    idx = {p: j for j, p in enumerate(eligible)}
    n = len(eligible)
    nan = float("nan")
    if n == 0:
        out.update({"obs_total": 0, "null_mean": 0.0, "null_sd": 0.0,
                    "z_seg": 0.0, "formed": 0, "binom_p": 1.0,
                    "ratio": nan, "null_min": nan, "null_max": nan,
                    "mc_p_lo": nan, "mc_p_hi": nan, "mc_p_2s": nan,
                    "inc_before": nan, "inc_after": nan, "collapsed_frac": nan,
                    "docs_changed": nan, "toks_changed": nan})
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
    # document key is (author, year, quarter): the stratum is its quarter
    strata = [(d[1], d[2]) for d in inc_doc] if null_kind == "stratified" else None
    size_before, freq_before = (Counter(inc_doc), Counter(inc_tok.tolist())) \
        if drift_reps else (None, None)
    rng = np.random.default_rng(SHUFFLE_SEED)
    null = np.zeros((R, n), dtype=np.int32)
    drifts = []
    for r in range(R):
        if null_kind == "label":
            sh = label_shuffle(inc_doc, inc_tok, rng)
        else:
            sh = label_shuffle_stratified(inc_doc, inc_tok, rng, strata)
        null[r], _ = pair_counts(sh)
        if r < drift_reps:
            drifts.append(margin_drift(inc_doc, inc_tok, sh, size_before, freq_before))

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
    summ = null_summary(int(obs.sum()), totals)
    out.update({k: summ[k] for k in ("ratio", "null_min", "null_max",
                                     "mc_p_lo", "mc_p_hi", "mc_p_2s")})
    out.update(drift_mean(drifts))
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


def all_cells():
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
    return cells


_ROWS = {}   # per-process cache: (stratum, lens) -> rows


def load_rows(stratum, lens):
    key = (stratum, lens)
    if key not in _ROWS:
        subs = WSB_SUBS if stratum == "WSB" else DD_SUBS
        unit = "" if lens == "union" else "AND unit_type = 'cashtag'"
        con = duckdb.connect()
        _ROWS[key] = [
            r for r in con.sql(f"""
                SELECT author, time, ticker FROM '{MENTIONS}'
                WHERE subreddit IN {subs!r} {unit}
            """).fetchall() if r[2] not in EXCLUDED_TICKERS]
        con.close()
    return _ROWS[key]


def cell_job(job):
    B, k, stratum, lens, null_kind, R_, drift_reps = job
    bs, be, ee = qdate(k), qdate(k + B), qdate(k + B + EVAL_Q)
    st = window_stat(load_rows(stratum, lens), bs, be, ee,
                     null_kind=null_kind, R=R_, drift_reps=drift_reps)
    uninf = int(lens == "cashtag" and st["n_eligible"] < CASHTAG_UNINF)
    return {"B": B, "window": k, "eval_start": qlabel(k + B),
            "eval_end": qlabel(k + B + EVAL_Q - 1),
            "stratum": stratum, "lens": lens, **st, "uninformative": uninf}


def parse_cells(spec):
    out = []
    for item in spec.split(","):
        B, k, stratum, lens = item.strip().split(":")
        out.append((int(B), int(k), stratum, lens))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--null", choices=NULL_KINDS, default="label")
    ap.add_argument("--R", type=int, default=R)
    ap.add_argument("--out", default=None)
    ap.add_argument("--headline", action="store_true")
    ap.add_argument("--cells", default=None)
    ap.add_argument("--drift", type=int, default=None)
    args = ap.parse_args()

    reg = os.path.join(ROOT, "preregistration_paper2.md")
    assert os.path.exists(reg) and "STATUS: REGISTERED" in open(reg).read(), \
        "paper-2 registration not frozen — refusing to run eval"
    registered_null = args.null == "label" and args.R == R
    if not registered_null:
        assert os.path.exists(NULLS_REG) and \
            "STATUS: REGISTERED" in open(NULLS_REG).read(), \
            "nulls amendment not registered — refusing to run a new null"

    if args.cells:
        cells = parse_cells(args.cells)
    elif args.headline:
        cells = list(HEADLINE)
    else:
        cells = all_cells()
    subset = len(cells) != len(all_cells())

    if args.out is None:
        if registered_null and not subset:
            out_path = OUT_TSV
        else:
            assert not (registered_null and subset), \
                "a subset run of the registered null needs --out"
            tag = f"{args.null}_R{args.R}" + ("_headline" if args.headline else "")
            out_path = os.path.join(ROOT, "reports", f"paper2_windows_z_{tag}.tsv")
    else:
        out_path = args.out
    registered_out = os.path.abspath(out_path) == os.path.abspath(OUT_TSV)
    assert not registered_out or (registered_null and not subset), \
        "refusing to overwrite the registered TSV with anything but the full registered run"
    # the registered null never emits the diagnostic by default: a
    # reproduction check must not double as a peek at a new quantity
    drift_reps = args.drift if args.drift is not None else (0 if registered_null else 10)
    cols = REG_COLS if registered_out else REG_COLS + WIDE_COLS

    jobs = [(B, k, s, l, args.null, args.R, drift_reps) for B, k, s, l in cells]
    print(f"null={args.null} R={args.R} workers={args.workers} cells={len(cells)} "
          f"drift_reps={drift_reps} -> {out_path}", flush=True)

    results = {}
    with open(out_path, "w") as f:
        f.write("\t".join(cols) + "\n")
        if args.workers > 1:
            ctx = mp.get_context("spawn")
            pool = ctx.Pool(args.workers)
            it = pool.imap(cell_job, jobs, chunksize=1)
        else:
            pool = None
            it = map(cell_job, jobs)
        for rec in it:
            results[(rec["B"], rec["window"], rec["stratum"], rec["lens"])] = rec
            f.write("\t".join(str(rec[c]) for c in cols) + "\n")
            f.flush()
            print(f"B={rec['B']} {rec['eval_start']}..{rec['eval_end']} "
                  f"{rec['stratum']}/{rec['lens']}: n={rec['n_eligible']} "
                  f"obs={rec['obs_total']} null={rec['null_mean']:.1f} "
                  f"z={rec['z_seg']:+.2f} formed={rec['formed']}"
                  f"{' UNINFORMATIVE' if rec['uninformative'] else ''}", flush=True)
        if pool is not None:
            pool.close()
            pool.join()

    # ---- registered scoring, primary cells only ----
    nw = NQ - B_PRIMARY - EVAL_Q + 1
    have = all((B_PRIMARY, k, s, "union") in results
               for s in ("WSB", "DD") for k in range(nw))
    if not have:
        print(f"\nsubset run: registered scoring skipped\nresults: {out_path}")
        return
    wsb = [results[(B_PRIMARY, k, "WSB", "union")] for k in range(nw)]
    dd = [results[(B_PRIMARY, k, "DD", "union")] for k in range(nw)]
    zs = [r["z_seg"] for r in wsb]
    ow = onset_window(zs)
    print(f"\n== REGISTERED SCORING (primary: B=4, union; null={args.null}, R={args.R}) ==")
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
    print(f"\nresults: {out_path}")


if __name__ == "__main__":
    main()
