# Run 5 registration — author-as-document re-cut (2026-08-29)

Motivation (Tier A, reports/tier_a.md): the science/HN contrast is a
mechanism contrast — suppressed pairs form at 67% where authors actively
combine concepts, 0.60% where threads merely react to headlines. Run 5 asks
whether HN *individuals* combine concepts even though HN *threads* do not:
the same suppressed-pair formulation, with the document redefined from
thread to (author, quarter). Diagnostic re-cut on banked data; $0 marginal.

## STATUS: design frozen pre-eval; density numbers appended below
(outcome-blind) before any outcome computation. Eval runs only after this
file is committed.

## Data derivation
- Source: primary extractor cache (deepseek-v4-flash-nothink_pv2_sv1,
  2015–2017 full-doc claims), quote->comment->author attribution
  (pipeline/build_author_concepts.py). Feasibility (3,000-doc sample,
  seed 20260829): 70% of claims attribute to a unique comment, 12% to
  title/self-text (story author), 13% unmatched quotes, 5% no quote,
  0.1% ambiguous -> 82% attributed; unattributed claims dropped.
- Known coverage limits (disclosed): only top-20-comment threads exist in
  the corpus, so author histories are partial; drops are LLM-paraphrase
  idiosyncrasies, assumed outcome-independent.

## Unit and document
- Unit: concept strings, lowercased exact identity (as runs 2–4).
- DOCUMENT = (author, calendar quarter): the set of concepts attributed to
  that author in that quarter. Rationale: a person bridging two concepts
  within ~90 days is the "edge forms in a mind" event; lifetime histories
  would clique-explode, thread-docs are the already-tested room view.
- Hub guard (amplification deconfounding, brief §4): author-quarter docs
  with > 100 distinct concepts are dropped from the primary analysis;
  sensitivity WITHOUT the guard reported alongside.

## Folds (same eras as runs 3–4)
- Fold 1: build 2015Q1–2016Q4, eval 2017Q1–2017Q4.
- Fold 2: build 2015Q1–2015Q4, eval 2016Q1–2016Q4.

## Eligibility, outcome, rankers (run-3 formulation, author-space throughout)
- F floor: concept in >= 20 distinct build author-docs. Fallback decided by
  the outcome-blind density check ONLY (if < 2,000 concepts pass, F >= 10);
  the choice is recorded below before eval.
- Eligible pair: E_build = f_i * f_j / N_docs >= 2 AND observed build
  co-occurrence = 0.
- Formation: >= 2 eval author-docs co-mention AND >= 2 distinct authors AND
  eval-window z >= 2 (chance-calibrated, as run 3).
- Rankers: common_neighbors (PRIMARY — per Tier A, closure is the only
  live ranker family); freq_product (confound control); suppression x
  affinity and affinity_only (continuity, non-primary; embeddings reused
  from pilot1_concepts registry); random (seed 20260829).

## Registered readouts and interpretation (before any outcome is seen)
1. HEADLINE: suppressed-pair formation base rate in author space, both
   folds, vs thread-space (fold 1: 0.60%, fold 2: 0.68%) and vs
   Science4Cast (67%).
   - >= 5% in both folds: "rooms buried the signal" supported; the HN kill
     acquires a measurement-artifact component and the author lens becomes
     the default for any future discourse corpus.
   - < 2% in both folds: mechanism story confirmed — HN individuals do not
     bridge suppressed gaps either; kill stands unqualified.
   - Between / folds disagree: indeterminate; report both, no relitigation.
2. SECONDARY: common_neighbors beats random AND freq_product at k=200 in
   both folds (same bar run 3 set; Tier A showed even science barely clears
   the freq_product part — reported, not load-bearing).
3. Qualitative: top-30 suppressed author-space pairs by common_neighbors
   with formation flags (the "what are the hits" table).

## Density check (outcome-blind, appended pre-eval 2026-08-29)
- Attribution at scale: 946,648 / 1,166,985 claims (81%), 2,495,756
  attributed concept rows (matches the 82% feasibility estimate).
- Fold 1: build author-docs 142,123 (hub guard dropped 1,106), eval 73,817
  (dropped 436); concepts/author-doc median 5, p90 21; F>=20 -> 8,419
  concepts (>= 2,000, so F=20 STANDS); 3.19M build co-occurring pairs;
  ELIGIBLE SUPPRESSED PAIRS: 364.
- Fold 2: build 70,880 (dropped 571), eval 71,243 (dropped 535); F>=20 ->
  4,346 concepts; 1.21M co-occurring pairs; ELIGIBLE SUPPRESSED PAIRS: 110.
- Structural observation recorded BEFORE outcomes: eligible suppressed
  pairs are ~70x rarer than in thread space on the same folds (364 vs
  25,161; 110 vs 7,505) — the author-space co-occurrence graph is dense,
  structurally resembling Science4Cast (281 suppressed per 10M sampled),
  not thread-space HN. k is capped at eligible-set size per registration;
  fold-2 k=200 readout is over 110 pairs.
