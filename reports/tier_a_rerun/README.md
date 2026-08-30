# Tier A re-execution record (2026-08-30)

Registered pre-run in `preregistration_tier_a_rerun.md` (commit 347e21a),
purpose: ordering hygiene for the original Tier A control, whose
registration and result were committed together (a884a49).

- Platform: fresh Vultr vc2-4c-8gb, x86-64 Ubuntu, numpy 2.2.6/OpenBLAS
  (original: Apple Silicon arm64, Accelerate). Instance created and
  destroyed same day; ~1 hour of runtime, ~$0.06.
- Inputs MD5-verified on the box against the registered checksums (all
  six matched; a Zenodo direct-fetch attempt returned error pages and
  was discarded by the same MD5 gate — files were then uploaded from the
  local copies).
- Harness: eval/run_tier_a.py at 347e21a (identical logic to the
  original; paths env-overridable, defaults unchanged).
- Result: `eval/compare_tier_a_rerun.py original_arm64/ rerun_x86/` —
  ALL FOUR folds PASS. Integer-exact as registered, and in fact
  byte-identical JSONs (max float delta 0): the registered 1e-9
  tolerance for cross-platform float drift was not needed for this
  integer-dominated, fixed-seed workload.
- Contents: `original_arm64/` (copies of the a884a49-era JSONs),
  `rerun_x86/` (box outputs), `rerun_x86.log` (full run log).
