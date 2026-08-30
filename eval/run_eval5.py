#!/usr/bin/env python3
"""Registered run 5: author-as-document re-cut (see preregistration_run5.md).

Document = (author, calendar quarter) over quote-attributed concepts.
Eligible: F>=20 concepts, E_build >= 2, observed build co-occurrence 0.
Outcome:  >=2 eval author-docs, >=2 distinct authors, eval z >= 2.

Modes:
  --density   outcome-blind build-window stats only (for the registration)
  (default)   full registered eval
Args: BUILD_END EVAL_END, e.g. 2017-01-01 2018-01-01 (build starts 2015-01-01)
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AC = os.path.join(ROOT, "data", "registry", "run5_author", "author_concepts.parquet")
EMB = os.path.join(ROOT, "data", "registry", "pilot1_concepts")
BUILD_START = "2015-01-01"
F = 20
E_MIN = 2.0
HUB_MAX = 100
K_VALUES = [50, 200, 1000]
RNG_SEED = 20260829


def main() -> None:
    reg = open(os.path.join(ROOT, "preregistration_run5.md")).read()
    assert "Run 5 registration" in reg
    density = "--density" in sys.argv
    noguard = "--noguard" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    build_end, eval_end = args[0], args[1]
    bs = datetime.fromisoformat(BUILD_START)
    be = datetime.fromisoformat(build_end)
    ee = datetime.fromisoformat(eval_end)

    con = duckdb.connect()
    rows = con.sql(f"""
        SELECT author, year(time) AS y, (month(time)-1)//3 AS q, concept, time
        FROM read_parquet('{AC}')""").fetchall()
    bdoc, edoc = defaultdict(set), defaultdict(set)
    for author, y, q, concept, ts in rows:
        if bs <= ts < be:
            bdoc[(author, y, q)].add(concept)
        elif be <= ts < ee:
            edoc[(author, y, q)].add(concept)
    if not noguard:
        nb, ne = len(bdoc), len(edoc)
        bdoc = {k: v for k, v in bdoc.items() if len(v) <= HUB_MAX}
        edoc = {k: v for k, v in edoc.items() if len(v) <= HUB_MAX}
        print(f"hub guard dropped build {nb-len(bdoc)}, eval {ne-len(edoc)}")
    print(f"build author-docs {len(bdoc)} | eval author-docs {len(edoc)}")

    bfreq = defaultdict(set)
    for d, s in bdoc.items():
        for c in s:
            bfreq[c].add(d)
    sizes = np.array([len(v) for v in bdoc.values()])
    print(f"concepts/author-doc: median {np.median(sizes):.0f} "
          f"p90 {np.percentile(sizes,90):.0f} max {sizes.max()}")
    for f_try in (20, 10):
        print(f"concepts with F>={f_try}: "
              f"{sum(1 for v in bfreq.values() if len(v) >= f_try)}")
    fs = {c for c, v in bfreq.items() if len(v) >= F}
    Nb = len(bdoc)

    co = defaultdict(int)
    neigh = defaultdict(set)
    for d, s in bdoc.items():
        ss = sorted(s & fs)
        for x in range(len(ss)):
            for y in range(x + 1, len(ss)):
                co[(ss[x], ss[y])] += 1
                neigh[ss[x]].add(ss[y])
                neigh[ss[y]].add(ss[x])
    print(f"frequent concepts {len(fs)} | build co-occurring pairs {len(co)}")

    fl = sorted(fs, key=lambda c: -len(bfreq[c]))
    eligible = []
    for idx, a in enumerate(fl):
        fa = len(bfreq[a])
        for b in fl[idx + 1:]:
            E = fa * len(bfreq[b]) / Nb
            if E < E_MIN:
                break
            key = (min(a, b), max(a, b))
            if co.get(key, 0):
                continue
            eligible.append({"pair": key, "E": E, "fa": fa,
                             "fb": len(bfreq[b])})
    print(f"eligible suppressed pairs: {len(eligible)}")
    if density:
        print("DENSITY MODE — stopping before any outcome computation.")
        return

    # rankers
    vecs = np.load(os.path.join(EMB, "embeddings.npy"))
    texts = json.load(open(os.path.join(EMB, "claim_texts.json")))
    vec_of = {t: k for k, t in enumerate(texts)}
    for p in eligible:
        a, b = p["pair"]
        cos = 0.0
        if a in vec_of and b in vec_of:
            cos = float(vecs[vec_of[a]] @ vecs[vec_of[b]])
        p["affinity"] = cos
        p["suppression_affinity"] = p["E"] * cos
        p["common_neighbors"] = len(neigh[a] & neigh[b])
        p["freq_product"] = p["fa"] * p["fb"]

    # outcome
    epair = defaultdict(set)
    efreq = defaultdict(int)
    for d, s in edoc.items():
        ss = sorted(s & fs)
        for c in ss:
            efreq[c] += 1
        for x in range(len(ss)):
            for y in range(x + 1, len(ss)):
                epair[(ss[x], ss[y])].add(d)
    Ne = len(edoc)
    formed = set()
    for pair, docs in epair.items():
        a, b = pair
        E = efreq[a] * efreq[b] / Ne
        if len(docs) >= 2 and len({d[0] for d in docs}) >= 2 and \
           (len(docs) - E) / max(np.sqrt(E), 1e-9) >= 2.0:
            formed.add(pair)
    hits = sum(1 for p in eligible if p["pair"] in formed)
    print(f"HEADLINE — formed among eligible suppressed: {hits}/{len(eligible)} "
          f"({hits / max(len(eligible), 1):.4%})")

    rng = np.random.default_rng(RNG_SEED)
    ks = [k for k in K_VALUES if k <= len(eligible)] or [len(eligible)]
    rankers = {
        "common_neighbors": sorted(eligible, key=lambda p: -p["common_neighbors"]),
        "freq_product": sorted(eligible, key=lambda p: -p["freq_product"]),
        "suppr_affinity": sorted(eligible, key=lambda p: -p["suppression_affinity"]),
        "affinity_only": sorted(eligible, key=lambda p: -p["affinity"]),
        "random": list(rng.permutation(np.array(eligible, dtype=object))),
    }
    print(f"{'ranker':<18}" + "".join(f"P@{k:<8}" for k in ks))
    results = {}
    for name, ranked in rankers.items():
        results[name] = {k: sum(1 for p in ranked[:k] if p["pair"] in formed) / k
                         for k in ks}
        print(f"{name:<18}" + "".join(f"{results[name][k]:<10.4f}" for k in ks))

    print("\nTop suppressed author-space pairs by common_neighbors:")
    for p in rankers["common_neighbors"][:30]:
        a, b = p["pair"]
        print(f"  cn={p['common_neighbors']:5d} E={p['E']:6.1f} "
              f"formed={int(p['pair'] in formed)}  '{a}' <-> '{b}'")

    tag = f"b{build_end[:4]}_e{eval_end[:4]}" + ("_noguard" if noguard else "")
    json.dump({"n_eligible": len(eligible), "hits": hits, "results": results},
              open(os.path.join(ROOT, "data", "registry", "run5_author",
                                f"eval5_{tag}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
