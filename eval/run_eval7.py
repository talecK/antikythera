#!/usr/bin/env python3
"""Registered run 7: scout class — bridge persistence + scout-weighted
ranking. See preregistration_run7.md (committed pre-eval, ff94e9f).

Stage A: split-half persistence of first-bridge precision (build era only).
Stage B: scout ranker over fold-1 eligible suppressed pairs vs controls.
Stage C: alert test — first eval bridger's precision vs formation.
"""
import math
import os
from collections import defaultdict
from datetime import datetime

import duckdb
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AC = os.path.join(ROOT, "data", "registry", "run5_author", "author_concepts.parquet")
F, E_MIN, HUB = 20, 2.0, 100
SEED = 20260830
MIN_EVENTS = 5


def spearman(x, y):
    def ranks(v):
        order = np.argsort(v, kind="stable")
        r = np.empty(len(v)); r[order] = np.arange(1, len(v) + 1)
        srt = np.array(v)[order]
        uniq, inv, cnt = np.unique(srt, return_inverse=True, return_counts=True)
        start = np.zeros(len(uniq)); start[1:] = np.cumsum(cnt)[:-1]
        r[order] = (start + (cnt + 1) / 2.0)[inv]
        return r
    rx, ry = ranks(np.array(x)), ranks(np.array(y))
    rx -= rx.mean(); ry -= ry.mean()
    d = math.sqrt((rx @ rx) * (ry @ ry))
    return float(rx @ ry / d) if d else 0.0


def fisher_one_sided(a, b, c, d):
    """P(X >= a) for table [[a,b],[c,d]] under hypergeometric."""
    n, K, N = a + b, a + c, a + b + c + d
    p = 0.0
    for k in range(a, min(n, K) + 1):
        p += (math.comb(K, k) * math.comb(N - K, n - k)) / math.comb(N, n)
    return p


def main() -> None:
    reg = open(os.path.join(ROOT, "preregistration_run7.md")).read()
    assert "Run 7 registration" in reg
    con = duckdb.connect()
    rows = con.sql(f"""SELECT author, year(time), (month(time)-1)//3, concept
                       FROM read_parquet('{AC}')
                       WHERE time < TIMESTAMP '2018-01-01'""").fetchall()
    docs = defaultdict(set)  # (author, qi) -> concepts; qi 0..11 from 2015Q1
    for author, y, q, concept in rows:
        docs[(author, (y - 2015) * 4 + q)].add(concept)
    docs = {k: v for k, v in docs.items() if len(v) <= HUB}
    bdocs = {k: v for k, v in docs.items() if k[1] <= 7}
    edocs = {k: v for k, v in docs.items() if k[1] >= 8}

    bfreq = defaultdict(set)
    for d, s in bdocs.items():
        for c in s:
            bfreq[c].add(d)
    fs = {c for c, v in bfreq.items() if len(v) >= F}
    Nb = len(bdocs)
    print(f"build docs {Nb} | eval docs {len(edocs)} | frequent {len(fs)}")

    # ---- one ordered pass over build quarters: first-bridge accounting ----
    first_q, first_auth = {}, {}
    later_others = defaultdict(set)  # track-era pairs only, capped at 3
    by_quarter = defaultdict(list)
    for (author, qi), s in bdocs.items():
        by_quarter[qi].append((author, sorted(s & fs)))
    for qi in range(8):
        for author, ss in by_quarter[qi]:
            for x in range(len(ss)):
                for y2 in range(x + 1, len(ss)):
                    p = (ss[x], ss[y2])
                    fq = first_q.get(p)
                    if fq is None:
                        first_q[p] = qi
                        first_auth[p] = {author}
                    elif fq == qi:
                        first_auth[p].add(author)
                    elif 2 <= fq <= 5:
                        lo = later_others[p]
                        if len(lo) < 3 and author not in first_auth[p]:
                            lo.add(author)
    print(f"build co-occurring pairs {len(first_q)}")

    # ---- events + per-author precision ----
    ev_half = {1: defaultdict(list), 2: defaultdict(list)}
    ev_all = defaultdict(list)
    for p, fq in first_q.items():
        if not (2 <= fq <= 5):
            continue
        outcome = int(len(later_others[p]) >= 2)
        half = 1 if fq <= 3 else 2
        for a in first_auth[p]:
            ev_half[half][a].append(outcome)
            ev_all[a].append(outcome)
    n_ev = sum(len(v) for v in ev_all.values())
    print(f"track-era bridge events {n_ev} | bridging authors {len(ev_all)} | "
          f"global catch-on rate "
          f"{sum(sum(v) for v in ev_all.values())/max(n_ev,1):.1%}")

    # ---- Stage A: persistence ----
    qual = [a for a in ev_half[1]
            if len(ev_half[1][a]) >= MIN_EVENTS and len(ev_half[2].get(a, [])) >= MIN_EVENTS]
    p1 = [sum(ev_half[1][a]) / len(ev_half[1][a]) for a in qual]
    p2 = [sum(ev_half[2][a]) / len(ev_half[2][a]) for a in qual]
    rho = spearman(p1, p2)
    rng = np.random.default_rng(SEED)
    flat = {h: [(a, o) for a in ev_half[h] for o in ev_half[h][a]] for h in (1, 2)}
    null = []
    for _ in range(1000):
        rs = {}
        for h in (1, 2):
            outs = np.array([o for _, o in flat[h]])
            rng.shuffle(outs)
            per = defaultdict(list)
            for (a, _), o in zip(flat[h], outs):
                per[a].append(o)
            rs[h] = per
        np1 = [sum(rs[1][a]) / len(rs[1][a]) for a in qual]
        np2 = [sum(rs[2][a]) / len(rs[2][a]) for a in qual]
        null.append(spearman(np1, np2))
    thr = float(np.percentile(null, 95))
    print(f"\nSTAGE A: qualified authors {len(qual)} | Spearman rho {rho:.4f} "
          f"| null95 {thr:.4f} | {'PASS' if rho > thr else 'FAIL'}")

    # ---- fold-1 eligible suppressed pairs + formation (run-5 logic) ----
    co = set(first_q)
    neigh = defaultdict(set)
    for p in first_q:
        neigh[p[0]].add(p[1]); neigh[p[1]].add(p[0])
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
    epair = defaultdict(set)
    efreq = defaultdict(int)
    for d, s in edocs.items():
        ss = sorted(s & fs)
        for c in ss:
            efreq[c] += 1
        for x in range(len(ss)):
            for y2 in range(x + 1, len(ss)):
                epair[(ss[x], ss[y2])].add(d)
    Ne = len(edocs)
    formed = set()
    for pair, dd in epair.items():
        a, b = pair
        E = efreq[a] * efreq[b] / Ne
        if len(dd) >= 2 and len({x[0] for x in dd}) >= 2 and \
           (len(dd) - E) / max(np.sqrt(E), 1e-9) >= 2.0:
            formed.add(pair)
    print(f"\neligible {len(eligible)} | formed {sum(1 for p in eligible if p in formed)}")

    # ---- Stage B: scout ranker vs controls ----
    prec = {a: sum(v) / len(v) for a, v in ev_all.items() if len(v) >= MIN_EVENTS}
    nev = {a: len(v) for a, v in ev_all.items() if len(v) >= MIN_EVENTS}
    hist = defaultdict(set)  # author -> frequent concepts in build (eligible vocab)
    elig_vocab = {c for p in eligible for c in p}
    for (author, qi), s in bdocs.items():
        for c in s & elig_vocab:
            hist[author].add(c)
    inv = defaultdict(set)  # concept -> qualified authors
    for a, cs in hist.items():
        if a in prec:
            for c in cs:
                inv[c].add(a)
    scout_sc, act_sc, nbridge = {}, {}, {}
    for p in eligible:
        bridgers = inv[p[0]] & inv[p[1]]
        nbridge[p] = len(bridgers)
        scout_sc[p] = max((prec[a] for a in bridgers), default=-1.0)
        act_sc[p] = max((nev[a] for a in bridgers), default=-1.0)
    nz = sum(1 for p in eligible if nbridge[p] > 0)
    print(f"STAGE B: pairs with >=1 qualified slow-bridger: {nz}/{len(eligible)}")
    rng2 = np.random.default_rng(SEED)
    rankers = {
        "scout(max prec)": sorted(eligible, key=lambda p: -scout_sc[p]),
        "activity(max n)": sorted(eligible, key=lambda p: -act_sc[p]),
        "common_neighbors": sorted(eligible, key=lambda p: -len(neigh[p[0]] & neigh[p[1]])),
        "random": [eligible[i] for i in rng2.permutation(len(eligible))],
    }
    ks = [50, 100, 200]
    print(f"{'ranker':<18}" + "".join(f"P@{k:<7}" for k in ks))
    for name, ranked in rankers.items():
        vals = "".join(f"{sum(1 for p in ranked[:k] if p in formed)/k:<9.3f}" for k in ks)
        print(f"{name:<18}{vals}")

    # ---- Stage C: alert test ----
    efirst_q, efirst_auth = {}, {}
    eby_q = defaultdict(list)
    for (author, qi), s in edocs.items():
        eby_q[qi].append((author, sorted(s & fs)))
    elig_set = set(eligible)
    for qi in range(8, 12):
        for author, ss in eby_q[qi]:
            for x in range(len(ss)):
                for y2 in range(x + 1, len(ss)):
                    p = (ss[x], ss[y2])
                    if p not in elig_set:
                        continue
                    fq = efirst_q.get(p)
                    if fq is None:
                        efirst_q[p] = qi; efirst_auth[p] = {author}
                    elif fq == qi:
                        efirst_auth[p].add(author)
    scored = [(p, max(prec[a] for a in efirst_auth[p] if a in prec))
              for p in efirst_q if any(a in prec for a in efirst_auth[p])]
    scored.sort(key=lambda t: t[1])
    n3 = len(scored) // 3
    bot, top = scored[:n3], scored[-n3:]
    bt = sum(1 for p, _ in bot if p in formed)
    tp = sum(1 for p, _ in top if p in formed)
    pv = fisher_one_sided(tp, len(top) - tp, bt, len(bot) - bt)
    print(f"\nSTAGE C: eligible pairs first-bridged in 2017 w/ qualified "
          f"bridger: {len(scored)} (of {len(efirst_q)} bridged)")
    print(f"  top tercile formed {tp}/{len(top)} ({tp/max(len(top),1):.1%}) | "
          f"bottom {bt}/{len(bot)} ({bt/max(len(bot),1):.1%}) | "
          f"Fisher one-sided p={pv:.4f} | "
          f"{'PASS' if tp/max(len(top),1) > bt/max(len(bot),1) and pv < 0.05 else 'FAIL'}")


if __name__ == "__main__":
    main()
