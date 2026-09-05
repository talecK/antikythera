"""Synthetic correctness checks only; no corpus or scientific outcomes."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
from curveball import Curveball


def state(rows):
    return tuple(tuple(sorted(row)) for row in rows)


def small_space():
    rows = [list(combinations(range(3), degree)) for degree in (1, 2, 1)]
    return [state(matrix) for matrix in product(*rows)
            if [sum(c in row for row in matrix) for c in range(3)] == [1, 2, 1]]


def exact_transitions(matrix):
    """Enumerate the mathematical kernel independently of native code."""
    transitions = Counter()
    pairs = list(combinations(range(len(matrix)), 2))
    for i,j in pairs:
        a,b = set(matrix[i]), set(matrix[j])
        common = a & b
        exclusive = sorted(a ^ b)
        allocations = list(combinations(exclusive, len(a-b)))
        weight = Fraction(1, len(pairs)*len(allocations))
        for allocation in allocations:
            result = list(matrix)
            result[i] = common | set(allocation)
            result[j] = common | (set(exclusive)-set(allocation))
            transitions[state(result)] += weight
    return transitions


def test_exact_small_kernel_uniform_stationary():
    matrices = small_space()
    assert len(matrices) == 5
    kernels = {m: exact_transitions(m) for m in matrices}
    for a in matrices:
        assert sum(kernels[a].values()) == 1
        assert kernels[a][a] > 0
        for b in matrices:
            assert kernels[a][b] == kernels[b][a]
    reached = {matrices[0]}
    for _ in matrices:
        reached |= {b for a in list(reached) for b in kernels[a]}
    assert reached == set(matrices)


def test_native_empirical_small_space():
    matrices = small_space()
    counts = Counter()
    with Curveball(matrices[0], 3, 9917) as chain:
        chain.step(100)
        for _ in range(30000):
            chain.step(1)
            counts[state(chain.rows())] += 1
        assert set(counts) == set(matrices)
        # A generous, deterministic smoke check, not a general mixing claim.
        assert all(abs(n/30000 - .2) < .025 for n in counts.values()), counts
        assert chain.diagnostics()["attempts"] == 30100


def test_margins_counts_and_replay():
    rng = np.random.default_rng(812)
    rows = [sorted(rng.choice(20, size=int(rng.integers(0, 12)), replace=False).tolist())
            for _ in range(50)]
    row_sums = [len(r) for r in rows]
    col_sums = np.bincount([x for r in rows for x in r], minlength=20)
    pairs = list(combinations(range(20), 2))
    with Curveball(rows, 20, 719) as a, Curveball(rows, 20, 719) as b:
        for _ in range(10):
            a.step(1000)
            matrix = a.rows()
            assert [len(r) for r in matrix] == row_sums
            assert np.array_equal(a.margins(), col_sums)
            expected = [sum(x in r and y in r for r in matrix) for x,y in pairs]
            assert np.array_equal(a.counts(pairs), expected)
            distance = sum(len(set(old)^set(new)) for old,new in zip(rows,matrix))
            assert a.diagnostics()["changed_binary_entries"] == distance
        b.step(10000)
        assert a.rows() == b.rows()
        assert a.diagnostics() == b.diagnostics()


def test_fixed_and_empty_states():
    for rows,columns in [([],0), ([[]],3), ([[0],[0,1]],2), ([[],[]],0)]:
        with Curveball(rows,columns,12) as chain:
            chain.step(100)
            assert chain.rows() == rows
            assert chain.diagnostics()["attempts"] == 100
            assert chain.diagnostics()["changed_binary_entries"] == 0


if __name__ == "__main__":
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_"):
            fn(); print("ok",name,flush=True)
    print("4 passed")
