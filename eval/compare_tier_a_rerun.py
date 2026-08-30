#!/usr/bin/env python3
"""Registered comparison for the Tier A re-execution
(preregistration_tier_a_rerun.md): integers exact, floats within 1e-9.

Usage: compare_tier_a_rerun.py <original_dir> <rerun_dir>
Walks the four tier_a_*.json pairs; exits non-zero on any violation.
"""
import json
import os
import sys

FOLDS = ["tier_a_y2019_d1_c25_m1.json", "tier_a_y2017_d3_c25_m1.json",
         "tier_a_y2017_d3_c25_m3.json", "tier_a_y2015_d5_c25_m1.json"]
TOL = 1e-9


def walk(a, b, path, viol, fmax):
    if isinstance(a, dict):
        if set(a) != set(b or {}):
            viol.append(f"{path}: key sets differ")
            return
        for k in a:
            walk(a[k], b[k], f"{path}.{k}", viol, fmax)
    elif isinstance(a, list):
        if len(a) != len(b):
            viol.append(f"{path}: list lengths differ")
            return
        for n, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{n}]", viol, fmax)
    elif isinstance(a, bool) or isinstance(a, int):
        if a != b:
            viol.append(f"{path}: int {a} != {b}")
    elif isinstance(a, float):
        d = abs(a - (b if isinstance(b, (int, float)) else float("nan")))
        fmax[0] = max(fmax[0], d)
        if not d <= TOL:
            viol.append(f"{path}: float {a} vs {b} (delta {d:g})")
    else:
        if a != b:
            viol.append(f"{path}: {a!r} != {b!r}")


def main():
    orig_dir, rerun_dir = sys.argv[1], sys.argv[2]
    ok = True
    for f in FOLDS:
        a = json.load(open(os.path.join(orig_dir, f)))
        b = json.load(open(os.path.join(rerun_dir, f)))
        viol, fmax = [], [0.0]
        walk(a, b, f, viol, fmax)
        status = "PASS" if not viol else "FAIL"
        ok = ok and not viol
        print(f"{f}: {status} | max float delta {fmax[0]:.3g}")
        for v in viol[:20]:
            print(f"  {v}")
    print("VERDICT:", "PASS (integer-exact, floats within 1e-9)" if ok
          else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
