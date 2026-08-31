#!/usr/bin/env python3
"""Fast subreddit filter for Reddit monthly dumps (stdin -> stdout, ndjson).

Chunk-scans bytes with one compiled regex instead of per-line matching:
~540MB/s vs ~111MB/s for BSD `grep -aiE` (measured 2026-08-30 on this box).
Match is case-sensitive on canonical subreddit casing, and tolerates the
optional space after the colon that the post-2023-03 crawler emits.
"""
import re
import sys

SUBS = ["wallstreetbets", "stocks", "investing", "SecurityAnalysis",
        "ValueInvesting", "StockMarket"]
# Two dump formats exist. Pushshift-era files (through 2023-03) are compact
# JSON: {"subreddit":"stocks"}. Arctic Shift's own crawler (2023-04 onward)
# emits spaces after colons: {"subreddit": "stocks"}. Matching only the
# compact form silently yields ZERO rows for every post-seam month.
PAT = re.compile(b'"subreddit": ?"(?:' + b"|".join(s.encode() for s in SUBS) + b')"')
CHUNK = 1 << 26


def main() -> None:
    inp, out = sys.stdin.buffer, sys.stdout.buffer
    tail, n = b"", 0
    while True:
        chunk = inp.read(CHUNK)
        if not chunk:
            break
        buf = tail + chunk
        cut = buf.rfind(b"\n") + 1
        tail, body = buf[cut:], buf[:cut]
        if PAT.search(body):
            for line in body.split(b"\n"):
                if PAT.search(line):
                    out.write(line + b"\n")
                    n += 1
    if tail and PAT.search(tail):
        out.write(tail + b"\n")
        n += 1
    sys.stderr.write(f"kept {n}\n")


if __name__ == "__main__":
    main()
