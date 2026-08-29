# Pre-registration — HN backtest, Pilot 1

Rule (brief, decisions 6–8 + protocol): every field below is committed BEFORE
the eval harness runs on a real fold. Changing any field after first eval =
new registered run, old result reported alongside.

## STATUS: DRAFT
(eval/run_eval.py --prereg refuses to run until this reads
"STATUS: REGISTERED". Flip only after build-window diagnostics confirm the
thresholds below, and BEFORE the first eval execution.)

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

## Registered corpus facts (fixed by the pull, 2026-08-28)
- Canonical source: bigquery-public-data.hacker_news.full (max ts 2026-08-27).
- Filter: type=story, not dead/deleted, score>=5 OR descendants>=3.
- Docs: title + self-text + top<=20 top-level comments (reply-count rank,
  +90d window). Known caveats in data/README.md (latest-value filter;
  2,016 pre-story comment timestamps).
