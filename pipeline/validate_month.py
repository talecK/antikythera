#!/usr/bin/env python3
"""Per-month smoke tests for the dump acquisition pipeline.

Today three data bugs reached the corpus (corrupt dump, sparse dump filtered
as if complete, and a JSON format seam the fast filter could not read). All
three shared a signature: output that looked plausible, or plausibly empty,
with nothing raising. These checks target that class directly.

The load-bearing one is DIFFERENTIAL: run the fast regex filter and a slow
json.loads filter over the SAME sample and require agreement. json.loads is
format-agnostic by construction, so any whitespace/field/escaping drift in a
future dump shows up as a mismatch rather than as silent zeros.

Usage:
  validate_month.py preflight <dump.zst>            # before filtering
  validate_month.py output <filtered.ndjson.gz> <YYYY-MM> <RC|RS>
"""
import gzip
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dump_filter import PAT, SUBS  # noqa: E402

SAMPLE_BYTES = 200_000_000
GATE_SUBS = set(SUBS)


def preflight(dump_path: str) -> list[str]:
    """Fast-vs-slow agreement on a sample of the dump. Format-agnostic."""
    p = subprocess.Popen(["zstd", "-dc", "--long=31", dump_path],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    buf = p.stdout.read(SAMPLE_BYTES)
    p.stdout.close()
    p.terminate()
    if not buf:
        return [f"preflight: decompressed 0 bytes from {os.path.basename(dump_path)}"]
    body = buf[:buf.rfind(b"\n") + 1]
    lines = body.split(b"\n")
    regex_hits = sum(1 for ln in lines if PAT.search(ln))
    json_hits, parsed, bad = 0, 0, 0
    for ln in lines:
        if not ln.strip():
            continue
        try:
            r = json.loads(ln)
            parsed += 1
            if r.get("subreddit") in GATE_SUBS:
                json_hits += 1
        except Exception:
            bad += 1
    problems = []
    if parsed == 0:
        problems.append("preflight: no line parsed as JSON — format unknown")
    if bad > parsed * 0.01:
        problems.append(f"preflight: {bad} unparseable lines vs {parsed} parsed")
    if json_hits and regex_hits < json_hits * 0.99:
        problems.append(
            f"preflight: FAST FILTER MISSES ROWS — regex {regex_hits} vs "
            f"json {json_hits} in {len(body)/1e6:.0f}MB sample. The dump's "
            f"JSON shape likely changed; fix dump_filter.PAT before running.")
    if json_hits == 0 and parsed > 1000:
        problems.append(
            f"preflight: sample has {parsed} records but none in the gate "
            f"subs — verify this month actually contains them")
    return problems


def output(path: str, month: str, kind: str) -> list[str]:
    """Invariants on the filtered output itself."""
    problems, n, wrong_sub, out_of_range, unparsed = [], 0, 0, 0, 0
    y, mo = int(month[:4]), int(month[5:7])
    lo = datetime(y, mo, 1, tzinfo=timezone.utc).timestamp()
    hi = (datetime(y + (mo == 12), (mo % 12) + 1, 1, tzinfo=timezone.utc)
          .timestamp())
    authors = set()
    with gzip.open(path, "rt", errors="replace") as f:
        for line in f:
            n += 1
            try:
                r = json.loads(line)
            except Exception:
                unparsed += 1
                continue
            if r.get("subreddit") not in GATE_SUBS:
                wrong_sub += 1
            ts = float(r.get("created_utc", 0))
            if not (lo - 86400 <= ts < hi + 86400):
                out_of_range += 1
            if r.get("author"):
                authors.add(r["author"])
    if n == 0:
        problems.append(f"output: {os.path.basename(path)} is EMPTY")
    if unparsed:
        problems.append(f"output: {unparsed}/{n} lines unparseable")
    # The dump filter is a line-level PRE-filter and is deliberately
    # over-inclusive: a crosspost carries the parent's subreddit inside
    # crosspost_parent_list, so the line matches while the record's own
    # subreddit differs. extract_tickers.py is the authoritative filter and
    # re-checks each record's own field with a real JSON parse. A few
    # percent here is expected; a large fraction means the pattern is wrong.
    if n and wrong_sub / n > 0.10:
        problems.append(f"output: {wrong_sub}/{n} ({wrong_sub/n:.0%}) rows "
                        f"from foreign subs — too high for crosspost leak")
    elif wrong_sub:
        problems.append(f"NOTE output: {wrong_sub}/{n} ({wrong_sub/n:.1%}) "
                        f"crosspost rows — expected, removed by extractor")
    if out_of_range > n * 0.01:
        problems.append(f"output: {out_of_range}/{n} timestamps outside {month}")
    floor = 20_000 if kind == "RC" else 500
    if n and n < floor:
        problems.append(f"output: only {n} rows (floor {floor}) — suspicious")
    if n and len(authors) < 50:
        problems.append(f"output: only {len(authors)} distinct authors")
    return problems


if __name__ == "__main__":
    mode = sys.argv[1]
    probs = preflight(sys.argv[2]) if mode == "preflight" \
        else output(sys.argv[2], sys.argv[3], sys.argv[4])
    fatal = [p for p in probs if not p.startswith("NOTE")]
    for p in probs:
        print(("     " if p.startswith("NOTE") else "FAIL ") + p)
    print("PASS" if not fatal else f"{len(fatal)} problem(s)")
    sys.exit(1 if fatal else 0)
