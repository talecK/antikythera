# Handoff — state of the Antikythera project (2026-08-30, RE-REVISED 2026-08-30 evening)

## PAPER PROGRAM HANDOFF (2026-09-01) — READ THIS FIRST FOR PAPER 1 / PAPER 2 WORK
## Consolidates a multi-session day; one new session should own both
## papers from here. Everything below the next "## Status" banner is the
## pre-paper project history and is still accurate for the machinery.

### Where the papers stand
- **Paper 1** ("The gaps that don't close"), reports/paper1_draft.md, last
  commit ddb7e29. Results FINAL (all numbers v2-regenerated, adversarially
  audited). Today: prose-only passes (abstract accessibility 6c8ae76, body
  long-sentence splits 086843c, "walled" defined at first use in 6.2), then
  another session resolved all [verify] DOI tags and added a
  competing-interests statement (ddb7e29). Header still says "awaiting
  author prose pass" — that is the only substantive open item.
- **Paper 2** ("Watching the walls go up"), reports/paper2_draft.md, v0.3,
  last commit 51c8441 (repo HEAD 468e859). Registered study, all numbers
  from the conforming run (21a9dc7); P1+P2+P3 PASS, onset 2021-04-01,
  excursion +28.6/+30.9 placebo-armored, DD walled through the squeeze.
  Drafted today from reports/paper2_results.md (operative), section by
  section, then: prose passes (no em-dashes, conventional register,
  accessible; abstract iterated with owner to grade-school register on
  the mechanism sentences); Sec 2.1 Related Work (four literatures, 11
  web-verified refs); anchor sources promoted into inline citations +
  reference entries (Sec 4.5; A5 date pinned 2021-02-27 via HN 26281147;
  A8 introduction date still unpinned); figures p2_fig1-3 produced
  (eval/make_paper2_figs.py, from committed TSVs only; placebo reps
  committed as reports/paper2_placebo_reps.tsv). Registration, results
  doc, and eval code were NOT modified at any point.
- **Paper 3** (absentia, ../absentia): not touched by this session; last
  known state in memory is "REGISTERED 823c479, H2 evals starting".

### Review artifacts (phone-readable, private, figures embedded)
- Paper 1: https://claude.ai/code/artifact/b6e82250-dc7e-42d1-9421-64eff6faeda9
- Paper 2: https://claude.ai/code/artifact/34b0ab8e-c6bd-48b2-af90-8d5874de0ba7
- Regenerate after ANY draft edit (markdown is the source of record):
  `python3 eval/render_paper_html.py paper2 --out <scratch>/paper2_draft_artifact.html`
  then republish with the Artifact tool passing the URL above as `url`
  (updates in place). Same for paper1. Pages cross-link in their headers.

### Outstanding before preprint-ready
Paper 2: (1) owner prose pass; (2) four DOIs tagged [verify] in the
references (Pedersen 2022 JFE; Watts 2002; Centola & Macy 2007;
Bikhchandani et al. 1992) plus a check for a journal version of Semenova
& Winkler (arXiv:2104.01847); (3) typeset to PDF with table numbering
(tables are unnumbered inline); (4) packaging only: A8 Wayback pass over
the subreddit rules page, contemporaneous April-2020 source for A1
(currently Forbes 2023 retrospective); (5) the paper-1 reference must
become paper 1's SocArXiv DOI at posting; (6) owner call: Figure 1 DD
panel has its own y-scale (shared x + chance band); one-line change to
share y. Estimate: ~half a day of mechanical work after the prose pass.
Paper 1: owner prose pass; typeset; one consistency sentence to check
(abstract "2006 to 2026" vs Sec 3.1 "active since 2007").

### Rules that bound today's edits (keep them)
- Owner prose rules: no em-dashes or AI-tell phrasing; conventional paper
  structure; accessible language, abstracts near grade 6-9, tested by
  paraphrasing as a layman. Abstracts carry findings only — procedural
  deviations, methods detail, provenance clauses live in the body.
- Paper 1 is final on results: cite, never reopen. Paper 2's registration,
  results doc, and eval code are frozen; drafts only.
- Every number traces to a committed artifact (paper 2 has a provenance
  table); prose passes never touch numbers, verdicts, tables, quoted
  registered language, or disclosure terms.
- Public-quote cautions (for outreach text, pre-review): keep the z-first
  framing (formation counts and their binomial p are secondary, no bar);
  "only above-chance excursion" always with "in this program"; Sec 6.2
  cascade-susceptibility sentences ("substrate", "scar") are labeled
  speculative and must carry the label; Sec 2.1 novelty sentence is
  unreviewed; quote the V4 disclosure whole or not at all; pair the
  conclusion's "the community that cascaded was the one without walls"
  with the abstract's hedge ("can say when the walls went up, but not the
  exact mechanism that built them").

### Outreach plan (from the outreach session antikythera-17, 2026-09-01;
### owner decides)
Both preprints to SocArXiv together (mutual citation), paper 2 to Hacker
News first with the post quoting the paper's own hedge line, paper 1 to
HN one to two weeks later. A lay-summary paragraph does not exist in
either draft and needs writing (outreach session drafts, paper session
fact-checks numbers, owner signs off, prose rules apply).

### Pending owner decisions
1. Ownership of paper_1 (original session gone from the bus; this session
   edited it under per-change approval).
2. Whether talecK/antikythera goes public at preprint time (both papers
   currently say "private during review; public at publication"; an HN
   thread will ask for it).

### Session hygiene
Multiple sessions touched the repo today (paper_1, paper_2, outreach
antikythera-17, plus this one). Working tree is clean at 468e859; nothing
is uncommitted or session-local except the rendered artifact HTML, which
the script regenerates. A new session picking up both papers needs only
this block, the two drafts, and the memory files.

## Status: FINAL on HN (run 8, registered 63b72d9). Under a
## shuffle-calibrated criterion there is NO above-chance gap formation in
## either space (author 3/364 & 1/110 vs ~1% floor; thread 20/25,161 &
## 11/7,505 — all at/below floor). The z>=2 criterion that produced every
## earlier positive HN rate (19-24%, 23.1%, 0.6%) is anti-conservative
## under doc-size heterogeneity (R1 placebo). CORRECTION (2026-08-30
## late): science's 67% is NOT z-criterion-based — it is benchmark
## edge-existence ground truth, so it is uncontaminated but was never
## comparable to the HN rates; the ladder was ill-posed, not merely
## miscalibrated (see report correction). The REAL
## finding, registered bar met at z=-9 (author) and z=-124/-162 (thread):
## suppressed pairs co-mention BELOW chance — segregation persists; gaps
## actively stay open. Detector/Foundry: CLOSED on HN. Thread-lens kill:
## STRENGTHENED. Tier A control: stands (harness fidelity, not criterion
## calibration). Gate: Q1/Q2 amended to the calibrated criterion
## (outcome-blind procedure registered in preregistration_run8.md) and
## UNBLOCKED — it now asks whether Reddit finance shows above-chance
## formation where HN shows none.

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
3. **Run 8 DONE (registered 63b72d9, results in reports/pilot1_runs.md)**:
   calibrated formation at/below the 1% false-positive floor in all four
   HN cells — the author-lens revival is closed for good, and the
   thread-space kill is strengthened (thread co-mention runs at ~1/4 of
   chance). Sub-chance persistence bar MET decisively: author z=-9.2/-9.3,
   thread z=-162/-124. Gate Q1/Q2 amended to the calibrated criterion per
   the outcome-blind procedure and unblocked. Science4Cast's 67%:
   corrected 2026-08-30 late — it is benchmark edge-existence ground
   truth, not z-criterion, hence uncontaminated but incommensurable with
   HN rates; whether it is mechanical under a shuffle null is untested
   and absentia's remit.

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
0. **DONE — Run 8 (see status banner).** No above-chance formation on HN
   in either space; segregation-persistence claim registered-met. The
   retired HN rates (19-24%, 23.1%, 0.6%) must never be quoted except
   as examples of the criterion trap; the science 67% is a different
   event (benchmark edge existence) and must never be compared to them.
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
2. **Variant gate: COMPLETE (v2, 2026-08-31).** Ran, was adversarially
   reviewed (reports/adversarial_review_2026-08-31.md), and was re-run on
   a deterministic harness with registered exclusions enforced — the v2
   table in reports/pilot1_runs.md supersedes all earlier gate numbers.
   Q1 null both folds (variant DEAD, MDR 3.7%/1.8%); Q1b segregation
   replicates (ALL/union -8.8/-17.7); WSB split regime-dependent (fold A
   at chance z=-0.1 even doc-matched, fold B segregated -9.0/-5.2
   subsampled); paper 2 (seed doc reports/paper2_seed.md) owns the
   transition question.
3. **Detector/standing-screen and Foundry plays: CLOSED on HN** (no
   above-chance event to detect). Revivable only by a gate pass.
4. Write-up (paper 1) is READY to draft and the story is now complete:
   certified thread-space negative -> criterion trap manufactures an
   author-space revival -> registered placebo catches it -> calibrated
   re-measurement finds the true regularity, sub-chance persistence
   ("the gaps that don't close", z -9 author / -124 to -162 thread).
   Methods contribution: the label-shuffle placebo as a mandatory control
   for co-occurrence formation claims; likely contaminates published
   results elsewhere (absentia tests the flagship case).
- Still banked: paraphrase-verdict dataset (claim-matcher training);
  Uzzi-Jones story-success flip; atlas trend analyses.
- SPUN OFF (2026-08-30): the Science4Cast critique (Tier A finding 1 —
  celebrated signal = popularity+closure) is now its own paper project at
  `../absentia` (prereg DRAFT there; reads this repo's Tier A data via
  symlink, treat `data/science4cast/` as shared read-only).
- Do NOT: chase within-set ranking (dead on three corpora); pay for the
  20-yr extraction before the detector proves value on 1–2.
