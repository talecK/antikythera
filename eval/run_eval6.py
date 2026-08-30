#!/usr/bin/env python3
"""Registered run 6: exposure lens x author space + articulated outcome.
See preregistration_run6.md (committed pre-eval). Universe identical to
run 5; new readouts: EXPOSEDxEXPOSED lens, claim-level articulated formation.
"""
import csv
import math
import os
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AC = os.path.join(ROOT, "data", "registry", "run5_author", "author_concepts.parquet")
LABELS = os.path.join(ROOT, "data", "atlas", "concept_exposure_labels.csv")
F, E_MIN, HUB = 20, 2.0, 100
FOLDS = [("2015-01-01", "2017-01-01", "2018-01-01"),
         ("2015-01-01", "2016-01-01", "2017-01-01")]


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main() -> None:
    reg = open(os.path.join(ROOT, "preregistration_run6.md")).read()
    assert "Run 6 registration" in reg
    exposed = {r["concept"] for r in csv.DictReader(open(LABELS))
               if r["economically_exposed"] == "1"}
    con = duckdb.connect()
    rows = con.sql(f"""SELECT author, year(time), (month(time)-1)//3, concept,
        time, doc_id, claim_id FROM read_parquet('{AC}')""").fetchall()

    pooled = {"exposed_elig": 0, "exposed_formed": 0}
    detail = []
    for bstart, bend, eend in FOLDS:
        bs = datetime.fromisoformat(bstart)
        be = datetime.fromisoformat(bend)
        ee = datetime.fromisoformat(eend)
        bdoc, edoc = defaultdict(set), defaultdict(set)
        eclaims = defaultdict(lambda: [set(), None])  # (doc,claim)->concepts,author
        for author, y, q, concept, ts, did, cid in rows:
            k = (author, y, q)
            if bs <= ts < be:
                bdoc[k].add(concept)
            elif be <= ts < ee:
                edoc[k].add(concept)
                ec = eclaims[(did, cid)]
                ec[0].add(concept); ec[1] = author
        bdoc = {k: v for k, v in bdoc.items() if len(v) <= HUB}
        edoc = {k: v for k, v in edoc.items() if len(v) <= HUB}

        bfreq = defaultdict(set)
        for d, s in bdoc.items():
            for c in s:
                bfreq[c].add(d)
        fs = {c for c, v in bfreq.items() if len(v) >= F}
        Nb = len(bdoc)
        co = set()
        for d, s in bdoc.items():
            ss = sorted(s & fs)
            for x in range(len(ss)):
                for y2 in range(x + 1, len(ss)):
                    co.add((ss[x], ss[y2]))
        fl = sorted(fs, key=lambda c: -len(bfreq[c]))
        eligible = []
        for i, a in enumerate(fl):
            fa = len(bfreq[a])
            for b in fl[i + 1:]:
                if fa * len(bfreq[b]) / Nb < E_MIN:
                    break
                key = (min(a, b), max(a, b))
                if key not in co:
                    eligible.append(key)
        elig_set = set(eligible)

        # author-space formation (run-5 outcome)
        epair = defaultdict(set)
        efreq = defaultdict(int)
        for d, s in edoc.items():
            ss = sorted(s & fs)
            for c in ss:
                efreq[c] += 1
            for x in range(len(ss)):
                for y2 in range(x + 1, len(ss)):
                    epair[(ss[x], ss[y2])].add(d)
        Ne = len(edoc)
        formed = set()
        for pair, docs in epair.items():
            a, b = pair
            E = efreq[a] * efreq[b] / Ne
            if len(docs) >= 2 and len({d[0] for d in docs}) >= 2 and \
               (len(docs) - E) / max(np.sqrt(E), 1e-9) >= 2.0:
                formed.add(pair)

        # articulated: same-claim co-occurrence in eval window
        art = defaultdict(lambda: [0, set()])  # pair -> [n_claims, authors]
        for (did, cid), (cset, author) in eclaims.items():
            ss = sorted(cset & fs)
            for x in range(len(ss)):
                for y2 in range(x + 1, len(ss)):
                    key = (ss[x], ss[y2])
                    if key in elig_set:
                        art[key][0] += 1
                        art[key][1].add(author)

        exp_pairs = [p for p in eligible if p[0] in exposed and p[1] in exposed]
        nf_all = sum(1 for p in eligible if p in formed)
        nf_exp = sum(1 for p in exp_pairs if p in formed)
        art_strict_all = sum(1 for p in eligible
                             if art[p][0] >= 2 and len(art[p][1]) >= 2)
        art_weak_all = sum(1 for p in eligible if art[p][0] >= 1)
        art_strict_exp = sum(1 for p in exp_pairs
                             if art[p][0] >= 2 and len(art[p][1]) >= 2)
        art_weak_exp = sum(1 for p in exp_pairs if art[p][0] >= 1)
        pooled["exposed_elig"] += len(exp_pairs)
        pooled["exposed_formed"] += nf_exp

        print(f"\n===== fold build->{bend[:4]} eval {bend[:4]}-{eend[:4]}")
        print(f"eligible {len(eligible)} | author-formed {nf_all} "
              f"({nf_all/max(len(eligible),1):.1%})")
        print(f"articulated all pairs: strict {art_strict_all}, "
              f"weak(>=1 claim) {art_weak_all}")
        print(f"EXPOSEDxEXPOSED: eligible {len(exp_pairs)} | author-formed "
              f"{nf_exp} | articulated strict {art_strict_exp} / weak {art_weak_exp}")
        for p in sorted(exp_pairs, key=lambda p: -(p in formed)):
            detail.append((bend[:4], p, p in formed, art[p][0],
                           len(art[p][1])))

    k, n = pooled["exposed_formed"], pooled["exposed_elig"]
    lo, hi = wilson(k, n)
    print(f"\n===== POOLED PRIMARY: exposed formation {k}/{n} "
          f"({k/max(n,1):.1%}; Wilson95 {lo:.1%}-{hi:.1%})")
    print("Registered read: >=3/26 survives; <=1/26 inert; 2/26 indeterminate.")
    print("\nAll exposed eligible pairs (fold, pair, author-formed, "
          "n articulated claims, n articulating authors):")
    for fold, p, fmd, nclaims, nauth in detail:
        print(f"  [{fold}] {'FORMED  ' if fmd else 'unformed'} "
              f"artic={nclaims}/{nauth}  '{p[0]}' <-> '{p[1]}'")


if __name__ == "__main__":
    main()
