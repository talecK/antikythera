# N2/N3 prospective pilot and production rule — 2026-09-04 Pacific

STATUS: REGISTERED. This protocol supersedes the historical draft below.
Registration is committed before any real-data Curveball chain, including
initialization and pilot outcomes. Original-null and completed M1 N1
results are known, including N1-d and D-b failures. MBP queue status is
user-reported; its results have not been inspected here. Predictions are
informed by those known results, not outcome-blind replications.

## Fixed scientific predictions and consequences

Each prediction is scored separately for N2 and N3 using production only:

- X-a: all 38 Paper 2 primary cells with original abs(z)>=3 retain sign.
- X-b: the unchanged full-series onset rule returns k=5 (2021Q2-Q3),
  with original P1, P2 and P3 all passing. This deliberately risks failure
  if the original two non-detection windows become negative under exact
  margins. Partial headline results cannot score this prediction.
- X-c: both WSB excursion cells k=3,4 have z>=5 and observed/null>1.
- X-d: all four Paper 1 cells have z<=-3 and observed/null<1.
- X-e: all four Paper 1 formed counts are <=0.01 times eligible counts.
  This is a literal count prediction, not a calibrated error-rate test.

No universal collapse-bias direction or Paper 2 1% count bound is predicted.
Failures remain failures. If either excursion has z<=3, withdraw the
claim of excursion robustness to that null; 3<z<5 is attenuated support
and fails X-c. If onset shifts by one window, report the spanning interval;
a larger shift or no onset withdraws exact-margin onset robustness. Failure
of X-d restricts segregation claims to the nulls/cells that support them.
Unresolved diagnostics are UNRESOLVED, never passes or scientific failures.
The original registrations and results remain primary historical records.

## Scope, seeds, starts and invariants

N2 and N3 target the uniform binary matrices described in the draft below.
Initial scope/order: Paper 2 WSB k=1,2,3,4,5,18; DD k=4,5; Paper 1 author
fold1,fold2 then thread fold1,fold2. Run both nulls for each cell. Extend
to the remaining 30 Paper 2 primary cells under both nulls regardless of
scientific signs, subject only to diagnostic/resource rules below.

Canonical cell IDs: p2_WSB_01 etc (two-digit k), p1_author_fold1 etc.
Label IDs follow sorted frequent labels; pairs are lexicographically sorted;
rows follow sorted document IDs and retain the frozen frequent-label set.
Zero rows are omitted from sampling but counted in the corpus census.
N3 blocks are sorted (year, zero-based quarter); N2 block key is 'all'.
Never recompute eligibility/support or discard additional hubs in samples.

Seed = unsigned little-endian first 8 bytes of SHA256 of UTF-8 string
'antikythera/n2n3/v1|PHASE|NULL|CELL|CHAIN|BLOCK'. PHASE is init-pilot,
pilot, init-production, or production; NULL is N2 or N3; CHAIN is 0..3;
BLOCK is 'all' or 'YYYYQn' with n=1..4. Independent logical seeds do not
change with workers, scheduling, diagnostics or restarts.

Four logical chains. Starts are valid matrices obtained from the observed
matrix with respectively 0,5,20,80 sweeps of the same Curveball kernel,
using the separate initialization namespace. A sweep is r attempted trades
(or r_q per quarter). Preserve self-loops. Export/recreate with the sampling
seed after initialization. These dispersed starts are NOT certified draws
from distant modes: report initial total counts and distance to observation,
and retain that limitation. Margin equality and native per-pair observed
counts against the frozen Python counters are mandatory before chains.
Verify row/column margins after initialization and after each stage; for N3
verify every block independently. Abort on any invariant failure.

## Pilot schedule and stopping rules

Save every sweep, including the initial transient. Candidate burn-in b is
5,10,20,40,80 sweeps. First collect 280 sweeps per chain, enough for 200
retained draws at every b. Evaluate every candidate in that fixed order
using ALL draws after b. Retain every diagnostic, including failed ones.
If none passes, extend the same chains to 480 then 880 sweeps (at least
400 then 800 post-b=80 samples); repeat the same candidate order.
Choose the first passing b at the first passing stage. No selective
thinning: production interval is one sweep. Pilot never enters production.

Required aggregate diagnostics: total eligible-pair document count and
binary-entry distance from the common observed matrix; rank-normalized
split R-hat (maximum of rank and folded) <1.01 and bulk ESS>=400 for both.
Total additionally needs 5%/95% tail ESS>=400, raw-mean MCSE<=0.05 null SD,
and SD MCSE<=0.05 null SD. SD MCSE uses the delta-method influence
((X-mean)^2), with autocorrelation ESS of that influence. These are
application precision choices, not theorems about Curveball mixing.
Diagnostic implementation must be cross-checked on independent reference
fixtures plus synthetic IID, sticky, shifted and scale-mismatched chains.

Report a deterministic panel of up to 16 pairs: equally spaced indices
including endpoints in the sorted eligible list (unique floor(linspace)).
Report panel rank/folded R-hat, bulk/tail ESS and raw count MCSE; panel
failures flag formation precision, not aggregate failure. Formation needs
additional production checks below. Average ranks handle ties. A sampled
constant gets undefined R-hat/ESS, not artificial perfect mixing. A required
constant diagnostic blocks passage unless fixedness is proved structurally;
if the aggregate is structurally fixed, report exact count/ratio and
undefined z instead of dividing by a tiny arbitrary SD.

Run at most two local workers, respecting the other project's load. Maximum
pilot per cell/null: 4*(105 + 880)*r attempts including starts (use sum r_q
for N3); stage checks stop a cell at two elapsed worker-hours, retaining
all artifacts and marking RESOURCE_LIMIT. Global new N2/N3 work is capped
at 72 summed worker-hours for this protocol. A stopped cell needs a new
prospective resource amendment to continue. Never relax diagnostics or
change scientific predictions to get a result. Run other cells as budget
permits. Report unresolved cells rather than extrapolating from eight.

## Production rule fixed before pilot

For a passing cell/null: fresh four starts and streams; burn-in is twice
the selected pilot b, then 400 saved sweeps per chain (1,600 pooled draws).
Recheck the same aggregate diagnostics on production. If they fail, extend
retained samples to 800 then 1,600 per chain; no changing burn-in or seeds.
Maximum production cell budget is two elapsed worker-hours. A failed final
stage is UNRESOLVED and its estimates are labeled provisional, not scored.
Report total mean, population SD (ddof=0), z, ratio, MCSEs, effective sample
sizes and per-chain summaries. Tail fractions are descriptive correlated
MCMC fractions without an exact permutation p-value claim.

For per-pair formation use NumPy linear 99th percentile on pooled integer
counts with frozen observed >=2 docs and >=2 authors support. Report full
pooled count and four leave-one-chain-out counts. For every supported pair
with observed>=2, diagnose I(null_count < observed): require rank/folded
R-hat<1.01 and indicator ESS>=400, plus its mean +/-2 MCSE wholly on one
side of 0.99 and matching the pooled percentile classification. Constants
remain unresolved unless fixed by binary column-count intersection bounds
(sum of per-block max(0,c_a+c_b-r) and min(c_a,c_b)) outside the observed
threshold. This is a marginal precision diagnostic, not simultaneous
coverage or a calibrated test. X-e is scorable only if all eligible-support
classification checks pass and leave-one-chain-out formed counts agree.
Otherwise preserve pooled count and flag formation UNRESOLVED; do not
extend solely because formation remains unresolved after aggregate passes.

## Provenance and interpretation

Archive input SHA256s, code and registration commit/hashes, canonical
matrix/label/row/pair/support hashes, seeds, compiler command/version,
library SHA256, interpreter architecture, package versions, timings and
attempt counters. Raw matrices and per-pair chain arrays remain in ignored
data/registry/nulls_revisions/curveball_v1; builds in work/; logs in logs/.
An interruption preserves incomplete outputs; resume only after checking
hashes, never silently overwrite. Re-estimate time using measured prepare,
trade and diagnostic/sample costs, not the synthetic trade benchmark alone.

The four-chain, R-hat and ESS recommendations follow Vehtari et al. (2021),
https://arxiv.org/abs/1903.08008. Exact stationarity of the Curveball kernel
is distinct from its finite-time convergence; see Carstens and Kleer,
https://arxiv.org/abs/1709.07290. No finite diagnostic proves mixing.

---

## Historical unregistered draft (preserved; superseded above)

# N2: exact binary margins and temporal constraints

STATUS: DRAFT — no real-data Curveball outcome may be computed yet.
Prepared during the registered N1 runs, 2026-09-04 Pacific.

This is a two-stage protocol. The sampling implementation is first
validated on synthetic matrices. A registered mixing pilot then chooses
production lengths using computational diagnostics. Pilot outcomes are
excluded from production estimates. The full production design and its
predictions are fixed before production streams run. No claim of full
outcome blindness is made: all original-null results are known and N1
results are arriving while this draft is prepared.

## Scientific targets

- N2: uniform binary document-by-frequent-label matrices with the
  observed row sums and column sums exactly fixed.
- N3: the same target separately within calendar quarter. Every
  document's row sum and each label's frequency within each quarter
  are fixed. This combines temporal and binary-margin constraints.
- Eligibility, document construction, hub exclusions and observed
  minimum document/author requirements remain frozen. Eligibility is
  never recomputed on a sampled evaluation matrix.
- Zero rows can be represented implicitly: their entries are forced
  zero in every admissible matrix. They remain included in corpus
  census counts, but are excluded from the number of active rows used
  to define computational work. This is a constant reduction of the
  state space, not state-dependent selection of tradable rows.

## Sampling kernel and reproducibility

Ordinary row-pair Curveball: choose two distinct active rows uniformly,
retain their shared labels, uniformly repartition their exclusive labels
while preserving each row's number of exclusive labels. An attempt that
leaves the matrix unchanged counts as an attempt; do not repeatedly
select pairs until a successful trade occurs. Store rows and label IDs
in canonical order. For N3, maintain an independent chain in each
quarter block, and compose their samples without trading across blocks.

The proposed compiled implementation uses the standardized
std::mt19937_64 engine, explicit unbiased bounded-integer rejection and
an explicit Fisher-Yates shuffle. Its output must not depend on the
standard library's choice of uniform_int_distribution or std::shuffle.
The Python reference uses the same mathematical transition kernel for
validation; matching its RNG stream is not required. Each chain's seed
and the exact source/build hashes will be archived. This new RNG is
specific to N2/N3; the registered label-shuffle RNG is unchanged.

## Proposed pilot (not yet authorized by a REGISTERED status)

Four independent logical chains per cell, scheduled according to memory
and available cores. Chain IDs are independent of worker scheduling.
Pilot checkpoint ladder: 5r, 10r, 20r, 40r, 80r attempted row-pair trades,
with r the number of active rows. For N3, a checkpoint at ar means ar_q
attempts in every quarter block q. These are candidate checkpoints, not
claims that a given length ensures mixing.

Collect scalar and pair-count diagnostics at intervals of r attempted
trades (r_q in each N3 block). Diagnose both movement away from the
initial matrix and agreement across chains in the total eligible-pair
count, its variance and relevant pair-count tails. Use dispersed valid
initial matrices where feasible and report their construction; agreement
among chains all started at the observed matrix is not sufficient.

The final pilot registration still needs: explicit seed namespaces;
initialization procedures; minimum diagnostic sample lengths; stopping
and doubling rules; maximum computational budget; rank/folded R-hat,
effective-sample-size and Monte Carlo error criteria; treatment of
constant/discrete diagnostics; and a rule for unresolved mixing. These
must be specified after synthetic correctness/performance tests and
before any real-data N2/N3 chain starts. Passing diagnostics will be
described as evidence of adequate mixing, not a proof of exact uniform
sampling at finite time.

## Production scope and reporting

Start with the eight registered Paper 2 headline cells under N2 and N3.
An onset/persistence robustness claim requires all 38 primary cells
under the relevant null, with unchanged onset scoring. Paper 1 needs
its four cells under exact margins to support claims beyond the
collapsed label null. A staged resource rule and specific production
predictions remain to be fixed before running.

Pool post-burn-in counts across adequately mixed chains for means,
standard deviations and per-pair thresholds. Report observed/null
ratios alongside z, chain diagnostics and Monte Carlo uncertainty.
Saved-draw count is not effective sample size. Binomial probabilities
are not used to establish a formed-count claim; correlated MCMC tail
fractions are not labelled exact permutation p-values. Preserve all
failed diagnostics and scientific predictions.

## Sources informing the design

- Strona et al. (2014), A fast and unbiased procedure to randomize
  ecological binary matrices with fixed row and column totals.
  https://doi.org/10.1038/ncomms5114
- Carstens (2015), Proof of uniform sampling of binary matrices with
  fixed row sums and column sums for the fast Curveball algorithm
  (with 2016 erratum). https://doi.org/10.1103/PhysRevE.91.042812
- Carstens and Kleer, Comparing the Switch and Curveball Markov Chains
  for Sampling Binary Matrices with Fixed Marginals.
  https://arxiv.org/abs/1709.07290
- Neal, A stopping rule for randomly sampling bipartite networks with
  fixed degree sequences, revised 2024.
  https://arxiv.org/abs/2305.04937v5
- Vehtari et al. (2021), Rank-normalization, folding, and localization:
  An improved R-hat for assessing convergence of MCMC.
  https://doi.org/10.1214/20-BA1221
