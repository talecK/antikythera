# Paper 2 single bounded Curveball extension — 2026-09-04 Pacific

STATUS: REGISTERED. Commit this protocol and its exact JSON plan before
any real-data extension initialization, pilot or production. All first-pass
results, including pilot outcomes and diagnostic failures, are known.
This is an outcome-informed precision extension, not a blind replication.
No extension chain has run at registration. The user agreed to one bounded
Paper 2 extension and no further large compute for this revision, except
a demonstrated implementation error requiring correction and affected reruns.

## Frozen scope and scientific predictions

The first-pass queue completed all 84 attempts. M1 independently verified
Paper 1's 104 files and Paper 2's 968 files, including all raw stage
diagnostics and production moments. Paper 1 aggregate prediction X-d passes
under N2 and N3; its formation prediction X-e remains unresolved. No Paper 1
cell is included in this extension and no new FDR analysis is undertaken.

Paper 2 has 44 unresolved cell/null combinations: 25 N2, 19 N3. Exact cell
order, original report SHA256 and matrix SHA256 are fixed in
reports/curveball_extension1_plan.json. Extend ALL those unresolved cases
in that order regardless of signs or apparent scientific promise. Prioritize
WSB k=3,4,5,2,0, then DD k=4,5, then remaining WSB and DD windows in
increasing order. Within a cell order N2 then N3 if unresolved. Dispatch
at most two jobs concurrently; scheduling speed cannot alter seeds.
Completed passing first-pass cells are retained, never rerun or replaced.

Keep original X-a, X-b and X-c predictions from preregistration_nulls_n2.md
unchanged, separately for each null. X-a: every originally detected primary
cell retains sign. X-b: full-series onset k=5 with original P1/P2/P3 all
passing. X-c: both WSB excursion cells k=3,4 have z>=5 and ratio>1. Score
using the union of passing first-pass production results and passing fresh
extension production results. Do not pool pilot draws, old unresolved draws,
or different nulls. Original first-pass prediction scores remain unchanged
in their own record; extension scores are a separate sensitivity result.
Any remaining missing/failed diagnostic cell keeps its dependent full-scope
prediction UNRESOLVED. A scientific failure is reported literally. In
particular, do not retrospectively substitute the existing-walls/temporary-
opening interpretation for X-b or call it a successful original prediction.

## Sampler, starts, seeds and diagnostics

Keep the original binary matrix, exact margin/quarter constraints,
eligibility, support, vocabulary, observed counts, Curveball kernel, and
one-sweep save interval unchanged. The existing Ensemble initialization
uses four chains with 0,5,20,80 sweeps from observation; these are valid
but are not certified starts from distant modes. Maintain its initialization,
common-observation distance and stage margin checks without modification.

Use the original seed function with distinct phase strings:
init-extension1-pilot, extension1-pilot, init-extension1-production,
extension1-production. Thus seed is the unsigned little-endian first eight
SHA256 bytes of UTF8 antikythera/n2n3/v1|PHASE|NULL|CELL|CHAIN|BLOCK.
Original seed streams and raw trajectories are preserved; extension starts
are fresh and deterministic. Pilot and production use independent streams.

Fresh pilot stages: 1760,3520,7040 saved sweeps per chain, cumulatively.
At each stage test candidate burn-in 80,160,320,640 in that fixed order,
using all subsequent draws. Select the first passing burn at the first
passing stage. No thinning or choice based on effect size. Failure at the
maximum stays UNRESOLVED. Production starts independently, burns twice
the chosen pilot burn, and saves 800,1600,3200 sweeps per chain in stages.
Stop at the first production stage passing the unchanged aggregate checks.

Use the original registered aggregate_diagnostics implementation unchanged:
rank/folded split R-hat<1.01 and bulk ESS>=400 for total and distance;
total tail ESS>=400 and mean/SD MCSE each <=0.05 null SD. Keep constants
undefined and all original limitations. Record the same deterministic
16-pair diagnostic panel. No thresholds are relaxed. The extension targets
aggregate Paper 2 predictions only: it does not compute or validate new
formation classifications and cannot support a new pair-discovery claim.

## Single resource envelope and stopping

Native ARM MBP, pinned Python 3.14.6, numpy 2.5.2, duckdb 1.5.5. Two
workers maximum, no duplicate M1 sampling. Global sampling wall budget:
21600 seconds (six hours), measured from queue start. Each cell/null gets
at most 5400 seconds (90 minutes), inclusive of initialization, pilot,
production and its diagnostic work. The earlier global 72-worker-hour
budget remains respected: this extension adds at most approximately 12
worker-hours plus finalization overhead; report actual usage. No automatic
second extension, retry of completed failures, or larger budget is allowed.

Check deadlines before phases and stages and before every saved sweep
or production burn sweep. Stop sampling at the first exhausted deadline.
Initialization, margin verification and final serialization/diagnostics
already in progress may finish; report that overhead separately from the
sampling budget. A resource-truncated stage is archived but cannot yield a
passing result. Not-yet-started jobs receive NOT_RUN_GLOBAL_BUDGET. Preserve
all partial arrays and failures; do not restart a partial extension silently.
A process interruption requires inspection and an explicit new operational
record, never a silent overwrite or expansion of this single budget.

## Preservation, scoring and reporting

Use data/registry/nulls_revisions/curveball_extension1/ for new raw files,
and reports/curveball_extension1_* for new results. Use the shared original
queue lock to exclude other Curveball queues. Original registrations,
first-pass files and user-interrupted M1 trajectories remain byte-identical.
Record exact source/registration/plan/input/matrix/old-report/build hashes,
versions, native architecture, seeds, starts, stage diagnostics and durations.
Guard scientific source bytes during the queue. Commit before launch.

After completion, transfer and independently verify raw output moments and
diagnostics, then score the fixed predictions using only passing production.
If excursion robustness fails, withdraw it for that null; if onset fails,
report that failure rather than moving a threshold. If diagnostics remain
unresolved, qualify the paper accordingly. No further large compute solely
for formation, no new multiple-testing project, no preprint publication and
no external outreach are authorized by this extension.
