# Handoff — state of the Antikythera project (2026-08-30)

## Status: original thesis KILLED, cleanly. Assets banked. Open to new ideas.

The discourse-gap thesis (never-co-mentioned idea pairs predict future
connection; see discourse-gap-engine-brief.md) was tested on 20 years of
Hacker News and falsified in four pre-registered runs across two folds plus
an ML sweep — full record in reports/pilot1_runs.md, registrations in
preregistration.md (git history proves reg-before-eval ordering throughout).

### The three load-bearing findings
1. **Granularity bracket**: claim-level units → co-occurrence graph is
   all-zeros (nothing repeats). Concept-level units → the graph is alive,
   but prediction reduces to popularity mechanics. Nothing in between was
   found where the thesis's machinery adds signal.
2. **The only real predictor is triadic closure** (shared neighbors),
   ~2.5% P@200 ≈ 4x random — generic network science, not the thesis, not
   a product.
3. **On economically-relevant vocabulary the target event barely exists**:
   suppressed exposed-concept pairs form above-chance connections ~8
   times/year on all of HN.

## What a new session inherits
- **Corpus**: 1.32M HN threads 2006–2026 (title + top-20 comments), clean
  parquet, `data/docs/`; raw pull + provenance in `data/README.md`. All
  heavy data lives on the NVMe ("/Volumes/1TB NVME 1/antikythera") via
  symlinks under data/.
- **Extraction caches** (immutable, keyed (doc, extractor)): full-doc
  claims+concepts 2015–2017 (1.17M claims), titles-claims all years.
  Extractor: deepseek-v4-flash, thinking DISABLED (config is part of the
  extractor id — thinking-on burns budget for nothing, see reports).
- **HN Atlas** (`data/atlas/` + README): concept trends, co-occurrence
  graph, first-seen indexes, exposure labels, ~600K-pair SAME/DISTINCT
  paraphrase dataset.
- **Pipeline** (all committed): pull, doc builder, batched exact clustering
  (bit-identical to sequential, checkpointed, status.json), adjudication,
  eval harnesses with leakage guards and prereg gates.

## Deferred: 20-year concept extraction (~$300–400)
Extending claims+concepts to all years completes the "OpenAlex-for-
discourse" registry-floor asset. DEFERRED (2026-08-30) because DeepSeek
tripled prices on Aug 17 (V4-Flash $0.44/$1.32 peak, 50% off outside
01:00–04:00 & 06:00–10:00 UTC) — likely a capacity crunch; re-check prices.
Runbook (resume-safe, run in off-peak window, ~overnight):
```
ulimit -n 8192 && .venv/bin/python pipeline/pilot1_extract.py \
  --years 2006 2007 2008 2009 2010 2011 2012 2013 2014 2018 2019 2020 \
  2021 2022 2023 2024 2025 2026 --workers 1024 --budget-usd 450
```
CAVEAT: client-side cost counters in the scripts use STALE prices
($0.14/$0.28); real billing is ~1.5–3x what they print. Fix before trusting.

## Operational lessons (paid for, don't re-buy)
1. DeepSeek: 1,024 concurrent requests fine; the GIL caps one Python
   process ~5K docs/min — shard processes to go faster. Halt-on-402 is
   wired in (prepaid balance runs dry silently otherwise).
2. Never pipe long stages through tail/grep — log to files (CLAUDE.md rule).
3. Exact 1M+-vector clustering: ~10h on the M1 mini, ~35min on a $2.6/h
   64-core Vultr box (key: ~/.config/pricemole/vultr.env; bootstrap script
   pipeline/box_bootstrap.sh). HNSW option exists but is uncertified.
4. No timeline claims without a microbenchmark; no eval without frozen
   registration. Both failed painfully when skipped.

## Fresh-idea starting points (untested, from the post-mortems)
- Equities/infosec corpora sidestep the unitization problem (tickers/CVEs
  are self-indexing) — the brief's niche #2/#3 remain unexplored.
- The paraphrase-verdict dataset could train/benchmark a claim-matcher.
- The Uzzi-Jones outcome flip: predict which STORIES succeed given they
  contain an atypical concept pair (success = points, measurable here).
- Concept trend data (atlas) supports "when did HN start caring about X"
  analyses with no further spend.
