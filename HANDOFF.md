# Handoff — state of the Antikythera project (2026-08-30, RE-REVISED 2026-08-30 evening)

## PAPER PROGRAM HANDOFF (2026-09-01) — READ THIS FIRST FOR PAPER 1 / PAPER 2 WORK
## Consolidates a multi-session day; one new session should own both
## papers from here. Everything below the next "## Status" banner is the
## pre-paper project history and is still accurate for the machinery.

### Term pass and lint (2026-09-02 evening)
- Both drafts passed through a mechanical jargon audit: 383 terms
  classified in reports/term_table.tsv (S/D/Q/R), 71 replaced, glosses
  added at first use, 20 overloaded sentences split (39a7aa1 paper 1,
  next commit paper 2). eval/term_lint.py all must report 0 failures
  before any render; a new term needs a table row. Artifacts and
  preprint PDFs regenerated after the pass.

### Data release v1 (2026-09-02, built, awaiting owner publish)
- Folder: data/release/v1 (symlink to the NVMe; 194 MB, 17 files).
  Built by pipeline/build_release.py (read-only over sources, refuses
  overwrites, source SHA-256 before/after all matched). Contents: the
  paper-2 ticker panel with authors replaced by a salted hash
  (11,200,484 rows, 976,889 authors, 6,623 tickers), the six HN atlas
  tables, the six paper-2 registered-run TSVs, stats.json, checksums,
  README.md (= reports/data_release_v1.md), zenodo_metadata.json
  (= reports/zenodo_metadata_v1.json).
- Salt: private/release_salt.txt (gitignored, mode 600). Losing it
  means later versions get new hashes; disclosed in the datasheet.
- 2026-09-02 evening: Zenodo and ORCID accounts made (email signup;
  GitHub integration not needed). Reserved DOI 10.5281/zenodo.22262036
  and ORCID 0009-0001-9034-5533 inserted into both papers (author line
  and Data availability), the datasheet, and the metadata; both
  artifacts republished. Flat upload staging at
  data/release/v1_zenodo_upload (8 files: panel parquet, README,
  metadata, stats, two checksum files, hn_atlas.zip, paper2_runs.zip).
  Sensitive-string sweep done over every file including parquet
  columns and parquet metadata: one leak (local absolute paths in
  SOURCE_CHECKSUMS.txt) fixed and the script patched (6fd75f5); no
  staging-project names anywhere in the upload.
- BEFORE THE REPO FLIP: data/README.md names the GCP staging project
  (antikythera_hn under the staging project id); scrubbed 2026-09-03. Not in the
  deposit.
- PUBLISHED 2026-09-03 (Zenodo clock): https://doi.org/10.5281/zenodo.22262036
  resolves to https://zenodo.org/records/22262036, all 8 files, 202.9 MB,
  server MD5s verified against local copies, CC BY 4.0, ORCID attached.
  Related-works entry points at the GitHub repo (still private; resolves
  after the flip). Two related_identifiers (SocArXiv DOIs) still to add
  as a metadata-only edit after posting; no new version needed.
- Preprint PDFs built (cfd2f55 adds --preprint DATE to the render
  script: no banner, no draft-status block, no TOC, no private links;
  header carries the Zenodo DOI and code URL): data/release/preprints/
  quiring_2026_ideas_that_never_meet_preprint.pdf (26 pp) and
  quiring_2026_watching_the_walls_go_up_preprint.pdf (29 pp), plus
  socarxiv_submission_sheet.md (titles, abstracts, tags, links, order).
  Recipe: render --preprint, disable the dark media query, print with
  Chrome --headless=new --no-pdf-header-footer --print-to-pdf.
- SUBMITTED to SocArXiv 2026-09-03, both pending moderation:
  paper 1 https://osf.io/preprints/socarxiv/3h76g_v1, paper 2
  https://osf.io/preprints/socarxiv/s4gpb_v1. License CC BY 4.0; subjects
  Sociology > Communication, Information Technologies, and Media Sociology
  + Economic Sociology (SocArXiv's tree has no Computer Sciences branch);
  data = Zenodo DOI, preregistration = Both, linked to the GitHub repo.
  Repo flipped public the same day after the staging project id and local
  absolute paths were scrubbed from the tree (owner call: id stays in
  history; it names a deleted staging dataset, not a credential).
- APPROVED 2026-09-04 (both public): paper 1 doi:10.31235/osf.io/3h76g_v1,
  paper 2 doi:10.31235/osf.io/s4gpb_v1 (only the versioned DOIs resolve;
  the bare 10.31235/osf.io/XXXXX form 404s). Same day: DOIs cross-inserted
  (b8908f9; render_paper_html preprint header now carries own + companion
  DOI), PDFs regenerated (26/29 pp), v2 of each uploaded via Create New
  Version (3h76g_v2, s4gpb_v2, pending moderation; metadata carries over,
  only the file step is repeated), both Claude artifacts republished, and
  the Zenodo record given both DOIs as related works (isSupplementTo,
  Publication/Preprint; metadata-only edit, still version 1.0.0). The
  original plan below is DONE except the v2 approvals.
- NEXT: when the v2s clear moderation, nothing further is required; the
  _v1 DOIs cited in each paper keep resolving. Old plan for reference,
  after both DOIs arrive: insert each into the other paper's references,
  re-render, upload v2 of both, add both DOIs to the Zenodo record as
  related works (metadata-only edit). Then: DOI into both papers'
  Data availability and paper 2's paper-1 reference, re-render, post
  both preprints to SocArXiv, fill the two related_identifiers.
- Deferred to a later deposit version: per-document HN claim
  extractions with quotes and the hashed author-attribution table.
- Rollout decision (owner, 2026-09-02): ship what exists; the
  many-subreddit transition survey and cohort readout wait for mentor
  or early feedback. Headline wording unchanged by owner call.

### Where the papers stand
- **Paper 1** ("Ideas that never meet online mark divided communities,
  not future discoveries"), reports/paper1_draft.md, v0.3, last commit
  e7694ba. Results FINAL (all numbers v2-regenerated, adversarially
  audited). 2026-09-01 evening: the paper polish playbook applied in
  full, one owner-approved pass per commit: venue limits verified
  (EPJ Data Science first, QSS alternative, written to the Nature
  Communications shape; 300ad98); abstract 313 -> 200 words on the
  template (f59f3a3 .. 3c2c45a); journal structure (Introduction,
  Results with measurement summary and registered-predictions Table 1,
  Discussion without subheadings, Methods last, Funding, commit
  appendix; fcd1fe0); references Crossref-verified and raised 20 -> 37
  (431c02b); jargon renames and definitions (6b6a91c, d037329); title
  changed by a parallel session (c62dc0d); figures: schematic Figure 1
  (eval/make_paper1_schematic.py) and data figures restyled on
  eval/paper2_figstyle.py, renumbered 2-4 (b2ebfd2, f4c9603); body
  read-aloud pass (45d0e71) and mannered-prose scan (62187ce). Main
  text 4,464 words, Methods 1,250, abstract 200, 4 figures, 3 tables.
  2026-09-02: external lay-reader pass (44 comments, 22 issues) applied
  as twelve wording edits (840815e); ecology null-model paragraph
  rewritten in plain terms and its overclaims removed here and in the
  Discussion cascade (9b520f1); ten literature characterizations
  corrected in both papers, one factual (Aghajohari et al. 2021 placed
  third, not first), Cinelli 2021 no longer cited for Reddit, LBD
  described as Swanson's shared-intermediate linkage with the
  eligibility rule stated as ours, Rzhetsky et al. 2015 added,
  Kleinberg 2003 removed (e7694ba; both verified against sources).
  Reviewer PDF path recorded in the playbook (render script + headless
  Chrome with the dark media query disabled); the Google Docs import
  truncates Table 1 and downsamples figures, do not use it. Table 1's
  registered readings still say "machinery" (quoted registered
  language, untouched). Results and Discussion have had no direct
  lay read yet.
  Open: typeset to PDF; keywords and an abbreviation list at
  submission; the private repository must be public (or a Zenodo
  deposit made) before posting; Acknowledgements "Not applicable" for
  EPJ at submission.
- **Paper 2** ("Watching the walls go up: r/wallstreetbets segregated after
  the GameStop squeeze"), reports/paper2_draft.md, v0.5, last commit 4d6bd9e
  (2026-09-02: intro Cinelli/Waller attribution and LBD description
  corrected with paper 1, "among the most stable features" dropped,
  cascade "seen in" -> "analogous to" e7694ba; "machinery" ->
  "instrument" at all sites and "eligible (we also call it suppressed)"
  to match paper 1, 4d6bd9e). Before that: last commit d684971
  (2026-09-01 evening: title trimmed b185aab, shuffle-null shorthand to
  standard phrasing 15c87a7, regime change wording 6ce2064, schematic
  panel c relaid 037309c, mannered-prose scan d684971). Earlier: v0.4,
  last commit 912859a. 2026-09-01 (this session): owner prose pass on
  the abstract (389 -> 198 words, unreferenced, Nature Communications
  template, general-implication closing sentence); declarative title
  (14 words); hedge line moved into the Conclusion paragraph; whole
  draft restructured to journal format (Introduction / Results /
  Discussion / Methods, Data + Code availability, Competing interests,
  Author contributions, standalone figure legends, provenance appendix),
  measurement-summary and predictions-table subsections added at the top
  of Results, four background refs added with [verify] DOIs. Venue plan
  revised: Nature Communications first (limits verified 2026-09-01:
  abstract 200, main text 5,000 excl. Methods, Methods <3,000, 70 refs,
  10 display items), PNAS Nexus alongside, EPJ DS floor; Nature Human
  Behaviour dropped as reach (needs a mechanism claim the paper declines
  to make). Same file serves SocArXiv. Later the same day: figures restyled on a shared
  style module with a validated palette and 64x48 px padding
  (eval/paper2_figstyle.py; owner markup rounds); jargon passes done
  (gate/bar/ladder/frozen/provenance and 20 more, each owner-approved).
  The whole process is written up as reports/paper_polish_playbook.md,
  the spec for applying the same passes to paper 1 in a new session.
  Schematic Figure 1 DONE (cdbb5d8,
  eval/make_paper2_schematic.py; old figures now 2-4); body prose pass
  DONE; all DOIs Crossref-verified, Semenova & Winkler cited to its 2025
  Quantitative Finance version. Earlier state, superseded but true of the machinery:
  v0.3 at 51c8441 (repo HEAD 468e859). Registered study, all numbers
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
Paper 2 (state at v0.5, e2c5c35+): prose, jargon and figure passes DONE;
all DOIs Crossref-verified, no [verify] tags left; tables numbered 1-7;
Figure 2 DD panel shares panel a's y-scale (owner call). A8 FINDING
(2026-09-01, post-registration, disclosed in Methods/Discussion/Intro):
Wayback captures of the WSB rules page show the sub-$1B market-cap
clause ABSENT on 2020-09-12 and PRESENT by 2021-01-22, i.e. A8 predates
the squeeze and is not a post-squeeze governance change; registered
anchor list and discrimination reading left as committed; no verdict
affected. A1 still cites the 2023 retrospective plus the pre-lawsuit
Forbes 2021-01-28 interview (paywalled); no 2020-dated article found in
four searches. Remaining before submission: (3) typeset to PDF; (4) A1 contemporaneous 2020 source if one turns up;
(5) the paper-1 reference must become paper 1's SocArXiv DOI at posting;
(6) confirm Nature Communications APC and read its human-behaviour
reporting page. Everything else is done.
Paper 1: typeset to PDF (reviewer copy path in the playbook, 2026-09-02
section); a second lay read of Results and Discussion on that PDF;
submission-time keywords, abbreviation list, Acknowledgements line;
repository public or Zenodo DOI before posting.
(The 2006/2007 consistency check is dissolved. 2026-09-02: the
"twenty years" claim itself was wrong and is corrected at cae7c38:
concept extraction and both folds cover 2015-2017 only, the extraction
cache and pipeline/build_author_concepts.py both filter to those
years; Methods now says so, and the program-level span is stated as
2015 to 2024 across two platforms. Paper 2's one echo of the claim is
corrected in the same pass.)

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
The full plan (named targets, send order, venue choices) is
people-related and kept OUT of version control in private/ (gitignored)
so it never enters a history that goes public at publication. Paper-3
note above is stale: absentia Stage 0 is done, H2 table ~a day from
2026-09-01, private remote created at github.com/talecK/absentia the
same day.

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
   64-core Vultr box (key: ~/.config/antikythera/vultr.env; bootstrap script
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
