# Pilot 0 report — titles-only registry sanity (2026-08-29)

## Verdict: PASS — proceed to Pilot 1

The full pipeline (pull → extract → embed → cluster → adjudicate → registry)
ran end-to-end at corpus scale. The registry's recurring head is coherent,
adjudicated merges are precise, and every failure encountered was
infrastructure (disk, balance), not method.

## Numbers
- Corpus: 1,315,846 / 1,315,936 titles extracted (99.993%); 90 stragglers in
  2 persistently-failing batches.
- Claims: 822,526 (0.63/title; titles are claim-sparse by design).
- Registry v1 (cosine ≥0.95 auto-merge vs anchors): 769,811 ideas, 95%
  singletons. Gray zone (0.85–0.95): 276,296 pairs.
- Adjudication (DeepSeek nothink, batched 20 pairs/call): 80% of backlog
  judged before balance exhaustion; 18.5–24% SAME rate; 67,412 merges.
- Registry v2: 702,399 ideas, 89% singletons. Head sizes 103/63/61/…
- Cost: extraction $11.26, adjudication $4.22, smoke tests $0.71.
  **Total spend to date: ~$16.20.**

## Quality evidence
- Head is real recurring discourse: "GitHub is having an outage" (103),
  "Programming is hard" (61), "We might live in a computer simulation" (54),
  "AI is a bubble" (32), "Bitcoin is in a bubble" (30), "PHP sucks." (27).
- Merge precision: 15/15 randomly sampled SAME verdicts were true paraphrase
  merges (e.g. "We must get football out of our universities" ↔ "Football
  should be removed from universities").
- Polarity: "Microsoft is dead" vs "Microsoft is not dead" resolved as
  distinct ideas (the embedding-only trap the adjudication layer exists for).

## Carry-forward items (granularity v2 / Pilot 1 design)
1. **Event-claims filter**: the biggest clusters are outage events ("X is
   down") — recurring events, not idea-connections; noise for gap
   prediction. Add a claim-type flag (event vs idea) at extraction or a
   registry-level filter.
2. **Finish adjudication backlog**: ~56K pairs (~$1.50) pending balance.
   Registry shape verdict does not depend on it.
3. **Transitive merge chains**: union-find merges are transitive (A~B, B~C
   ⇒ A~C even if A≁C never judged). Monitor cluster drift at Pilot 1 scale;
   consider centroid re-check on chains > depth 2.
4. **Singleton tail (89%)** is expected for title-level discourse; Pilot 1's
   comment-inclusive docs repeat ideas far more. Not a granularity verdict.
5. Balance ops: both providers now halt cleanly on 402; keep ≥$10 balance
   for Pilot 1 runs.

## Invariants honored
- Extraction cached immutably per (doc, extractor_id); adjudication verdicts
  cached per pair-hash; every stage resume-safe; registry versions coexist.
