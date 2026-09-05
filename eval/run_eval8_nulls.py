#!/usr/bin/env python3
"""Paper 1, new nulls on the four run-8 cells (preregistration_nulls.md).

run_eval8.py stays frozen: its single generator stream across the four
cells (author fold1, fold2, thread fold1, fold2) is part of the registered
record and cannot be parallelized without changing every number. This
script reuses its universe builders, eligibility, and pair counting
verbatim, seeds each cell independently (default_rng([SEED, cell_index])),
and draws the null through eval/nulls.py:

  --null label       the registered sampler under per-cell seeds; z should
                     match run 8 within Monte Carlo noise (a seeding check,
                     not a reproduction of run 8)
  --null stratified  labels permuted within the document's calendar
                     quarter (author space: the quarter in the document
                     key; thread space: the quarter of the thread's first
                     claim)
  --R N              replicates (default 100)
  --workers N        cells in a spawn pool (max useful: 4)
  --drift N          margin-drift diagnostic on the first N replicates
                     (default 10)

Refuses to run unless preregistration_nulls.md reads STATUS: REGISTERED.
Writes reports/paper1_nulls_<null>_R<R>.tsv and, per space, a JSON with
the formed pairs next to the run-8 JSONs.
"""
import argparse
import hashlib
import json
import multiprocessing as mp
import os
import platform
import subprocess
import sys
from pathlib import Path
from collections import Counter, defaultdict

import duckdb
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_eval8 import (  # noqa: E402
    author_universe, thread_universe, eligible_set, pair_doc_counts,
    binom_sf_ge, FOLDS, SEED, PC, ROOT)
from nulls import (label_shuffle, label_shuffle_stratified, margin_drift,  # noqa: E402
                   null_summary, drift_mean)

NULLS_REG = os.path.join(ROOT, "preregistration_nulls.md")
CELLS = [("author", "fold1"), ("author", "fold2"),
         ("thread", "fold1"), ("thread", "fold2")]
COLS = ["space", "fold", "null_kind", "R", "seed", "build_docs", "eval_docs",
        "frequent", "eligible", "obs_total", "null_mean", "null_sd", "z_seg",
        "ratio", "null_min", "null_max", "mc_p_lo", "mc_p_hi", "mc_p_2s",
        "formed", "floor", "binom_p", "drift_reps", "inc_before", "inc_after",
        "collapsed_frac", "docs_changed", "toks_changed"]


def thread_doc_quarter():
    con = duckdb.connect()
    rows = con.sql(f"SELECT doc_id, min(time) FROM read_parquet('{PC}/claims.parquet') "
                   "GROUP BY doc_id").fetchall()
    con.close()
    return {d: (t.year, (t.month - 1) // 3) for d, t in rows}


def summarize_counts(obs, null, eligible, supported):
    """Pool replicate counts before estimating moments and pair thresholds."""
    p99 = np.percentile(null, 99, axis=0)
    formed = [(list(p), int(obs[j]), float(p99[j]))
              for j, p in enumerate(eligible)
              if supported[j] and obs[j] > p99[j] and obs[j] >= 2]
    return null_summary(int(obs.sum()), null.sum(axis=1)), formed


def cell_stat(space, fold_name, be, ee, null_kind, R, drift_reps, seed,
              batches=None, artifact_dir=None):
    bdoc, edoc, author_fn = (author_universe if space == "author"
                             else thread_universe)(be, ee)
    fs, eligible = eligible_set(bdoc)
    eligible = sorted(eligible)
    idx = {p: j for j, p in enumerate(eligible)}
    n = len(eligible)
    obs, docs_of = pair_doc_counts(edoc, fs, idx)
    reference_path = (os.path.join(ROOT, "data", "registry", "run5_author",
                                   "run8_author.json") if space == "author"
                      else os.path.join(PC, "run8_thread.json"))
    with open(reference_path) as f:
        reference = json.load(f)[fold_name]
    if n != reference["eligible"] or int(obs.sum()) != reference["obs_total"]:
        raise RuntimeError(f"{space}/{fold_name}: observed structure differs from run 8")
    supported = np.array([len({author_fn(d) for d in docs_of.get(p, set())}) >= 2
                          for p in eligible])
    if space == "author":
        quarter_of = lambda d: (d[1], d[2])  # noqa: E731
    elif null_kind == "stratified":
        tq = thread_doc_quarter()
        quarter_of = lambda d: tq[d]        # noqa: E731
    inc_doc, inc_con = [], []
    # sorted() on documents too (run 8 iterated edoc in insertion order;
    # this is a new stream, so the stricter clause applies)
    for d in sorted(edoc):
        for c in sorted(edoc[d] & fs):
            inc_doc.append(d)
            inc_con.append(c)
    inc_con = np.array(inc_con, dtype=object)
    strata = [quarter_of(d) for d in inc_doc] if null_kind == "stratified" else None
    size_before, freq_before = (Counter(inc_doc), Counter(inc_con.tolist())) \
        if drift_reps else (None, None)
    batch_count = batches if batches is not None else 1
    seeds = [seed + [s] for s in range(batch_count)] if batches is not None else [seed]
    null = np.zeros((R * batch_count, n), dtype=np.int32)
    drifts = []
    batch_summaries = []
    for s, batch_seed in enumerate(seeds):
        rng = np.random.default_rng(batch_seed)
        for r in range(R):
            sh = label_shuffle(inc_doc, inc_con, rng) if null_kind == "label" \
                else label_shuffle_stratified(inc_doc, inc_con, rng, strata)
            null[s * R + r], _ = pair_doc_counts(sh, fs, idx)
            if r < drift_reps:
                drifts.append(margin_drift(inc_doc, inc_con, sh, size_before, freq_before))
            if (r + 1) % 20 == 0:
                print(f"  {space} {fold_name} {null_kind} batch {s+1}/{batch_count} "
                      f"rep {r+1}/{R}", flush=True)
        bs, bf = summarize_counts(obs, null[s * R:(s + 1) * R], eligible, supported)
        batch_summaries.append({"batch": s, "seed": batch_seed, **bs,
                                "formed": len(bf)})
    summ, formed = summarize_counts(obs, null, eligible, supported)
    k = len(formed)
    rec = {"space": space, "fold": fold_name, "null_kind": null_kind, "R": len(null),
           "seed": str(seeds if batches is not None else seed),
           "build_docs": len(bdoc), "eval_docs": len(edoc),
           "frequent": len(fs), "eligible": n, "obs_total": int(obs.sum()),
           **{k_: summ[k_] for k_ in ("null_mean", "null_sd", "z_seg", "ratio",
                                     "null_min", "null_max", "mc_p_lo",
                                     "mc_p_hi", "mc_p_2s")},
           "formed": k, "floor": 0.01 * n,
           "binom_p": binom_sf_ge(k, n, 0.01) if k else 1.0,
           "drift_reps": len(drifts), **drift_mean(drifts),
           "formed_pairs": formed, "batches": batch_summaries,
           "reference_structure_matches": True}
    if artifact_dir is not None:
        path = Path(artifact_dir) / f"{space}_{fold_name}.npz"
        # Exclusive creation protects an earlier realization from replacement.
        with path.open("xb") as f:
            np.savez_compressed(f, observed=obs, null_counts=null,
                                eligible=np.asarray(eligible, dtype=str),
                                supported=supported, seeds=np.asarray(seeds))
        rec["replicate_artifact"] = str(path.relative_to(ROOT))
        rec["replicate_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return rec


def cell_job(job):
    ci, null_kind, R, drift_reps, batches, artifact_dir = job
    space, fold_name = CELLS[ci]
    be, ee = next((b, e) for nm, b, e in FOLDS if nm == fold_name)
    seed = [SEED, ci]
    return cell_stat(space, fold_name, be, ee, null_kind, R, drift_reps, seed,
                     batches, artifact_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--null", choices=("label", "stratified"), default="stratified")
    ap.add_argument("--R", type=int, default=100)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--drift", type=int, default=10)
    ap.add_argument("--space", choices=("all", "author", "thread"), default="all")
    ap.add_argument("--seeds", type=int, default=None,
                    help="A1 thread analysis: 10 batches, pooled for primary estimates")
    args = ap.parse_args()
    assert os.path.exists(NULLS_REG) and "STATUS: REGISTERED" in open(NULLS_REG).read(), \
        "nulls amendment not registered — refusing to run"
    if args.R < 2 or args.workers < 1 or not 0 <= args.drift <= args.R:
        ap.error("R >= 2, workers >= 1 and 0 <= drift <= R required")
    if args.seeds is not None and (args.seeds, args.R, args.null, args.space) != \
            (10, 100, "label", "thread"):
        ap.error("A1 registers --seeds 10 only with --R 100 --null label --space thread")
    tag = f"{args.null}_R{args.R}"
    if args.space != "all":
        tag += f"_{args.space}"
    if args.seeds is not None:
        tag += f"_seeds{args.seeds}"
    out_tsv = os.path.join(ROOT, "reports", f"paper1_nulls_{tag}.tsv")
    artifact_dir = os.path.join(ROOT, "data", "registry", "nulls_revisions", tag)
    Path(artifact_dir).mkdir(parents=True, exist_ok=False)
    jobs = [(ci, args.null, args.R, args.drift, args.seeds, artifact_dir)
            for ci, (space, _) in enumerate(CELLS)
            if args.space == "all" or space == args.space]
    print(f"null={args.null} R={args.R} workers={args.workers} -> {out_tsv}", flush=True)
    if args.workers > 1:
        pool = mp.get_context("spawn").Pool(min(args.workers, len(CELLS)))
        it = pool.imap(cell_job, jobs, chunksize=1)
    else:
        pool = None
        it = map(cell_job, jobs)
    recs = []
    with open(out_tsv, "x") as f:
        f.write("\t".join(COLS) + "\n")
        for rec in it:
            recs.append(rec)
            f.write("\t".join(str(rec[c]) for c in COLS) + "\n")
            f.flush()
            print(f"NULLS {rec['space']} {rec['fold']} {rec['null_kind']} R={rec['R']}: "
                  f"obs {rec['obs_total']} vs null {rec['null_mean']:.0f} "
                  f"(sd {rec['null_sd']:.0f}) z={rec['z_seg']:+.1f} "
                  f"ratio={rec['ratio']:.3f} formed {rec['formed']}/{rec['eligible']} "
                  f"(floor {rec['floor']:.1f}) collapsed_frac={rec['collapsed_frac']:.4f}",
                  flush=True)
    if pool is not None:
        pool.close()
        pool.join()
    for space, path in (("author", os.path.join(ROOT, "data", "registry", "run5_author")),
                        ("thread", PC)):
        js = {r["fold"]: r for r in recs if r["space"] == space}
        if not js:
            continue
        with open(os.path.join(path, f"run8_nulls_{tag}.json"), "x") as f:
            json.dump(js, f, indent=1)
    manifest = {"commit": subprocess.check_output(["git", "-C", ROOT, "rev-parse", "HEAD"],
                                                   text=True).strip(),
                "python": sys.version, "architecture": platform.machine(),
                "numpy": np.__version__, "duckdb": duckdb.__version__,
                "rng": "numpy.random.PCG64", "ddof": 0,
                "arguments": vars(args), "cells": recs}
    with open(os.path.join(ROOT, "reports", f"paper1_nulls_{tag}.json"), "x") as f:
        json.dump(manifest, f, indent=2)
    if args.seeds is not None:
        columns = ["space", "fold", "batch", "seed", "R", "null_mean", "null_sd",
                   "z_seg", "ratio", "formed"]
        with open(out_tsv.replace(".tsv", "_batches.tsv"), "x") as f:
            f.write("\t".join(columns) + "\n")
            for rec in recs:
                for batch in rec["batches"]:
                    row = {"space": rec["space"], "fold": rec["fold"], **batch}
                    f.write("\t".join(str(row[c]) for c in columns) + "\n")
    print(f"results: {out_tsv}")


if __name__ == "__main__":
    main()
