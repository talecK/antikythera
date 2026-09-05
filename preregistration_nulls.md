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

---

## Amendment A1 — reproduction audit and pooled thread rerun

STATUS: REGISTERED, 2026-09-04 Pacific (2026-09-05 UTC), before the
new runs below. The owner delegated execution of the revision after
discussing these choices with Codex. This appendix supersedes the
conflicting reproduction and reporting clauses above; the original text
and predictions remain in the record. No N1 or R=1000 outcome has been
examined by the takeover session at this point.

### Known results and limits of verification

The owner reports an M3 reproduction of all 204 Paper 2 cells: counts,
null means, standard deviations, z and formation counts agree exactly;
66 binomial probabilities differ by at most 6.4e-13 relatively between
arm64 and x86_64 libm. Paper 1 author space reproduces; thread-space
shuffle realizations differ because a DuckDB join supplies unpinned
document order. These are reported results, not independently inspected
M3 logs. Code inspection confirms that run_eval8.run_space sorts labels
but not documents. The frozen script and its published outputs remain
unchanged. The earlier hash-seed check did not establish query-order
determinism. The replacement thread estimates are new Monte Carlo
estimates under the same label-shuffle distribution, not recovered
copies of the original random stream.

### Numerical comparison and local gate

Integer counts must agree exactly when replaying identical draws.
Same-environment floating results are checked exactly; cross-platform
means, standard deviations and z may differ by
abs(new-reference) <= 1e-12 + 1e-10*abs(reference). Positive representable
binomial probabilities may differ relatively by at most 1e-9, with no
absolute probability tolerance. Underflowed probabilities cannot certify
tail agreement; a stable log-probability comparison is needed if such a
case occurs. Registered decisions must agree exactly, even when numeric
tolerances pass. This engineering tolerance is chosen after observing
the reported platform discrepancy and is not claimed to be prospective
to that audit.

Before N1, locally replay the already reported Paper 2 cells WSB k=0,1
and DD k=0 at B=4, union, R=100 without drift diagnostics, to a new file;
compare against the archived TSV. Check Paper 1 observed counts and
eligible counts against the archived JSONs in the corrected runner.
The impossible exact-thread-stream requirement in runbook step 1 is
replaced by these structural checks and the seeded rerun below. The
full M3 replay remains owner-reported until its artifacts are recovered.
Record environment, code commit, seeds, commands and reference hashes.

### Thread estimates and diagnostics

For each thread fold, generate 10 independent batches of 100 label
shuffles, with seed default_rng([20260831, cell_index, batch_index]),
cell_index=2 for fold1 and 3 for fold2, batch_index=0,...,9. Sort document
IDs, labels and the eligible-pair output ordering. Pool all 1000
per-pair replicate counts for the primary null mean, population standard
deviation (ddof=0, retained for comparability), z, observed/null ratio,
per-pair 99th percentile and formation count. Do not average batch z or
batch ratios to produce the primary estimate. Retain all batch summaries
and integer replicate arrays. Batch ranges describe Monte Carlo
variability, not confidence intervals or uncertainty across populations.
The 1000-draw percentile estimate is a precision extension of the
100-draw procedure; its formation count need not equal the old count.

New predictions, motivated by already observed large negative values:
T-a: every batch z < -100 in both thread folds. T-b: each batch formed
count <= 0.01 times its eligible count (a nominal reference, not an exact
false-positive expectation). T-c: (max batch ratio - min batch ratio)
/ pooled ratio <= 0.05 in each fold. Report each separately, regardless
of outcome. The original P1-b comparison still uses the separately
registered seed [20260831, cell_index] at R=100, not these batches.

### Execution and interpretation clarifications

The N1 full-series run means the 38 B=4 union cells only, as specified
under Cells above. The command previously selected all 204 cells; correct
its selection before execution without changing the sampler. R=1000
headline runs include drift on the first 10 replicates for both nulls.

The structural direction of collapse is fewer binary incidences than
shuffled slots. This alone does not prove a universal direction of error
relative to a uniform fixed-binary-margin ensemble for each eligible
pair, aggregate or z. Rule 4's blanket conservatism claim is withdrawn;
the direction relative to N2 will be measured. The N2 requirement stands.

Binomial probabilities of formed counts are legacy descriptive outputs:
pair events are dependent and their nominal reference is not an exact
binomial model. Likewise +1 Monte Carlo tail summaries of the collapsed
label null do not establish exchangeability of the observed binary
matrix with draws from a different sample space. They are reported as
simulation tail summaries, without claiming an exact calibrated test.
Ordinary correlated Curveball output will not inherit an exact
independent-permutation p-value guarantee.

Passing eight N2 headline cells will establish robustness only for those
cells. Claims about N2 onset and persistence require the 38 primary
cells. A separate N2 protocol will specify a mixing pilot and the
quarter-stratified fixed-margin combination before those runs. New-null
results may change either paper's conclusions; the existing onset is
currently supported under the original null only. Public manuscript
updates remain on hold pending the required robustness results.

### A1 provenance note before N1 execution

Direct inspection of the published B=4 union table during the local gate
shows that N1-d's phrase "as under the registered null" is factually
incorrect. Outside the excursion, formed/n exceeds 0.01 in WSB windows
k=0,1,2,5,9,12,16,18 (for example 2/77 at k=1 and 6/498 at k=5).
N1-d remains unchanged and will be scored literally. A realized count
above 0.01*n is not by itself evidence against a calibrated 1% per-pair
test; that reference is not a deterministic upper bound. No new-null
outcome was inspected to identify this error.
