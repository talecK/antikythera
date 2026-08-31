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
- [ ] Acquisition complete; validate_month + volume table amendment
      committed.
- [ ] Causal-anchor list amendment committed.
- [ ] Per-window census + B-ladder decision amendment committed,
      owner-reviewed.
- [ ] STATUS flipped to REGISTERED by the owner's explicit go, committed.
