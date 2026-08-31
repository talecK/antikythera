#!/usr/bin/env python3
"""Does API-sourced data cover the same items as dump-sourced data?

Fold B's WSB months come from the torrent; unavailable months would have to
be API-filled, which would put a provenance seam INSIDE fold B. This
measures whether that seam changes coverage, using a 3-day window of
2023-03 (a month held from BOTH sources).
"""
import gzip
import json
import os
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pull_reddit_gate import API, fetch  # noqa: E402

BASE = "/Volumes/1TB NVME 1/antikythera/data/reddit_gate"
LO, HI = "2023-03-14", "2023-03-17"

api_ids, n, before = set(), 0, HI
while True:
    q = urllib.parse.urlencode({
        "subreddit": "wallstreetbets", "limit": "auto",
        "fields": "id,created_utc", "after": LO, "before": before,
        "sort": "desc"})
    data = fetch(f"{API}/comments/search?{q}").get("data") or []
    if not data:
        break
    for r in data:
        api_ids.add(r["id"])
    n += len(data)
    before = str(min(r["created_utc"] for r in data))
    if n % 20000 < len(data):
        print(f"  api {n} rows", flush=True)
    time.sleep(0.4)
print(f"API  WSB {LO}..{HI}: {len(api_ids)} unique ids", flush=True)

import datetime as dt
lo_ts = dt.datetime.fromisoformat(LO).replace(tzinfo=dt.timezone.utc).timestamp()
hi_ts = dt.datetime.fromisoformat(HI).replace(tzinfo=dt.timezone.utc).timestamp()
dump_ids = set()
with gzip.open(f"{BASE}/dump_filtered/filtered_RC_2023-03.ndjson.gz", "rt",
               errors="replace") as f:
    for line in f:
        r = json.loads(line)
        if r.get("subreddit") == "wallstreetbets" and \
           lo_ts <= float(r["created_utc"]) < hi_ts:
            dump_ids.add(r["id"])
print(f"DUMP WSB {LO}..{HI}: {len(dump_ids)} unique ids", flush=True)

both, a_only, d_only = api_ids & dump_ids, api_ids - dump_ids, dump_ids - api_ids
tot = len(api_ids | dump_ids)
print(f"\nboth {len(both)} | API-only {len(a_only)} | DUMP-only {len(d_only)}")
print(f"API covers {len(api_ids)/max(tot,1):.2%} of union; "
      f"DUMP covers {len(dump_ids)/max(tot,1):.2%}")
print(f"ratio API/DUMP = {len(api_ids)/max(len(dump_ids),1):.4f}")
