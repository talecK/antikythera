# Antikythera data release v1: Reddit finance ticker panel and Hacker News concept atlas

Datasheet for the Zenodo deposit accompanying two preprints:

- Quiring, K. (2026). Ideas that never meet online mark divided
  communities, not future discoveries. SocArXiv, DOI at posting.
- Quiring, K. (2026). Watching the walls go up: r/wallstreetbets
  segregated after the GameStop squeeze. SocArXiv, DOI at posting.

Deposit DOI: inserted at publication. Cite the deposit, not this file.

License: to be set by the depositor at publication. The derived tables
contain no Reddit or Hacker News text.

Code and registrations: https://github.com/talecK/antikythera (public
at publication). The release was assembled by
`pipeline/build_release.py`, which reads every source once, records its
SHA-256 before and after, and refuses to overwrite any existing path.

## Contents

| File | Rows | Size | What it is |
|---|---:|---:|---|
| reddit_ticker_mentions_2019_2024.parquet | 11,200,484 | 113 MB | One row per stock-ticker mention in six finance subreddits, 2019 to 2024, author replaced by a salted hash |
| hn_atlas/concept_freq_monthly.parquet | | 4.4 MB | Monthly mention and document counts per extracted Hacker News concept, 2015 to 2017 |
| hn_atlas/concept_cooccurrence.parquet | | 18 MB | Document-level concept co-occurrence edges (at least 2 shared documents) with first-seen date, 2015 to 2017 |
| hn_atlas/concept_first_seen.parquet | | 4 MB | Earliest appearance and total mentions per concept, 2015 to 2017 |
| hn_atlas/title_claims_2006_2026.parquet | about 1.16 M | 22 MB | Clustered claims extracted from Hacker News story titles across the full 2006 to 2026 archive |
| hn_atlas/concept_exposure_labels.csv | 5,997 | 96 KB | Economic-exposure label (0 or 1) per concept under the registered rule |
| hn_atlas/claim_pair_verdicts.parquet | about 600 K | 32 MB | Near-duplicate claim pairs with SAME, DISTINCT, or UNSURE verdicts; usable as a paraphrase benchmark |
| paper2_runs/paper2_windows_z.tsv | 204 cells | | Registered rolling-window segregation z series, conforming run |
| paper2_runs/paper2_window_census.tsv | | | Outcome-blind eligible-pair census per window and build length |
| paper2_runs/paper2_placebo_reps.tsv | 40 | | Excursion placebo replicates with per-replicate seeds |
| paper2_runs/paper2_volume_table.tsv | 864 | | Per-file row counts from the integrity pass, committed before any outcome |
| paper2_runs/*_v1_superseded.tsv | | | First-run outputs retained as disclosed superseded artifacts (Amendment V4) |
| stats.json | | | Counts quoted in this datasheet, computed at build |
| CHECKSUMS.txt | | | SHA-256 of every released file |
| SOURCE_CHECKSUMS.txt | | | SHA-256 of every source before and after the build |

## Reddit ticker panel

### Source

Arctic Shift API, one collection pass on 2026-08-31, 864 monthly files
covering posts and comments for r/wallstreetbets, r/stocks,
r/investing, r/StockMarket, r/ValueInvesting, and r/SecurityAnalysis,
2019-01 through 2024-12 (98,084,631 raw rows). Pull script and runbook:
`pipeline/pull_reddit_paper2.py`, `pipeline/fleet_collector_paper2.sh`.
Raw content is not redistributed; the pull specification reproduces it.

### Columns

| Column | Type | Meaning |
|---|---|---|
| author_hash | string | First 16 hex characters of SHA-256(salt + username). Consistent within this release, so rows group by author; not reversible without the salt, which is not released |
| time | int64 | Unix seconds, UTC, of the post or comment |
| subreddit | string | One of the six above |
| ticker | string | Uppercase symbol, resolved against the SEC company_tickers table |
| unit_type | string | `cashtag` if written as $GME, `bare` if written as GME |
| kind | string | `post` or `comment` |
| item_id | string | Reddit item id (t3_ posts and t1_ comments share raw ids; the kind column disambiguates) |
| score | int64 | Vote score of the item at collection time. Collected for a separately registered follow-up; no registered readout in the papers uses it |

### Extraction rules (frozen before any evaluation)

- Cashtag: `$` followed by 1 to 5 letters, case-insensitive, must
  resolve to an SEC symbol.
- Bare: an uppercase 2 to 5 letter token that is an SEC symbol and not
  in a committed stoplist of English and finance-jargon collisions.
  Single-letter symbols are cashtag-only.
- Hygiene: items by `[deleted]` or AutoModerator dropped; duplicates
  removed per (kind, monthly shard); at most 50 tickers per item.
- No language model anywhere; deterministic and re-runnable from
  `pipeline/extract_tickers_paper2.py`, which imports the unit rules
  from `pipeline/extract_tickers.py`.

### What the papers apply at load time, not in this file

The panel is released as extracted. The registered analyses then drop
five index and macro symbols (SPY, QQQ, VIX, BTC, ETH), drop
author-quarters with more than 50 distinct tickers as hubs, count a
ticker as frequent at 20 or more distinct author-quarters in a build
period, and read the two unit types either pooled (union lens, primary)
or cashtag-only (sensitivity lens). Apply the same filters to reproduce
the papers' cells.

### Counts

| Subreddit | Rows | Hashed authors |
|---|---:|---:|
| wallstreetbets | 9,386,300 | 828,314 |
| stocks | 1,042,935 | 154,299 |
| investing | 380,515 | 91,944 |
| StockMarket | 240,950 | 61,140 |
| ValueInvesting | 138,950 | 24,893 |
| SecurityAnalysis | 10,834 | 2,782 |
| total | 11,200,484 | 976,889 |

Distinct tickers: 6,623. By kind and unit type: comments 9,686,449 bare
and 598,568 cashtag; posts 737,986 bare and 177,481 cashtag.

### Caveats

- Survivorship: the SEC table lists current registrants at snapshot
  time, so symbols delisted before August 2026 are invisible.
- The bare lens is noisier than the cashtag lens; some uppercase words
  that are also symbols survive the stoplist. The papers treat cashtag
  as the sensitivity lens for this reason.
- A small number of rows carry a 2018-12-31 date: UTC timestamps at the
  edge of the first monthly file.
- Author hashing: one salt for the whole release, held privately. If a
  later version is built with a new salt, its hashes will not join to
  this version's. Do not attempt to re-identify authors.
- Score is the value at collection time, years after posting for most
  items.

## Hacker News concept atlas

Derived from the Hacker News public archive (BigQuery public dataset
`bigquery-public-data.hacker_news.full`, canonical; ClickHouse public
playground as an independent mirror), filtered to stories with score at
least 5 or at least 3 descendants, each document being the story title
plus its top 20 top-level comments by reply count within 90 days. The
concept and claim layer was extracted by a pinned commercial language
model (DeepSeek V4-Flash, thinking disabled; prompt and decoding
configuration are part of the cache key in the code release).

Coverage: the concept tables cover 2015 through 2017 (202,721 filtered
stories, 1.17 million claims). The title-claims table covers the full
2006 to 2026 archive from titles only. Concepts are extractor-normalized
lowercase strings with no clustering, so variants such as "ml" and
"machine learning" are separate rows. Rebuild any table with
`pipeline/build_atlas.py`.

The per-document claim extractions with verbatim quotes and the author
attribution table are not in this version; they are planned for a later
version of the same deposit.

## Registered-run outputs

The six TSV files under `paper2_runs/` are copied byte-for-byte from the
code repository at the commits named in paper 2's commit appendix.
`paper2_windows_z.tsv` holds every cell of the conforming run (two
strata, two lenses, three build lengths). The superseded first-run files
are retained because their outcomes were seen before a disclosed
correction; both runs agree on every verdict.

## Provenance and integrity

`SOURCE_CHECKSUMS.txt` records the SHA-256 of each of the 13 source
files before and after the build; all 13 matched. `CHECKSUMS.txt`
records the SHA-256 of each released file. The build script, this
datasheet, and the Zenodo metadata are committed to the code
repository; the data files are not.

## Contact

Kevin Quiring, independent researcher. Issues against the code
repository are the preferred channel.
