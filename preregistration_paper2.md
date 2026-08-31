# Paper 2 registration — "Watching the walls go up" (drafted 2026-08-31)

## STATUS: DRAFT — PENDING OWNER REVIEW. Not registered. No rolling-window
## or rebuilt-fold statistic may be computed until this line reads
## "STATUS: REGISTERED", the file is committed, and the owner has reviewed
## it in-session. Any eval script for this study must refuse to run in
## eval mode until then (same mechanism as eval/run_gate.py).

Question: did r/wallstreetbets transition from the only wall-free state
ever observed in this program (fold A, seg z = -0.2, exactly chance) to
walled (fold B, z = -8.7), WHEN did it happen, and does the timing
discriminate between candidate mechanisms?

Source observation: paper 1 Sec 6.3, gate table commit 1386fc0, reported
there as measured with no interpretation (exploratory split, frozen rule).
Paper 1 is FINAL on that observation; this study cites it and does not
reopen it. Seed context: reports/paper2_seed.md.

## Blindness statement (honest scope)

The fold-level WSB endpoints (z = -0.2 in 2019, z = -8.7 in 2024) are
KNOWN — they motivate the study and cannot be un-seen. What is registered
here as pre-outcome is everything BETWEEN and AROUND those endpoints: no
rolling-window statistic, no rebuilt-fold cell, and no per-window census
has been computed at draft time, and none will be until registration.
The predictions below therefore bet on the SHAPE and TIMING of the
transition, not on its existence at the endpoints.

## Corpus (acquisition in flight at draft time; outcome-blind)

- Single source (Arctic Shift API), single pull era (2026-08-31 fleet,
  pipeline/pull_reddit_paper2.py + fleet_collector_paper2.sh), landing in
  data/paper2/pull — never mixed with the reddit_gate corpus.
- wallstreetbets 2019-01..2024-12 monthly shards (72), plus the five DD
  control subs (SecurityAnalysis, ValueInvesting, StockMarket, stocks,
  investing) over the same 72 months — uniform fields and pull era for
  treatment and control.
- FIELDS include `score` (owner gate decision 1, 2026-08-31). Score is
  collected for the engagement-stratification mechanism follow-up; NO
  score-dependent readout is registered in this document, and any later
  score analysis is a separate registration.
- 2020-2021 are deliberately INCLUDED (owner gate decision 2): the
  transition is the object of study; the fold-straddling exclusion rule
  from the gate does not apply to a continuous-time design.
- Hygiene as everywhere: deleted/removed authors and AutoModerator
  dropped; dedup by item id; extractor = pipeline/extract_tickers.py
  (frozen unit definitions: union lens primary, cashtag sensitivity,
  committed stoplist, SEC resolution, SPY/QQQ/VIX excluded, hub guard
  HUB_MAX = 50).

### Outcome-blind acquisition checks (appended before any statistic)
- validate_month span/parse/floor checks on every shard.
- Per-month row counts vs neighbours and vs the runbook §0 volume table;
  a month at 0 or ~5% of neighbours is a failure to fix, not data.
- The completed per-month volume table is committed as an amendment to
  this file BEFORE any window census is computed.

## Part A — provenance-hardening of the fold-B endpoint (confirmatory)

Rebuild the gate's fold B with the Pushshift-era dump months
(2022-01..2023-03) replaced by the API months from this pull, giving
uniform API provenance in BOTH folds, then recompute the WSB-dependent
gate cells (MEME and ALL, fold B) under the FROZEN gate criterion:
per-pair label-shuffle p99, R = 100, numpy default_rng seed 20260831,
formation floor >= 2 docs / >= 2 authors, segregation z per run 8 —
reusing eval/run_gate.py, which imports run_eval8.binom_sf_ge, so the
statistic is identical by construction. Fold definitions unchanged
(build 2022-01-01..2023-12-31, eval 2024).

- Registered expectation: fold-B MEME segregation z stays <= -3
  (transition endpoint is real, not a provenance artifact). Prior
  evidence this is low-risk: measured API/dump agreement 0.9996 with
  API-only = 0 (preregistration_gate.md A1').
- If z retreats to |z| < 3 under uniform provenance: the paper-1 split
  is provenance-limited; Part B proceeds but the paper's framing changes
  from "when did the walls go up" to "the transition claim does not
  survive provenance hardening" — reported as measured either way.
- Part A removes confound 2 (provenance) ONLY. It says nothing about
  timing.

## Part B — the transition study (primary)

### Design
- Document = (author, calendar quarter), as everywhere in this program.
- Rolling windows stepped ONE QUARTER: window w_k has build = quarters
  [k, k+B) and eval = the 2 quarters [k+B, k+B+2), over the 24 quarters
  2019Q1..2024Q4. Eval length is FIXED at 2 quarters.
- Build length B is chosen OUTCOME-BLIND from {4, 6, 8} quarters by the
  registered ladder: the shortest B whose per-window census (below)
  gives a MEDIAN eligible-pair count >= 100 in the WSB/union cell.
  Shorter localizes the transition better; the ladder exists so the
  choice is a census property, not a researcher degree of freedom.
- Eligibility per window, identical to the gate: frequency floor F >= 20
  distinct build-window author-docs per ticker; eligible ("suppressed")
  pair = E_build = f_i * f_j / N_docs >= 2 AND zero observed build
  co-mentions.
- PRIMARY statistic per window: the run-8 segregation z — total observed
  eval co-mention doc count over eligible suppressed pairs vs the
  label-shuffle null total (R = 100, numpy default_rng seed 20260831,
  concept column permuted over (doc, ticker) incidences restricted to
  the frequent set, within-doc duplicates collapsed), machinery imported
  from run_eval8 — identical to the gate by construction.
- Formation counts per window: SECONDARY, reported, no bar attached
  (known underpowered at these window sizes; gate power table).
- SENSITIVITY (registered 2026-08-31, pre-census): after the primary z
  series is computed at the ladder-chosen B, the full z series is ALSO
  computed at the other two B values and plotted alongside. No bars
  attach to the sensitivity curves; they are computed and reported
  regardless of outcome, so the window-length choice cannot be what
  makes the transition appear.
- SECONDARY onset estimate (registered 2026-08-31, pre-census): a
  one-break step fit on the primary z series over non-LOW-POWER
  windows — for every interior candidate break location, fit the
  two-segment piecewise-constant model by least squares; the point
  estimate is the SSE-minimizing break; reported with the set of
  candidate breaks whose SSE is within 10% of the minimum, as a range.
  Purpose: an uncertainty band on the onset date for the mechanism
  discussion (fast scale-driven vs lagging governance-driven). No bar
  attached; P1/P2 are scored ONLY by the primary threshold rule.
- Strata: WSB (treatment) and DD-union-of-5-subs (control), computed
  identically and independently. Lens: union primary, cashtag
  sensitivity (if cashtag yields < 20 eligible pairs in a window it is
  reported UNINFORMATIVE for that window, never as a negative).

### Outcome-blind census gate (hard ordering)
The per-window eligible-pair and document counts for every window, both
strata, both lenses, plus the B-ladder decision, are computed WITHOUT
evaluating any eval-window statistic, committed as a dated amendment to
this file, and reviewed by the owner BEFORE the first segregation z is
computed. Windows whose eligible-pair count is < 30 (WSB/union) are
marked LOW-POWER in that amendment, in advance, and are plotted but
excluded from the onset rule below.

### Registered predictions
Onset definition (frozen): the ONSET WINDOW is the earliest window w
with z_w <= -3 such that every later window also has z <= -3, allowing
at most one later exception; the ONSET TIME is the start of w's eval
interval. If no such window exists, there is no onset (P1 fails).

- **P1 (existence of a transition):** at least 2 consecutive non-LOW-
  POWER windows with |z| < 3 occur BEFORE the onset window, and at least
  2 consecutive windows with z <= -5 occur at or after it. Both halves
  required; the endpoints (2019 at chance, 2024 walled) make P1 the
  registered bet that the transition is VISIBLE and LOCALIZABLE at
  quarterly resolution rather than an artifact of the fold endpoints.
- **P2 (timing):** the onset time lies within [2021-01-01, 2021-12-31].
  The GME event is 2021-01; moderation and structural changes followed
  through 2021. No sharper timing claim is registered, because no
  sharper claim has a pre-named source yet (see causal anchors).
- **P3 (control specificity):** the DD/union z series contains NO window
  pair (w, w+1), both non-LOW-POWER, with z_w > -3 and z_{w+1} <= -5,
  anywhere in eval range 2020-01..2022-12. DD's deepening (fold A -10.0
  to fold B -16.3) is predicted GRADUAL; a comparable DD discontinuity
  would indicate an era-wide narrative effect rather than a
  WSB-specific structural change.

PRIMARY CELL, named explicitly for every bar (clarified 2026-08-31 on
peer-review advice, pre-outcome; this was always the intent of "union
primary" above): P1 and P2 are scored on the WSB stratum, union lens, at
the ladder-chosen primary B (= 4 quarters per Amendment V3). P3 is
scored on the DD stratum, union lens, same B. No other cell scores any
bar; every other cell (cashtag, B=6, B=8) is sensitivity or descriptive.

DETERMINISM RULE for the eval implementation (binding, from the gate's
adversarial review finding 1.2): no set or dict iteration may feed the
seeded RNG or any order-sensitive accumulation — every incidence list is
sorted before permutation. The paper-2 eval script must reuse run_gate's
fixed pair_counts/shuffle machinery or replicate its sorted() discipline
verbatim, and this is checked in review before the first run.

Scoring: P1+P2+P3 all pass = the transition claim as designed. P1 pass
with P2 fail = a transition exists but the GME-era timing story is
wrong; report the measured onset, no stretch. P1 fail = the endpoints do
not resolve into a localizable transition at this resolution; report the
full z series as measured. P3 fail = era confound cannot be excluded;
the paper reports the WSB series WITH the DD discontinuity alongside and
claims no community-specific mechanism.

### Causal anchors (collect BEFORE any window is computed)
Dated WSB governance events — moderation-rule changes, daily-thread
containment, flair policy — from the subreddit wiki, mod announcements,
and contemporaneous coverage, collected and committed as an amendment
BEFORE the first z is computed. These are the causal-ordering anchors
for the mechanism discussion. Any post-hoc timing comparison against an
anchor not in that committed list is labelled exploratory.

### Mechanism discrimination (discussion-level, not additional bars)
- Scale/fragmentation predicts onset fast, tracking the ~30x subscriber
  explosion (2021 Q1).
- Governance predicts onset lagging the event by months (rule changes
  through 2021).
- Era narratives predict a parallel DD discontinuity — P3 is its test.
- The cascade-susceptibility framing stays OUT of the registration and
  appears only in the discussion, marked speculative.

### Confound statement (plain, as the seed requires)
The era confound (2020-21 macro regime, COVID, zero-commission influx)
is NOT removable observationally. The design's answer is (a) a
within-community comparison across continuous time under uniform
provenance — no fold boundary, no source seam co-located with the
phenomenon — and (b) the DD-as-control contrast (P3). A P1+P2+P3 pass
supports "WSB-specific structural transition in 2021" and cannot by
itself separate the candidate mechanisms; that separation is the job of
the causal anchors and is reported as ordering evidence, not causal
identification.

## House rules binding this study
1. Registration committed and owner-reviewed BEFORE any outcome
   computation; density/coverage checks are outcome-blind amendments.
2. The z >= 2 Poisson criterion is RETIRED; only the label-shuffle
   machinery (run_eval8) is valid.
3. Long stages log to files, never pipes. Every git command anchored
   with -C. Data stays out of git.
4. Push after committing; never rebase/rewrite.
5. Paper 1 is final; cite, don't reopen.

## Freeze checklist (all must be true before eval)
- [x] Acquisition complete; validate_month + volume table amendment
      committed. (Amendment V1, 2026-08-31.)
- [x] Causal-anchor list amendment committed. (Amendment V2, 2026-08-31:
      reports/paper2_anchors.md — 8 dated governance events A1-A8 with
      sources and the frozen mechanism-discrimination reading; A8's
      introduction date is flagged as unpinned and unusable for timing
      claims until separately dated.)
- [x] Per-window census + B-ladder decision amendment committed
      (Amendment V3 below, 2026-08-31); owner review pending.
- [ ] STATUS flipped to REGISTERED by the owner's explicit go, committed.

---

## AMENDMENT V1 — acquisition complete, outcome-blind integrity + volume
## table (2026-08-31, appended before any census or statistic)

Acquisition completed 2026-08-31 07:10 local: 77/77 shards home in ~4.1h
wall, teardown verified (0 instances by tag, collector + independent API
check). 864 files (72 WSB months + 5 DD subs x 72 months, comments and
posts), 98,084,631 rows total, ~5.6GB gz.

Integrity pass (pipeline/validate_paper2.py, full parse of every row):
PASS with zero failures — no missing shard, no unparseable line, no
month with >1% out-of-span timestamps, `score` present on every row, no
zero or <5%-of-neighbour month. Full per-shard table:
reports/paper2_volume_table.tsv (kind, sub, month, rows, distinct
authors, out-of-span count, missing-score count). One transient during
acquisition: a single dropped rsync (wsb-2024-04, 05:52), self-healed on
the next sweep with byte-identical sizes; no data implication.

Cross-validation against the runbook §0 spot values (from the prior
acquisition era): 2022-06 = 1.13M, 2023-09 = 510K, 2024-03 = 962K — all
match this pull exactly.

WSB comments per month (thousands):

| year | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | total |
|------|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|------:|
| 2019 | 250 | 179 | 213 | 331 | 285 | 262 | 260 | 398 | 299 | 356 | 325 | 258 | 3.4M |
| 2020 | 512 | 1041 | 2604 | 1914 | 1546 | 1817 | 1508 | 1350 | 1408 | 1196 | 1521 | 1756 | 18.2M |
| 2021 | 8047 | 6681 | 4183 | 1682 | 1364 | 2184 | 1099 | 1010 | 1005 | 922 | 1052 | 1003 | 30.2M |
| 2022 | 1367 | 1158 | 1125 | 1093 | 1265 | 1131 | 1084 | 1717 | 1200 | 1161 | 1002 | 921 | 14.2M |
| 2023 | 902 | 808 | 940 | 625 | 657 | 639 | 600 | 632 | 510 | 577 | 528 | 542 | 8.0M |
| 2024 | 667 | 901 | 961 | 815 | 788 | 665 | 698 | 870 | 551 | 598 | 658 | 659 | 8.8M |

DD comments per sub-year (thousands, 2019..2024):
stocks 205/1129/1844/1443/693/646; investing 579/1110/830/510/413/486;
StockMarket 80/222/491/366/233/196; ValueInvesting 2/12/106/132/109/228;
SecurityAnalysis 21/32/12/3/2/1.

Outcome-blind observations recorded now, before any census:
- The WSB volume regime break is visible in raw volume (2020-03 COVID
  spike 2.6M; 2021-01 GME 8.0M). Volume is NOT the studied statistic;
  the shuffle null conditions on realized documents, and the density
  check (per-window eligible-pair census) remains the registered gate
  before any z.
- SecurityAnalysis decays to ~1-2K comments/yr by 2023-24; the DD
  control is registered as the UNION of the five subs, so this changes
  nothing, but per-sub sparsity is noted here before anyone sees a
  result it could explain.

---

## AMENDMENT V3 — per-window census + B-ladder decision (2026-08-31,
## outcome-blind: eligibility structure only, no eval statistic computed)

Extraction: 98,084,631 items -> 11,200,484 mentions (frozen unit rules
imported from the gate extractor; zero resume-duplicates). Census:
eval/census_paper2.py (imports build_docs/E_MIN/F from run_gate.py;
structurally cannot compute the statistic). Full table for all three B
values, both strata, both lenses: reports/paper2_window_census.tsv.

### B-ladder decision (registered rule applied mechanically)
| B | windows | median eligible (WSB/union) | min | max | LOW-POWER (<30) |
|---|--------:|---------------------------:|----:|----:|----------------:|
| 4q | 19 | **116** | 46 | 501 | 0 |
| 6q | 17 | 275 | 96 | 702 | 0 |
| 8q | 15 | 628 | 214 | 844 | 0 |

**PRIMARY B = 4 quarters** — the shortest rung meets the median >= 100
bar. B=6 and B=8 become the registered sensitivity curves. NO window in
any B is LOW-POWER (< 30 eligible pairs), in either stratum, union lens:
every window enters the onset rule. Cashtag lens: several early windows
sit below 20 eligible pairs and will be reported UNINFORMATIVE per the
frozen rule.

### Consistency anchor (outcome-blind)
The first B=4 window (build 2019, eval 2020Q1-Q2) reproduces the gate's
fold-A WSB structure on the new corpus: 44,304 build docs (gate fold-A
MEME census: 44,304 eval docs over the same 2019 year, same construction)
— the two independently-pulled corpora agree exactly on shared ground.

### Registered observation on the census shape (before any z)
Eligible-pair counts co-move with era volume (46-78 pre-2021 windows,
~500 GME-era, ~100 by 2023-24). The shuffle null conditions on realized
documents per window, so per-window z values are each internally
calibrated; but between-window comparability rests on the null's
conditioning, and windows differ up to ~10x in build docs. The onset
rule (threshold crossings) uses only per-window calibration and is
unaffected; readers comparing raw z magnitudes ACROSS windows are
comparing different-powered tests — the paper must plot eligible-pair
counts under the z series. Recorded before any z exists.

### Sequencing note
2020Q4-2021Q1 eval windows straddle the GME event itself; the census
shows their eligibility structure is intact (125/316 pairs). No window
is excluded for era reasons — per gate decision 2, the transition is
the object.
