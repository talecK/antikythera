# Pilot 1 — registered run log

## Run 1 (2026-08-30) — claim units — DEGENERATE
- Fold 2015-16 build / 2017 eval; F>=10 claim-ideas (355); eligible 58,183.
- 0 edges formed. Root cause: claim granularity makes the co-occurrence
  graph all-zeros (only 26 pairs of frequent ideas hit >=2 eval docs at
  all). Not a thesis result. Protocol: granularity rebuild.

## Run 2 (2026-08-30) — concept-string units — PASSED, THEN KILLED BY AUTOPSY
- Same fold; F>=20 concepts (10,404); eligible ~19.0M; base rate 0.175%.
- Pre-registered readout: gap P@50/200/1000 = 0.70-0.80 / 0.67-0.70 / 0.53;
  all baselines ~0. Criterion technically met.
- Exploratory probes (declared before interpretation):
  1. freq_product_only ranker: 0.82 / 0.68 / 0.52 — MATCHES gap everywhere.
  2. Chance-calibrated formation (eval z>=2): 117,109 formed; gap collapses
     to 0.10 / 0.055 / 0.062 — still matched by freq-only.
- VERDICT: the pass was popularity-driven mean reversion. |z|=sqrt(E) for
  zero-observation pairs is monotone in the frequency product, so gap_score
  ~ freq^1.5 x affinity ~ freq-only. Thesis terms added zero signal.
- Structural lesson: "never co-occurred" among frequent pairs is not by
  itself an anomaly; the anomaly is "expected to co-occur, didn't."

## Run 3 (planned) — suppressed-pair formulation
- Eligible: E_build >= threshold AND observed co-occurrence = 0
  ("statistically suppressed" pairs — the thesis's actual gaps).
- Outcome: chance-calibrated formation (eval z >= 2, >=2 docs, >=2 authors).
- Rankers: suppression x affinity; common-neighbors (Science4Cast feature);
  freq-product (confound control, must LOSE for a pass); random.
- Feasibility check pending: count of suppressed pairs at E>=2.

## Ledger
- API ~$75.5 (extraction 51.2 + adjudication 10.6 + smoke 0.7 + pilot0 13)
- Compute: box $4. All folds cached; runs 1-3 reuse everything.
