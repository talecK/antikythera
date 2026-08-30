# Handoff — state of the Antikythera project (2026-08-30, RE-REVISED 2026-08-30 evening)

## Status: author-lens revision ITSELF REVISED by registered placebo (R1,
## reports/pilot1_runs.md "Robustness suite"). The 19-24% author-space
## formation rate is BELOW its mechanical (label-shuffle) floor of 34-47%:
## the z>=2 criterion is anti-conservative under doc-size heterogeneity.
## No current evidence that individuals bridge suppressed pairs at
## enriched rates. Detector claim SUSPENDED pending run 8
## (shuffle-calibrated formation criterion + ladder recalibration).
## Thread-lens kill stands. Tier A positive control stands (harness
## faithfully finds planted signal; criterion calibration is a separate
## defect). Gate MUST NOT flip to REGISTERED until Q1 bars are re-derived
## under the corrected criterion.

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

### RE-REVISION (2026-08-30 evening — registered robustness suite R1-R4,
### preregistration_robustness.md 31bc9ab; results in reports/pilot1_runs.md)
1. **R1 placebo FAILED against the frozen bar, in the strong direction**:
   an eval-window label shuffle (doc sizes + concept totals preserved)
   "forms" 124.6/364 and 52.0/110 suppressed pairs on average — the
   observed 70 and 26 are 6.1 and 5.3 sd BELOW the mechanical null. The
   z>=2 formation criterion under-counts chance co-mention when doc sizes
   are heterogeneous. Points 2-3 above are accordingly SUSPENDED: the
   19-24% rate is not bridging enrichment, and the 1-in-5-vs-1-in-160
   detector arithmetic is criterion-confounded (thread-space needs its own
   shuffle null before any ratio is quoted).
2. **What survives**: author-space structural density (census numbers are
   outcome-free); segregation persistence (suppressed pairs co-mention
   LESS than chance — a real, negative-direction regularity); R3's
   articulation pattern (77% of formed pairs never articulated in-cache;
   co-mention precedes articulation 12/22, trails 4/22); R2/R4 show the
   measured rate is not a window or attribution artifact — the defect is
   the criterion, not the plumbing.
3. **Mandatory before anything else runs: run 8** — shuffle-calibrated
   formation (per-pair null from the label shuffle), recomputed in author
   AND thread space, ladder recalibrated (science rung = absentia's
   remit). The Reddit gate's Q1 bars are uninterpretable as drafted and
   the gate must not flip to REGISTERED until re-derived.

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

## Next steps (RE-REVISED 2026-08-30 evening; ordered by information per dollar)
0. **Run 8 FIRST (blocks everything below): shuffle-calibrated formation.**
   Register: pair forms iff observed eval co-mention exceeds its own
   label-shuffle null (p99, R=100), recomputed in author AND thread space,
   both folds. Recalibrate the ladder; re-derive gate Q1 bars. Until then
   the 19-24%, 23.1%, 0.6%, and 67% numbers must not be quoted as rates
   ("R1 placebo failed" is the honest one-liner). Science4Cast rung is
   absentia's remit — flag it to that repo.
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
2. **Variant gate: ON HOLD at DRAFT pending run 8.** Acquisition/census
   may continue (outcome-blind); Q1 interpretation bars and the calibration
   ladder in preregistration_gate.md are stale as written and must be
   re-derived under the corrected criterion before STATUS flips to
   REGISTERED. Corpus and units sections remain valid.
3. **Detector/standing-screen and Foundry plays: SUSPENDED** until run 8
   re-establishes (or kills) an above-chance formation event. The 1-in-5
   arithmetic is criterion-confounded; do not quote it.
4. Write-up: still viable but the story changed — now "certified negative
   + a measurement-criterion trap that manufactured a false revival, caught
   by a registered placebo." Arguably a stronger methods paper; the "gaps
   close in people, not rooms" headline is withdrawn unless run 8 revives
   a calibrated version of it.
- Still banked: paraphrase-verdict dataset (claim-matcher training);
  Uzzi-Jones story-success flip; atlas trend analyses.
- SPUN OFF (2026-08-30): the Science4Cast critique (Tier A finding 1 —
  celebrated signal = popularity+closure) is now its own paper project at
  `../absentia` (prereg DRAFT there; reads this repo's Tier A data via
  symlink, treat `data/science4cast/` as shared read-only).
- Do NOT: chase within-set ranking (dead on three corpora); pay for the
  20-yr extraction before the detector proves value on 1–2.
