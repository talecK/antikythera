# Data provenance — HN pull

## Source decision (2026-08-28, final)
- **Canonical source: HN BigQuery public dataset**
  (`bigquery-public-data.hacker_news.full`, max ts 2026-08-27, 49.45M rows),
  per the brief. Pulled via CTAS into staging dataset
  `pricemole-g4a:antikythera_hn` (deleted after export), exported locally via
  Storage Read API → `raw/hn_bq/*.parquet`. SQL: `sql/bq/*.sql`.
  Exporter: `pipeline/export_bq.py`.
- **Robustness mirror: ClickHouse public playground**
  (`play.clickhouse.com`, user `play`, no auth): `default.hackernews_history`,
  ReplacingMergeTree(update_time) ORDER BY id, live-updated, 49.44M ids.
  Queried with `FINAL` (latest version per id) → `raw/hn/`. SQL:
  `sql/*.tmpl`. Puller: `pipeline/pull_hn.sh`. Pulled first while GCP auth
  was unavailable; kept as an independent-mirror cross-check.
- Cross-check: per-year filtered story counts agree within <1% every year
  (residual = mirror sync timing + late vote drift).

## Filter spec (pre-registered; brief §Experiment protocol)
- Stories: `type='story' AND deleted=0 AND dead=0 AND (score>=5 OR descendants>=3)`.
- Yield: ~60–100K stories/yr (2007–2026), ~1.36M total. Brief's ~150K/yr
  estimate was high; same order of magnitude.

## Pull decisions (logged for pre-registration)
1. "Top ~20 comments" = TOP-LEVEL comments ranked by direct-reply count desc,
   then time asc, take 20 per story. No comment scores exist in any HN dump;
   reply count is the engagement proxy. Deeper replies reachable via the
   skeleton.
2. Comment window (canonical/BigQuery): comment.time ≤ story.time + 90 days,
   per story. (Mirror/playground used a coarser story-year + 90d window —
   marginal edge differences expected.) HN threads die within days.
3. Playground caps results at 1M rows → mirror's comment skeleton pulled
   monthly; stories and top-20 comments yearly (max observed ~558K rows/yr).
4. Text kept raw (HTML entities intact) — decoding happens downstream at
   extraction time; raw pull is immutable.

## Layout
Canonical (BigQuery):
- `raw/hn_bq/stories_filtered.parquet` — id, time, by, title, url, text, score, descendants (1,315,936 rows)
- `raw/hn_bq/comments_top20.parquet` — story_id, id, time, by, text, n_replies (7,071,121 rows)
- `raw/hn_bq/comment_skeleton.parquet` — id, parent, time, by, n_replies (42,246,310 rows)

Mirror (playground):
- `raw/hn/stories/stories_YYYY.parquet`
- `raw/hn/comments_top20/comments_YYYY.parquet`
- `raw/hn/comment_skeleton/skeleton_YYYY_MM.parquet`
- `raw/hn/pull.log` — pull run log

Reproduce: `sql/bq/*.sql` + `pipeline/export_bq.py` (canonical);
`pipeline/pull_hn.sh 2006 2026` (mirror; idempotent).
Verify: `pipeline/verify_pull.py`.

## Mirror completeness (2026-08-28, final)
- Stories 21/21 years, top-20 comments 21/21 years: COMPLETE.
- Comment skeleton: 197/248 months (gaps: 2014-02..2018-04 block + 2026
  partials). Cause: playground quota `queries_per_normalized_hash = 100/hr`
  — all monthly skeleton queries share one normalized hash, so bulk backfill
  stalls at ~100 chunks/hour. Decision: skeleton stays CANONICAL-ONLY
  (BigQuery file is complete + verified); the mirror's job — independent
  cross-check of the doc corpus (stories + comments) — is fully served.
  `pull_hn.sh` is idempotent; re-running in a fresh quota hour fills gaps if
  ever wanted. Do not engineer around the quota (shared free service).

## Leakage notes
- Every row carries its HN `time`. No derived fields peek forward.
- Caveat: score/descendants/kids are LATEST values, not point-in-time — the
  filter itself is therefore not point-in-time (a story's final score decides
  inclusion). Acceptable for the backtest doc spine; do NOT use score as a
  time-indexed feature without a point-in-time re-pull.
- Deleted/dead items are excluded as of pull date (survivorship vs a true
  point-in-time crawl; uniform across folds).
- 2,016 top-20 comments (0.03%) have comment.time < story.time: HN's
  second-chance pool re-timestamps stories, so early comments can predate the
  story's final timestamp. Zero comments beyond the +90d window. Treat story
  `time` as approximate for these; comment times are authentic.

## Verification (2026-08-28, canonical)
- Row counts match staged BigQuery tables exactly:
  1,315,936 stories / 7,071,121 top-20 comments / 42,246,310 skeleton rows.
- 0 duplicate story ids; 0 orphan top-20 comments; 0 stories with >20
  comments; 0 null/empty titles.
- Staging dataset `pricemole-g4a:antikythera_hn` deleted after export
  (reproducible from `sql/bq/*.sql`).
