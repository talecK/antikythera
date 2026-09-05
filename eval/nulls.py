#!/usr/bin/env python3
"""Permutation nulls for the co-mention statistic, in one place.

Every sampler takes the evaluation window's incidence lists (one entry per
(document, label) slot, documents and labels sorted by the caller per the
registration determinism clause) and an explicitly passed numpy Generator,
and returns a document -> set-of-labels map on which the caller's pair
counter runs unchanged.

Samplers
  label_shuffle            the registered null (run 8, gate, paper 2):
                           one permutation of the label column. Moved
                           here verbatim; byte-identical output for a
                           given generator state.
  label_shuffle_stratified permutes labels only within strata (e.g. the
                           calendar quarter of the document), so a label
                           can never move across quarters.

Both samplers rebuild documents as sets, so two identical labels landing
in one document collapse to one. That is the property the 2026-09-04
critique flagged: the null is NOT fixed-fixed. margin_drift() measures the
collapse per replicate so it can be reported. A margin-preserving sampler
(curveball) is deferred to a later amendment and is not implemented here.

Summaries
  margin_drift   incidences before/after collapse, documents and labels
                 whose margin changed.
  null_summary   mean, sd, z, observed/null ratio, and Monte Carlo
                 p-values with the +1 correction (Phipson & Smyth 2010).
"""
from collections import Counter, defaultdict

import numpy as np


def label_shuffle(inc_doc, inc_tok, rng):
    """Registered null: permute the label column once, rebuild documents."""
    perm = rng.permutation(inc_tok)
    sh = defaultdict(set)
    for d, t in zip(inc_doc, perm):
        sh[d].add(t)
    return sh


def label_shuffle_stratified(inc_doc, inc_tok, rng, strata):
    """Permute labels within each stratum only.

    strata: one hashable, sortable key per incidence (same length as
    inc_doc). Strata are visited in sorted order so the generator is
    consumed deterministically for a given input.
    """
    inc_tok = np.asarray(inc_tok, dtype=object)
    groups = defaultdict(list)
    for i, g in enumerate(strata):
        groups[g].append(i)
    perm = np.empty(len(inc_tok), dtype=object)
    for g in sorted(groups):
        ix = np.array(groups[g], dtype=np.int64)
        perm[ix] = rng.permutation(inc_tok[ix])
    sh = defaultdict(set)
    for d, t in zip(inc_doc, perm):
        sh[d].add(t)
    return sh


def margin_drift(inc_doc, inc_tok, docmap, size_before=None, freq_before=None):
    """How far one shuffled replicate's margins sit from the observed ones.

    Returns a dict with:
      inc_before    number of (document, label) slots fed to the sampler
      inc_after     number of distinct (document, label) pairs after the
                    set rebuild; inc_before - inc_after slots collapsed
      docs_changed  documents whose distinct-label count changed
      toks_changed  labels whose document count changed
    size_before / freq_before: Counter(inc_doc) / Counter(inc_tok), passed
    in by callers that evaluate many replicates of one cell.
    """
    if size_before is None:
        size_before = Counter(inc_doc)
    if freq_before is None:
        freq_before = Counter(inc_tok.tolist() if hasattr(inc_tok, "tolist") else inc_tok)
    freq_after = Counter()
    inc_after = 0
    docs_changed = 0
    for d, s in docmap.items():
        inc_after += len(s)
        if len(s) != size_before.get(d, 0):
            docs_changed += 1
        for t in s:
            freq_after[t] += 1
    docs_changed += sum(1 for d in size_before if d not in docmap)
    toks_changed = sum(1 for t in set(freq_before) | set(freq_after)
                       if freq_before.get(t, 0) != freq_after.get(t, 0))
    return {"inc_before": len(inc_doc), "inc_after": inc_after,
            "docs_changed": docs_changed, "toks_changed": toks_changed}


def null_summary(obs_total, totals):
    """Standardized and Monte Carlo summaries of one cell's null totals.

    totals: array of the statistic under R null replicates.
    mc_p_lo  = (#{null <= obs} + 1) / (R + 1)
    mc_p_hi  = (#{null >= obs} + 1) / (R + 1)
    mc_p_2s  = min(1, 2 * min(mc_p_lo, mc_p_hi))
    ratio    = obs / null mean (nan when the null mean is 0)
    """
    totals = np.asarray(totals, dtype=np.float64)
    R = len(totals)
    mean, sd = float(totals.mean()), float(totals.std())
    z = (obs_total - mean) / max(sd, 1e-9)
    lo = (int((totals <= obs_total).sum()) + 1) / (R + 1)
    hi = (int((totals >= obs_total).sum()) + 1) / (R + 1)
    return {"null_mean": mean, "null_sd": sd, "z_seg": float(z),
            "ratio": float(obs_total / mean) if mean > 0 else float("nan"),
            "null_min": float(totals.min()), "null_max": float(totals.max()),
            "mc_p_lo": lo, "mc_p_hi": hi, "mc_p_2s": min(1.0, 2 * min(lo, hi)),
            "R": R}


DRIFT_KEYS = ("inc_before", "inc_after", "docs_changed", "toks_changed")


def drift_mean(drifts):
    """Average a list of margin_drift dicts; adds collapsed_frac."""
    if not drifts:
        return {k: float("nan") for k in DRIFT_KEYS} | {"collapsed_frac": float("nan")}
    out = {k: float(np.mean([d[k] for d in drifts])) for k in DRIFT_KEYS}
    out["collapsed_frac"] = ((out["inc_before"] - out["inc_after"]) / out["inc_before"]
                             if out["inc_before"] else float("nan"))
    return out
