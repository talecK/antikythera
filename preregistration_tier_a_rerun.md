# Tier A re-execution registration (2026-08-30)

## Purpose (ordering hygiene, disclosed plainly)

The original Tier A positive control's registration and result were
committed TOGETHER in one commit (a884a49), so the commit history cannot
by itself prove the design was frozen before that evaluation ran (every
other evaluation in this project has a registration commit strictly
preceding its result commit). This re-execution closes that gap: this
file is committed BEFORE the re-run starts, the harness is unchanged,
and the outputs are compared against the originals.

What this can and cannot prove, stated in advance: a deterministic
re-run cannot retroactively prove the ORIGINAL run's design was
outcome-blind; that rests on the session record plus the fact that the
design is run 3's harness, whose own registration (f1304dc) predates
Tier A entirely. What the re-run does prove is that the committed
design, executed from a pre-committed registration, produces the
committed results.

## Platform disclosure (plain language)

The original ran on the project workstation: Apple Silicon (arm64,
macOS, numpy on Accelerate BLAS). This re-execution runs on a freshly
provisioned x86-64 Linux cloud instance (Vultr, numpy on OpenBLAS),
chosen because the workstation is currently loaded with another
project's evaluations. Basic arithmetic is identical across these
platforms; large floating-point reductions (AUC sums, embedding dot
products) may differ in trailing digits because summation order and
BLAS backends differ. Therefore the registered expectation is:

- ALL integer outcomes identical to the originals: per-fold n_pairs,
  formed counts, universe sizes, and the headline suppressed-set counts
  (188/281 pooled across folds as reported in reports/tier_a.md).
- ALL floating-point outcomes (P@k, AUC) equal to the originals within
  absolute tolerance 1e-9.
- Both platforms' JSON outputs committed side by side.

Any deviation beyond this is reported as a discrepancy, not smoothed
over.

## Frozen procedure

1. Harness: eval/run_tier_a.py at the current commit, byte-identical
   logic; the only change since a884a49 is that the two hardcoded paths
   became environment-overridable (TIER_A_ROOT, TIER_A_BASE) with
   unchanged defaults, committed with this registration.
2. Inputs: the four benchmark pickles and two auxiliary files, verified
   on the box by MD5 against the local copies used in the original run:
   - SemanticGraph_delta_1_cutoff_25_minedge_1.pkl  47102593a73a0931f5ef8333bdfe8891
   - SemanticGraph_delta_3_cutoff_25_minedge_1.pkl  30043131a026d635a2e61b376b1a373d
   - SemanticGraph_delta_3_cutoff_25_minedge_3.pkl  f341548b8f58283e7ad179b4137c4937
   - SemanticGraph_delta_5_cutoff_25_minedge_1.pkl  0a793ade3d034a8540d705fb23b715bb
   - concept_embeddings.npy                         d56e1d882001d49a39adf78541bc98f9
   - full_concepts_new.txt                          b2a95a90810a40ea05725505581b5635
   Pickles are fetched from the public Zenodo record 7882892 where
   possible, else uploaded; either way the MD5 gate above decides.
3. Runs: the same four full (no --sample) invocations as the original,
   one per pickle. Output logged to files, unpiped.
4. Comparison: scripted, integer-exact / float<=1e-9 as above, against
   data/science4cast/tier_a_{y2019_d1,y2017_d3,y2017_d3...m3,y2015_d5}
   _c25_m1|m3.json. Comparison report and both JSON sets committed under
   reports/tier_a_rerun/.
5. Instance destroyed after retrieval; cost noted in the report.
