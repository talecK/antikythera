#!/usr/bin/env python3
"""Run the registered large analyses on the M3; resume completed jobs safely.

From the repository: .venv/bin/python eval/run_revision_queue.py --workers 8
Use --check-only to validate inputs without evaluating a new statistic.
No git mutation, upload, or manuscript publication is performed.
"""
import argparse
import csv
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def plan(workers):
    return [
        ("paper2_label_R1000", ["eval/run_paper2.py", "--headline", "--R", "1000",
          "--null", "label", "--drift", "10", "--workers", str(workers)],
         ["reports/paper2_windows_z_label_R1000_headline.tsv"]),
        ("paper2_stratified_R1000", ["eval/run_paper2.py", "--headline", "--R", "1000",
          "--null", "stratified", "--drift", "10", "--workers", str(workers)],
         ["reports/paper2_windows_z_stratified_R1000_headline.tsv"]),
        ("paper1_thread_pooled", ["eval/run_eval8_nulls.py", "--null", "label",
          "--space", "thread", "--seeds", "10", "--R", "100", "--workers", "2"],
         ["reports/paper1_nulls_label_R100_thread_seeds10.tsv",
          "reports/paper1_nulls_label_R100_thread_seeds10_batches.tsv",
          "reports/paper1_nulls_label_R100_thread_seeds10.json",
          "data/registry/pilot1_concepts/run8_nulls_label_R100_thread_seeds10.json",
          "data/registry/nulls_revisions/label_R100_thread_seeds10/thread_fold1.npz",
          "data/registry/nulls_revisions/label_R100_thread_seeds10/thread_fold2.npz"]),
    ]


def validate_output(job, outputs):
    for name in outputs:
        if not (ROOT / name).is_file():
            raise RuntimeError(f"Missing output: {name}")
    with (ROOT / outputs[0]).open() as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    expected_rows = 2 if job == "paper1_thread_pooled" else 8
    if len(rows) != expected_rows or any(int(r["R"]) != 1000 for r in rows):
        raise RuntimeError(f"Unexpected row count or R in {outputs[0]}")
    return {name: sha256(ROOT / name) for name in outputs}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()
    if args.workers < 1:
        ap.error("workers must be positive")
    os.chdir(ROOT)
    import numpy
    import duckdb
    expected_versions = ("3.14.6", "2.5.2", "1.5.5")
    actual_versions = (platform.python_version(), numpy.__version__, duckdb.__version__)
    if actual_versions != expected_versions:
        raise SystemExit(f"Pinned environment required: {expected_versions}; found {actual_versions}")
    checksum_path = ROOT / "reports/revision_input_checksums.json"
    checksums = json.loads(checksum_path.read_text())
    for name, expected in checksums.items():
        if not (ROOT / name).is_file() or sha256(ROOT / name) != expected:
            raise SystemExit(f"Input missing or checksum mismatch: {name}")
    print(f"PASS: {len(checksums)} source files verified; {actual_versions}; "
          f"architecture={platform.machine()}", flush=True)
    if args.check_only:
        return
    (ROOT / "logs").mkdir(exist_ok=True)
    lock = (ROOT / "logs/revision_queue_m3.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("Another M3 queue is already running in this checkout")
    state_path = ROOT / "reports/revision_queue_m3.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"jobs": {}}
    code = {name: sha256(ROOT / name) for name in [
        "eval/run_revision_queue.py", "eval/run_paper2.py", "eval/run_eval8_nulls.py",
        "eval/nulls.py", "eval/run_eval8.py", "eval/run_gate.py",
        "preregistration_nulls.md"]}

    def save():
        temp = state_path.with_suffix(".tmp")
        temp.write_text(json.dumps(state, indent=2) + "\n")
        temp.replace(state_path)

    for job, command, outputs in plan(args.workers):
        if any(sha256(ROOT / name) != expected for name, expected in code.items()):
            raise SystemExit("Analysis code or registration changed while the queue was running; inspect before resuming")
        previous = state["jobs"].get(job)
        if previous and previous["status"] == "complete":
            if any(sha256(ROOT / name) != sha for name, sha in previous["outputs"].items()):
                raise SystemExit(f"Completed output changed: {job}; inspect before resuming")
            print(f"SKIP completed and verified: {job}", flush=True)
            continue
        # Never destroy an existing partial or independently computed result.
        conflicts = [name for name in outputs if (ROOT / name).exists()]
        if conflicts:
            raise SystemExit(f"Preserved existing files for {job}: {conflicts}. "
                             "Archive and inspect the partial run before restarting this job.")
        started = time.time()
        log_path = f"logs/m3_{job}.log"
        record = {"status": "running", "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "command": [".venv/bin/python", *command],
                  "commit_at_start": subprocess.check_output(
                      ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(),
                  "code_sha256": code, "source_manifest_sha256": sha256(checksum_path),
                  "python": platform.python_version(), "numpy": numpy.__version__,
                  "duckdb": duckdb.__version__, "architecture": platform.machine(),
                  "log": log_path}
        state["jobs"][job] = record
        save()
        print(f"START {job}; progress log: {log_path}", flush=True)
        try:
            with (ROOT / log_path).open("a") as log:
                subprocess.run([sys.executable, *command], cwd=ROOT, stdout=log,
                               stderr=subprocess.STDOUT, check=True)
            record["outputs"] = validate_output(job, outputs)
            record["status"] = "complete"
        except BaseException as exc:
            record["status"] = "failed"
            record["error"] = type(exc).__name__
            raise
        finally:
            record["wall_seconds"] = round(time.time() - started, 3)
            save()
        print(f"DONE {job}: {record['wall_seconds'] / 60:.1f} minutes", flush=True)
    print("All three large analyses complete. Keep data/registry/nulls_revisions/ "
          "(raw replicate arrays). Return the reports and this manifest for scoring.", flush=True)


if __name__ == "__main__":
    main()
