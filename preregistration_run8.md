# Run 8 registration — shuffle-calibrated formation, author + thread space (2026-08-30)

Motivation: R1 (preregistration_robustness.md, results in
reports/pilot1_runs.md) showed the z>=2 formation criterion is
anti-conservative under doc-size heterogeneity — the label-shuffle null
"forms" 34-47% of eligible suppressed pairs vs 19-24% observed. Run 8
replaces the criterion with a per-pair empirical null and re-measures
formation in BOTH spaces, both folds. This is the ladder recalibration;
gate Q1 bars are re-derived from its OUTCOME-INDEPENDENT structure (the
criterion), not its rates.

## STATUS: frozen pre-eval. Committed before any run-8 outcome is computed.
Prior exposure (disclosed): R1's aggregate null distributions and the
observed z>=2 formed counts are known (70/364, 26/110 author-space; null
means 124.6/52.0). Per-pair calibrated outcomes, thread-space shuffle
nulls, and all sub-chance totals below have NOT been computed.

## Universes (both unchanged from their registered runs)
- AUTHOR space: run 5 exactly — author_concepts.parquet, document =
  (author, quarter), hub guard 100, F>=20, E_build>=2 & obs build co=0.
  Folds: build 2015-2016 / eval 2017; build 2015 / eval 2016.
- THREAD space: run 3 exactly — pilot1_concepts claims.parquet + doc
  authors, document = thread, F>=20, E>=2 & obs=0, same fold windows
  (build = all pre-eval data, as run 3).

## Calibrated formation criterion (frozen)
- Shuffle: eval-window label shuffle as R1 (incidence (doc, concept)
  restricted to the frequent set; permute concept column; collapse
  within-doc duplicates). R = 100 replicates per space per fold, one
  numpy default_rng seed 20260831 drawn sequentially
  (author-f1, author-f2, thread-f1, thread-f2).
- Per-pair null: the R co-mention doc counts for that pair; threshold =
  empirical p99 (numpy percentile, linear interpolation).
- Pair FORMS (calibrated) iff: observed eval co-mention doc count
  STRICTLY exceeds its p99 threshold AND >= 2 docs AND >= 2 distinct
  authors. Per-pair false-positive rate ~1% by construction.

## Registered readouts
1. PRIMARY — calibrated formed count per space per fold, vs the
   false-positive floor Binomial(n_eligible, 0.01), one-sided exact test.
   - Significant (p < 0.01) in BOTH author-space folds: above-chance
     formation is real; detector story revives on the calibrated rate,
     which becomes the HN-author ladder rung.
   - Not significant in EITHER author-space fold: no evidence individuals
     bridge suppressed pairs above chance; the author-lens revival is
     closed for good; paper 1 proceeds as certified-negative + criterion
     trap.
   - Mixed folds: indeterminate; report, no stretch.
   Thread-space results are reported on the same basis (expected ~floor,
   given run 3's 0.6% under an easier criterion; no bar attached).
2. SUB-CHANCE PERSISTENCE (the headline candidate): per space per fold,
   total observed co-mention doc-count summed over eligible pairs vs the
   null distribution of the same total across the R replicates; report
   mean, sd, z. Registered claim bar: z <= -3 in both author-space folds
   => "suppressed pairs co-mention below chance; community segregation
   persists" is claimed in the paper. Otherwise it is a discussion point.
3. LADDER (descriptive): calibrated rates for author/thread x fold1/2
   with Wilson 95% CIs, replacing the retired 19-24%/0.6% rungs. The
   Science4Cast 67% rung is explicitly out of scope (absentia's remit).
4. QUALITATIVE: the calibrated-formed pair list (expected small),
   with observed counts vs p99 thresholds.

## Gate re-derivation (committed procedure, applied after readout 1)
preregistration_gate.md (DRAFT) Q1 is amended to the calibrated
criterion verbatim (same shuffle, R=100, p99, minima) with bars:
calibrated formed count significantly above the 1% floor (one-sided
binomial p < 0.01) in BOTH folds => structure exists, variant graduates;
not significant in both => dead; mixed => indeterminate. Q2 (DD vs MEME)
compares calibrated rates. These bars do not depend on run 8's rates —
only on the criterion — so this amendment is registered here, now,
outcome-blind.

## Execution
- Script eval/run_eval8.py (asserts this file committed); output logged to
  data/registry/run5_author/run8.log and data/registry/pilot1_concepts/
  run8_thread.log; JSONs alongside.
