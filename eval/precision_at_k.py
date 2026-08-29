#!/usr/bin/env python3
"""Eval harness: precision-at-k on 12-month edge formation, vs 3 baselines.

An EDGE FORMS in the eval window when >= MIN_ADOPTERS distinct authors
co-mention the idea pair in docs dated inside the window (independent-author
adoption; immune to single viral threads).

Candidate rankers (the pre-registered comparison set):
  1. gap_score  — high freq x high affinity x deep-negative-z (the thesis)
  2. random     — random eligible pairs (baseline A)
  3. affinity   — pure embedding-affinity ranking, no co-occurrence null (baseline B)
  4. freq_growth— frequency-growth extrapolation on the pair's endpoints (baseline C)

All rankers see ONLY data with doc_time < eval_start (leakage guard asserts).
Parameters marked PREREG come from preregistration.md and must be committed
there before this script is first run on a real fold.
"""
import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class FoldSpec:
    build_start: str   # inclusive, ISO date  (PREREG)
    eval_start: str    # build/eval boundary  (PREREG)
    eval_end: str      # eval_start + 12mo    (PREREG)


K_VALUES: list[int] = []       # PREREG — e.g. [50, 200, 1000]
MIN_ADOPTERS: int = 0          # PREREG — distinct-author threshold for "edge formed"
ELIGIBLE_PAIR_SPEC: dict = {}  # PREREG — affinity threshold, per-idea frequency floor


def precision_at_k(ranked_pairs: list[tuple[int, int]],
                   formed: set[tuple[int, int]],
                   k: int) -> float:
    top = ranked_pairs[:k]
    return sum(1 for p in top if p in formed) / k if top else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fold", required=True, help="fold name from preregistration.md")
    ap.add_argument("--extractor", required=True)
    ap.add_argument("--registry-version", required=True)
    ap.parse_args()
    raise SystemExit(
        "Harness skeleton: rankers land after the registry exists (Pilot 1). "
        "PREREG constants must be filled from preregistration.md before first "
        "real run — this guard is part of the pre-registration discipline."
    )


if __name__ == "__main__":
    main()
