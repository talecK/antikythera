# Tier A — positive control on Science4Cast (2026-08-29)

Registration: `preregistration_tier_a.md` (frozen before outcomes touched).
Harness: `eval/run_tier_a.py`. Data: Zenodo 7882892 (MD5 verified), concept
names + repo code cached in `data/science4cast/`. Full logs:
`data/science4cast/tier_a_full.log`; per-fold JSON `tier_a_*.json`.

## Registered pass criteria — BOTH MET
1. common_neighbors P@200 lift over random >= 10x on primary fold:
   **0.785 vs 0.0075 base rate = ~105x**. PASS.
2. Rank-AUC within 0.05 of repo baseline on matching config
   (delta_1_cutoff_25_minedge_1): ours (common_neighbors, plain feature)
   **0.899** vs their 15-feature MLP baseline **0.851**. PASS (consistent
   with the paper's own finding that pure network features are competitive).

The eval machinery detects the known signal at full strength. **The HN null
was not a harness artifact; the kill is certified corpus-scoped.**

## Results (full 10M-pair sample per fold)

P@200 / AUC by fold:

| ranker            | d3 c25 m1 (2017→20) PRIMARY | d3 c25 m3 (weight>=3) | d5 c25 m1 (2015→20) | d1 c25 m1 (2019→20) |
|-------------------|------------------------------|-----------------------|----------------------|----------------------|
| base rate         | 0.750%                       | 0.031%                | 1.533%               | 0.227%               |
| suppr_affinity    | 0.690 / 0.867                | 0.355 / 0.970         | 0.820 / 0.834        | 0.395 / 0.890        |
| affinity_only     | 0.180 / 0.564                | 0.015 / 0.604         | 0.240 / 0.561        | 0.030 / 0.562        |
| common_neighbors  | **0.785 / 0.874**            | **0.380 / 0.973**     | **0.860 / 0.831**    | **0.475 / 0.899**    |
| freq_product      | 0.690 / 0.866                | 0.345 / 0.968         | 0.820 / 0.832        | 0.385 / 0.889        |
| random            | 0.005 / 0.502                | 0.000 / 0.503         | 0.030 / 0.500        | 0.000 / 0.501        |

## The three findings that matter beyond the pass

1. **The science signal is also ~entirely popularity + closure.**
   freq_product matches common_neighbors within noise on every fold
   (P@200 0.69 vs 0.785; AUC within 0.01); suppression x affinity adds
   nothing; embedding affinity is near-dead there too (AUC ~0.56). Run 3's
   registered bar ("beat freq_product decisively") is a bar the celebrated
   benchmark result itself would essentially fail. The run-2 autopsy
   structure — popularity mean-reversion carries the ranking — is a property
   of the method family on BOTH corpora, not an HN pathology.

2. **The thesis's actual object (suppressed pairs) behaves oppositely on the
   two corpora.** Pairs with E >= 2 and zero co-occurrence are vanishingly
   rare in the dense science graph (281 of 10M sampled pairs; mean degree
   ~199) and when they exist they form at **67%** within 3 years (188/281).
   On HN they were plentiful (25,161) and inert (**0.60%**). One number
   pair now carries the whole corpus contrast: 67% vs 0.6%. In science,
   "expected but absent" is a strong tell that the edge is imminent; on HN
   it tells you nothing. (Within the science suppressed subset all rankers
   converge toward the 67% base — eligibility does the work, ranking adds
   little.)

3. **Unitization noise is NOT the decisive killer.** The benchmark's RAKE
   units are conspicuously mushy ('extensive experiment', 'main
   contribution', 'wide range') — comparable to the HN concept mush — yet
   the signal survives at 100x. Signal survival is set by the corpus's
   generative process (authors actively combining concepts), not by unit
   cleanliness. Implication for the equities/infosec variant: its case must
   rest on the mechanism (analysts/researchers actively hunting
   connections), not primarily on tickers/CVEs being clean units.

## Implications for the ladder
- Tier B (our LLM extractor on raw abstracts) is now OPTIONAL: its target
  hypothesis (unitization destroys signal) lost most of its prior via
  finding 3. Run only if full pipeline certification is wanted before new
  spend (~$30–60).
- The discriminating experiment for the variant is the angle-5 base-rate
  gate: measure suppressed-pair frequency AND formation rate in
  financial/security discourse before any extraction spend. Science-like
  (rare but hot) => variant live; HN-like (plentiful but inert) => dead.
- Leakage caveat as registered: affinity used a 2023 embedding model over a
  2017 build window — tolerated in a control, and it changes nothing since
  affinity carried no signal anyway.
