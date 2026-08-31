#!/usr/bin/env python3
"""Variant-gate corpus pull: Reddit finance subs via the Arctic Shift API.

Resume-safe: one shard per (kind, subreddit, year); each shard paginates by
descending created_utc cursor and checkpoints after every batch. Output:
ndjson (one line per item) per shard, gzip'd on completion. Polite: single
worker, ~2 req/s ceiling, exponential backoff on errors/timeouts.

Usage: pull_reddit_gate.py SUB YEAR_START YEAR_END      (years inclusive)
       pull_reddit_gate.py SUB --month YYYY-MM [YYYY-MM ...]  (single months)
"""
import gzip
import json
import os
import sys
import time
import urllib.parse
import urllib.request

OUT = os.environ.get("PULL_OUT",
    "/Volumes/1TB NVME 1/antikythera/data/reddit_gate/pull")
API = "https://arctic-shift.photon-reddit.com/api"
FIELDS = {
    "comments": "id,author,created_utc,body,link_id",
    "posts": "id,author,created_utc,title,selftext",
}
UA = "antikythera-gate/0.1 (research; contact kquiring@gmail.com)"


def fetch(url: str) -> dict:
    delay = 1.0
    for attempt in range(8):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(delay)
            delay = min(delay * 2, 120)
    raise RuntimeError(f"gave up: {url}")


def pull_shard(kind: str, sub: str, year, before: str = None,
               after: str = None) -> None:
    os.makedirs(OUT, exist_ok=True)
    tag = f"{kind}_{sub}_{year}"
    done_path = os.path.join(OUT, f"{tag}.ndjson.gz")
    part_path = os.path.join(OUT, f"{tag}.part")
    ck_path = os.path.join(OUT, f"{tag}.cursor")
    if os.path.exists(done_path):
        print(f"{tag}: done (cached)", flush=True)
        return
    if before is None:
        before = f"{year + 1}-01-01"
    if os.path.exists(ck_path):
        before = open(ck_path).read().strip()
    n = 0
    with open(part_path, "a") as out:
        while True:
            q = urllib.parse.urlencode({
                "subreddit": sub, "limit": "auto", "fields": FIELDS[kind],
                "after": after or f"{year}-01-01", "before": before,
                "sort": "desc",
            })
            data = fetch(f"{API}/{kind}/search?{q}").get("data") or []
            if not data:
                break
            for row in data:
                out.write(json.dumps(row) + "\n")
            n += len(data)
            before = str(min(r["created_utc"] for r in data))
            out.flush()
            with open(ck_path, "w") as ck:
                ck.write(before)
            if n % 30000 < len(data):
                print(f"{tag}: {n} rows (cursor {before})", flush=True)
            time.sleep(float(os.environ.get("PULL_SLEEP", "0.4")))
    with open(part_path, "rb") as f_in, gzip.open(done_path + ".tmp", "wb") as f_out:
        f_out.writelines(f_in)
    os.replace(done_path + ".tmp", done_path)
    os.remove(part_path)
    if os.path.exists(ck_path):
        os.remove(ck_path)
    print(f"{tag}: COMPLETE {n} rows", flush=True)


def month_bounds(m: str):
    y, mo = int(m[:4]), int(m[5:7])
    nxt = f"{y + (mo == 12):04d}-{(mo % 12) + 1:02d}-01"
    return f"{m}-01", nxt


def main() -> None:
    sub = sys.argv[1]
    if sys.argv[2] == "--month":
        for m in sys.argv[3:]:
            after, before = month_bounds(m)
            for kind in ("comments", "posts"):
                pull_shard(kind, sub, m, before=before, after=after)
        return
    y0, y1 = int(sys.argv[2]), int(sys.argv[3])
    for year in range(y0, y1 + 1):
        for kind in ("comments", "posts"):
            pull_shard(kind, sub, year)


if __name__ == "__main__":
    main()
