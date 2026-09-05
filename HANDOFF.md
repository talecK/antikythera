# Extension sleep delay corrected — 2026-09-04 23:36 Pacific

A status check found the MBP entering maintenance sleep despite the
original caffeinate -i assertion. pmset directly recorded a 612-second
sleep from23:22:37 to23:32:49 and other short maintenance transitions.
Both workers remained intact and resumed; no result or chain was restarted.

Added a run-scoped AC system-sleep assertion, caffeinate -isu -w40239,
PID40399. Readback confirmed PreventSystemSleep=1. MBP is on AC, lid open.
The additional assertion exits with the queue; no permanent power setting
was changed. Operational record:
reports/curveball_extension1_power_recovery.json.

Because macOS monotonic time pauses during system sleep, an external
UTC wall guard (PID40400) now enforces the ORIGINAL deadline of
2026-09-05T12:21:31.528183Z (05:21 Pacific), without changing scientific
source hashes or extending the registered budget. It checks exact queue
PID/command and only terminates that queue and its own worker children
at deadline, preserving existing artifacts. Code:
eval/curveball_extension_wall_guard.py (MBP executes identical bytes from
work/curveball_extension_wall_guard.py). Remote runtime record:
reports/curveball_extension1_wall_guard.json. Inspect that record alongside
the queue manifest: a wall-budget stop may leave the queue manifest RUNNING
and the last stage partial; treat those as resource-limited, never passing.

At recovery both workers were still on WSB_03 extension pilots. No
extension result had completed. Paper1 remains independently verified.
Keep the MBP on AC and awake; do not change scientific sources mid-run.

---

# Paper 1 substantive rewrite plan saved for next session

The user agreed that Paper 1 needs a substantive rewrite in light of the
completed tests, and requested a written plan for a new session. Read
reports/paper1_rewrite_plan.md for the agreed approach, evidence boundaries,
original-PDF comparison baseline, prior-art finding, known inconsistencies,
deliverables and acceptance checks. The manuscript rewrite has NOT been
performed in this planning session. Current prose still mixes old definitive
discovery claims with robust aggregate results and unresolved pair formation.

The plan is documentation only; it does not change scientific results or
authorize publication or additional compute. Existing Paper 2 operations are
separate. The operational status below was NOT reverified during this planning
session; check current evidence before acting on its RUNNING banner.

---

# LIVE bounded Paper 2 extension — verified 2026-09-04 23:21 Pacific

The single registered extension is NOW RUNNING on native ARM MBP.
SSH andrej@Kevins-MacBook-Pro.local; checkout
/Users/andrej/workspace/antikythera. Started 2026-09-05T06:21:31Z.
Parent PID40239, workers40246/40247; ps and queue manifest verify active
work on p2_WSB_03 N2/N3. Command: caffeinate -i .venv/bin/python
 eval/run_curveball_extension.py. Sampling code commit:
4a43dae0916b4bfa7abc8adc1cd5e0e69c06ea68. Registration was committed
before launch at62539a6, then merged with completed MBP first-pass history.
Both machines' main were consolidated and pushed at4a43dae before launch.

Native preflight verified44 exact jobs and pinned environment; all four
extension synthetic tests passed on MBP. Launch/provenance evidence:
reports/curveball_extension1_launch.json. Runtime log on MBP:
logs/curveball_extension1_queue.log, per-job logs
logs/curveball_extension1_<cell>_<null>.log. Queue manifest:
reports/curveball_extension1_queue.json. New raw arrays under
 data/registry/nulls_revisions/curveball_extension1/.

Two workers; 21600-second sampling wall budget from launch, nominal cutoff
2026-09-05T12:21:31Z (05:21 Pacific), plus recorded finalization overhead.
Per-case cap5400seconds. Budget expiry/remaining diagnostic failures stay
unresolved. No second extension, Paper1 formation sampling or FDR project.
Do not alter MBP scientific code/registration or pull M1 documentation
updates during this run. M1 does verification and manuscripts only.

Both first-pass audits and Paper1 scoring are COMPLETE. Paper1 Xd PASS
under both nulls; Xe UNRESOLVED under both. Table5 records verified results.
Paper2 original first-pass scores are preserved; extension score tool is
 eval/score_curveball_extension.py. Next: inspect native extended-pilot
progress, transfer/hash-verify finished extension outputs, independently
recompute stage diagnostics/moments before scientific scoring, then finish
both papers and final visual QA. The existing first-pass verifier needs
an explicit extension path for production with formation NOT_EVALUATED;
do not mislabel that as a failed formation test or pool pilot arrays.
No preprints/outreach or absentia/H2 changes are authorized.

MBP GitHub read access works but its push lacks credentials. Consolidation
was completed by transferring its incremental git bundle over authorized
SSH to M1 and pushing from M1. Do not request passwords or copy credentials.

---

# Single bounded Paper 2 extension prepared — 2026-09-04 Pacific

Both full first-pass audits are complete: Paper 1 104 files, Paper 2 968
files, with raw stage diagnostics/moments/formation checks recomputed and
all frozen input/census/code/matrix hashes verified. Paper 2: 13 N2 and
19 N3 passing cells; 25 N2 and 19 N3 unresolved. The first-pass queue
finished all 84 attempts. Final queue snapshot:
reports/curveball_first_pass_completed_queue.json. All original first-pass
predictions/results remain unchanged; Xa/Xb/Xc are unresolved, Xd passes,
Xe remains unresolved for both nulls.

The user accepted one bounded Paper 2 extension, then no further large
compute except correction of a demonstrated implementation error. Protocol:
preregistration_nulls_extension1.md. Exact 44-job plan:
reports/curveball_extension1_plan.json. Commit both before any real chain.
New driver eval/run_curveball_extension.py reuses the original Ensemble,
kernel and diagnostic implementation unchanged. Fresh extension1 seed
phase names; pilot 1760/3520/7040 with candidate burns80/160/320/640;
fresh production800/1600/3200, burn twice selected pilot burn. Two workers,
six-hour global sampling wall limit, 90 minutes per case; resource-truncated
stages cannot pass. First-pass passing cells are not rerun. No new Paper 1
sampling or formation/FDR work. Four synthetic extension tests pass,
including budget exits and an actual native-kernel pilot/production check.

The extension has NOT yet started at this checkpoint. Next: consolidate
MBP's completed report changes with this main, verify native environment,
run its preflight and four extension tests, then launch detached with
caffeinate. Save launch/process evidence, and do not alter scientific
sources in the MBP checkout during the extension. Score only its passing
production, combined with passing first-pass cells, via
 eval/score_curveball_extension.py. Keep original first-pass scores separate.

---

# Paper 1 independently verified; first-pass queue complete — 2026-09-04

The MBP manifest directly reports COMPLETE, 84/84 registered cell/null
attempts. It has NOT started an extension. M1 Paper 1 verification is
COMPLETE: all 104 transferred files and all raw moments/stage diagnostics/
formation checks match. Durable audit:
reports/paper1_curveball_verification.json; verifier:
eval/verify_curveball_results.py. X-d PASS under both N2 and N3; X-e
UNRESOLVED under both. Seven of eight formation checks are unresolved;
N3 author fold2 passes with zero formed pairs. Paper 1 Table 5 now records
these results. Original reports and failures remain intact.

The user accepted this remaining compute plan: one prospectively registered
bounded extension for Paper 2 unresolved cases, then no further large
compute unless a demonstrated implementation error requires correction.
No extra Paper 1 sampling solely for formation precision; no new FDR
project. Qualify those claims in the revision. Proposed Paper 2 extension
budget is roughly 4-6 MBP hours; define exact rules and commit before any
new chain. Do not describe that extension as running yet.

Next: transfer/hash-verify all finished Paper 2 arrays/reports, inspect
diagnostic failures, implement/validate and register the single bounded
extension, execute it on MBP with exclusive ownership, then finish both
manuscripts and final visual QA. Both papers remain unreleased. SSH/rsync
access and merged-main consolidation remain authorized. Do not touch
absentia/H2 or contact anyone. See prior block for host/path details.

---

# LIVE MBP Curveball queue — verified 2026-09-04 21:53 Pacific

The network transfer and native restart are COMPLETE. SSH access:
andrej@Kevins-MacBook-Pro.local; checkout:
/Users/andrej/workspace/antikythera. Main was safely fast-forwarded to
83760dec39c0322a4780461081f2025496410434 before launch. User's historical
notes are preserved as documented below; untracked logs/reference remain.

MBP queue started at 2026-09-05T04:53:29Z, PID 38106; workers 38114/38115.
Direct ps and live logs verify active computation in p2_WSB_04 under
both N2 and N3. Three completed cell attempts per null were hash-verified
and skipped, including unresolved attempts. Native arm64 Python 3.14.6,
numpy 2.5.2 and duckdb 1.5.5. Hardware directly verified: M3 Max, 14
physical cores, 36 GiB memory. Two workers as registered; no additional
M1 queue or duplicate MBP jobs. Transfer preflight verified 172 repository
files, 56 payload files and 26 required inputs; 53 missing payload files
installed, 3 existing identical files retained. Four kernel, five pipeline
and two result-verification tests passed natively before launch.

Command: caffeinate -i .venv/bin/python eval/run_curveball_queue.py
--cells all --workers 2. Remote aggregate log:
logs/curveball_queue_mbp_v1.log; remote per-cell logs:
logs/curveball_<cell>_<N2|N3>.log. Queue manifest:
reports/curveball_queue_v1.json. M1 copy of launch/test/environment evidence:
reports/curveball_mbp_launch.json. Process is detached from SSH and has
caffeinate. Do not modify MBP scientific code or registration while it runs.
Do not pull M1 documentation checkpoints into the live MBP checkout.

Next: inspect actual native pilot timings for a fresh ETA, verify and
incorporate finished remote outputs using hashes, finish literal scoring,
then complete manuscript revisions. Completed unresolved cells still
require a separate prospective extension before any retry. No preprint
publication/outreach is authorized. Local M1 remains available for review
and manuscripts, not duplicate sampling. SSH and rsync are authorized.

---

# MBP connection verified and transfer in progress — 2026-09-04 21:54 Pacific

SSH access is now verified at andrej@Kevins-MacBook-Pro.local, checkout
/Users/andrej/workspace/antikythera. A direct process inspection found no
Antikythera queue/evaluation jobs running. Its .venv is native arm64,
Python 3.14.6, numpy 2.5.2 and duckdb 1.5.5. This supersedes the earlier
user-reported-only idle status. M1 Antikythera remains stopped.

The MBP had uncommitted historical reproduction notes in pilot1_runs.md.
They were copied and hash-verified on both machines, preserved as a git
stash on MBP, and incorporated verbatim in
reports/m3_historical_reproduction_gate_notes.md. Its untracked logs/ and
reference/ remain untouched. No original notes were discarded.

The user authorized merged main and network rsync. Consolidated main was
pushed at 2e5de10; this follow-up preserves recovered historical notes.
Next: safely fast-forward MBP main, rsync the verified transfer directory,
run native preflight and tests, then launch the registered two-worker
queue. Do not claim it started until process/log evidence confirms it.

---

# Consolidated main and direct transfer authorized — 2026-09-04

The user requested merging current code/reports/draft revisions onto main
while both Antikythera queues are idle, and authorized rsync of project
data to MBP as needed. M1 process exit is verified; MBP idle remains
user-reported until connection/remote checks. No saved SSH alias was
found; the MBP SSH address and checkout path have been requested.
Do not infer an address or claim remote execution before verification.

All completed M3 artifacts have been verified and merged locally. Current
N2/N3 outcomes and failed/aborted stages are preserved. The active work
is consolidating/pushing main and arranging the data transfer/native MBP
restart. No public preprint upload or external contact is authorized.

---

# M1 stopped for immediate MBP transfer — 2026-09-04 21:41 Pacific

User explicitly requested killing the current cell and restarting on MBP.
Queue parent 8428 and its workers 8436/8437 received SIGTERM; ps verified
all three exited. No other project/process was signaled. No M1 N2/N3
computation remains active. Do not restart it on M1 or duplicate MBP work.

Both interrupted WSB_04 attempts are preserved under
reports/curveball_interrupted_m1_20260905/ and the matching ignored raw
subdirectory. reports/curveball_m1_interruption.json maps every original
path to its archived path and SHA256. All 12 moved files were verified
byte-identical. Charge 1045.829384 worker-seconds to the global budget;
the queue now includes interruption ledger time automatically. Scientific
kernel, seeds, diagnostics, sampling limits and registration are unchanged.
Restart only this interrupted cell, with original seeds; do not retry the
completed UNRESOLVED cells absent a prospective extension registration.

A transfer bundle is being prepared in work/m1_curveball_handoff and
will be delivered in Downloads/m1-curveball-handoff.tar.gz. It includes
an incremental git bundle based on b84435b, all existing Curveball raw
artifacts/matrices, a checksum manifest and a complete MBP prompt.
The user now requests consolidating current work on merged main. The
MBP should sync that main before starting, use native ARM and pinned
versions, and isolate subsequent results on a new results branch if useful. Verify the bundle, input hashes and nine synthetic tests
before running the same 42-cell queue; completed attempts are verified
and skipped. The MBP has NOT yet been launched or directly contacted.

---

# MBP handoff boundary requested — 2026-09-04 21:41 Pacific

This operational update supersedes the queue scheduling status below.
The user is preparing to move N3 to MBP. SIGINT was sent ONLY to the M1
queue parent (PID 8428), whose ProcessPoolExecutor shutdown waits for its
active workers. Both workers continue p2_WSB_04 normally; no new cell
will be scheduled by this parent. Do not interrupt those workers or
start replacement jobs while this cell is active. Verify both final
cell reports and worker exit before preparing the remaining-cell manifest.
The queue manifest may omit this final cell because its parent was
interrupted while awaiting futures; use hash-verified per-cell reports
as completion evidence. Boundary request record:
reports/curveball_mbp_handoff_boundary.json.

Latest completed cell p2_WSB_03 is UNRESOLVED for BOTH N2 and N3 at
maximum pilot length, with no production. Preserve the failed stages;
pilot effect estimates cannot establish excursion robustness.
N3 first started 21:05:33 Pacific. Native ARM Python is installed on M1,
but the pinned .venv is Intel Python 3.14.6 and runs through Rosetta.
No replacement environment or MBP benchmark has been started. A hardware
move is distinct from any prospectively registered sampling extension.

---

# Active revision checkpoint — 2026-09-04 21:29 Pacific

This block supersedes the older session-transition checkpoint below.
The authorized M1 revision is IN PROGRESS; do not launch a duplicate queue.

- Checkout stays `/Users/andrej/workspace/antikythera`, local main. N2/N3
  registration was committed at 5215719 before any real-data chain;
  implementation/validation at f4e812b. First result and scoring work at
  8e55822. M3 results merged locally at d50d952. No M1 push or preprint
  publication has occurred in this session. Current uncommitted reports,
  manuscript/figure edits and diagnostics are intentional; preserve them.
- RUNNING: `caffeinate -i .venv/bin/python eval/run_curveball_queue.py
  --cells all --workers 2`, logs/curveball_queue_v1.log. Two independent
  null workers per serially prepared cell, all 42 cells x N2/N3. At this
  checkpoint it is evaluating WSB k=3, the first excursion cell. Per-null
  progress logs: logs/curveball_<cell>_<N2|N3>.log. The queue uses a shared
  lock under ignored data/registry/nulls_revisions/curveball_v1/. Do not
  edit the scientific source files or N2/N3 registration while this queue
  runs: source hashes are guarded before each cell and before production.
  Scoring, manuscript and figure files can be edited independently.
- Both first-cell production results passed aggregate diagnostics:
  p2_WSB_01 (eval 2020Q2-Q3) N2 z=-4.6546, ratio=.84327, 6400 draws;
  N3 z=-4.7421, ratio=.84657, 3200 draws. Pilot draws are excluded.
  N2 formation precision unresolved; N3 formation precision passes.
  This is a changed reading from original z~+1.5, not a reproduction.
- Second cell p2_WSB_02 N2: production passes, z=-2.97688, ratio=.82201,
  6400 draws; formation precision unresolved. N3 pilot failed at the
  maximum 880 sweeps per chain (total R-hat about 1.014); no production
  ran. This remains UNRESOLVED. Preserve failed stages. No thresholds or
  predictions have been relaxed; any further pilot-length/resource
  amendment must be prospective and preserve this attempt.
- All scientific predictions are fixed at the top of
  preregistration_nulls_n2.md; the historical DRAFT below is preserved,
  not operative. eval/score_curveball.py scores only hash-verified
  production results that pass diagnostics. Full-series predictions
  remain pending/unresolved; headline cells alone cannot settle onset.

## M3 is now verified artifact evidence

The user supplied pushed branch codex/m3-revision-results (1ca9817), then
/Users/andrej/Downloads/m3-thread-raw.tar.gz. Fetch/read occurred only on
M1, not in the MBP checkout. The six-file results commit has been merged
into local main at d50d952. Recorded code/input-manifest hashes and all
output hashes match. Both raw thread arrays were copied into ignored
local data/ at their manifest paths. The companion ignored JSON was
reconstructed from identical embedded report records and matches its
exact manifest hash. Independently recomputed pooled and all batch
means, SD, z, ratio, and formation counts. Full audit:
reports/m3_incorporation_verification.json. Earlier report-only audit
files are historical and superseded. No direct remote process telemetry
has been inspected; the manifest records all three assigned jobs complete.

R-a/R-b/T-a/T-b/T-c PASS. N1-d and D-b still FAIL. Machine-readable
scoring: reports/nulls_amendment_scores.json. Pooled thread z=-162.8774
and -124.2746, ratios .2500673/.2784329, formed 11/25161 and 9/7505.
Paper 2 R1000 excursions: label z=31.8441/33.6004; N1=18.0051/28.9301.
The raw NPZs, not averages of batch z, produce the primary estimates.

## Remaining work

- Let the registered local Curveball queue finish, inspect every failed
  stage and score predictions literally. Decide whether unresolved
  cells justify a further prospectively registered length extension;
  never silently rerun or relax criteria. Current real timing: small
  cells need several minutes per null; the first large excursion cell
  takes about .8 seconds per saved four-chain sweep. Re-estimate from
  matrix/phase timings; several more hours of local work are plausible,
  with HN thread counting cost not yet measured. No deadline was set.
- Both drafts have corrected nominal-count, control-specificity, onset
  date, statistic and margin descriptions, plus completed N1 and M3
  summaries. Result-dependent abstracts, tables and conclusions still
  need final N2/N3 findings. Paper 2 may need a substantive interpretation
  change if the prior nondetection regime is not robust.
- New schematic/formation figures use *_revision filenames; original
  figure files are untouched. Three figure PDFs were rendered with
  Poppler and visually checked after a heading-overlap correction.
  Current term lint: zero failures, nine stale-entry warnings.
  Full revised manuscript PDFs are NOT yet produced/visually checked.
  Local HTML previews are work/paper1_revision.html and
  work/paper2_revision.html (regenerate after edits).
- Diagnostic validation: four synthetic kernel tests + five pipeline
  tests; independent ArviZ 0.22.0 fixtures in tests/fixtures/. The
  reference environment lives in work/diagnostic_reference_env; original
  .venv stayed pinned and unchanged. Two result-verification tests pass.
- No absentia files or H2 jobs have been changed. No external outreach,
  revised preprint publication, or MBP workload duplication is authorized.

---

# Session transition checkpoint — 2026-09-04 20:42 Pacific

This is the latest operational checkpoint. Read it before the older
handoff blocks below. The user requested a clean handoff to a fresh
session while the MBP continues computing. No new scientific runs were
started during this checkpoint.

## Resume here

- Active M1 checkout: `/Users/andrej/workspace/antikythera`, branch `main`.
  Latest scientific/code commit is `f8013b4`, confirmed pushed to origin.
  The following checkpoint commit changes only this handoff.
- No Antikythera evaluation, Curveball, or queue process is running on
  the M1 at this checkpoint. Two Python H2 convergence processes were
  found, but their working directory is `/Users/andrej/workspace/absentia`;
  these belong to another project. Do not stop, modify, or duplicate them.
  Consider their CPU use before choosing local pilot worker counts.
- The user reports the M3 MBP is STILL RUNNING its assigned queue.
  That is user-reported status, not remotely inspected telemetry.
  No MBP queue results, logs, branch, or manifest have been received or
  inspected in this coordinating session. All new numerical findings
  below come from completed local M1 runs.
- The earlier app task inventory exposed only local tasks, not the MBP
  task/host. Do not claim direct communication with the MBP. Exchange
  completed reports via its separate results branch or user-provided
  artifacts. No messages have been sent to that task from here.
- Do not pull or alter code in the MBP checkout while its queue runs.
  The older “M3 pickup” instructions below apply only before queue start.
  M3 owns Paper 2 headline label R=1000, headline stratified R=1000,
  and Paper 1 thread 10 independent batches of R=100 with pooled output.
  Do not start duplicate copies on M1.
- Preserve the user-authorized takeover: continue revising both papers,
  implementing and testing necessary robustness work, and committing
  reproducible code/results. Historical “final / do not reopen” statements
  are superseded for this revision. Do not publish revised preprints yet.
  Do not contact external people. No outreach authorization was given.

## Completed and verified locally

Read `reports/nulls_amendment_scores.json` and the latest appendices of
`reports/pilot1_runs.md` for machine-readable scores and provenance.

1. Three-cell Paper 2 replay exactly matches all 16 published fields.
   All four Paper 1 eligible counts and observed totals also match.
   Audit: `reports/reproduction_audit_2026-09-04.tsv` and `.json`.
   Original frozen outputs/scripts have been preserved.
2. Paper 1 canonical label R=100 seed check: P1-b PASS, largest relative
   z change 7.46%. Outputs: `reports/paper1_nulls_label_R100.tsv/.json`.
3. Paper 2 N1 (quarter-stratified collapsed-label null), all 38 primary
   cells, R=100: complete in 1276.81 seconds. N1-a/b/c PASS; onset remains
   k=5, evaluation 2021Q2–Q3, with P1/P2/P3 passing. Excursion ratios are
   1.5687 and 1.6267 (z=19.6267 and 30.4467). N1-d FAILS in seven
   non-excursion WSB cells. The historical premise that every such cell
   was already below the nominal 1% formed-count reference was false;
   disclosed before N1 without changing the prediction. Output:
   `reports/paper2_windows_z_stratified_R100.tsv`.
4. Paper 1 N1 R=100: all four cells pass P1-a. Output:
   `reports/paper1_nulls_stratified_R100.tsv/.json`.
5. D-b FAILS because thread collapse is smaller than author collapse in
   both HN folds. WSB N1 collapse reaches about 13% in excursion cells.
   Exact binary-margin sensitivity therefore remains required.
6. Curveball has passed FOUR SYNTHETIC tests (exact five-state kernel,
   empirical native sampling, margins/counts/replay, fixed/empty cases).
   Log: `logs/takeover_curveball_tests.log`. Source:
   `eval/curveball_kernel.cpp`, `eval/curveball.py`,
   `tests/test_curveball.py`. Synthetic 588k-row benchmark is about
   2.72 million attempted trades/second; see
   `reports/curveball_synthetic_benchmark_m1.json`. This is NOT evidence
   of real-matrix mixing or an estimate of complete production runtime.

## Immediate next work — N2/N3 still require implementation

`preregistration_nulls_n2.md` is DRAFT. No real-data Curveball chain or
outcome has been run. Finish and commit the prospective pilot design
before running any real-data N2/N3, including pilot outcomes. Fix the
scientific predictions before the pilot too: known observed counts plus
pilot null means can already reveal effects. Do not claim blindness.

The current draft proposes four logical chains, candidate burn-in levels
5r/10r/20r/40r/80r, and sampling intervals r (per-quarter r_q for N3).
These are draft choices, not established mixing bounds. Still specify:
seed namespaces, valid dispersed initialization, diagnostic sample sizes,
stopping/doubling rules and maximum budget, rank/folded R-hat, effective
sample sizes and mean/SD Monte Carlo errors, discrete/constant handling,
and what to report when mixing remains unresolved. Use evidence-backed
choices; do not silently turn this draft into a fixed 5r heuristic.

Implement canonical matrix preparation and the real-data pilot runner,
plus validated diagnostics. Reuse frozen eligibility and observed-support
rules; verify observed counts with the native kernel before sampling.
No such preparation/diagnostics/pilot runner exists yet. Keep raw arrays
under ignored data/, scratch/builds under work/, and logs under logs/.
The existing wrapper compiles for the Python interpreter architecture;
M1 .venv is x86_64 under Rosetta, not native arm64. Its macOS SDK header
search is explicit. Record source/build/compiler/architecture metadata.
Do not change the pinned original-run environment to add dependencies.

N2 fixes binary row/column margins; N3 also fixes label frequencies within
quarter. Eight Paper 2 headline cells are the initial scope, but onset
and persistence claims require all 38 primary cells under the relevant
null. Paper 1 needs its four cells. Preserve failed diagnostics and
predictions; finite-chain diagnostics are evidence, not a mixing proof.

When MBP results arrive, verify queue manifest, code/input/output hashes,
and completeness before incorporation. Extend
`eval/score_nulls_amendment.py`: R-a/R-b/T-a/T-b/T-c currently remain
PENDING_M3 (placeholders, not automatic detection). The primary thread
estimate pools all 1,000 per-pair draws before means, SD, z, and p99
thresholds; batch ranges show Monte Carlo variation, not confidence
intervals. Do not average batch z values as the primary estimate.

Finally revise both manuscripts' result-dependent abstracts, prose,
tables, and figures; current drafts are explicitly unfinished. Existing
method/presentation corrections are already committed. Term lint had
zero failures and eight stale-entry warnings. No revised PDF has been
rendered or visually checked yet. Preserve historical registrations and
published reference artifacts. Preprint uploads remain on hold.

## Interpretive constraints to carry forward

- Statistic is sum of per-pair document counts, not a union of documents.
- Slot shuffle followed by deduplication does not fix binary margins.
  Incidence loss alone does not establish a universal bias direction
  relative to the exact-margin null; the blanket conservatism claim was
  withdrawn in A1.
- z is a standardized null effect, not a normal-tail significance claim.
  Pair-dependent formed counts do not justify calibrated binomial p.
  MCMC tail fractions are not automatically exact permutation p-values.
- Passing P3 does not rule out DD's simultaneous ratio step, establish
  WSB-specific causation, or date onset to an exact day. DD step was
  pre-observed. Abs(z)<3 is non-detection, not equivalence.
- N1 successes do not settle exact-margin robustness. Do not guarantee
  either paper's conclusions survive before N2/N3 results are available.

The previous ETA (2–4 hours to initial Curveball checks; 1–2 days for full
runs and revised drafts) was a rough work estimate, not a running-job
completion prediction. Re-estimate after pilot throughput and mixing.

---

# Current execution handoff — Codex takeover, 2026-09-04 Pacific

This block supersedes conflicting instructions and conclusions in the
historical handoff below. The owner delegated the revision to Codex and
is setting up the M3 MBP to share the large computations.

## Ownership and current runs
- M1 owns the 38-cell Paper 2 N1 series at R=100 (three workers), log
  logs/takeover_n1_primary.log, output
  reports/paper2_windows_z_stratified_R100.tsv. It completed in 1276.81 seconds; all 38 rows are present.
  N1-a/b/c PASS, N1-d FAIL. Onset remains 2021Q2, P1/P2/P3 PASS.
- M1 completed the four-cell Paper 1 label seeding check at R=100;
  reports/paper1_nulls_label_R100.tsv and .json, source commit 8365fe5.
  P1-b PASS, max z difference 7.46%. The HN component of D-b FAILS:
  thread collapse is smaller than author collapse. Full details are
  appended to reports/pilot1_runs.md. Paper 1 N1 is now also complete:
  all four cells satisfy P1-a. See reports/nulls_amendment_scores.json.
- M3 is assigned ONLY the larger runs in eval/run_revision_queue.py:
  Paper 2 label and stratified headline cells at R=1000 (drift=10),
  then Paper 1 thread space, 10x100 independent label batches with
  pooled primary summaries. These have not started on the M1.

## M3 pickup
Open the existing checkout with its real data/ directory. Pull the
latest main without discarding local modifications. Use the pinned
.venv: Python 3.14.6, numpy 2.5.2, duckdb 1.5.5. From the repo root:

    .venv/bin/python eval/run_revision_queue.py --check-only
    caffeinate -i .venv/bin/python eval/run_revision_queue.py --workers 8

The queue verifies 24 source parquet SHA-256 values before evaluation,
logs each job to logs/m3_<job>.log, and writes
reports/revision_queue_m3.json with start commit, code hashes, seeds via
child manifests, timings and output hashes. Completed jobs are skipped
only if their output hashes match. Existing partial outputs are
preserved and require inspection before restarting that job. Raw
replicate arrays stay in data/registry/nulls_revisions/ and out of git.
Do not launch Curveball or change registrations from the M3 task.
Return the queue manifest and generated reports to the coordinating
M1 task. Do not overwrite the M1's running N1 table, draft changes,
HANDOFF, or shared run log. No automatic git push or publication is
performed by the queue.

## Registered correction and local evidence
- A1, e939759, specifies numerical tolerances, reported versus inspected
  gate evidence, canonical ordering and pooled thread summaries.
- 8365fe5 discloses that the prior N1-d rationale about the 1% floor was
  already false in the published table. The prediction itself remains
  unchanged and must be scored literally.
- Local three-cell Paper 2 replay exactly matches all 16 published
  fields; all four Paper 1 observed totals and eligible counts match.
  Evidence and baseline hashes: reports/reproduction_audit_2026-09-04.*.
  Full M3 gate remains owner-reported; its raw artifacts are not here.
- The frozen run_eval8.py and published outputs remain unchanged.
  The corrected runner archives per-pair integer draws and computes
  pooled z, ratio and formation thresholds, not averages of batch z.
- Code audit found that the N1 command selected 204 cells despite the
  38-cell registration. selected_cells() now enforces the registered
  scope. Tests include scope and pooled-statistic checks.

## Scientific and manuscript status
Both drafts are explicitly marked revision-in-progress and not ready
for public release. Known method definitions, extraction identity,
subscriber arithmetic, repository status and the DD-step description
have been corrected. Result-dependent prose, tables and figures still
need the full robustness results. Term lint currently has zero failures.

Do not repeat these historical overclaims: collapse proves negative z
conservative under fixed margins; a nominal 1% reference is an exact
floor or deterministic upper bound; binomial formed-count probabilities
are calibrated despite pair dependence; P3 passing rules out a DD step;
the two papers' conclusions are guaranteed unchanged before N1/N2.
The new registration appendix states their qualifications explicitly.

Next: incorporate M3 results and finish a
registered Curveball mixing pilot and exact-margin plus quarter-stratified
exact-margin design, then revise result-dependent claims and figures.
The N2 document is DRAFT. The new compiled Curveball kernel has passed
synthetic tests (including an independently enumerated five-state
transition kernel, native sampling, margins and counts). A 588k-row
synthetic benchmark records about 2.72 million attempts/second on M1
x86_64; this is throughput evidence, not a real-matrix mixing bound.
Eight headline cells alone do not establish an onset/persistence rule
across the full series. Preserve all original registrations and failed
predictions. Public preprint updates remain on hold.

---

# Handoff — state of the Antikythera project (2026-08-30, RE-REVISED 2026-08-30 evening)

## PAPER PROGRAM HANDOFF (2026-09-01) — READ THIS FIRST FOR PAPER 1 / PAPER 2 WORK
## Consolidates a multi-session day; one new session should own both
## papers from here. Everything below the next "## Status" banner is the
## pre-paper project history and is still accurate for the machinery.

### Critique response: nulls amendment (2026-09-04) — CURRENT PICKUP POINT
Written 2026-09-04 evening for a takeover by another agent. Everything
in this block is true as of commit 39c3d2e on main (origin in sync,
nothing unpushed, working tree clean). The MBP session described below
has NOT pushed anything; its results exist only as the owner's report,
transcribed here.

#### 1. State of the repo
- Branch main, HEAD 39c3d2e. Three commits today on top of c559f66:
  dc3a540 (portability + requirements.txt), e50b1b9 (registered nulls
  amendment + code + tests), 39c3d2e (HANDOFF + mbp_inputs.txt).
- Machines: M1 (this repo checkout, /Users/andrej/workspace/antikythera;
  the NVMe with all data stays here, mounted at
  "/Volumes/1TB NVME 1/antikythera/data", reached through the data/
  symlinks: docs, extractions, extractions_raw, paper2, raw, registry,
  release, science4cast, reddit_gate). M3 MBP (a clone; data/ is a real
  directory holding the 26 files in mbp_inputs.txt, 1.45 GB, copied
  from the NVMe at the same relative paths).
- Environments: .venv on each machine from requirements.txt (Python
  3.14.6, numpy 2.5.2, duckdb 1.5.5). IMPORTANT: the M1 venv is an
  x86_64 interpreter under Rosetta (platform.machine() == x86_64); the
  MBP venv is arm64. The permutation stream is identical on both; libm
  lgamma/exp differ by ulps, which shows up only in binom_p.
- No jobs are running on the M1. The only M1 real-data run today was
  the 3-cell pool reproduction check (registered null; WSB k=0,1 and
  DD k=0; byte-identical), output in the session scratchpad only, not
  kept.

#### 2. What the critique said and what we verified (2026-09-04)
External model-generated review of both preprints. Verified against
code and drafts:
- The label-shuffle null (run_eval8.run_space, run_paper2.window_stat,
  run_gate.analyse) permutes the label column and rebuilds documents as
  sets, so duplicate labels collapse: NOT fixed-fixed. Both drafts say
  it "holds every document's size and every concept's frequency fixed"
  (paper1_draft.md lines ~122, 197, 311, 780, 796; paper2_draft.md
  ~238). Measured collapse (registered null, first 10 replicates): WSB
  B=4 k=0 collapsed_frac 0.057, WSB k=1 0.058, DD k=0 0.033. Bias
  direction: collapse removes incidences, null pair counts deflate;
  negative z conservative, positive z (Paper 2 excursion) anti-
  conservative, per-pair p99 slightly easier to exceed (formation was
  at the floor anyway).
- Statistic definition: code sums per-pair document counts (obs.sum());
  prose says "documents holding any eligible pair". Prose is wrong.
- DD control (reports/paper2_windows_z.tsv, B=4 union): z not monotone
  (-8.1 -9.8 -8.9 -7.7 -8.6 -11.6 -10.7 -10.3 -9.6 -9.4 -7.2 -8.0 -6.7
  -10.2 -10.1 -10.6 -11.2 -12.1 -15.7); observed/null ratio steps from
  0.59-0.73 (eval 2020Q1..2021Q1) to 0.37-0.51 (2021Q2 onward),
  coincident with the WSB onset. WSB ratios: 0.80 1.06 1.10 2.32 1.69
  then 0.68 0.36 0.31 0.35 0.52 0.76 0.28 0.59 0.52 0.49 0.67 0.60 0.75
  0.71. paper2_draft.md line ~449 "gradually and monotonically" is
  false. P3 unaffected (DD never at chance or excursion).
- "30-fold" (paper2_draft.md ~30, 109, 159) contradicts its own anchor
  A2 (1.8M -> 9M subscribers = fivefold); either re-source to a volume
  figure or correct.
- Extraction model never named in Paper 1 (deferred to the cache key,
  ~line 595). Paper 2 lines ~788 and ~859 still say "private during
  review" (repo is public).
- Onset should be stated as the window whose eval interval covers
  2021Q2-Q3; |z|<3 is non-detection, not equivalence; the step-fit
  near-tie set is not a CI.
- Prior art: bipartite backbone work (Neal 2014 FDSM, Saracco BiCM,
  Zweig & Kaufmann) already uses fixed-fixed nulls; the defensible claim
  is that LBD / co-occurrence z-scoring has not. Cite Neal; cite 2-3
  papers using the Poisson z-criterion being retired.
- 1 percent floor is "at most 1 percent nominal", not exact; binomial
  on formed counts assumes independence (fails); z is an effect size in
  null-SD units, not a tail probability. Both cut against the
  alternative, so the kill stands.
- Impact: Paper 1 kill and Paper 2 onset not at risk. Paper 2 excursion
  (+28.6, +30.9) is the exposed result until N1 and curveball run.

#### 3. What was built today (all committed)
- eval/nulls.py: label_shuffle (registered sampler moved verbatim;
  test asserts identical output to the inline code), label_shuffle_
  stratified (permute within strata, strata visited sorted),
  margin_drift (inc_before/inc_after/docs_changed/toks_changed;
  precomputed Counters optional), null_summary (mean, sd, z, ratio,
  null_min/max, mc_p_lo/hi/2s with the +1 correction), drift_mean.
- eval/run_paper2.py: --workers N (spawn pool; workers load their own
  rows via duckdb; parent writes rows in registered order; per-cell
  fresh default_rng(20260831) so output is order-independent), --null
  label|stratified, --R, --headline (8 cells: WSB union B=4 k in
  1,2,3,4,5,18; DD union B=4 k in 4,5), --cells "B:k:stratum:lens,...",
  --drift N. Registered path (label, R=100, all cells, no --out) writes
  reports/paper2_windows_z.tsv with the 16 registered columns only.
  Anything else requires preregistration_nulls.md STATUS: REGISTERED,
  refuses to overwrite the registered TSV, writes
  reports/paper2_windows_z_<null>_R<R>[_headline].tsv with 14 wide
  columns (null_kind R ratio null_min null_max mc_p_lo mc_p_hi mc_p_2s
  drift_reps inc_before inc_after collapsed_frac docs_changed
  toks_changed). Drift default: 0 for the registered null, 10 otherwise
  (changed after the reproduction check accidentally emitted drift).
- eval/run_eval8_nulls.py: Paper 1's four cells, per-cell seed
  default_rng([20260831, cell_index]), documents iterated sorted,
  --null stratified|label, --R, --workers (<=4), --drift. Output
  reports/paper1_nulls_<null>_R<R>.tsv and data/registry/{run5_author,
  pilot1_concepts}/run8_nulls_<null>_R<R>.json. Thread-space strata =
  quarter of the thread's first claim (min(time) per doc_id from
  claims.parquet). run_eval8.py is untouched.
- tests/test_nulls.py: 7 tests; `.venv/bin/python tests/test_nulls.py`.
- preregistration_nulls.md: STATUS: REGISTERED. Predictions N1-a..d,
  R-a/b, D-b (D-a withdrawn and disclosed), P1-a/b; decision rules 1-5;
  runbook steps 1-6. Rule 4 is ALREADY TRIGGERED by the drift values:
  curveball (N2) required on the headline cells before v2 under a
  further amendment (not yet drafted).
- mbp_inputs.txt: the 26 data files the MBP needs.
- Memory note for Claude sessions: project-critique-response-nulls.md
  (not part of the repo).

#### 4. MBP reproduction gate (runbook step 1) — RUN, RESULT REPORTED BY OWNER, NOT COMMITTED
- Paper 2, `run_paper2.py --workers 8` (arm64): all 204 cells; every
  eligible count, observed total, null mean, null sd, z, formed count
  byte-identical to the published TSV; registered scoring reprinted
  unchanged (onset eval 2021Q2, P1/P2/P3 pass). Only drift: binom_p in
  66 of 204 rows, max relative difference 6.4e-13 (libm on arm64 vs the
  M1's x86_64 Rosetta interpreter). An x86_64 interpreter on the MBP
  reproduces the published bytes. The Paper 2 stream is reproducible.
- Paper 1, `run_eval8.py` serial: author space reproduces exactly in
  both folds. Thread space does NOT: fold1 z = -178.8 (published
  -152.3), formed 20 (published 22); fold2 z = -116.3 (published
  -123.2). Observed totals and eligible counts identical. Cause,
  verified on the MBP: thread_universe's DuckDB hash join has no ORDER
  BY and run_space iterates edoc in insertion order before the
  permutation; the document set is stable, the order is not, even
  between consecutive runs on the M1. Published thread-space null
  values are single draws from an unpinned stream and cannot be
  regenerated anywhere. The 2026-08-31 determinism check covered
  hash-seed variation only. Sign and scale not in doubt (every draw
  below -100, formation at the floor). Paper 2, run_gate, and author
  space sort documents and are unaffected. run_eval8_nulls.py already
  sorts.
- Whether the MBP's gate outputs (TSV diff, JSONs, logs) were saved is
  not known here; the MBP session was told to log to logs/<step>.log
  and to keep reference/ copies of the run8 JSONs. Check that clone.
- Runbook steps 2-6 have NOT run. No N1, R=1000, or curveball value
  exists anywhere.

#### 5. Registered decisions vs proposals awaiting the owner
REGISTERED (preregistration_nulls.md, commit e50b1b9): the registered
null stays primary for v1 claims; N1, D, Monte Carlo p, R=1000 on the
headline cells; predictions and rules 1-5; N2 required (rule 4
triggered); v2 uploads on hold.
PROPOSED, NOT DECIDED (owner has been asked; also put to the external
reviewer as questions a-c):
- Gate standard: byte identity for counts and z; p-values within 1e-9
  relative; platform and interpreter architecture recorded per run;
  do not chase byte identity through an x86_64 emulator. Keep the
  published TSV as the x86 baseline and log the arm64 diff.
- Thread space: re-report as 10 independent seeds at R=100 under
  sorted document iteration (z mean and range, formed range, ratio mean
  and range), nondeterminism disclosed and scoped, in a dated
  registered note appended to preregistration_nulls.md with a
  prediction (every seed z < -100, formation at the floor in all,
  ratio within 5 percent across seeds). Alternative on the table: one
  re-baselined draw (rejected in our recommendation) or R=1000 plus a
  few seeds.
- Curveball design (trades per row before first sample, thinning,
  independent chains vs one thinned chain per core): open; the MBP
  session was to draft preregistration_nulls_n2.md as STATUS: DRAFT.
- A paste-ready follow-up to the external reviewer with these results
  and questions was drafted in conversation; whether it was sent is
  unknown.

#### 6. Remaining work, in order
1. Owner decides the two proposals above. Then append the dated note
   to preregistration_nulls.md (tolerance clause; thread-space 10-seed
   re-report with its prediction; nondeterminism disclosure), commit,
   push. Do not run anything new before that commit.
2. Add a --seeds N mode to run_eval8_nulls.py for the thread-space
   re-report (registered sampler, sorted iteration, seeds
   default_rng([20260831, cell_index, s])), one TSV row per seed;
   extend tests; commit, push.
3. MBP, from the runbook: step 2 `run_paper2.py --null stratified
   --workers 8` (full series, ~15-20 min on an M3 Pro); step 3
   `run_paper2.py --headline --R 1000 --workers 8` and the same with
   `--null stratified` (~15-20 min each); step 4 `run_eval8_nulls.py
   --null stratified --workers 4` and `--null label --workers 4`
   (~3 min each), plus the new 10-seed thread-space run (~10 x 5 min).
   Every run `>> logs/<step>.log 2>&1`. Score every prediction
   (N1-a..d, R-a/b, D-b, P1-a/b, and the new thread-space prediction)
   PASS/FAIL with numbers in reports/pilot1_runs.md, apply rules 1-5
   as written, commit the TSVs/JSONs/log summaries, push.
4. Draft preregistration_nulls_n2.md (curveball: chain length,
   thinning, per-chain seeds, headline cells, predictions), owner
   review, flip to REGISTERED, run on the 8 headline cells (~1 h with
   one chain per core, plus a second independent chain set as the
   convergence check), score, commit.
5. Prose pass on both drafts (reports/paper1_draft.md,
   reports/paper2_draft.md): statistic definition; drop "fixed-fixed"
   and state the collapse bias; ratios in every table; Monte Carlo p;
   onset as a window; |z|<3 as non-detection; DD step disclosed;
   "monotonically" removed; 30-fold corrected; extraction model named
   in Methods; repo status line; Neal 2014 / FDSM and LBD citations;
   abstract and conclusion scoped to the tested criterion; Paper 1
   thread-space numbers as ranges with the determinism qualification;
   registration history consolidated. Then eval/term_lint.py all (0
   failures), re-render (eval/render_paper_html.py), regenerate
   preprint PDFs, upload SocArXiv v2s, add related identifiers on
   Zenodo.
Expected compute for steps 3-4 on an M3 Pro: about 2.5 to 3.5 h wall.

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
