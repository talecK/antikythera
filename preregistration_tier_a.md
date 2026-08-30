# Tier A registration — positive control on Science4Cast (2026-08-29)

Purpose: instrument calibration, NOT a discovery claim. Question: does the
run-3 eval machinery detect link-formation signal on a corpus where signal is
known to exist (Krenn et al., NMI 2023), and what does that known-positive
look like under our severity (P@k over suppressed pairs) rather than theirs
(AUC over sampled pairs)?

Written BEFORE any solution vector is read. The solution bits ship inside the
same pkl files as the inputs; blindness here means: no ranker-vs-solution
intersection is computed before this file is saved. (Weaker than the HN runs'
git-committed ordering; disclosed.)

## Data (Zenodo 10.5281/zenodo.7882892, downloaded 2026-08-29)
- PRIMARY: SemanticGraph_delta_3_cutoff_25_minedge_1.pkl
  (build = edges to end-2017, predict formation by end-2020, vertices with
  degree >= 25 at 2017, formation = edge weight >= 1 in 2020 multigraph)
- SENSITIVITY A: ..._delta_3_cutoff_25_minedge_3.pkl — formation = weight >= 3
  (closest available analogue of run 3's ">=2 docs" robustness bar; the pkls
  carry no per-edge author/paper ids, so author-independence and eval-window
  z-calibration CANNOT be reproduced — this is the acknowledged gap between
  their outcome and run 3's outcome).
- SENSITIVITY B: ..._delta_5_cutoff_25_minedge_1.pkl (2015→2020; era closest
  to the HN fold).
- Units: benchmark concepts, node index = line number in full_concepts_new.txt
  (64,719 lines; RAKE-extracted, curated by the benchmark authors).

## Mapping run 3 onto their sample
- Universe = their 10M sampled unconnected pairs (uniform over
  degree-cutoff-passing, unconnected-at-build pairs). P@k on this sample
  estimates P@k on their full candidate universe.
- Build-graph stats from the pkl edge list (multiplicity = co-mention events):
  s_i = weighted degree, M = total edge events, N_i = unweighted degree,
  neighbor sets unweighted.
- Suppressed-pair eligibility (run-3 analogue): observed co-occurrence = 0
  (guaranteed by construction) AND configuration-null expectation
  E_ij = s_i * s_j / (2M) >= 2. (HN run 3 used doc-marginal E = f_i f_j / N;
  per-doc concept sets are not recoverable from the edge lists, so the
  configuration-model null substitutes. Same monotone structure in the
  marginals; disclosed.)
- Reported on BOTH: (i) the eligible-suppressed subset, (ii) the full sample.

## Rankers (mirror run 3)
1. suppression_affinity = E_ij * cosine
2. affinity_only = cosine (BAAI/bge-small-en-v1.5 over concept strings —
   LEAKAGE CAVEAT: 2023 embedding model post-dates the 2017 build window;
   tolerated in a pipeline-sensitivity control, disqualifying in a discovery
   run; graph rankers are clean)
3. common_neighbors = |neighbors(i) ∩ neighbors(j)| at build
4. freq_product = s_i * s_j (confound control)
5. random (seed 20260829)

## Metrics
- P@k, k in {50, 200, 1000}, on eligible-suppressed subset and full sample.
- Their AUC (calculate_ROC-equivalent, computed as rank-AUC) per ranker on
  the full sample — comparability anchor to the published ~0.85–0.93 range
  and to the repo's expected_output baseline log.
- Base rates for every universe reported.

## Interpretation (registered before results)
- Instrument PASSES the control if, on the PRIMARY dataset, common_neighbors
  (the ranker that "worked" on HN) achieves P@200 lift over random >= 10x on
  the full sample, and its rank-AUC lands within 0.05 of the repo baseline
  for the matching configuration (implementation-correctness check).
- The science-vs-HN contrast is then quantified as (P@200 lift here) vs the
  HN run-3 value (2.5x–5x over random at 4x lift; base rate 0.60%).
- If common_neighbors FAILS to beat random convincingly here, the harness or
  the mapping is broken — debug before drawing any conclusion; no claim about
  HN follows from a broken control.
- Suppressed-subset results are reported descriptively either way: they show
  what run 3's exact severity does to a known-live corpus.

## Explicitly out of scope for Tier A
- Author-independence outcome, chance-calibrated (z>=2) outcome — need
  per-paper data (Tier B).
- Any claim about discourse; this is a scientific-literature corpus.
