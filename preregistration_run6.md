# Run 6 registration — exposure lens x author space (2026-08-30)

Question: does the run-5 author-space detector survive restriction to
economically-relevant vocabulary (run 4's frozen EXPOSED labels), and how
much of author-space "formation" is articulated connection (both concepts
in one extracted claim) rather than co-interest?

Written and committed BEFORE any run-6 outcome is computed. Author-space
formation outcomes for the ALL-pairs lens were already seen in run 5
(19%/24%); the EXPOSED-lens and ARTICULATED outcomes have not been seen.

## Data
- data/registry/run5_author/author_concepts.parquet REBUILT with claim_id
  (doc-local claim index; pipeline/build_author_concepts.py) — same
  attribution logic, one new column; row-identity otherwise unchanged.
- Exposure labels: data/atlas/concept_exposure_labels.csv — run 4's frozen
  verdicts, UNCHANGED. Coverage check (outcome-blind, 2026-08-30): 100% of
  eligible-pair concepts are labeled (413/413 fold 1, 149/149 fold 2);
  no new classification needed.

## Universe (unchanged from run 5)
- Folds, document = (author, quarter), hub guard 100, F>=20, E>=2 & obs=0.
- Outcome-blind counts: fold 1 = 364 eligible, of which EXPOSEDxEXPOSED 20;
  fold 2 = 110 eligible, EXPOSEDxEXPOSED 6.

## Outcomes
1. AUTHOR-SPACE formation (as run 5): >=2 eval author-docs, >=2 distinct
   authors, eval z>=2.
2. ARTICULATED formation (new): both concepts in the concept list of ONE
   extracted claim (same doc_id + claim_id), in the eval window.
   - strict: >=2 such claims by >=2 distinct authors.
   - weak (descriptive): >=1 such claim.
   No z-calibration (claim-level pair co-occurrence is too sparse for a
   stable null; disclosed).

## Lenses
- A (primary): EXPOSEDxEXPOSED eligible pairs, both folds, POOLED (n=26)
  given small n; per-fold counts reported.
- B: all eligible pairs (articulated outcome only — author-space formation
  for lens B was run 5's result).

## Registered readouts and interpretation
1. PRIMARY: pooled exposed formation count/26 (author-space outcome).
   - >=3/26 (>=11.5%): detector provisionally survives economic vocabulary
     (vs thread-space exposed 8/1452 = 0.55% and 1/428; and vs author-space
     all-pairs 19-24%). Next-step implication: variant gate proceeds with
     author lens + exposure-native units.
   - <=1/26: economically-relevant suppressed pairs are inert even in
     author space; HN contributes nothing further to the variant decision.
   - 2/26: indeterminate; report, no interpretation stretch.
2. SECONDARY (descriptive, no pass/fail): articulated-formation rates on
   lenses A and B — calibrates how much of "formation" is real connection
   vs co-interest. Expected much lower than author-space rates.
3. QUALITATIVE: the full exposed-pair list (26 names) with all outcome
   flags — small enough to read whole.
- Small-n caveat: 26 pooled pairs; exact counts and Wilson 95% CI reported;
  no precision-at-k, no ranking claims (ranking is dead per runs 3/5/Tier A).
