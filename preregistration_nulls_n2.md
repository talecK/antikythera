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
