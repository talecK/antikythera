# Robustness registration — author-lens referee checks R1–R4 (2026-08-30)

Purpose: paper-1 (HN negative + author-lens revision) robustness suite.
Four checks on banked data, $0 API. R1 is the only one that can change a
conclusion; R2–R4 are sensitivity trim. All specs frozen here BEFORE any
outcome is computed; script `eval/run_robustness.py` asserts this file is
committed. Universe, folds, and constants are run 5's unless stated
(preregistration_run5.md: document = (author, quarter), hub guard 100,
F >= 20, E_build >= 2 & observed build co-occurrence 0; formation = >= 2
eval author-docs, >= 2 distinct authors, eval z >= 2; folds: build
2015–2016 / eval 2017, and build 2015 / eval 2016).

Prior exposure (disclosed): run-5 headline outcomes (70/364 = 19.2%,
26/110 = 23.6%) and run-6 articulated counts over the ELIGIBLE set
(strict 4+2, weak 13+11) are known. Nothing below has been computed:
no placebo replicate, no alternative-window eval, no formation x
articulation cross-tab or timing, no attribution-subset eval.

## R1 — placebo: eval-window label shuffle (the load-bearing check)

Question: is the 19–24% formation rate a person-level signal, or does the
author-quarter pooling produce it mechanically from marginal frequencies?

- Eligible set: run 5's, per fold, from the REAL build window (unchanged).
- Shuffle: collect eval-window incidence pairs (author-doc, concept),
  concepts restricted to the frequent set; permute the concept column
  across incidence slots; collapse within-doc duplicates. Preserves doc
  sizes (minus collapsed dupes) and concept totals; destroys within-doc
  concept association.
- Replicates: R = 100 per fold, numpy default_rng seed 20260830 (one rng,
  replicates drawn sequentially).
- Readout: formation count among eligible pairs per replicate (identical
  formation criterion, z recomputed per replicate from shuffled freqs);
  report null mean, null 99th percentile, null max, vs observed 70 / 26.
- Interpretation (frozen):
  - Observed count > null 99th percentile in BOTH folds: placebo PASSED —
    formation is not mechanical pooling; run-5 headline stands.
  - Null mean >= 50% of observed in EITHER fold: substantial mechanical
    component — run 5's meaning is REVISED accordingly in the paper and
    HANDOFF; we commit to reporting this as a revision, not a nuance.
  - Between: report both numbers; headline gains a disclosed mechanical
    floor equal to the null mean.

## R2 — document-window sensitivity

Question: is (author, quarter) load-bearing, or does the effect survive
resizing the document window?

- Windows: (author, month) and (author, half-year); quarter = registered
  primary, not recomputed. Folds and all constants unchanged (F >= 20 on
  distinct author-docs of the new size; hub guard 100 concepts; E >= 2).
- Readout per window per fold: eligible-pair count and formation rate.
- Interpretation (frozen): formation rate >= 5% (run-5 bar) in both folds
  for a window => that window corroborates. Any window/fold below 5% is
  reported as a window-sensitivity limitation verbatim; no relitigation.
  Eligible-set collapse (< 30 pairs in a fold) => that cell is reported
  as UNINFORMATIVE, not as a negative.

## R3 — formation x articulation cross-tab + timing (pre-articulation claim)

Question: run 6 showed articulation is rare over the eligible set; the
paper's claim is about FORMED pairs specifically, and about ordering.

- Universe: the run-5 formed pairs (70 fold 1, 26 fold 2), recomputed
  deterministically by the run-5 harness.
- Articulation event: both concepts in one extracted claim's concept list
  (same doc_id + claim_id), searched over the FULL claims cache
  2015-01-01..2017-12-31 (beyond eval windows; cache limit disclosed).
- Readouts (descriptive, no pass/fail):
  1. Of formed pairs, count with zero articulating claim ever (in-cache).
  2. For formed pairs with >= 1 articulating claim: first co-mention
     eval quarter vs first articulating claim's story quarter; report the
     lead-time distribution (quarters) and the count where co-mention
     strictly precedes articulation.
  3. Same cross-tab restricted to eval-window articulation only
     (comparability with run 6's numbers).
- Framing commitment: if articulation typically PRECEDES co-mention, the
  "detector fires before anyone writes the connecting claim" sentence is
  withdrawn from the paper; rates alone do not support it.

## R4 — attribution robustness (conservative comment lens)

Question: does the headline depend on title/self-text attributions (12% of
attributed claims) or on submitter self-attribution?

- Variant universe: drop every attribution row whose author equals the
  story author of its doc_id (over-inclusive by construction: removes all
  title/self-text attributions AND submitters' own comment attributions —
  a conservative bound, disclosed as such). Rebuild author-docs, frequent
  set, eligible set, and outcomes from scratch under run-5 constants.
- Readout per fold: eligible count, formation rate.
- Interpretation (frozen): >= 5% in both folds => headline robust to
  attribution-path bias. Below in either fold: reported as a limitation;
  the 19% unattributed-claims caveat additionally remains as disclosed in
  run 5 (unattributed claims cannot be restored by any subset analysis).

## Execution notes (frozen)

- Script: eval/run_robustness.py, modes --r1 --r2 --r3 --r4; long output
  logged to data/registry/run5_author/robustness_*.log (no pipes).
- Order of execution: R1, R3, R2, R4. Results appended to
  reports/pilot1_runs.md under "Robustness suite"; interpretation strictly
  per the bars above.
