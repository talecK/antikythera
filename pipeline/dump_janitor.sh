#!/bin/bash
# Deletes downloaded dump files whose filtered output already exists.
# Guards against slot-cleanup misses in pull_dump_months.py stalling on disk.
BASE="/Volumes/1TB NVME 1/antikythera/data/reddit_gate"
while true; do
  for f in "$BASE"/dl*/reddit/*/*.zst; do
    [ -e "$f" ] || continue
    b=$(basename "$f" .zst)          # e.g. RC_2023-01
    kind=${b%%_*}; month=${b#*_}
    out="$BASE/dump_filtered/filtered_${kind}_${month}.ndjson.gz"
    if [ -f "$out" ] && [ -s "$f" ]; then
      echo "$(date +%H:%M:%S) janitor: removing $b (filtered output exists)"
      rm -f "$f"
    fi
  done
  sleep 300
done
