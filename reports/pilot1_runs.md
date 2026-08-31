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

### Run 7 addendum (2026-08-30) — POST-HOC diagnostics (exploratory, labeled)
Prompted by owner challenge: was stage A powered to see a real trait?
1. Power: YES for meaningful effects. Simulated stable traits at the exact
   per-author event counts: trait SD 0.03/0.05/0.10 -> expected split-half
   rho 0.28/0.46/0.68 (100% detectable vs null95 0.035); observed 0.012.
   Caveat: sims assume independent events; within-author outcome dependence
   (shared topics/moments) inflates noise ~3x (chi ratio), which drags the
   SD=0.03 case toward marginal — but SD>=0.05 (scouts reliably ~2x base
   rate) stays firmly excluded.
2. Overdispersion: heterogeneity EXISTS — chi 47,100 vs null 14,701
   (p<0.001). Reconciliation with rho~0: author outcomes correlate WITHIN a
   period but not ACROSS periods. Bridging success is bursty/situational
   (being in the right topic at the right moment), not a persistent skill.
3. SCOPE correction: all run-7 conclusions are HN-scoped. Reputational
   ranking was tested only here (graph/semantic failed on HN AND science).
   Negative transfers weakly; the variant registration should carry a cheap
   scout-module secondary readout rather than dropping the idea.

## Robustness suite R1-R4 (2026-08-30) — R1 PLACEBO FAILS: run-5/6 rates are sub-mechanical
Registered pre-eval (preregistration_robustness.md, commit 31bc9ab).
Harness sanity: reproduces run 5 exactly (364/70, 110/26) before any check.

- **R1 PLACEBO (load-bearing): FAILED — committed revision clause fires.**
  Eval-window label shuffle (doc sizes and concept totals preserved,
  within-doc association destroyed; R=100/fold, seed 20260830):
  - fold 1: observed 70 formed vs null mean 124.6 (sd 8.9, p99 140,
    min 105) — observed is 6.1 sd BELOW the mechanical null.
  - fold 2: observed 26 vs null mean 52.0 (sd 4.9, p99 63, min 42) —
    5.3 sd BELOW.
  Reading: the z>=2 formation criterion's internal null (Poisson-style on
  doc counts) is badly anti-conservative under author-doc size
  heterogeneity — random relabeling "forms" 34%/47% of suppressed pairs.
  The 19-24% headline is NOT person-level bridging enrichment; it sits
  UNDER the pooling-mechanics floor. Direction flip: eligible suppressed
  pairs co-mention LESS than chance given eval marginals — build-window
  segregation persists into eval. Per the frozen interpretation, run 5's
  meaning is REVISED (not nuanced): author-space "formation at 19-24%" is
  substantially mechanical; the 30x author-vs-thread enrichment is
  criterion-confounded (thread-space shuffle null not computed here; out
  of registered scope). Knock-ons, in order: run 6's 23.1% exposed rate
  (same criterion) inherits the confound; the cross-corpus ladder
  (science 67% / HN-authors 20% / HN-threads 0.6%) is criterion-bound and
  cannot calibrate anything until each rung gets its own shuffle null
  (Science4Cast rung = absentia's scope); the variant gate's Q1 bars are
  uninterpretable as registered.
- **R2 window sensitivity: rates >=5% everywhere** (month 9.7%/20.6%,
  half-year 15.8%/27.8%; eligible 618/189 and 304/90) — the measured rate
  is not a quarter-window artifact. Post-R1 this corroborates that the
  artifact lives in the formation criterion, not the window plumbing.
- **R3 formation x articulation + timing** (descriptive): pooled, 74/96
  formed pairs (77%) have NO articulating claim anywhere in the 2015-2017
  cache; of 22 ever-articulated, first co-mention strictly precedes first
  articulation in 12, ties in 6, trails in 4. The registered withdrawal
  condition (articulation typically precedes co-mention) does NOT fire;
  the pre-articulation pattern stands, now conditional on "formation"
  surviving recalibration under a corrected null.
- **R4 attribution lens: robust as measured** — dropping every
  story-author-attributed row (conservative over-exclusion) gives
  24.9%/27.5% on 209/69 eligible; the rate is not an attribution-path
  artifact.
- Net: the robustness suite did its job on the check that could change a
  conclusion. The author-lens revision of the kill is itself revised:
  what survives of runs 5/6 is (a) the structural finding that
  author-space co-occurrence graphs are dense/science-like (eligibility
  census numbers are outcome-free and stand), (b) the persistence of
  segregation (suppressed pairs under-co-mention chance, -5 to -6 sd),
  and (c) the R3 articulation pattern. What does not survive: any claim
  that individuals bridge suppressed pairs at enriched rates under the
  current criterion.
- Follow-up (not run, needs registration): run 8 — shuffle-calibrated
  formation (pair forms iff observed eval co-mention docs exceed its own
  per-pair shuffle p99), recomputed in author AND thread space; ladder
  recalibration; gate Q1 bars re-derived from the corrected criterion
  BEFORE the gate flips to REGISTERED.

## Run 8 (2026-08-30) — shuffle-calibrated formation: NO above-chance formation ANYWHERE; sub-chance persistence CONFIRMED at scale
Registered pre-eval (preregistration_run8.md, commit 63b72d9). Criterion:
pair forms iff observed eval co-mention docs > per-pair label-shuffle p99
(R=100, seed 20260831) AND >=2 docs AND >=2 authors (~1% false-positive
floor per pair by construction).
- PRIMARY: calibrated formed counts sit AT or BELOW the false-positive
  floor in every cell:
  - author fold 1: 3/364 (floor 3.6, one-sided binomial p=0.71)
  - author fold 2: 1/110 (floor 1.1, p=0.67)
  - thread fold 1: 20/25,161 (floor 251.6, p=1)
  - thread fold 2: 11/7,505 (floor 75.0, p=1)
  Registered interpretation applies: no evidence that individuals (or
  threads) bridge suppressed pairs above chance. The author-lens revival
  is CLOSED FOR GOOD. The detector is dead on HN under an honest null.
- SUB-CHANCE PERSISTENCE (registered bar z<=-3 both author folds): MET,
  overwhelmingly. Total co-mention over eligible pairs vs shuffle null:
  - author: 746 vs 1,055 (z=-9.2) and 454 vs 651 (z=-9.3) — ~70% of chance
  - thread: 12,098 vs 48,373 (z=-162) and 7,866 vs 28,230 (z=-124) —
    ~25-28% of chance.
  The paper claims it: suppressed pairs co-mention BELOW chance;
  community/topic segregation persists into the eval year in both spaces.
  This is the corpus's real, large, replicated regularity — gaps don't
  close; they actively stay open.
- LADDER RECALIBRATION: the retired rungs (19-24% author, 0.6% thread)
  are replaced by "calibrated rate indistinguishable from the 1% floor"
  in all four HN cells. The Science4Cast 67% rung is untested under this
  criterion and is absentia's remit; until re-measured there, NO
  cross-corpus rate comparison is quotable.
- GATE: the outcome-blind amendment registered in preregistration_run8.md
  is applied — gate Q1/Q2 move to the calibrated criterion with
  floor-relative bars. The gate's question is now sharp: does financial
  discourse show above-chance calibrated formation where HN shows none?
- Thread-space depth note: thread co-mention at ~1/4 of chance means the
  original 0.6% "formation rate" was itself mostly criterion artifact on
  top of massive under-mixing; runs 1-4's kill is thereby STRENGTHENED.

## Variant gate — FOLD A INTERIM (2026-08-30; registered, interim clause)
Harness ported to the run-8 criterion before running (imports
run_eval8.binom_sf_ge); registration REGISTERED with the interim clause
committed pre-eval. Fold A acquisition complete (API, 14.6M items);
FOLD B RAN ON PARTIAL ACQUISITION (15/36 months) and its numbers are NOT
reportable — they are re-run when the dump loop finishes. Fold-A-only
results cannot meet or fail a registered bar (bars need both folds).

| stratum | lens | eligible | Q1 formed (floor, p) | Q1b seg z | obs vs null |
|---------|------|---------:|----------------------|----------:|-------------|
| ALL  | union   | 169 | 0 (1.7, p=1)     |  **-9.4** | 341 vs 555 |
| ALL  | cashtag |  54 | 0 (0.5, p=1)     |      -2.4 |  62 vs  84 |
| DD   | union   | 144 | 1 (1.4, p=0.765) | **-10.0** | 166 vs 358 |
| DD   | cashtag |  22 | 0 (0.2, p=1)     |      -2.7 |   4 vs  12 |
| MEME | union   |  62 | 1 (0.6, p=0.464) |  **-0.2** | 150 vs 152 |
| MEME | cashtag |  32 | 0 (0.3, p=1)     |      -1.1 |  37 vs  44 |

1. **Q1 formation: null, as predicted.** 0-1 formed per cell, every cell at
   or below its false-positive floor. Per the registered power table this
   licenses "no effect larger than ~3.7%", NOT "no effect".
2. **Q1b segregation REPLICATES on a second platform and unit type**:
   ALL z=-9.4, DD z=-10.0 — within 0.2 of HN author-space (-9.2/-9.3)
   despite different platform, units (tickers vs LLM concepts), community
   and years. DD co-mentions at 46% of chance.
3. **NEW, UNREGISTERED, STRATUM SPLIT (exploratory, flagged as such):**
   the segregation effect is entirely in the DD stratum. MEME (WSB) sits
   at z=-0.2 — 150 observed vs 152 expected, i.e. exactly chance. This is
   NOT a power artifact: at DD's effect size MEME would show ~70 vs 152
   (z~-7). Reading: analyst-style subs are topically segregated (people
   keep lanes); meme culture co-mentions tickers at chance with respect to
   prior structure — undifferentiated attention. This is the better-powered
   form of the Q2 mechanism question, as anticipated when Q2 was demoted,
   but the split itself was not registered and must be replicated on fold B
   before any claim.

### Gate fold-B amendment (2026-08-30 evening) — DD cells EXEMPT from the
### partial-acquisition disclaimer; valid as run
The earlier blanket ("fold B ran on partial acquisition; not reportable")
was overcautious for the DD stratum: DD is built ENTIRELY from the API
pull, which was complete (build 2022-23 + eval 2024, 265K mentions in
2024) before the gate ran. Only WSB comes from the dump loop. Cell status:
- **fold B DD union: z = -16.5 (obs 358 vs null 824; 43% of chance),
  formed 0/281 (floor 2.8) — VALID, final. DD cashtag: z = -4.6, 0/44.**
- Combined with fold A: segregation replicates in the analyst stratum in
  BOTH folds on BOTH platforms (Reddit -10.0/-16.5; HN -9.2/-9.3), with
  calibrated formation null throughout (power caveat: MDR ~4%).
- ALL and MEME fold-B cells remain pending WSB dump completion (~14h;
  2023-04..2024-12). The exploratory DD-vs-MEME split (WSB at chance,
  z=-0.2 fold A) awaits its fold-B test there — no claim before that.
- On WSB completion: rebuild the mentions parquet, re-run the full gate
  table; DD numbers must reproduce (added WSB rows never enter the DD
  stratum) — any drift is a red flag, not noise.
