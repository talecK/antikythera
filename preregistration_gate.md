# Variant gate registration — Reddit finance discourse (2026-08-30)

## STATUS: REGISTERED (2026-08-30) — design frozen; fold-A census recorded
## outcome-blind at commit f27680f; fold-B census appended when acquisition
## completes.

### INTERIM RUN CLAUSE (added 2026-08-30, before any gate outcome computed)
Fold A acquisition is COMPLETE (API-sourced, 14.6M items) and its census is
already committed. Fold B is ~40% acquired. Fold A is therefore evaluated
NOW as a declared INTERIM, under the frozen design and the amended
(run-8) criterion; fold B is evaluated when acquisition completes.
- The registered conclusions require BOTH folds. No fold-A-only result may
  be reported as meeting or failing a registered bar; it is an interim
  observation and must be labelled as such wherever it appears, including
  in Paper 1 Sec 6.3.
- Seeing fold A before fold B runs cannot change the design: every bar,
  the criterion, the power table and the unit rules are frozen above and
  committed. No parameter may be altered after this point; any change
  would constitute a new registration reported alongside this one.
- The gate harness (eval/run_gate.py) was ported to the run-8 criterion
  BEFORE this run (it previously implemented the retired z>=2 rule) and
  IMPORTS run_eval8.binom_sf_ge so the HN and Reddit statistics are
  identical by construction.
(`eval/run_gate.py` refuses to run in eval mode until this line reads
"STATUS: REGISTERED".)

Question the gate answers (RESCOPED 2026-08-30, post-run-8): primarily,
does below-chance SEGREGATION replicate on a second platform and unit
type (Q1b); secondarily, does financial discourse show any above-chance
calibrated formation where HN shows none (Q1). Original framing follows.
Original: does financial discourse have the structure the
instrument needs? Specifically (Q1) do author-space suppressed ticker pairs
exist and form at a usable rate, and (Q2) does connection-seeking culture
close gaps faster than reactive culture — the first CONTROLLED test of the
mechanism story that runs 5/6 and Tier A built.

Calibration ladder RETIRED (2026-08-30, run 8): the z>=2 criterion behind
the 67% / ~20% / 0.6% rungs is anti-conservative under doc-size
heterogeneity (R1 placebo), and under the shuffle-calibrated criterion HN
shows NO above-chance formation in either space (run 8,
reports/pilot1_runs.md). The gate therefore asks an open question, not a
ladder placement: does financial discourse show above-chance calibrated
formation where HN shows none?

## Corpus and provenance (disclosed seams)
- Subreddits: DD stratum = SecurityAnalysis, ValueInvesting, StockMarket,
  stocks, investing. MEME stratum = wallstreetbets.
- Fold A data comes from the Arctic Shift API; fold B from the monthly
  Pushshift/Arctic-Shift dumps (torrent). Seam is ALIGNED WITH FOLDS, so it
  confounds A-vs-B comparisons but NOT the within-fold DD-vs-MEME test,
  which is the registered mechanism question.
- Dumps before 2023-04 are Pushshift collection, later months are Arctic
  Shift's own crawler; that seam sits inside fold B.
- Deleted/removed authors and AutoModerator are dropped; items appearing in
  both tracks are de-duplicated by item id.

## Units (frozen in pipeline/extract_tickers.py, committed 2026-08-30)
- PRIMARY LENS "union": $CASHTAG plus uppercase 2-5 letter bare symbols,
  both required to resolve in the SEC company_tickers table, bare symbols
  filtered by the committed STOPLIST (forum/finance jargon that is also a
  registered symbol: OP, IRS, DD, FCF, DRS, ATH, ...). Stoplist was built
  from an OUTCOME-BLIND audit of the top-100 bare hits on a 200K-item
  sample and is frozen as committed.
- SENSITIVITY LENS "cashtag": cashtags only (noise-free by construction).
  Outcome-blind smoke test shows this lens is ~10x sparser; if it yields no
  eligible pairs it is reported as UNINFORMATIVE, never as a negative.
- Index/vol ETFs (SPY, QQQ, VIX) are excluded as macro hubs, matching the
  run-6 finding that promiscuous nodes swamp suppressed-pair sets.
- Known bias: the SEC table lists CURRENT registrants, so symbols delisted
  before the snapshot are invisible (survivorship). This shrinks the
  universe; it does not bias whether an observed suppressed pair forms.

## Formulation (identical to registered runs 5/6, units swapped)
- Document = (author, calendar quarter); hub guard drops author-quarters
  with > 50 distinct tickers.
- Frequency floor F >= 20 distinct build-window author-docs per ticker
  (fallback F >= 10 ONLY if the outcome-blind census yields < 200 eligible
  pairs in a stratum; the choice is recorded below before eval).
- Eligible ("suppressed") pair: E_build = f_i * f_j / N_docs >= 2 AND zero
  observed build co-mentions.
- Formation (AMENDED 2026-08-30 per the outcome-blind procedure registered
  in preregistration_run8.md; the z>=2 criterion is retired after failing
  the R1 placebo): a pair FORMS iff its observed eval co-mention doc count
  STRICTLY exceeds its per-pair label-shuffle p99 (R = 100 eval-window
  shuffles, numpy default_rng seed 20260831, concept column permuted over
  (doc, ticker) incidences restricted to the frequent set, within-doc
  duplicates collapsed) AND >= 2 eval author-docs AND >= 2 distinct
  authors. Per-pair false-positive rate ~1% by construction.

## Folds
- A: build 2017-01-01..2018-12-31, eval 2019 (pre-GME, pre-COVID).
- B: build 2022-01-01..2023-12-31, eval 2024 (post-GME regime).
- 2020-2021 excluded entirely: COVID + GME are regime breaks, and the
  project's own lesson is that folds must not straddle them.

## Registered readouts
1. **Q1 HEADLINE (bars AMENDED 2026-08-30 per preregistration_run8.md,
   outcome-blind)** — calibrated formed count among suppressed pairs, ALL
   stratum, union lens, both folds, vs the false-positive floor
   Binomial(n_eligible, 0.01), one-sided exact test.
   - p < 0.01 in BOTH folds: financial discourse shows above-chance gap
     formation where HN (run 8) shows none; the variant graduates to a
     funded registered run.
   - Not significant in BOTH folds: no above-chance formation anywhere
     tested; the variant is DEAD and the project closes on a clean
     negative across two platforms and three unit types.
   - Mixed: indeterminate; report, no interpretation stretch.
   Also reported: the sub-chance persistence readout — now PROMOTED to
   co-primary, see Q1b.

1a. **REGISTERED POWER (added 2026-08-30, outcome-blind; binomial exact,
   alpha = 0.01, floor p0 = 0.01, fold-A census counts).** Formed pairs
   needed for significance, and the smallest TRUE formation rate the gate
   can detect (power 80% / 50%):

   | cell | n eligible | k needed | MDR@80% | MDR@50% |
   |------|-----------:|---------:|--------:|--------:|
   | ALL / union   | 169 | 6 | 3.7% | 2.4% |
   | DD / union    | 144 | 6 | 4.5% | 3.0% |
   | MEME / union  |  62 | 4 | 7.8% | 4.9% |
   | ALL / cashtag |  54 | 4 | 9.0% | 5.8% |

   CONSEQUENCE, registered in advance: a non-significant Q1 licenses only
   "no LARGE effect (>~4%) in this corpus", NEVER "no effect". Any writeup
   of a null must quote the MDR alongside it. Fold-B numbers are appended
   when acquisition completes; if fold B's eligible count differs
   materially, its own MDR is computed and reported the same way.

1b. **Q1b SEGREGATION (CO-PRIMARY, promoted 2026-08-30)** — total observed
   co-mention over eligible suppressed pairs vs the shuffle-null total,
   as z, per fold and per stratum (the run-8 statistic, same null).
   Rationale for promotion: this is the surviving, strongly-powered
   finding of run 8 (author z = -9.2/-9.3, thread z = -162/-124), it is a
   directional test rather than a rare-event count, and it is adequately
   powered at the fold-A census sizes where Q1 is not. Reddit is a
   structurally independent corpus (self-indexing units, financial
   vocabulary, different community), so this is the strongest available
   replication test.
   - z <= -3 in both folds: below-chance segregation REPLICATES on a
     second platform and unit type; the finding generalises beyond HN.
   - |z| < 3 in both folds: segregation is HN-specific; run 8's result
     does not generalise, and the paper's claim narrows accordingly.
   - Mixed / positive z: report as measured, no interpretation stretch.
2. **Q2 MECHANISM (the controlled test)** — DD vs MEME calibrated
   formation within each fold. Registered prediction: DD > MEME.
   - Reported twice: raw, and with MEME author-quarters randomly
     subsampled (seed 20260830) to match the DD document count, because
     document count enters eligibility and the shuffle null.
   - UNDERPOWERED BY CONSTRUCTION (registered 2026-08-30): at the fold-A
     census, DD needs 6 formed pairs and MEME 4 to clear the floor at all,
     and both cells are expected to sit at 1-2 under the null. Q2 is
     therefore DEMOTED to descriptive: it can only report a large
     asymmetry, and "DD ~= MEME" here is NOT evidence that culture does
     not matter. The mechanism claim I attached to this comparison
     (a "controlled test") is withdrawn; the segregation readout (Q1b)
     compared across strata is the better-powered version of the same
     question and is reported alongside.
   - DD > MEME in both folds (non-overlapping CIs in at least one):
     mechanism story survives its first controlled test.
   - DD ~= MEME (or both at floor): connection-seeking culture confers no
     above-chance bridging — consistent with run 8's HN closure; reported
     as such.
   - MEME > DD: whatever forms is hype propagation, not insight;
     redirects the design, does not kill it.
3. **Q3 SCOUT (secondary, per the run-7 scope correction)** — run-7's
   split-half persistence test on ticker bridges, ALL stratum. Reported
   with the same overdispersion diagnostic; no pass/fail bar attached.
4. **Q4 HYGIENE** — duplicate/copypasta rate by stratum; WSB pre-2021
   (fold A) vs post-2021 (fold B) as a within-community mechanism-shift
   observation.

## Out of scope for the gate (belongs to the variant proper, if it opens)
- Any price or return analysis. The gate tests discourse structure only.
- Cross-validation against analyst co-coverage / EDGAR co-search peers
  (Ali-Hirshleifer 2020; Lee-Ma-Wang 2015) as economic ground truth — a
  designed follow-up, not part of this decision.

## Census (outcome-blind, appended before eval)

### Fold A — COMPLETE (2026-08-30; API-sourced, 14.6M items)
| stratum | lens | build docs | eval docs | tickers | co-pairs | SUPPRESSED |
|---------|------|-----------:|----------:|--------:|---------:|-----------:|
| ALL  | union   | 99,321 | 68,606 | 1,187 | 202,268 | **169** |
| ALL  | cashtag | 23,717 | 14,206 |   347 |  21,781 |  54 |
| DD   | union   | 56,147 | 29,070 |   849 | 100,493 | 144 |
| DD   | cashtag |  8,815 |  2,816 |   164 |   5,966 |  22 |
| MEME | union   | 52,373 | 44,304 |   735 | 103,089 |  62 |
| MEME | cashtag | 16,374 | 11,942 |   239 |  12,437 |  32 |

### F decision: PRIMARY F = 20 STANDS; the F>=10 fallback is NOT invoked.
Outcome-blind sweep on the complete fold A (suppressed pairs, ALL/union):
F=20 -> 169, F=15 -> 184, F=10 -> 187, F=5 -> 187. Relaxing F saturates
because added tickers are rarer and fail E >= 2. The fallback existed to
rescue an under-powered census; since it cannot add pairs, invoking it
would only admit marginal tickers. Recorded before any outcome was computed.

### Structural reading (outcome-blind, recorded pre-eval)
The ticker graph is DENSE: ~169 suppressed pairs against 202,268 observed
co-mention pairs among frequent tickers. Structurally this matches
Science4Cast (281 per 10M sampled) and HN author-space (364/110) — the
"rare" half of rare-but-hot — and is the opposite of HN thread-space
(25,161 plentiful-but-inert). Whether these pairs are HOT is precisely the
eval. Cashtag lens is thin but NOT empty (54/22/32), so it is a usable
sensitivity check rather than the pre-declared UNINFORMATIVE case.

### Fold B — PARTIAL at census time (dump loop ~20/36 months); numbers
appended when acquisition completes. Eval-2024 months were not yet
downloaded when this table was produced (MEME fold-B eval docs read 0),
so no fold-B number here is final and none was interpreted.

---

## DATED AMENDMENT — 2026-08-30 evening, provenance and missing months
## Committed BEFORE any WSB-dependent outcome is computed. Amends by
## addition; nothing above is reworded or deleted.

### A1. The provenance seam is no longer fold-aligned — correction
The "Corpus and provenance" section states the API/dump seam is ALIGNED
WITH FOLDS and therefore does not touch the within-fold DD-vs-MEME
comparison. That is now FALSE and is corrected here rather than rewritten
above. Cause: the monthly-dumps torrent (~16 seeders, 3.8TB archive) does
not hold every file — RC_2023-04 arrives as 27GB of zeros with zero swarm
growth over a measured 60s while adjacent months download normally. Months
the swarm cannot serve must be filled from the API, so within fold B the
DD stratum is API-sourced while the MEME stratum becomes mixed. The seam
now lies BETWEEN STRATA, i.e. exactly on the registered DD-vs-MEME
comparison and on the exploratory split.

The comparison's validity therefore rests on MEASURED SOURCE EQUIVALENCE
rather than on design alignment:
- `pipeline/provenance_check.py`, WSB 2023-03-14..17, both sources:
  API 99.94% of union, dump 100.00%, ratio API/DUMP = 0.9994
  (~70 of 113,705 ids differ). No material coverage or density difference,
  hence no document-size heterogeneity of the kind that produced the R1
  artifact.
- Supporting, and independent of sourcing: fold A produced the stratum
  split under UNIFORM provenance (both strata API), so the split's
  existence does not depend on fold-B sourcing at all.

### A2. MANDATORY PRECONDITION before any WSB-dependent cell is computed
The equivalence above was measured in the BUILD window. Formation and the
segregation z are evaluated in 2024, so the check MUST be repeated on at
least one overlap window inside the EVAL year, with both sources holding
that window, and the result recorded here. If eval-year equivalence is not
materially the same (ratio within 0.99-1.01), the mixed-provenance MEME
cells are reported as provenance-limited and interpreted accordingly.

### A3. Missing-month handling rule — fixed NOW, outcome-blind
Cells are computed on available months; every missing month is NAMED in
the results; the registered bars apply UNCHANGED. The shuffle-calibrated
criterion conditions on realized documents (the null inherits any density
step), so a hole is statistically tolerable. Choosing between reporting
and withholding AFTER seeing which way a cell fell is not permitted, which
is why this rule is committed before the outcome exists. Fallback: only if
WSB eval-year data is MAJORITY-missing are the ALL/MEME fold-B cells
withheld, leaving DD-only fold B (final, unaffected) as the fold-B result.

### A4. Gap-fill source: API only
Unavailable months are filled from the Arctic Shift API, not from the
per-month torrents that exist for 2024-04+. Reason: archive months up to
2024-03 were "reformatted and updated with additional data sources"
relative to the standalone per-month releases, so using both would create
THREE provenance classes inside one eval window with no pairwise
equivalence measurement. The API path gives exactly two classes with the
measured 0.9994 equivalence above. Per-month torrents are used only if the
API path fails, and any such use is disclosed with its own check.

### A5. Unavailable months (live list)
Recorded in `data/reddit_gate/unavailable_months.txt` as the loop
encounters them; reproduced in the results section at completion.
Known at amendment time: 2023-04.
