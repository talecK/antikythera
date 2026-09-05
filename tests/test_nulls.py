#!/usr/bin/env python3
"""Tests for eval/nulls.py. Run with `.venv/bin/python tests/test_nulls.py`
(plain asserts; also collectable by pytest if it is ever installed)."""
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "eval"))
from nulls import (label_shuffle, label_shuffle_stratified, margin_drift,  # noqa: E402
                   null_summary, drift_mean)


def _toy(seed=7, ndocs=40, ntok=12, per_doc=(1, 6)):
    """Deterministic toy incidence lists in registration order."""
    rng = np.random.default_rng(seed)
    docs = {}
    for i in range(ndocs):
        q = (2021, i % 2)                       # two strata, like a 2-quarter window
        k = int(rng.integers(per_doc[0], per_doc[1] + 1))
        toks = set(f"T{int(x)}" for x in rng.integers(0, ntok, k))
        docs[(f"a{i}", *q)] = toks
    inc_doc, inc_tok = [], []
    for d in sorted(docs):
        for t in sorted(docs[d]):
            inc_doc.append(d)
            inc_tok.append(t)
    return docs, inc_doc, np.array(inc_tok, dtype=object)


def test_label_shuffle_matches_registered_inline():
    """The moved sampler must consume the generator exactly as the inline
    code in run_paper2.window_stat / run_eval8.run_space did."""
    _, inc_doc, inc_tok = _toy()
    a = label_shuffle(inc_doc, inc_tok, np.random.default_rng(20260831))
    rng = np.random.default_rng(20260831)
    perm = rng.permutation(inc_tok)                # verbatim registered code
    b = defaultdict(set)
    for d, t in zip(inc_doc, perm):
        b[d].add(t)
    assert dict(a) == dict(b)


def test_label_shuffle_is_not_fixed_fixed():
    """Documents rebuilt as sets collapse duplicates: the critique's point."""
    inc_doc = [("d1", 0, 0), ("d1", 0, 0), ("d2", 0, 0), ("d2", 0, 0)]
    inc_tok = np.array(["A", "B", "A", "C"], dtype=object)
    # force the {A,A},{B,C} outcome by hand and measure it
    sh = {("d1", 0, 0): {"A"}, ("d2", 0, 0): {"B", "C"}}
    d = margin_drift(inc_doc, inc_tok, sh)
    assert d == {"inc_before": 4, "inc_after": 3, "docs_changed": 1,
                 "toks_changed": 1}, d


def test_margin_drift_zero_on_identity():
    docs, inc_doc, inc_tok = _toy()
    d = margin_drift(inc_doc, inc_tok, docs)
    assert d["inc_before"] == d["inc_after"] == len(inc_doc)
    assert d["docs_changed"] == 0 and d["toks_changed"] == 0
    m = drift_mean([d, d])
    assert m["collapsed_frac"] == 0.0


def test_stratified_preserves_per_stratum_label_multiset():
    docs, inc_doc, inc_tok = _toy()
    strata = [(d[1], d[2]) for d in inc_doc]
    sh = label_shuffle_stratified(inc_doc, inc_tok, np.random.default_rng(1), strata)
    # every document is still present and non-empty
    assert set(sh) == set(docs)
    # before collapse, each stratum's label multiset is preserved: check by
    # re-running the permutation step and comparing multisets per stratum
    rng = np.random.default_rng(1)
    groups = defaultdict(list)
    for i, g in enumerate(strata):
        groups[g].append(i)
    for g in sorted(groups):
        ix = np.array(groups[g])
        before = Counter(inc_tok[ix].tolist())
        after = Counter(rng.permutation(inc_tok[ix]).tolist())
        assert before == after, g
    # and no label crossed strata: labels present in stratum g after the
    # shuffle are a subset of labels present in g before it
    for g in sorted(groups):
        ix = set(groups[g])
        before = {inc_tok[i] for i in ix}
        after = set()
        for i in ix:
            after |= sh[inc_doc[i]]
        assert after <= before, g


def test_stratified_with_one_stratum_equals_unstratified():
    _, inc_doc, inc_tok = _toy()
    one = [0] * len(inc_doc)
    a = label_shuffle_stratified(inc_doc, inc_tok, np.random.default_rng(5), one)
    b = label_shuffle(inc_doc, inc_tok, np.random.default_rng(5))
    assert dict(a) == dict(b)


def test_stratified_is_deterministic():
    _, inc_doc, inc_tok = _toy()
    strata = [(d[1], d[2]) for d in inc_doc]
    a = label_shuffle_stratified(inc_doc, inc_tok, np.random.default_rng(9), strata)
    b = label_shuffle_stratified(inc_doc, inc_tok, np.random.default_rng(9), strata)
    assert dict(a) == dict(b)


def test_null_summary_pvalues():
    totals = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])  # R = 10
    s = null_summary(9, totals)                 # below every replicate
    assert s["mc_p_lo"] == 1 / 11 and s["mc_p_hi"] == 1.0
    assert s["mc_p_2s"] == 2 / 11
    s = null_summary(14, totals)                # 5 at or below, 6 at or above
    assert s["mc_p_lo"] == 6 / 11 and s["mc_p_hi"] == 7 / 11
    assert s["mc_p_2s"] == 1.0
    assert abs(s["ratio"] - 14 / 14.5) < 1e-12
    assert s["R"] == 10 and s["null_min"] == 10 and s["null_max"] == 19
    z = (14 - totals.mean()) / totals.std()
    assert abs(s["z_seg"] - z) < 1e-12


def test_registered_cell_scope():
    from run_paper2 import selected_cells, HEADLINE
    primary = selected_cells("stratified")
    assert len(primary) == 38
    assert set(primary) == {(4, k, s, "union")
                            for s in ("WSB", "DD") for k in range(19)}
    assert len(selected_cells("label")) == 204
    assert selected_cells("stratified", headline=True) == HEADLINE
    assert selected_cells("label", explicit="4:0:WSB:union") == [(4, 0, "WSB", "union")]


def test_pool_counts_before_estimating_z_and_formation():
    from run_eval8_nulls import summarize_counts
    eligible = [("A", "B"), ("A", "C")]
    observed = np.array([8, 3])
    first = np.array([[0, 0], [2, 0]], dtype=np.int32)
    second = np.array([[10, 1], [12, 1]], dtype=np.int32)
    pooled = np.concatenate([first, second])
    summary, formed = summarize_counts(observed, pooled, eligible, [True, True])
    totals = np.array([0, 2, 11, 13])
    assert summary["R"] == 4
    assert summary["z_seg"] == (11 - totals.mean()) / totals.std()
    assert summary["ratio"] == 11 / totals.mean()
    assert formed == [(["A", "C"], 3, 1.0)]
    batch_z = [summarize_counts(observed, b, eligible, [True, True])[0]["z_seg"]
               for b in (first, second)]
    assert not np.isclose(summary["z_seg"], np.mean(batch_z))
    _, unsupported = summarize_counts(observed, pooled, eligible, [True, False])
    assert unsupported == []


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok", fn.__name__)
    print(f"{len(fns)} passed")
