# Handoff — state of the Antikythera project (2026-08-30, REVISED 2026-08-30)

## Status: kill REVISED. Thread-lens kill stands; author-lens re-cut (run 5)
## shows the target event is real at ~20%/yr. We own a DETECTOR, not a
## telescope. Instrument certified by a passed positive control (Tier A).

The discourse-gap thesis (never-co-mentioned idea pairs predict future
connection; see discourse-gap-engine-brief.md) was tested on 20 years of
Hacker News and falsified THERE in four pre-registered runs across two folds plus
an ML sweep — full record in reports/pilot1_runs.md, registrations in
preregistration.md (git history proves reg-before-eval ordering throughout).

### The three load-bearing findings (original kill, thread lens)
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

### REVISION (2026-08-30 session — Tier A + run 5, both registered/committed)
1. **Tier A positive control PASSED** (`reports/tier_a.md`): the exact
   run-3 harness on the Science4Cast benchmark finds the known signal at
   ~105x lift; the HN null was not a harness artifact. Also learned there:
   the celebrated science signal is itself just popularity+closure
   (freq_product ties common_neighbors; embedding affinity dead, AUC~0.56),
   and the benchmark's RAKE units are as mushy as ours — so the thesis's
   distinctive ranking machinery adds nothing on ANY corpus, and unitization
   noise was NOT the HN killer. Calibration: suppressed pairs form at 67%
   in science vs 0.6% thread-HN.
2. **Run 5 (author-as-document re-cut) FLIPS the measurement story**
   (`preregistration_run5.md`, run log): with document = (author, quarter)
   over quote-attributed concepts (81% attribution,
   `pipeline/build_author_concepts.py`), suppressed pairs are rare
   (364/110 per fold, science-like structure) and form at **19%/24%** vs
   0.60%/0.68% thread-space — registered >=5% bar met both folds. HN
   individuals DO bridge expected-but-absent pairs; comment threads never
   showed it. The kill acquires a measurement-artifact component.
3. **Detector, not telescope**: ranking WITHIN the eligible suppressed set
   beats nothing (here, and in science's suppressed subset alike).
   Eligibility is the entire instrument: ~360 flagged pairs/yr at ~1-in-5
   formation vs 1-in-160 background. Author-space co-occurrence is the
   default lens for all future corpora.

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

## Next steps (revised 2026-08-30; ordered by information per dollar)
1. **DONE — Run 6: exposure lens x author space (registered d3844c1,
   result b244d65): PRIMARY MET.** Exposed pairs form at 23.1% pooled
   (6/26), same as all-pairs author space; thread-space was 0.55%. The
   detector survives economic vocabulary. Articulated-formation readout:
   ~zero — formation is pre-articulation audience convergence, i.e. the
   detector fires before anyone writes the connecting claim (this is the
   product-shaped fact). HN's exposed slice is thin (~13 flags/yr): density
   must come from the variant corpus.
1b. **DONE — Run 7 (scout class, ff94e9f/c9cf264 + addendum 58645df):
   FAILED, HN-SCOPED.** No persistent bridge-precision trait (rho 0.012 vs
   null95 0.035); post-hoc diagnostics show the test was well-powered for
   trait SD>=0.05 AND that author heterogeneity is real but situational
   (overdispersion chi 47,100 vs 14,701 — bursts, not skills). Scope:
   graph/semantic ranking failed on HN and science; reputational only on
   HN — the negative transfers weakly. Gate below is census-PRIMARY;
   register a cheap scout-module secondary in the variant, don't drop it.
2. **Variant gate (cheap; likely $0 API): author-space suppressed-pair
   census on financial/infosec discourse.** Tickers/CVE-IDs are REGEXABLE —
   the gate needs a corpus pull but no LLM extraction. Measure suppressed
   count + formation rate in author space; calibrated thresholds now exist:
   science 67% / HN-authors ~20% / HN-threads 0.6%. Science-like or
   HN-author-like => variant graduates to a registered run; thread-like =>
   dead. Corpus candidates: Reddit finance/netsec, StockTwits, oss-security.
3. **If 1 or 2 pays: build the detector as a standing screen** (cron
   pipeline emitting the ~few-hundred-pair watchlist + formation tracking),
   and/or the Foundry play: LLM writes the connective content for flagged
   pairs — a 1-in-5 early-hit rate needs no ranking.
4. Write-up is now publishable-grade (passed positive control + "gaps close
   in people, not rooms" lens result) — optional credibility asset.
- Still banked: paraphrase-verdict dataset (claim-matcher training);
  Uzzi-Jones story-success flip; atlas trend analyses.
- Do NOT: chase within-set ranking (dead on three corpora); pay for the
  20-yr extraction before the detector proves value on 1–2.
