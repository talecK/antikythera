"""Synthetic-only Curveball throughput benchmark; never opens corpus files."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
from curveball import Curveball, SOURCE, build_library


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=588000)
    ap.add_argument("--columns", type=int, default=1000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(20260904)
    degrees = rng.choice([1, 2, 5, 20], size=args.rows, p=[.6, .2, .15, .05])
    rows = [rng.choice(args.columns, int(degree), replace=False).tolist() for degree in degrees]
    pairs = [(i, i+1) for i in range(args.columns-1)]
    started = time.perf_counter()
    with Curveball(rows, args.columns, 20260904) as chain:
        build_seconds = time.perf_counter()-started
        started = time.perf_counter()
        chain.step(5*args.rows)
        trade_seconds = time.perf_counter()-started
        started = time.perf_counter()
        counts = chain.counts(pairs)
        count_seconds = time.perf_counter()-started
        diagnostics = chain.diagnostics()
    result = {"synthetic_only": True, "rows": args.rows, "columns": args.columns,
              "degree_distribution": {"1": .6, "2": .2, "5": .15, "20": .05},
              "incidences": int(degrees.sum()), "attempts": 5*args.rows,
              "build_seconds": build_seconds, "trade_seconds": trade_seconds,
              "count_seconds": count_seconds, "attempts_per_second": 5*args.rows/trade_seconds,
              "diagnostics": diagnostics, "statistic": int(counts.sum()),
              "architecture": platform.machine(), "python": platform.python_version(),
              "numpy": np.__version__,
              "compiler": subprocess.check_output(["clang++", "--version"], text=True).splitlines()[0],
              "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "binary_sha256": hashlib.sha256(build_library().read_bytes()).hexdigest()}
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__ == "__main__":
    main()
