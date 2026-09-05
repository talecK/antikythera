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

### Correction (2026-08-30, late) — the science "67%" rung was never z-criterion
Flagged by the gate session, verified against eval/run_tier_a.py: Tier A
formation is the BENCHMARK'S OWN ground truth (`sol` from the pkl — any
edge appears in the target-year graph), not our z>=2 criterion, which
that harness never contained. Consequences for the record:
1. The 67% (188/281) is NOT contaminated by the R1-exposed criterion
   defect. Statements above tying the "67 / 20 / 0.6 ladder" to the z>=2
   criterion are wrong for the 67 rung specifically.
2. Worse for the ladder, not better: 67% ("any edge appears") and the HN
   rates ("z>=2 co-mention, >=2 distinct authors") were DIFFERENT EVENTS
   from day one — the cross-corpus comparison was ill-posed regardless of
   criterion calibration. The ladder is retired on both grounds.
3. Tier A certifies harness correctness (eligibility, ranking, P@k, AUC
   0.899 vs published 0.851) — it never exercised, and cannot certify,
   the formation criterion.
4. Whether the benchmark's 67% is substantially mechanical (target-year
   densification) is untested; a shuffle null there is absentia's scope.
Paper Sec 4.2/6.1 rewritten accordingly; HANDOFF banner corrected.

## VARIANT GATE — FINAL (2026-08-31 02:21; registration preregistration_gate.md
## + amendments A1-A6', all committed pre-outcome)
Corpus final: 49.2M items, 4.55M ticker mentions, 41.5M unique items;
provenance = dumps for the Pushshift era (2022-01..2023-03) + API for the
Arctic-Shift era (2023-04..2024-12, uniform eval year per A6/A6') + fold A
API. NO missing months (A3 hole never triggered; 2023-04 API-filled).

| fold | stratum | lens | eligible | Q1 formed (floor, p) | Q1b seg z | obs/null |
|---|---|---|---:|---|---:|---|
| A | ALL  | union   | 169 | 0 (1.7, p=1)     |  -9.4 | 341/555 |
| A | ALL  | cashtag |  54 | 0 (0.5, p=1)     |  -2.4 | 62/84 |
| A | DD   | union   | 144 | 1 (1.4, p=.765)  | -10.0 | 166/358 |
| A | DD   | cashtag |  22 | 0 (0.2, p=1)     |  -2.7 | 4/12 |
| A | MEME | union   |  62 | 1 (0.6, p=.464)  |  -0.2 | 150/152 |
| A | MEME | cashtag |  32 | 0 (0.3, p=1)     |  -1.4 | 37/45 |
| B | ALL  | union   | 487 | 2 (4.9, p=.956)  | -17.6 | 710/1344 |
| B | ALL  | cashtag | 192 | 0 (1.9, p=1)     |  -9.8 | 138/331 |
| B | DD   | union   | 281 | 0 (2.8, p=1)     | -16.3 | 358/823 |
| B | DD   | cashtag |  44 | 0 (0.4, p=1)     |  -4.5 | 11/41 |
| B | MEME | union   | 213 | 1 (2.1, p=.882)  |  -8.7 | 369/596 |
| B | MEME | cashtag | 141 | 0 (1.4, p=1)     |  -8.0 | 102/223 |

REGISTERED READOUTS:
1. **Q1 formation: NOT significant in either fold** (ALL/union p=1, p=.956).
   Registered branch applies: no above-chance calibrated gap formation on a
   second platform — the variant is DEAD; the project's positive hypothesis
   closes on a clean two-platform, three-unit-type negative. Power caveat
   (registered): licenses only "no effect > ~3.7% (fold A) / ~2.1% (fold
   B)", never "no effect".
2. **Q1b segregation: REPLICATES — registered bar met.** ALL/union
   z = -9.4 and -17.6 (bar: z<=-3 both folds). Suppressed ticker pairs
   co-mention at 61%/53% of chance. Robust across lenses in fold B
   (cashtag -9.8). The HN finding generalises: gaps actively stay open.
3. **Q2 / exploratory split: DOES NOT SURVIVE fold B.** Fold A: DD -10.0
   vs MEME -0.2 (at chance). Fold B: DD -16.3 vs MEME -8.7 — WSB is
   strongly segregated post-GME. The community-type moderator is NOT a
   stable property; on its face the split is regime-dependent (WSB
   pre-2020: at chance; post-2021: segregated), reported as measured with
   no interpretation stretch per the frozen rule. The stable finding is
   stratum-independent segregation in fold B.
4. **DD reproduction check: PASSES.** z -16.3 vs -16.5 across corpus
   rebuilds = shuffle-simulation noise (obs identical at 358; eligible
   identical at 281; build docs differ by ONE, 122,816 vs 122,815 —
   dedup-order artifact, disclosed).
5. NOT RUN (disclosed): Q3 scout module and Q4 hygiene counts — secondary,
   no bars attached; can be computed from the banked corpus at any time.

## POST-REVIEW RERUN v2 (2026-08-31) — deterministic harness, registered exclusions enforced; ALL CONCLUSIONS HOLD
Triggered by the adversarial review (reports/adversarial_review_2026-08-31.md,
committed verbatim at 45455bc). Fixes at f89cb2b: sorted incidence iteration
(finding 1.2 — the registered seed previously pinned nothing), SPY/QQQ/VIX +
BTC/ETH exclusion enforced at gate load (1.4), Q2 MEME-subsample implemented
(2.2), R2/R4 shuffle nulls added (1.1), timestamped outputs (2.8), run-5
noguard sensitivity delivered (2.1). Every quoted number regenerated from
single clean artifacts. THIS TABLE SUPERSEDES the "VARIANT GATE — FINAL"
table above, which mixed two nondeterministic runs (finding 1.3), including
one wrong primary count (fold A MEME formed: reported 1, final artifact 0;
under the deterministic harness it is 2 — the count was seed-noise all along,
p ns in every version).

Gate v2 (data/registry/gate_eval.json + timestamped copy; log gate_rerun_v2.log):
| fold | stratum | lens | eligible | Q1 formed (floor, p) | Q1b z | obs/null |
|---|---|---|---:|---|---:|---|
| A | ALL  | union   | 166 | 0 (1.7, p=1)      |  -8.8 | 334/544 |
| A | ALL  | cashtag |  56 | 0 (0.6, p=1)      |  -2.8 | 62/88 |
| A | DD   | union   | 146 | 0 (1.5, p=1)      | -10.1 | 168/359 |
| A | DD   | cashtag |  19 | 0 (0.2, p=1)      |  -2.8 | 3/13 |
| A | MEME | union   |  62 | 2 (0.6, p=0.128)  |  -0.1 | 151/153 |
| A | MEME | cashtag |  32 | 0 (0.3, p=1)      |  -1.2 | 39/46 |
| B | ALL  | union   | 478 | 1 (4.8, p=0.992)  | -17.7 | 726/1383 |
| B | ALL  | cashtag | 191 | 0 (1.9, p=1)      | -10.6 | 99/263 |
| B | DD   | union   | 281 | 1 (2.8, p=0.941)  | -17.1 | 359/826 |
| B | DD   | cashtag |  39 | 0 (0.4, p=1)      |  -4.3 | 9/29 |
| B | MEME | union   | 209 | 1 (2.1, p=0.878)  |  -9.0 | 369/595 |
| B | MEME | cashtag | 140 | 0 (1.4, p=1)      |  -7.6 | 80/186 |

- Q1: ns everywhere (min p=0.128). Fold-B ALL/union's single formed pair is
  ARM x BBAI — the disclosed IPO-backfill artifact (review 2.6). MDRs at the
  v2 census: fold A 3.7% (n=166, k=6), fold B 1.8% (n=478, k=11) — fold B
  post-hoc arithmetic by the registered formula, labeled as such.
- Q1b: ALL/union -8.8 / -17.7 — registered bar met, both folds, unchanged.
- Q2 REGISTERED SUBSAMPLE (first execution): MEME docs matched to DD counts,
  seed 20260830 — fold A z=-0.0 (at chance even matched), fold B z=-5.2
  (segregated even subsampled). Neither stratum reading is a doc-count
  artifact.
- Run 8 v2: author 2/364 (p=0.88) & 0/110 (p=1); totals z -8.9 / -8.6;
  thread 22/25,161 & 12/7,505 (p=1); totals z -152.3 / -123.2.
- R1 v2: null mean 125.1 (sd 9.5) vs obs 70 (-5.8 sd); 53.0 (5.4) vs 26
  (-5.0 sd). R2/R4 SHUFFLE NULLS (new): observed formation is below the
  null MINIMUM of 100 replicates in every window and lens (month 60<133,
  39<53; half 48<86, 25<35; comment-lens 52<62, 19<25) — the paper's Sec
  5.2 claim is now measured, not asserted.
- Run-5 noguard sensitivity (delivered per 2.1): without the hub guard the
  suppressed universe collapses to 41 (fold 1) and 9 (fold 2) eligible
  pairs — hub documents' combinatorial co-occurrence destroys eligibility;
  the guard is load-bearing for universe existence, not a rate tweak.
- Seed-noise note: pre-fix runs varied by hash order (documented +-0.5-0.7
  in |z|, and 0-2 in small formed counts). v2 numbers reproduce exactly
  from seed 20260831 under PYTHONHASHSEED-independent sorted iteration.

### v2 addendum (2026-08-31, post second review pass): MDR k-values for the
### record — fold A n=166: k=6 (P(X>=6|166,.01)=0.0068); fold B n=478: k=11
### (P(X>=11|478,.01)=0.00975, a 2.5% margin under alpha — at n+-4 the
### threshold moves to k=12/2.1%, hence the paper quotes "roughly 2 percent").
### Second pass verified v2 end-to-end: traceability PASS, determinism PASS
### (PYTHONHASHSEED-independent to 6 decimals), no stale numbers.


## Nulls amendment: local takeover and registered label-seed check (2026-09-04)
Registration and source: A1 at e939759; pre-run clarification at 8365fe5.
The three-cell Paper 2 local replay agrees exactly in all 16 published
columns. All four Paper 1 observed totals and eligible counts agree
with the archived JSONs. Full M3 reproduction remains owner-reported.

Paper 1 label-shuffle seeding check (R=100; per-cell seeds as registered):
| space | fold | observed/null | z | formed/eligible | z change from archived run 8 |
|---|---|---:|---:|---:|---:|
| author | fold1 | 0.7067 | -9.54 | 1/364 | 7.46% |
| author | fold2 | 0.7025 | -8.39 | 0/110 | 2.08% |
| thread | fold1 | 0.2500 | -157.34 | 21/25161 | 3.29% |
| thread | fold2 | 0.2784 | -128.64 | 10/7505 | 4.44% |

P1-b: PASS; maximum relative z change 7.46%, below the 20% bar.

The HN component of D-b fails under the registered label null: thread
collapse is 0.314% and 0.367%, below author collapse of 0.474% and
0.568%, respectively. The temporal-null and WSB components are pending.
These are Monte Carlo seed checks under the original label null, not
validation of a fixed-margin null. Binomial outputs are historical
descriptions; the 1% reference is not a guaranteed bound on realized
counts or evidence that each observed pair is a false positive.

Artifacts: reports/paper1_nulls_label_R100.tsv and .json (environment,
seeds, formed pairs and raw-count checksums). Integer replicate arrays
are retained under data/registry/nulls_revisions/label_R100/.
The source TSV and run-8 JSONs were not overwritten. The 38-cell N1
series is running locally; the large R=1000 and pooled thread runs are
assigned to the M3 queue and have not started here.


## Nulls amendment: completed quarter-stratified checks (2026-09-04)

Paper 2: all 38 primary cells completed locally, source commit 8365fe5,
three workers, 1276.81 seconds wall time. Paper 1: all four cells
completed, source commit b84435b, one worker. Exact commands and raw
progress logs are in logs/takeover_n1_primary.log and
logs/takeover_paper1_n1.log.

| prediction | outcome | evidence |
|---|---|---|
| N1-a | PASS | Every originally detected cell keeps its sign; both original non-detection windows remain within abs(z)<3 |
| N1-b | PASS | Onset k=5, evaluation 2021Q2-Q3; P1/P2/P3 pass; no later exceptions |
| N1-c | PASS | Excursion z=19.63 and 30.45; observed/null=1.569 and 1.627 |
| N1-d | FAIL | Seven non-excursion cells exceed the nominal 0.01*n reference |
| P1-a | PASS | All four HN z<=-3 and formed<=0.01*n |
| P1-b | PASS | Original-null seeded check reported above |
| D-b | FAIL | HN thread collapse is smaller than author collapse; the WSB N1 component is in the predicted direction |
| R-a, R-b, T-a, T-b, T-c | PENDING | Assigned to the M3; no result imported here |

N1-d exceptions (all WSB): k=0 (1/45), k=1 (2/77), k=2 (2/64),
k=5 (6/498), k=9 (3/225), k=10 (2/146), k=16 (2/71). These literal
prediction failures are not calibrated tests of above-chance formation.

Paper 1 N1 details:

| space | fold | observed/null | z | formed/eligible |
|---|---|---:|---:|---:|
| author | fold1 | 0.7066 | -10.89 | 2/364 |
| author | fold2 | 0.6970 | -7.33 | 0/110 |
| thread | fold1 | 0.2504 | -168.24 | 15/25161 |
| thread | fold2 | 0.2784 | -104.10 | 14/7505 |

The WSB N1 collapse fractions are 6.50% and 7.54% in the two original
non-detection windows, versus 13.00% and 12.86% in the excursion. The
original-null WSB component of D-b awaits the M3 headline diagnostics.
DD ratios are 0.692 at k=4 and 0.459 at k=5: the control step remains
visible under N1 although P3 passes its narrower threshold rule.

Decision rules: N1 does not trigger excursion withdrawal or onset
revision. N2 remains required; these results do not validate exact
binary margins. Public manuscript release remains on hold.

Machine-readable scoring, including artifact SHA-256 values:
reports/nulls_amendment_scores.json, generated by
eval/score_nulls_amendment.py. The frozen published TSV and run-8
JSONs retain their original hashes.

## N2/N3 prospective registration and first exact-margin result (2026-09-04)

Registration 5215719 fixes all scientific predictions before any real-data
Curveball chain. Implementation f4e812b passed four kernel tests and five
pipeline/diagnostic tests, including independently generated ArviZ 0.22.0
fixtures at relative/absolute tolerance 1e-10. Reference validation used an
isolated work/ environment; the original pinned .venv was unchanged.
`reports/curveball_validation_v1.json` records the build and validation.

First cell: Paper 2 WSB k=1, evaluation 2020Q2-Q3, N2 (exact binary margins,
no quarter restriction). Native counts agree with every frozen observed
pair count, including total 695 over 77 eligible pairs. The pilot failed
at 280 and 480 saved sweeps per chain and passed at 880 with selected
burn-in 20 sweeps. Fresh production used burn-in 40; stages with 400 and
800 saved sweeps per chain failed, and 1600 passed. All failed diagnostic
records and raw arrays are preserved. No pilot draws entered production.

Production, 6400 pooled draws: null mean 824.1721875, population SD
27.7514646274, z=-4.6546079364, observed/null=0.8432703876. This formerly
non-detected original-null cell (z approximately +1.5) becomes negative
under N2. The aggregate result is diagnostically usable; formation-tail
classification remains UNRESOLVED. The full-series onset prediction is
not scored from this one cell. These outcomes were not known when X-b
was registered and that prediction remains unchanged.

Artifact: `reports/curveball_p2_WSB_01_N2.json`; canonical preparation:
`reports/curveball_matrix_p2_WSB_01.json`; all stage records have separate
report files and raw SHA256s. Pilot and production took approximately
163 and 285 seconds respectively, excluding initial corpus preparation.
This is local M1 timing for one cell, not an ETA for the larger thread
matrices. N3 on this cell is running at this entry. MBP remains
user-reported running; no outputs have been received or incorporated.
A read-only shared-remote branch listing exposed only main.

The same first cell also completed N3 (exact margins within quarter):
pilot stages 280/480 failed and 880 passed with burn-in 40. Fresh
production used burn-in 80; 400 sweeps per chain failed and 800 passed.
The 3200 pooled production draws give null mean 820.9553125, SD
26.5608182390, z=-4.7421473001 and observed/null=0.8465747032. Aggregate
and formation diagnostics pass for N3. Both exact-margin variants therefore
remove the original non-detection reading in this first window. Full-series
predictions remain pending. N3 pilot/production took 151.91/144.02 seconds.

The complete registered 42-cell scope (38 Paper 2 plus four Paper 1), both
N2 and N3, is now queued on two M1 workers via
`eval/run_curveball_queue.py --cells all --workers 2`. Matrices prepare
serially before the two nulls run concurrently. The shared lock excludes
the earlier serial runner; completed first-cell outputs were hash-checked
and skipped. The queue records its own code hashes and per-cell result
hashes in `reports/curveball_queue_v1.json`. Neither MBP workloads nor
absentia H2 jobs are launched or modified by this queue.

## M3 results independently incorporated (2026-09-04)

Fetched results branch `codex/m3-revision-results`, commit 1ca9817.
That commit adds six report files only; its parent is b84435b. The
queue manifest records all three jobs complete on arm64, using the
pinned versions and the expected code and input-manifest hashes. This
is verified artifact evidence, not live remote process telemetry.

The branch omitted ignored raw data as intended. The owner supplied
`m3-thread-raw.tar.gz`; both thread NPZ SHA256s match the queue manifest.
The companion ignored JSON was reconstructed from the identical cell
records embedded in the supplied report JSON; its exact bytes also
match the queue manifest. Independently recomputed all pooled and batch
means, SDs, z, ratios and formation counts from the integer arrays.
All comparisons pass, with exact integer counts and registered floating
tolerances. Verification artifacts: `reports/m3_import_verification.json`,
`reports/m3_incorporation_verification.json`, and
`reports/m3_raw_transfer_verification.json`. Earlier report-only review
files are retained as chronological evidence, superseded by this audit.
Merged the six report files into local main at d50d952. Original M1
registrations, results and local working changes were preserved. Raw
arrays remain under ignored data/; no new remote push or preprint upload.

| prediction | outcome | evidence |
|---|---|---|
| R-a | PASS | All eight label-null headline z estimates within 20% of original; largest change 13.94% |
| R-b | PASS | Six strongly detected cells have two-sided simulation-tail summary 2/1001; the two original nondetection cells have 0.140 and 0.194 |
| T-a | PASS | Every thread batch z<-100 in both folds |
| T-b | PASS | Every batch formed count<=0.01*eligible |
| T-c | PASS | Batch ratio range / pooled ratio is 0.0992% and 0.2431%, below 5% |

Pooled thread results (1000 draws, pooled before moments and percentiles):
fold1 observed/null=0.2500673, z=-162.8774, formed 11/25161;
fold2 observed/null=0.2784329, z=-124.2746, formed 9/7505.
Batch z ranges are -178.93 to -144.59 and -148.01 to -113.42;
these are Monte Carlo batch ranges, not confidence intervals.

Paper 2 headline excursion estimates at R=1000:
original label null: ratios 2.3115/1.6947, z=31.8441/33.6004;
quarter-stratified label null: ratios 1.5707/1.6235, z=18.0051/28.9301.
WSB original-null collapse is 12.829%/12.720% in the excursion, versus
5.828%/6.858% in the two preceding cells. That component of D-b is in
the predicted direction, but D-b still FAILS due to its HN component.
N1-d also remains FAIL. Full updated literal scoring is in
`reports/nulls_amendment_scores.json`. N2/N3 work remains in progress.

## Current Curveball outcomes and user-directed M1 stop (2026-09-04)

WSB k=2 N2 passes aggregate production diagnostics: z=-2.97688,
observed/null=0.82201, 6400 pooled draws; formation unresolved. Its N3
pilot remains UNRESOLVED at 880 sweeps per chain. WSB k=3 reaches the
same pilot cap without passing under either null; no production runs.
X-a, X-b and X-c are therefore UNRESOLVED under both nulls, while
Paper 1 predictions await their cells. These diagnostic failures are
preserved and do not constitute scientific failures or usable effects.

At 2026-09-05T04:41:07Z the user requested stopping M1 immediately and
restarting on MBP. Only the queue parent and its two workers were sent
SIGTERM, and their exit was verified. WSB k=4 was interrupted during its
pilot; saved 280/480 stages and initialization/provenance files remain
byte-identical in an explicit archive. No result is assigned to the
interrupted cell. The path/SHA map is reports/curveball_m1_interruption.json.
The queue budget now charges the 1045.829384 summed worker-seconds from
these interrupted attempts. No kernel, seed, sampling-limit or diagnostic
rule changed. Host transfer instructions restart only the interrupted
cell and unstarted cells, preserving completed unresolved attempts.

## Paper 1 exact-margin verification complete (2026-09-04 Pacific)

The full MBP queue reports COMPLETE, 84/84 cell/null attempts. Paper 1's
104 files (246,229,276 bytes) were transferred to M1 using an immutable
file manifest. File hashes, frozen input/census/matrix/code provenance,
all saved aggregate diagnostic stages, production moments, and formation
checks were recomputed and matched. This audit resampled no data.
Verifier: eval/verify_curveball_results.py; audit:
reports/paper1_curveball_verification.json. Raw files remain ignored.

X-d PASS under both N2 and N3 for all four HN cells. Exact-margin ratios
are .681-.694 in author space and .247-.274 in thread space. X-e remains
UNRESOLVED under both nulls: seven cell/null combinations fail one or
more pair-classification precision checks. N3 author fold2 passes those
checks with zero formed pairs. Original and failed results are retained.
Table 5 in paper1_draft.md records the final aggregate outcomes and
qualifies the descriptive counts. No further Paper 1 sampling solely for
formation precision or new FDR project is planned for this revision.

The user accepted one prospectively registered, bounded Paper 2 extension
after the initial queue; retain all unresolved results, preserve thresholds,
and stop after that extension absent a demonstrated implementation error.
The extension has NOT started; full Paper 2 import/audit and prospective
registration must precede it.

## Paper 2 audit and single bounded extension registration (2026-09-04)

All 76 first-pass Paper 2 attempts independently audited on M1: 968 files,
raw moments, stage diagnostics, formation checks and 38 frozen primary
censuses match. N2 has 13 passing/25 unresolved cells; N3 has 19 passing/
19 unresolved. No unresolved first-pass effect is treated as a result.
The complete first-pass queue snapshot is preserved separately.

The user accepted one bounded extension and no further large sampling
for this revision except correction of an implementation error. Registered
protocol preregistration_nulls_extension1.md and its exact 44-job JSON plan
retain original predictions and diagnostics. Fresh pilot stages1760/3520/
7040, candidate burns80/160/320/640; independent production800/1600/3200,
burn twice selected pilot burn. Native MBP, two workers, six-hour sampling
wall limit and 90 minutes per case, plus explicit finalization overhead.
Original kernel, Ensemble and diagnostics are unchanged. Four synthetic
tests pass. No real extension chain has run before this registration.

## First extension window independently verified (2026-09-05 Pacific)

The MBP extension resolved WSB k=3 (2020Q4-2021Q1) under both nulls.
Both pilots passed at1760 sweeps; fresh production passed at1600 sweeps
per chain, 6400 pooled draws. M1 verified 22 transferred files, code/input/
matrix hashes, all stage diagnostics and raw summary moments. N2 ratio
1.0825390954, z3.0072213753; N3 ratio0.8957238145, z-4.4503406946.
This window does not meet X-c's z>=5 under either null, and the N3 sign
reverses the original positive result. Full-scope prediction scoring
remains pending while other required extension cells run. Do not score
these diagnostic passes as scientific prediction passes. Sources:
reports/curveball_extension1_verification_001.json and matching manifest.

A status check also identified maintenance sleep on MBP despite the
original idle-sleep assertion. Added process-bound caffeinate -isu and
verified PreventSystemSleep=1 on AC. An external UTC wall guard enforces
the original05:21Pacific deadline because macOS monotonic time pauses
in system sleep. No scientific source or sampling budget was changed.

## Final bounded extension verified (2026-09-05 Pacific)

All44 extension attempts completed, passing aggregate production diagnostics,
with no resource-limited cases. M1 independently verified496files,
164,102,602bytes, all frozen hashes/censuses, stage diagnostics and raw
moments. Original32 passing cases plus44 extension cases resolve all76
Paper2 cell/null cases. X-a, X-b and X-c FAIL under both N2 and N3.
N2 onset k4 with P1false; N3 onset k0 with P1/P2false, all later WSB
windows z<=-3. The second excursion reverses under both nulls. Full
values and interpretation: reports/curveball_extension1_conclusions.md.
The queue exited by08:36:55UTC, about2h15 after start; summed attempt
durations4.140worker-hours. No further sampling planned; original results
and failed predictions preserved. No formation inference added. Final
audit and immutable transfer manifest use the extension1_*_final names.
