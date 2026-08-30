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

## Run 3 (2026-08-30) — suppressed-pair formulation — FAILED
- 25,161 suppressed pairs (E>=2, obs=0); 151 formed above chance (0.60%).
- Pre-registered primary (suppression x affinity): P@k = 0 across the board.
- freq_product control: 0 (suppression selects against it, as designed).
- Faint residues: affinity_only 4x random on fold 1 (did NOT replicate on
  fold 2); common_neighbors ~2.5x random in both folds (5/200 hits — the
  oldest generic feature in network science, not the thesis).
- Nominal technicality: common_neighbors met run 3's badly-drafted pass
  condition; flagged as registration-design error, not claimed.

## Check 1 (learned ranker, exploratory) — CEILING = TRIADIC CLOSURE
- GBM over 10 features, 5-fold CV: P@200 = 0.025 (4.2x lift) — identical to
  common_neighbors alone. Feature importance: adamic_adar 0.07, everything
  else ~0 (cosine did not register). No learnable signal beyond closure.

## Run 4 (2026-08-30) — economic-exposure lens — TERMINAL, FAILED
- 5,998 pair-eligible concepts classified EXPOSED/INERT by control-plane
  model under one written rule (1,055 EXPOSED); verdicts frozen pre-eval.
- Exposed lens: fold 1 = 8 formed / 1,452 eligible, all rankers at random;
  fold 2 = 1 formed / 428. exposed x focused lens: EMPTY in both folds
  (exposed concepts are inherently high-promiscuity connectors).
- Registered success bar (beat random AND freq_product at k=200, both
  folds): FAILED decisively.

## FINAL VERDICT — KILL (per run 4's pre-registered terminal clause)
The thesis-specific machinery (co-occurrence nulls, suppression scoring,
semantic affinity over gaps) produced zero incremental predictive signal in
four registered runs, two folds, and an ML sweep. The only real pattern is
textbook triadic closure at ~2.5% precision. On financially-relevant
vocabulary the target event (suppressed pair forming above chance) occurs
~8 times/year on all of HN — no instrument can be built on that base rate.
Clean negative: discourse gaps on HN do not close in a predictable,
exploitable way at any granularity tested.

Assets retained: 20-yr corpus + doc pipeline, 1.3M-doc extraction cache,
registry/eval infrastructure (portable to any future corpus), batched
clustering (16x), full pre-registration audit trail in git.

## Run 3 (original plan, superseded by the above) — suppressed-pair formulation
- Eligible: E_build >= threshold AND observed co-occurrence = 0
  ("statistically suppressed" pairs — the thesis's actual gaps).
- Outcome: chance-calibrated formation (eval z >= 2, >=2 docs, >=2 authors).
- Rankers: suppression x affinity; common-neighbors (Science4Cast feature);
  freq-product (confound control, must LOSE for a pass); random.
- Feasibility check pending: count of suppressed pairs at E>=2.

## Ledger
- API ~$75.5 (extraction 51.2 + adjudication 10.6 + smoke 0.7 + pilot0 13)
- Compute: box $4. All folds cached; runs 1-3 reuse everything.

## Run 5 (2026-08-29, post-kill diagnostic) — author-as-document re-cut
- Registered pre-eval in preregistration_run5.md (commit ce6d639); doc =
  (author, quarter) over quote-attributed concepts (81% of cached claims
  attribute; pipeline/build_author_concepts.py).
- Structure (outcome-blind, recorded pre-eval): eligible suppressed pairs
  collapse from 25,161/7,505 (thread space) to 364/110 (author space) on
  the same folds — the author graph is dense, structurally Science4Cast-
  like (there: 281 per 10M sampled), not thread-HN-like.
- HEADLINE: suppressed-pair formation 70/364 = 19.23% (fold 1) and
  26/110 = 23.64% (fold 2), vs 0.60%/0.68% thread-space. Registered
  >=5%-both-folds threshold MET decisively -> "rooms buried the signal"
  supported: HN individuals DO bridge expected-but-absent concept pairs;
  thread-level co-occurrence was the wrong measurement for the mechanism.
- SECONDARY (ranking): FAILED, as registered-anticipated. common_neighbors
  P@200 = 0.195 vs random 0.230 (fold 1); fold-2 capped k equals the full
  set so P = base rate. Same behavior as Science4Cast's suppressed subset:
  ELIGIBILITY carries all the signal, ranking within it adds none.
- Net: the kill verdict acquires a measurement-artifact component. What
  exists on HN is a suppressed-set DETECTOR (~30x enrichment over the
  thread-space event rate), not a ranked telescope. Author-space
  co-occurrence becomes the default lens for any future discourse corpus.
- Caveats: concept vocabulary still generic; 364/110 eligible pairs is a
  small universe; only top-20-comment threads sampled, so author histories
  are partial; 19% attribution loss assumed outcome-independent.

## Run 6 (2026-08-30) — exposure lens x author space + articulated outcome
- Registered pre-eval (preregistration_run6.md, commit d3844c1). Universe =
  run 5; labels = run 4's frozen verdicts (100% coverage, outcome-blind).
- PRIMARY MET: pooled EXPOSEDxEXPOSED formation 6/26 = 23.1% (Wilson95
  11.0-42.1%; fold 1: 3/20, fold 2: 3/6) vs registered >=3/26 bar. Same
  rate as all-pairs author space (19%/24%); vs thread-space exposed 0.55%/
  0.23%. The detector survives economically-relevant vocabulary.
- Exposed hits: google<->housing costs, pricing<->saudi arabia,
  github<->spacex (2017); real estate<->security, artificial
  intelligence<->pricing, microsoft<->sustainability (2016).
- SECONDARY (articulated = both concepts in ONE extracted claim, eval
  window): all-pairs strict 4+2, weak 13+11 of 364+110 eligible; exposed
  strict 0, weak 1. Author-space formation is almost never an articulated
  connection — it is pre-articulation audience convergence. The detector
  fires BEFORE anyone writes the connecting claim.
- Scale caveat: on HN the exposed slice is thin (~13 flags/yr, ~3 form).
  Density must come from a finance/security-native corpus (variant gate).

## Run 7 (2026-08-30) — scout class: FAILED all three stages
- Registered pre-eval (preregistration_run7.md, ff94e9f). 1.6M track-era
  bridge events, 27,258 bridging authors, catch-on rate 6.5%.
- Stage A (PRIMARY, persistence): split-half Spearman rho = 0.012 vs null95
  = 0.035 across 4,236 qualified authors — FAIL. First-bridge precision has
  zero measurable persistence: bridging is state, not trait.
- Stage B (telescope): scout ranker P@50 = 0.14 — BELOW random (0.24);
  activity and common_neighbors ≈ random. FAIL. Also: 364/364 eligible
  pairs had a qualified slow-bridger — the notion is too common to select.
- Stage C (alert): top-tercile first-bridger precision 28.2% formed vs
  bottom 25.4%, Fisher p=0.43. FAIL.
- Registered interpretation applies: scout products are dead on HN; the
  variant gate proceeds CENSUS-ONLY (identities not first-class). Ranking
  within the eligible set remains dead on every feature family tried:
  graph (runs 3/5), semantic (runs 2-4), reputational (run 7).
- Scope caveat: HN vocabulary + quarterly buckets; a finance-native retest
  is nearly free once a gate corpus exists, but carries no priority claim.
