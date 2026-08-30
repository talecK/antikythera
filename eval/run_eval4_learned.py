#!/usr/bin/env python3
"""Check 1: learned link predictor over suppressed pairs (exploratory,
labeled — a positive here triggers a fresh registered confirmation fold).

Features per eligible pair (build window only): common neighbors, Jaccard of
neighborhoods, Adamic-Adar, preferential attachment (log), embedding cosine,
E_build, min/max degree, growth ratios. Model: gradient-boosted trees via
sklearn. Train/test split BY PAIR, stratified, 5-fold CV; report mean P@k on
held-out pairs (each pair scored only by a model that never saw it).
"""
import json
import os
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("REGISTRY_OUT", os.path.join(ROOT, "data", "registry", "pilot1_concepts"))
EVAL_START, EVAL_END = "2017-01-01", "2018-01-01"
F, E_MIN = 20, 2.0


def main() -> None:
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
    mid = datetime.fromisoformat("2016-01-01")
    early, late = defaultdict(int), defaultdict(int)
    for d, c, ts, by in rows:
        author_of[d] = by
        if ts < es:
            bfreq[c].add(d)
            bdoc[d].add(c)
            (late if ts >= mid else early)[c] += 1
        elif ts < ee:
            edoc[d].add(c)
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
    deg = {c: len(neigh[c]) for c in fs}

    vecs = np.load(os.path.join(OUT, "embeddings.npy"))
    texts = json.load(open(os.path.join(OUT, "claim_texts.json")))
    vec_of = {t: k for k, t in enumerate(texts)}

    fl = sorted(fs, key=lambda c: -len(bfreq[c]))
    pairs, X = [], []
    for i, a in enumerate(fl):
        fa = len(bfreq[a])
        va = vecs[vec_of[a]]
        for b in fl[i + 1:]:
            fb = len(bfreq[b])
            E = fa * fb / Nb
            if E < E_MIN:
                break
            if co.get((min(a, b), max(a, b)), 0):
                continue
            cn = neigh[a] & neigh[b]
            un = neigh[a] | neigh[b]
            aa = sum(1.0 / np.log(max(deg[c], 2)) for c in cn)
            g_a = late[a] / max(early[a], 1)
            g_b = late[b] / max(early[b], 1)
            pairs.append((min(a, b), max(a, b)))
            X.append([len(cn), len(cn) / max(len(un), 1), aa,
                      np.log(deg[a] * deg[b] + 1), float(va @ vecs[vec_of[b]]),
                      E, min(fa, fb), max(fa, fb), g_a * g_b,
                      abs(np.log(fa / fb))])
    X = np.array(X)
    print(f"eligible: {len(pairs)}")

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
    y = np.array([1 if p in formed else 0 for p in pairs])
    print(f"positives: {y.sum()}/{len(y)} ({y.mean():.4%})")

    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import StratifiedKFold
    scores = np.zeros(len(y))
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=7).split(X, y):
        m = HistGradientBoostingClassifier(max_iter=300, random_state=7)
        m.fit(X[tr], y[tr])
        scores[te] = m.predict_proba(X[te])[:, 1]
    order = np.argsort(-scores)
    for k in (50, 200, 1000):
        print(f"learned P@{k}: {y[order[:k]].mean():.4f}")
    base = y.mean()
    print(f"base rate: {base:.4f} | lift@200: {y[order[:200]].mean() / base:.1f}x")
    feat_names = ["common_n", "jaccard", "adamic_adar", "log_pref_attach",
                  "cosine", "E_build", "min_freq", "max_freq", "growth", "freq_asym"]
    m = HistGradientBoostingClassifier(max_iter=300, random_state=7).fit(X, y)
    from sklearn.inspection import permutation_importance
    imp = permutation_importance(m, X, y, n_repeats=3, random_state=7)
    for n, v in sorted(zip(feat_names, imp.importances_mean), key=lambda t: -t[1])[:5]:
        print(f"  feature {n}: {v:.4f}")


if __name__ == "__main__":
    main()
