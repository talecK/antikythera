#!/usr/bin/env python3
"""Registered run 3: suppressed-pair formulation (see preregistration.md).

Eligible: F>=20 concept pairs, E_build >= 2, observed build co-occurrence 0.
Outcome:  chance-calibrated formation (eval z>=2, >=2 docs, >=2 authors).
Rankers:  suppression_affinity (E_build * cos), affinity_only,
          common_neighbors, freq_product (confound control), random.
"""
import json
import os
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("REGISTRY_OUT", os.path.join(ROOT, "data", "registry", "pilot1_concepts"))
EVAL_START = os.environ.get("EVAL_START", "2017-01-01")
EVAL_END = os.environ.get("EVAL_END", "2018-01-01")
F = 20
E_MIN = 2.0
K_VALUES = [50, 200, 1000]
RNG_SEED = 20260830


def main() -> None:
    prereg = open(os.path.join(ROOT, "preregistration.md")).read()
    assert "REGISTERED RUN 3" in prereg, "run 3 not registered"
    es, ee = datetime.fromisoformat(EVAL_START), datetime.fromisoformat(EVAL_END)

    con = duckdb.connect()
    rows = con.sql(f"""
        SELECT c.doc_id, c.claim, c.time, d."by" AS author
        FROM read_parquet('{OUT}/claims.parquet') c
        JOIN (SELECT doc_id, min(authors[1]) AS "by"
              FROM read_parquet('{ROOT}/data/docs/docs_*.parquet') GROUP BY doc_id) d
          ON c.doc_id = d.doc_id
    """).fetchall()

    bfreq = defaultdict(set)
    bdoc, edoc = defaultdict(set), defaultdict(set)
    author_of = {}
    for d, c, ts, by in rows:
        author_of[d] = by
        if ts < es:
            bfreq[c].add(d)
            bdoc[d].add(c)
        elif ts < ee:
            edoc[d].add(c)
    fs = {c for c, v in bfreq.items() if len(v) >= F}
    Nb = len(bdoc)
    print(f"build docs {Nb} | eval docs {len(edoc)} | frequent concepts {len(fs)}")

    co = defaultdict(int)
    neigh = defaultdict(set)
    for d, s in bdoc.items():
        ss = sorted(s & fs)
        for x in range(len(ss)):
            for y in range(x + 1, len(ss)):
                co[(ss[x], ss[y])] += 1
                neigh[ss[x]].add(ss[y])
                neigh[ss[y]].add(ss[x])

    # embeddings for affinity
    vecs = np.load(os.path.join(OUT, "embeddings.npy"))
    texts = json.load(open(os.path.join(OUT, "claim_texts.json")))
    vec_of = {t: k for k, t in enumerate(texts)}

    fl = sorted(fs, key=lambda c: -len(bfreq[c]))
    eligible = []
    for i, a in enumerate(fl):
        fa = len(bfreq[a])
        va = vecs[vec_of[a]]
        for b in fl[i + 1:]:
            E = fa * len(bfreq[b]) / Nb
            if E < E_MIN:
                break
            key = (min(a, b), max(a, b))
            if co.get(key, 0):
                continue
            cos = float(va @ vecs[vec_of[b]])
            eligible.append({
                "pair": key, "E": E, "affinity": cos,
                "suppression_affinity": E * cos,
                "common_neighbors": len(neigh[a] & neigh[b]),
                "freq_product": fa * len(bfreq[b]),
            })
    print(f"eligible suppressed pairs: {len(eligible)}")

    # outcome: chance-calibrated formation in eval window
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
        if len(docs) >= 2 and len({author_of[d] for d in docs}) >= 2 and \
           (len(docs) - E) / max(np.sqrt(E), 1e-9) >= 2.0:
            formed.add(pair)
    hits = sum(1 for p in eligible if p["pair"] in formed)
    print(f"formed among eligible: {hits}/{len(eligible)} "
          f"({hits / max(len(eligible), 1):.4%})")

    # lenses: all / exposed-pairs / exposed x focused (run 4 registration)
    lenses = {"all": eligible}
    exp_file = os.environ.get("EXPOSED_FILE")
    if exp_file:
        exposed = {l.strip() for l in open(exp_file) if l.strip()}
        lenses["exposed"] = [p for p in eligible
                             if p["pair"][0] in exposed and p["pair"][1] in exposed]
        import math
        prom = {c: len(neigh[c]) / math.sqrt(len(bfreq[c])) for c in fs}
        cut = sorted(prom.values())[int(len(prom) * 2 / 3)]
        lenses["exposed_focused"] = [p for p in lenses["exposed"]
                                     if prom[p["pair"][0]] < cut and prom[p["pair"][1]] < cut]

    rng = np.random.default_rng(RNG_SEED)
    all_results = {}
    for lens, elig in lenses.items():
        if not elig:
            print(f"\n== lens {lens}: EMPTY ==")
            all_results[lens] = {}
            continue
        ks = [k for k in K_VALUES if k <= len(elig)] or [len(elig)]
        lhits = sum(1 for p in elig if p["pair"] in formed)
        print(f"\n== lens {lens}: {len(elig)} eligible, {lhits} formed "
              f"({lhits / max(len(elig), 1):.4%}) ==")
        rankers = {
            "suppr_affinity": sorted(elig, key=lambda p: -p["suppression_affinity"]),
            "affinity_only": sorted(elig, key=lambda p: -p["affinity"]),
            "common_neighbors": sorted(elig, key=lambda p: -p["common_neighbors"]),
            "freq_product": sorted(elig, key=lambda p: -p["freq_product"]),
            "random": list(rng.permutation(np.array(elig, dtype=object))),
        }
        print(f"{'ranker':<18}" + "".join(f"P@{k:<8}" for k in ks))
        all_results[lens] = {}
        for name, ranked in rankers.items():
            all_results[lens][name] = {k: sum(1 for p in ranked[:k] if p["pair"] in formed) / k
                                       for k in ks}
            print(f"{name:<18}" + "".join(f"{all_results[lens][name][k]:<10.4f}" for k in ks))
    json.dump({"n_eligible": len(eligible), "hits": hits, "results": all_results},
              open(os.path.join(OUT, "eval3_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
