# Pre-registration — HN backtest, Pilot 1

Rule (brief, decisions 6–8 + protocol): every field below is committed BEFORE
the eval harness runs on a real fold. Changing any field after first eval =
new registered run, old result reported alongside.

## STATUS: REGISTERED (2026-08-30, pre-eval)
Build-window diagnostics reviewed OUTCOME-BLIND before registration:
- 726,846 build-window ideas; 355 pass F>=10 (2,236 pass F=5); max freq 44.
- Eligible gap pairs at primary thresholds: 50,673 (well-posed; k<=1000 ok).
- Observation, logged not acted on: affinity>=0.55 retains 81% of frequent
  pairs (BGE cosines run high) — the filter is loose but identical across
  all rankers. Revisit only in a future registered run.
- SENSITIVITY (pre-declared before eval): F=5 rerun (1,745,049 eligible);
  reported alongside primary, never substituted for it.
- Registry: box-built batched-exact (bit-identity-validated), adjudicated
  (380,248 pairs, 101,130 merges, $6.35), assignments_v2.

## Primary extractor
- extractor_id: `deepseek-v4-flash-nothink_pv2_sv1`
  (DeepSeek V4 Flash, thinking disabled, prompt v2, schema v1)
- Passed schema-hygiene smoke test 2026-08-28 (105/105 JSON, 99/105 strict).

## DEVIATION from brief decision 6 (2–3 parallel extractors)
- Pilot 1 first pass runs a SINGLE extractor (owner's call, 2026-08-29;
  Qwen and Haiku-subsample skipped). Cross-extractor agreement — the
  paraphrase-noise robustness check (open question 2) — is DEFERRED, not
  dropped: docs are cached, a second extractor can replay the fold later
  for ~$15–35. Any positive Pilot 1 result is provisional until that check.

## Fold (Pilot 1: one fold)
- build_start: 2015-01-01
- eval_start:  2017-01-01
- eval_end:    2018-01-01
- Rationale: mid-size volumes (73K/68K build, 62K eval docs), platform-era
  discourse well clear of the COVID and LLM regime shifts; other regimes
  covered by full-run folds.

## Registry build
- Embedding: BAAI/bge-small-en-v1.5 (2023 release — predates eval window).
- Clustering: incremental vs first-claim anchors, auto-merge cosine >= 0.95,
  gray zone [0.85, 0.95) adjudicated (DeepSeek nothink, adjudication_v1);
  UNSURE = DISTINCT. Union-find merge application.

## Eligible-pair spec
- Per-idea frequency floor F: >= 10 distinct build-window docs (raw counts).
- Affinity threshold A: centroid cosine >= 0.55.
- Pair must have ZERO co-mentions in the build window.

## Scoring
- Decay half-life H: 365 days (to eval_start).
- z for a gap pair: -sqrt(E), E = N * p_i * p_j over build docs.
- gap_score = decayed_freq_i * decayed_freq_j * affinity * |z|.

## Edge formation (primary outcome)
- Pair forms iff >= 2 eval-window docs co-mention it AND those docs span
  >= 2 distinct story authors (independent-author adoption).

## Eval
- Metric: precision-at-k, k in {50, 200, 1000}.
- Baselines (same eligible set): random (seed 20260829), affinity-only
  ranking, frequency-growth ranking (product of ideas' late/early build
  growth ratios).
- Success: gap_score P@k exceeds ALL three baselines at k=200; report all k.

## REGISTERED RUN 2 (2026-08-30, pre-eval) — granularity rebuild 1
- Run 1 (claim units) was DEGENERATE: 0 formations among 58,183 eligible
  (only 26 pairs total hit >=2 eval docs). Not a thesis result.
- Rebuild 1a unit: CONCEPT STRINGS (lowercased exact identity, no
  clustering) from the same cached extractions. Same fold, same outcome
  definition (>=2 docs AND >=2 distinct story authors), same baselines,
  same k values, same half-life and affinity threshold.
- F (unit-relative, set from outcome-blind density check): >= 20 distinct
  build docs -> 10,444 concepts; 2.46M build co-occurring pairs.
  (Outcome-side count of formed edges was observed during the density
  check — disclosed: ~66K never-connected pairs form. Ranking results
  remain unseen at registration.)
- Affinity term/baseline use the concept's own embedding (unit = single
  string, centroid degenerates to the embedding itself).

## REGISTERED RUN 3 (2026-08-30, pre-eval) — suppressed-pair formulation
- Motivation: run 2 autopsy showed zero-observation among frequent pairs is
  not an anomaly; gap ranking degenerated to the frequency product. Run 3
  tests the thesis's actual object: pairs EXPECTED to co-occur that don't.
- Eligible: concept pairs (F>=20 units, unchanged) with E_build >= 2 and
  observed build co-occurrence = 0. Feasibility (outcome-blind): 25,161.
- Outcome (primary): chance-calibrated formation — eval-window z >= 2 AND
  >= 2 docs AND >= 2 distinct story authors.
- Rankers: (a) suppression x affinity = E_build * cosine; (b) affinity_only;
  (c) common_neighbors (count of frequent concepts co-occurring with BOTH
  ends in build — Science4Cast's strongest classical feature); (d)
  freq_product (confound control — a pass REQUIRES beating it); (e) random.
- Success: (a) or (c) beats freq_product AND random at k=200. k in
  {50, 200, 1000}; k capped at eligible-set size.
- Everything else unchanged from run 2.

## Registered corpus facts (fixed by the pull, 2026-08-28)
- Canonical source: bigquery-public-data.hacker_news.full (max ts 2026-08-27).
- Filter: type=story, not dead/deleted, score>=5 OR descendants>=3.
- Docs: title + self-text + top<=20 top-level comments (reply-count rank,
  +90d window). Known caveats in data/README.md (latest-value filter;
  2,016 pre-story comment timestamps).
