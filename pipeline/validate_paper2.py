#!/usr/bin/env python3
"""Outcome-blind integrity pass over the paper-2 API pull (runbook §5).

API-file variant of validate_month.py: those checks assume dump files
(own-subreddit field, WSB-sized floors); API shards carry no subreddit
field and include tiny DD months, so the applicable invariants are:
  - every line parses as JSON (rows, not bytes)
  - timestamp span inside the shard's month (±1 day tolerance, <=1%)
  - `score` present on ~all rows (the field this pull exists to add)
  - per-month volume vs neighbours: a month at 0 or <5% of its larger
    neighbour (same sub, same kind) is a failure, not a small month
  - distinct-author count reported (informational)

Emits a TSV volume table (stdout section TABLE) and FAIL/NOTE lines
(section CHECKS). Exit 1 if any FAIL. Reads every row of every shard —
run backgrounded with output to a file.
"""
import glob
import gzip
import json
import os
import sys
from datetime import datetime, timezone

PULL = "/Volumes/1TB NVME 1/antikythera/data/paper2/pull"
SUBS = ["wallstreetbets", "stocks", "investing", "StockMarket",
        "ValueInvesting", "SecurityAnalysis"]
MONTHS = [f"{y}-{m:02d}" for y in range(2019, 2025) for m in range(1, 13)]


def scan(path: str, month: str):
    y, mo = int(month[:4]), int(month[5:7])
    lo = datetime(y, mo, 1, tzinfo=timezone.utc).timestamp()
    hi = datetime(y + (mo == 12), (mo % 12) + 1, 1,
                  tzinfo=timezone.utc).timestamp()
    n = unparsed = out_of_range = no_score = 0
    authors = set()
    with gzip.open(path, "rt", errors="replace") as f:
        for line in f:
            n += 1
            try:
                r = json.loads(line)
            except Exception:
                unparsed += 1
                continue
            ts = float(r.get("created_utc", 0))
            if not (lo - 86400 <= ts < hi + 86400):
                out_of_range += 1
            if "score" not in r:
                no_score += 1
            a = r.get("author")
            if a:
                authors.add(a)
    return n, unparsed, out_of_range, no_score, len(authors)


def main() -> None:
    rows = {}   # (kind, sub, month) -> stats
    fails, notes = [], []
    for sub in SUBS:
        for month in MONTHS:
            for kind in ("comments", "posts"):
                path = os.path.join(PULL, f"{kind}_{sub}_{month}.ndjson.gz")
                if not os.path.exists(path):
                    fails.append(f"FAIL missing shard {kind}_{sub}_{month}")
                    continue
                st = scan(path, month)
                rows[(kind, sub, month)] = st
                n, unp, oor, nos, na = st
                tag = f"{kind}_{sub}_{month}"
                if unp:
                    fails.append(f"FAIL {tag}: {unp}/{n} unparseable")
                if n and oor > n * 0.01:
                    fails.append(f"FAIL {tag}: {oor}/{n} ts outside {month}")
                if n and nos:
                    fails.append(f"FAIL {tag}: {nos}/{n} rows missing score")
                print(f"scanned {tag}: {n} rows", flush=True)
    # neighbour-volume sanity (comments are the load-bearing series)
    for sub in SUBS:
        for i, month in enumerate(MONTHS):
            st = rows.get(("comments", sub, month))
            if st is None:
                continue
            n = st[0]
            nb = [rows[("comments", sub, MONTHS[j])][0]
                  for j in (i - 1, i + 1)
                  if 0 <= j < len(MONTHS) and ("comments", sub, MONTHS[j]) in rows]
            big = max(nb) if nb else 0
            if n == 0:
                fails.append(f"FAIL comments_{sub}_{month}: 0 rows")
            elif big and n < big * 0.05:
                fails.append(f"FAIL comments_{sub}_{month}: {n} rows vs "
                             f"neighbour {big} (<5%)")

    print("\n== TABLE (kind\tsub\tmonth\trows\tauthors\toor\tno_score)")
    for (kind, sub, month), (n, unp, oor, nos, na) in sorted(rows.items()):
        print(f"{kind}\t{sub}\t{month}\t{n}\t{na}\t{oor}\t{nos}")
    print("\n== CHECKS")
    for line in fails + notes:
        print(line)
    total = sum(st[0] for st in rows.values())
    print(f"\n== SUMMARY shards={len(rows)} total_rows={total} "
          f"fails={len(fails)}")
    print("PASS" if not fails else "PROBLEMS")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
