# Historical M3 reproduction-gate notes recovered during transfer

These notes were uncommitted on the MBP results branch at 1ca9817 and
were recovered over authenticated SSH on 2026-09-05 UTC. The text below
is preserved verbatim. Statements about pending jobs, required owner
calls and Python 3.14.7 describe that earlier session, not current status.
Current completed M3 results and pinned Python 3.14.6 were independently
verified later; see HANDOFF.md and reports/m3_incorporation_verification.json.

The full original pilot1_runs.md was preserved on both machines with
SHA256 243769ef876e0df5a73e42abe5cbfad487c6a28073acade5062d2c811011e9e6.
MBP backup: work/pre_curveball_sync_20260905/pilot1_runs.md and its patch.
The original change also remains in the MBP git stash. Untracked logs/
and reference/ were left in place.

---

## Nulls amendment, runbook step 1 — REPRODUCTION GATE (2026-09-04, M3 MBP): BOTH GATES FAIL; step 2 NOT run
Registration: preregistration_nulls.md (STATUS: REGISTERED). Machine: M3 Max
(14 cores, 39 GB), native arm64 venv, Python 3.14.7, numpy 2.5.2, duckdb
1.5.5 (requirements.txt frozen from the M1's venv, which turned out to be
x86_64 CPython 3.14.6 under Rosetta). Inputs: the 26 files in mbp_inputs.txt
rsynced from the M1 NVMe (1,447,984,127 bytes). tests/test_nulls.py 7/7.

Gate 1a: `run_paper2.py --workers 8` (registered null, R=100, 204 cells),
447 s wall. reports/paper2_windows_z.tsv NOT byte-identical: 66 of 204 rows
differ, ALL in binom_p only, max relative difference 6.4e-13 (e.g. WSB B=4
k=0: 0.36381451393612796 -> 0.36381451393612785). Every other column
(n_eligible, obs_total, null_mean, null_sd, z_seg, formed, uninformative)
identical in every row; registered scoring reprinted unchanged (onset window
5, P1/P2/P3 PASS). Cause: binom_sf_ge (math.lgamma / exp) under arm64 libm
vs the M1's x86_64 libm; the same function under an x86_64 CPython 3.14.7
on the M3 returns the M1's values exactly. Diff saved to logs/gate_paper2.diff;
tracked TSV restored to HEAD.

Gate 1b: `run_eval8.py` serial, 121 s wall, diffed against the M1's JSONs
(reference/). Author space: eligible, formed, formed_pairs, obs_total,
null_total_mean, null_total_sd, z_total identical in both folds (fold1
binom_p 0.87945293805304 -> 0.8794529380532494, same libm effect). Thread
space FAILS substantively:
| fold | field | M1 (reference) | M3 arm64 |
|---|---|---:|---:|
| 1 | null_total_mean | 48378.42 | 48352.54 |
| 1 | null_total_sd | 238.17 | 202.73 |
| 1 | z_total | -152.33 | -178.83 |
| 1 | formed | 22 | 20 |
| 2 | null_total_mean | 28274.27 | 28249.73 |
| 2 | null_total_sd | 165.70 | 175.34 |
| 2 | z_total | -123.17 | -116.25 |
| 2 | formed | 12 | 12 (different pairs) |
obs_total (12098 / 7866) and eligible (25161 / 7505) identical, so the
universe reproduces and the permutation stream does not. Cause, verified:
run_eval8.thread_universe() is a DuckDB hash join (claims x docs GROUP BY)
with no ORDER BY, and run_space() iterates edoc in dict insertion order
before rng.permutation (the 2026-08-31 fix sorted only the concept sets,
finding 1.2). The eval-document SET is identical on both machines (md5 of
the sorted keys matches), the insertion ORDER is not, and it is not stable
run to run on ONE machine either: two consecutive probes gave different
orders on the M3 (d19b1a0698df, 34db6870a275) and on the M1 (789370769eec,
552705a65bde); pinning DuckDB threads to 8 or 4 does not recover the M1's
order. Author space has a single-table scan and its order matched across
machines and runs. Consequence: the committed run-8 thread-space numbers
(z -152.3 / -123.2, formed 22 / 12) cannot be regenerated exactly anywhere,
including on the M1; the "determinism PASS" of 2026-08-31 covered
PYTHONHASHSEED only. The sign and scale are not in doubt (both reruns give
z < -100), but the byte-level gate as registered cannot pass for thread
space without a code change to the frozen script. run_eval8_nulls.py
already iterates sorted(edoc), so the amendment's new-null streams are
deterministic. Run-8 JSONs in data/ restored from reference/ (SHA-256
2c9d152e..., 39fd4149...); the arm64 outputs kept in logs/arm64_run8/.

Decision rule: per the runbook, nothing below step 1 was run. Owner call
needed on (a) x86_64 venv vs re-baselining Paper 2's binom_p on arm64, and
(b) the Paper 1 thread-space gate.

Addendum, x86_64 diagnostic (same session): run_eval8.py rerun under an
x86_64 CPython 3.14.7 (uv) on the M3, 167 s incl. install. Author space
now matches the M1 byte for byte INCLUDING binom_p (confirms the libm
cause for gate 1a). Thread space still fails (fold1 z -179.41, formed 21;
fold2 z -109.04), a third distinct value set, confirming the order
nondeterminism is independent of architecture. Outputs in logs/x86_run8/.
