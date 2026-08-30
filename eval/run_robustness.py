#!/usr/bin/env python3
"""Registered robustness suite R1-R4 (see preregistration_robustness.md).

Universe/constants are run 5's (preregistration_run5.md). Modes:
  --r1   placebo: eval-window label shuffle, 100 replicates/fold
  --r2   document-window sensitivity: (author, month) and (author, half)
  --r3   formation x articulation cross-tab + timing on formed pairs
  --r4   conservative comment lens (drop rows author == story author)
Log to data/registry/run5_author/robustness_<mode>.log via redirection.
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from itertools import combinations

import duckdb
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AC = os.path.join(ROOT, "data", "registry", "run5_author", "author_concepts.parquet")
RAW = os.path.join(ROOT, "data", "raw", "hn_bq")
OUTDIR = os.path.join(ROOT, "data", "registry", "run5_author")
BUILD_START = datetime(2015, 1, 1)
FOLDS = [  # (name, build_end, eval_end)
    ("fold1", datetime(2017, 1, 1), datetime(2018, 1, 1)),
    ("fold2", datetime(2016, 1, 1), datetime(2017, 1, 1)),
]
F = 20
E_MIN = 2.0
HUB_MAX = 100
R1_REPS = 100
R1_SEED = 20260830


def load_rows(drop_story_author=False):
    con = duckdb.connect()
    if drop_story_author:
        q = f"""
            SELECT a.author, a.time, a.concept
            FROM read_parquet('{AC}') a
            JOIN '{RAW}/stories_filtered.parquet' s ON a.doc_id = s.id
            WHERE a.author IS DISTINCT FROM s."by" """
    else:
        q = f"SELECT author, time, concept FROM read_parquet('{AC}')"
    return con.sql(q).fetchall()


def bucket(ts, window):
    if window == "quarter":
        return (ts.year, (ts.month - 1) // 3)
    if window == "month":
        return (ts.year, ts.month)
    if window == "half":
        return (ts.year, (ts.month - 1) // 6)
    raise ValueError(window)


def build_docs(rows, build_end, eval_end, window):
    bdoc, edoc = defaultdict(set), defaultdict(set)
    for author, ts, concept in rows:
        if BUILD_START <= ts < build_end:
            bdoc[(author, *bucket(ts, window))].add(concept)
        elif build_end <= ts < eval_end:
            edoc[(author, *bucket(ts, window))].add(concept)
    bdoc = {k: v for k, v in bdoc.items() if len(v) <= HUB_MAX}
    edoc = {k: v for k, v in edoc.items() if len(v) <= HUB_MAX}
    return bdoc, edoc


def eligible_pairs(bdoc):
    bfreq = defaultdict(int)
    for s in bdoc.values():
        for c in s:
            bfreq[c] += 1
    fs = {c for c, n in bfreq.items() if n >= F}
    Nb = len(bdoc)
    co = set()
    for s in bdoc.values():
        ss = sorted(s & fs)
        for a, b in combinations(ss, 2):
            co.add((a, b))
    fl = sorted(fs, key=lambda c: -bfreq[c])
    eligible = []
    for idx, a in enumerate(fl):
        fa = bfreq[a]
        for b in fl[idx + 1:]:
            E = fa * bfreq[b] / Nb
            if E < E_MIN:
                break
            key = (min(a, b), max(a, b))
            if key not in co:
                eligible.append(key)
    return fs, set(eligible)


def formed_pairs(edoc, fs, eligible):
    """Formation restricted to the eligible set; returns pair -> doc set."""
    efreq = defaultdict(int)
    epair = defaultdict(set)
    for d, s in edoc.items():
        ss = sorted(s & fs)
        for c in ss:
            efreq[c] += 1
        for pr in combinations(ss, 2):
            if pr in eligible:
                epair[pr].add(d)
    Ne = len(edoc)
    formed = {}
    for pair, docs in epair.items():
        a, b = pair
        E = efreq[a] * efreq[b] / Ne
        if len(docs) >= 2 and len({d[0] for d in docs}) >= 2 and \
           (len(docs) - E) / max(np.sqrt(E), 1e-9) >= 2.0:
            formed[pair] = docs
    return formed


def r1():
    rows = load_rows()
    rng = np.random.default_rng(R1_SEED)
    out = {}
    for name, be, ee in FOLDS:
        bdoc, edoc = build_docs(rows, be, ee, "quarter")
        fs, eligible = eligible_pairs(bdoc)
        observed = len(formed_pairs(edoc, fs, eligible))
        print(f"{name}: eligible {len(eligible)} observed formed {observed}",
              flush=True)
        docs = list(edoc.keys())
        inc_doc, inc_con = [], []
        for d in docs:
            for c in edoc[d] & fs:
                inc_doc.append(d)
                inc_con.append(c)
        inc_con = np.array(inc_con, dtype=object)
        null_counts = []
        for r in range(R1_REPS):
            perm = rng.permutation(inc_con)
            sh = defaultdict(set)
            for d, c in zip(inc_doc, perm):
                sh[d].add(c)
            null_counts.append(len(formed_pairs(sh, fs, eligible)))
            if (r + 1) % 10 == 0:
                print(f"  {name} rep {r+1}/{R1_REPS} "
                      f"(running mean {np.mean(null_counts):.2f})", flush=True)
        nc = np.array(null_counts)
        out[name] = {"observed": observed, "eligible": len(eligible),
                     "null_mean": float(nc.mean()),
                     "null_p99": float(np.percentile(nc, 99)),
                     "null_max": int(nc.max()),
                     "null_counts": null_counts}
        print(f"R1 {name}: observed {observed} vs null mean {nc.mean():.2f} "
              f"p99 {np.percentile(nc, 99):.1f} max {nc.max()}", flush=True)
    json.dump(out, open(os.path.join(OUTDIR, "robustness_r1.json"), "w"),
              indent=1)


def r2():
    rows = load_rows()
    out = {}
    for window in ("month", "half"):
        for name, be, ee in FOLDS:
            bdoc, edoc = build_docs(rows, be, ee, window)
            fs, eligible = eligible_pairs(bdoc)
            formed = formed_pairs(edoc, fs, eligible)
            n, h = len(eligible), len(formed)
            out[f"{window}_{name}"] = {"eligible": n, "formed": h,
                                       "rate": h / n if n else None}
            print(f"R2 {window} {name}: build docs {len(bdoc)} "
                  f"F>=20 concepts {len(fs)} eligible {n} formed {h} "
                  f"({h/max(n,1):.2%})", flush=True)
    json.dump(out, open(os.path.join(OUTDIR, "robustness_r2.json"), "w"),
              indent=1)


def r3():
    rows = load_rows()
    con = duckdb.connect()
    claims = con.sql(f"""
        SELECT doc_id, claim_id, min(time) AS ts, list(DISTINCT concept)
        FROM read_parquet('{AC}') GROUP BY doc_id, claim_id""").fetchall()
    out = {}
    for name, be, ee in FOLDS:
        bdoc, edoc = build_docs(rows, be, ee, "quarter")
        fs, eligible = eligible_pairs(bdoc)
        formed = formed_pairs(edoc, fs, eligible)
        print(f"{name}: formed {len(formed)}", flush=True)
        # first co-mention quarter per formed pair (earliest eval doc)
        first_co = {p: min((d[1], d[2]) for d in docs)
                    for p, docs in formed.items()}
        # articulating claims across full cache 2015-2017
        art_all = defaultdict(list)   # pair -> [claim ts]
        fset = set(formed)
        for _, _, ts, cl in claims:
            cs = sorted(set(cl) & fs)
            if len(cs) < 2:
                continue
            for pr in combinations(cs, 2):
                if pr in fset:
                    art_all[pr].append(ts)
        never = [p for p in formed if p not in art_all]
        in_eval = [p for p, tss in art_all.items()
                   if any(be <= t < ee for t in tss)]
        led, tied, lagged = [], [], []
        for p, tss in art_all.items():
            aq = min((t.year, (t.month - 1) // 3) for t in tss)
            cq = first_co[p]
            (led if cq < aq else tied if cq == aq else lagged).append(
                (p, cq, aq))
        print(f"R3 {name}: formed {len(formed)} | never articulated "
              f"(2015-2017 cache) {len(never)} | articulated-in-eval "
              f"{len(in_eval)}", flush=True)
        print(f"  timing among articulated: co-mention first {len(led)}, "
              f"same quarter {len(tied)}, articulation first {len(lagged)}",
              flush=True)
        for p, cq, aq in sorted(led + tied + lagged):
            print(f"    {p[0]!r} <-> {p[1]!r}: first co-mention {cq}, "
                  f"first articulation {aq}", flush=True)
        out[name] = {"formed": len(formed), "never_articulated": len(never),
                     "articulated_in_eval": len(in_eval),
                     "co_first": len(led), "same_q": len(tied),
                     "art_first": len(lagged)}
    json.dump(out, open(os.path.join(OUTDIR, "robustness_r3.json"), "w"),
              indent=1)


def r4():
    rows = load_rows(drop_story_author=True)
    print(f"comment-lens rows: {len(rows)}", flush=True)
    out = {}
    for name, be, ee in FOLDS:
        bdoc, edoc = build_docs(rows, be, ee, "quarter")
        fs, eligible = eligible_pairs(bdoc)
        formed = formed_pairs(edoc, fs, eligible)
        n, h = len(eligible), len(formed)
        out[name] = {"eligible": n, "formed": h,
                     "rate": h / n if n else None}
        print(f"R4 {name}: build docs {len(bdoc)} F>=20 {len(fs)} "
              f"eligible {n} formed {h} ({h/max(n,1):.2%})", flush=True)
    json.dump(out, open(os.path.join(OUTDIR, "robustness_r4.json"), "w"),
              indent=1)


def main():
    reg = open(os.path.join(ROOT, "preregistration_robustness.md")).read()
    assert "Robustness registration" in reg
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    {"--r1": r1, "--r2": r2, "--r3": r3, "--r4": r4}[mode]()


if __name__ == "__main__":
    main()
