# Pre-registration — HN backtest

Rule (brief, decisions 6–8 + protocol): every field below is committed BEFORE
the eval harness runs on a real fold. Robustness extractors may be listed but
ONE is primary. Changing any field after first eval = new registered run,
old result reported alongside.

## Status: DRAFT — no field is registered yet. Do not run eval.

## Primary extractor
- extractor_id: TBD (provider + pinned model version + prompt v + schema v)
- chosen after schema-hygiene smoke test (action item 5), before Pilot 1 eval

## Robustness extractors
- TBD (1–2; cross-extractor agreement check per open question 2)

## Fold boundaries (Pilot 1: one fold, 2 build years + 1 eval year)
- build_start: TBD
- eval_start:  TBD
- eval_end:    TBD (eval_start + 12 months)

## Eligible-pair spec (open question 3 — freeze before eval)
- per-idea frequency floor: TBD
- embedding-affinity threshold: TBD
- embedding model (must predate eval window): TBD (name + checkpoint hash)

## Edge-formation definition
- MIN_ADOPTERS (distinct authors co-mentioning in eval window): TBD

## k values
- TBD (e.g. 50 / 200 / 1000)

## Time decay
- half-life (days): TBD (open question 4)

## Registered corpus facts (fixed by the pull, 2026-08-28)
- Canonical source: bigquery-public-data.hacker_news.full (max ts 2026-08-27)
- Filter: type=story, not dead/deleted, score>=5 OR descendants>=3
- 1,315,936 stories; docs = title + self-text + top<=20 top-level comments
  ranked by reply count desc, time asc, within story.time + 90d
- Known caveats: latest-value filter (not point-in-time); 2,016 pre-story
  comment timestamps (second-chance pool); see data/README.md
