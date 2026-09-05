#!/usr/bin/env python3
"""Tier A positive control: run-3 rankers on a Science4Cast benchmark fold.

See preregistration_tier_a.md (written before any solution bit was read).

Input pkl (Krenn et al. NMI 2023, Zenodo 7882892):
  [edges (n,3) int [v1,v2,day-since-1990], pairs (10M,2), solution (10M,),
   year_start, delta, vertex_degree_cutoff, min_edges]
Usage: run_tier_a.py <pkl> [--sample FRAC] (sample = microbenchmark mode)
"""
import json
import os
import pickle
import sys
import time

import numpy as np

ROOT = os.environ.get("TIER_A_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.environ.get("TIER_A_BASE",
                      os.path.join(ROOT, "data", "science4cast"))
E_MIN = 2.0
K_VALUES = [50, 200, 1000]
RNG_SEED = 20260829
NV = 64719

POP = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint16)


def rank_auc(scores: np.ndarray, y: np.ndarray) -> float:
    """Mann-Whitney AUC (equivalent to the benchmark's calculate_ROC)."""
    order = np.argsort(scores, kind="stable")
    ranks = np.empty(len(scores)); ranks[order] = np.arange(1, len(scores) + 1)
    # average ranks for ties
    srt = scores[order]
    uniq, inv, cnt = np.unique(srt, return_inverse=True, return_counts=True)
    start = np.zeros(len(uniq)); start[1:] = np.cumsum(cnt)[:-1]
    avg = start + (cnt + 1) / 2.0
    ranks[order] = avg[inv]
    npos = int(y.sum()); nneg = len(y) - npos
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def p_at_k(scores: np.ndarray, y: np.ndarray, ks) -> dict:
    order = np.argsort(-scores, kind="stable")
    return {k: float(y[order[:k]].mean()) for k in ks if k <= len(y)}


def main() -> None:
    reg = open(f"{ROOT}/preregistration_tier_a.md").read()
    assert "Tier A registration" in reg
    pkl_path, frac = sys.argv[1], 1.0
    if "--sample" in sys.argv:
        frac = float(sys.argv[sys.argv.index("--sample") + 1])

    t0 = time.time()
    with open(pkl_path, "rb") as f:
        edges, pairs, sol, year_start, delta, cutoff, minedge = pickle.load(f)
    edges = np.asarray(edges); pairs = np.asarray(pairs)
    sol = np.asarray(sol).astype(np.int8)
    print(f"fold: build<=end-{year_start} predict+{delta}y cutoff={cutoff} "
          f"minedge={minedge} | {len(edges)} edge events | {len(pairs)} pairs "
          f"| base rate {sol.mean():.5%}")

    if frac < 1.0:
        n = int(len(pairs) * frac)
        pairs, sol = pairs[:n], sol[:n]
        print(f"MICROBENCH: first {n} pairs")

    # build-graph stats: weighted degree, unique-edge neighbor bitsets
    s = np.bincount(edges[:, 0], minlength=NV) + np.bincount(edges[:, 1], minlength=NV)
    M = len(edges)
    a = np.minimum(edges[:, 0], edges[:, 1]).astype(np.int64)
    b = np.maximum(edges[:, 0], edges[:, 1]).astype(np.int64)
    uniq = np.unique(a * NV + b)
    ua, ub = uniq // NV, uniq % NV
    print(f"unique undirected edges: {len(uniq)} ({time.time()-t0:.0f}s)")
    nbytes = (NV + 7) // 8
    A = np.zeros((NV, nbytes), dtype=np.uint8)
    for rr, cc in ((ua, ub), (ub, ua)):
        np.bitwise_or.at(A, (rr, cc // 8), (1 << (cc % 8)).astype(np.uint8))
    udeg = POP[A].sum(axis=1).astype(np.int64)
    print(f"bitsets built ({time.time()-t0:.0f}s); "
          f"mean unweighted degree {udeg[udeg>0].mean():.1f}")

    vecs = np.load(f"{BASE}/concept_embeddings.npy")

    i, j = pairs[:, 0], pairs[:, 1]
    E = s[i].astype(np.float64) * s[j] / (2 * M)
    freq_product = s[i].astype(np.float64) * s[j]
    affinity = np.zeros(len(pairs), dtype=np.float64)
    cn = np.zeros(len(pairs), dtype=np.int32)
    chunk = 50_000
    for c0 in range(0, len(pairs), chunk):
        c1 = min(c0 + chunk, len(pairs))
        affinity[c0:c1] = np.einsum("ij,ij->i", vecs[i[c0:c1]], vecs[j[c0:c1]])
        cn[c0:c1] = POP[np.bitwise_and(A[i[c0:c1]], A[j[c0:c1]])].sum(axis=1)
        if c0 % (chunk * 40) == 0:
            print(f"  cn {c1}/{len(pairs)} ({time.time()-t0:.0f}s)")
    print(f"features done ({time.time()-t0:.0f}s)")

    rng = np.random.default_rng(RNG_SEED)
    rankers = {
        "suppr_affinity": E * affinity,
        "affinity_only": affinity,
        "common_neighbors": cn.astype(np.float64),
        "freq_product": freq_product,
        "random": rng.random(len(pairs)),
    }
    universes = {"full_sample": np.ones(len(pairs), dtype=bool),
                 "suppressed_E>=2": E >= E_MIN}
    out = {"fold": [int(year_start), int(delta), int(cutoff), int(minedge)],
           "n_pairs": len(pairs), "results": {}}
    for uname, mask in universes.items():
        ym = sol[mask]
        print(f"\n== {uname}: {int(mask.sum())} pairs, "
              f"{int(ym.sum())} formed ({ym.mean():.5%}) ==")
        ks = [k for k in K_VALUES if k <= mask.sum()]
        hdr = f"{'ranker':<18}" + "".join(f"P@{k:<8}" for k in ks) + "AUC"
        print(hdr)
        out["results"][uname] = {"n": int(mask.sum()), "formed": int(ym.sum())}
        for name, sc in rankers.items():
            pk = p_at_k(sc[mask], ym, ks)
            auc = rank_auc(sc[mask], ym)
            out["results"][uname][name] = {"p_at_k": pk, "auc": auc}
            print(f"{name:<18}" + "".join(f"{pk[k]:<10.4f}" for k in ks)
                  + f"{auc:.4f}")

    # qualitative: top-30 suppressed pairs by common_neighbors, with outcomes
    names = [l.rstrip("\n") for l in open(f"{BASE}/full_concepts_new.txt")]
    mask = universes["suppressed_E>=2"]
    if mask.sum() > 0:
        idx = np.flatnonzero(mask)
        top = idx[np.argsort(-cn[idx], kind="stable")[:30]]
        print("\nTop suppressed pairs by common_neighbors:")
        for t in top:
            print(f"  cn={cn[t]:5d} E={E[t]:7.1f} formed={int(sol[t])}  "
                  f"'{names[i[t]]}' <-> '{names[j[t]]}'")

    if frac == 1.0:
        tag = f"y{year_start}_d{delta}_c{cutoff}_m{minedge}"
        json.dump(out, open(f"{BASE}/tier_a_{tag}.json", "w"), indent=1)
        print(f"\nsaved tier_a_{tag}.json")


if __name__ == "__main__":
    main()
