# Nulls amendment — response to the 2026-09-04 external critique (both papers)

## STATUS: REGISTERED (2026-09-04). Predictions below were written before
## any new-null statistic was computed on real data. The only real-data
## run before this commit was the registered null on three already
## published cells, to verify that the process pool reproduces the
## committed TSV rows (it did, byte for byte). That check also emitted
## the drift diagnostic for those three cells, because the diagnostic
## defaulted on for any non-registered output path. Those three values
## are disclosed below and the diagnostic prediction is withdrawn for
## them; the default has been changed so a reproduction check emits no
## diagnostic.

## What this amends

Paper 1 (run 8, preregistration_run8.md) and Paper 2
(preregistration_paper2.md) both use one permutation null: shuffle the
label column of the evaluation window's (document, label) incidence list
and rebuild documents as sets. Both drafts describe it as holding "every
document's size and every concept's frequency fixed". An external
reviewer (a model-generated review received 2026-09-04) pointed out that
the set rebuild collapses duplicate labels, so neither margin is held
exactly. The description is wrong; the algorithm is what was registered
and run. This amendment does not change the registered primary null for
the v1 claims. It adds, as registered robustness analyses:

- **D (diagnostic).** Margin drift of the registered null per cell:
  incidences before and after the set collapse, documents and labels
  whose margin changed. Reported as the mean over the first 10
  replicates of each cell.
- **N1 (stratified null).** Labels permuted only within the document's
  calendar quarter (Paper 2 documents are author-quarters; Paper 1
  author-space documents are author-quarters; Paper 1 thread-space
  documents take the quarter of the thread's first claim). This answers
  the reviewer's timing objection (labels popular in different quarters
  cannot be paired by the null). It has the same collapse property as
  the registered null; D is reported for it too.
- **Monte Carlo p-values** with the +1 correction (Phipson and Smyth
  2010) and observed/null ratios, alongside z, for every cell.
- **R = 1000** on the headline cells, registered null and N1.

A margin-preserving null (curveball or swap sampler, Strona et al. 2014;
Neal 2014) is named here as **N2** and deferred: it is required only if D
shows material collapse (rule below). Anything else the review asked for
(fixed pair panels, newcomer split, per-subreddit controls) is future
work and not part of this amendment.

## Code

- eval/nulls.py: the registered sampler moved verbatim (test: identical
  output to the inline code for a given generator state), the
  stratified sampler, the drift diagnostic, and the summaries.
- eval/run_paper2.py: --null, --R, --workers, --headline, --cells,
  --drift. The registered path (--null label, --R 100, all cells) writes
  the registered TSV with the registered columns and must reproduce it
  byte for byte in any worker count. Any other configuration refuses to
  run unless this file reads STATUS: REGISTERED, writes to a separate
  TSV, and adds the wide columns.
- eval/run_eval8_nulls.py: the four run-8 cells under per-cell seeds
  default_rng([20260831, cell_index]). run_eval8.py is untouched.
- tests/test_nulls.py: 7 tests, all passing at registration.
- Determinism clause carried over: incidence lists sorted by document
  then label before the generator sees them; strata visited in sorted
  order; one fresh generator per cell (Paper 2: seed 20260831 as
  registered; Paper 1: the per-cell seed above).

## Cells

- **Paper 2 full primary series under N1**, R = 100: B = 4, union, WSB
  and DD, 19 windows each (38 cells). The sensitivity B and cashtag cells
  are not rerun under N1.
- **Paper 2 headline cells**, registered null and N1, R = 1000, D on:
  WSB union B=4 windows k = 1, 2 (the two chance windows before the
  onset), 3, 4 (the excursion), 5 (the onset window), 18 (the last
  window); DD union B=4 windows k = 4, 5 (the control's step at eval
  2021Q2, see disclosure below).
- **Paper 1 four cells** (author fold1, fold2; thread fold1, fold2):
  N1 at R = 100 with D, and the registered sampler under per-cell seeds
  at R = 100 as a seeding check.

## Disclosure of what is already known

- All registered-null values in both papers are known.
- The DD control's observed/null ratio series was computed from the
  released Paper 2 TSV on 2026-09-04 while assessing the review: it
  steps from about 0.6 to 0.7 (eval windows 2020Q1 to 2021Q1) to about
  0.4 to 0.5 (2021Q2 onward), coincident with the WSB onset window. Its
  z series is not monotone (-8.1, -9.8, -8.9, -7.7, -8.6, -11.6, then
  -6.7 to -15.7). This is a pre-observed fact, not a prediction, and the
  v2 text must present it as such. It does not affect P3 as registered
  (DD never reached chance or excursion).
- No N1 statistic and no R = 1000 value has been computed on real data
  at registration.
- Drift values ARE known for three cells from the pool reproduction
  check (registered null, first 10 replicates): WSB B=4 k=0
  collapsed_frac 0.057 (7,756 of 78,060 documents changed size), WSB
  k=1 (a headline cell) 0.058, DD k=0 0.033. That is 3 to 6 percent of
  incidences collapsing, well above the 2 percent threshold this
  amendment was drafted with. Decision rule 4 below is therefore
  already triggered for the headline cells: N2 (curveball) is required
  before v2. D remains reported for every cell; the threshold prediction
  is withdrawn rather than reworded.

## Predictions (falsifiable; written before running)

Paper 2, N1 at R = 100 on the primary series:

- **N1-a.** Every primary cell with |z| >= 3 under the registered null
  keeps its sign under N1. Cells with |z| < 3 may land anywhere in
  (-3, 3).
- **N1-b.** The registered onset rule applied to the N1 series returns
  the same onset window (eval start 2021Q2), and P1, P2, P3 pass as
  registered.
- **N1-c.** Both excursion windows (eval start 2020Q4 and 2021Q1) have
  z >= +5 under N1.
- **N1-d.** Formation stays at or below the 1 percent floor in every
  primary cell except the two excursion windows, as under the
  registered null.

Headline cells, R = 1000:

- **R-a.** z under the registered null at R = 1000 lies within 20
  percent of its R = 100 value in every headline cell (the first 100
  replicates of the R = 1000 stream are the R = 100 stream, so this is
  a check on the null's tail, not on the seed).
- **R-b.** Monte Carlo two-sided p at R = 1000 is at its floor (2/1001)
  in every headline cell with |z| >= 5, and above 0.05 in the two chance
  windows.

Diagnostic D:

- **D-a.** Withdrawn before registration (see disclosure): three
  observed values already exceed the drafted 2 percent threshold. D is
  reported for every cell with no pass threshold.
- **D-b.** Directional prediction, still blind: collapsed_frac is
  larger in the excursion windows (k = 3, 4) than in the chance windows
  (k = 1, 2), because the excursion is when label frequencies are most
  skewed (a few tickers dominate) and collapse is driven by skew. Paper
  1 thread space (documents up to 100 concepts, hub concepts) has a
  larger collapsed_frac than Paper 1 author space.

Paper 1, N1:

- **P1-a.** All four segregation z remain <= -3 under N1 and formation
  stays at or below the floor in all four cells.
- **P1-b.** The per-cell-seeded registered sampler gives z within 20
  percent of the run-8 value in all four cells.

## Decision rules (fixed now)

1. The registered null remains the primary null for every v1 claim. v2
   reports N1 alongside it in every table where the registered null
   appears, with ratios and Monte Carlo p.
2. If N1-c fails but both excursion z are > +3, the excursion is
   reported as present but attenuated by timing, and the abstract says
   so. If either excursion z is <= +3 under N1, the excursion section is
   withdrawn from the claims and the abstract is rewritten around the
   onset alone.
3. If N1-b fails by one window in either direction, v2 states the onset
   as the range spanning the two windows. If it fails by more, the
   onset claim is withdrawn pending N2.
4. N2 (curveball) is required for the headline cells before v2 (the 2
   percent threshold is already exceeded, see disclosure), under a
   further amendment that fixes the chain length, thinning, and its
   own predictions. Until N2 runs, v2 text may report the registered
   null and N1 with the drift numbers stated, but must not describe
   either as margin-preserving. The direction of the collapse bias is
   stated in v2: collapse removes incidences, so null pair counts are
   deflated; negative z are conservative, positive z (the excursion)
   are anti-conservative.
5. Every prediction's outcome is reported in the run log whether it
   passes or fails. No prediction is reworded after the fact.

## Run order (the MBP runbook)

1. Reproduction gate: `run_paper2.py --workers N` (registered null, all
   cells) must leave reports/paper2_windows_z.tsv unchanged under git;
   `run_eval8.py` serially must reproduce the run-8 JSONs. Nothing
   below runs until both pass.
2. `run_paper2.py --null stratified --workers N` (full series).
3. `run_paper2.py --headline --R 1000 --workers 8` and
   `run_paper2.py --headline --null stratified --R 1000 --workers 8`.
4. `run_eval8_nulls.py --null stratified --workers 4` and
   `run_eval8_nulls.py --null label --workers 4`.
5. Append outcomes to reports/pilot1_runs.md against the predictions
   above.
6. Draft the N2 amendment (chain length, thinning, per-chain seeds,
   predictions) and run it on the headline cells; then the prose pass.
