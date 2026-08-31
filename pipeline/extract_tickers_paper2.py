#!/usr/bin/env python3
"""Paper 2: extract ticker mentions from the paper-2 API corpus.

Unit rules are IMPORTED from the frozen gate extractor (extract_tickers.py:
CASHTAG/BARE regexes, STOPLIST, SEC resolution, GATE_SUBS, hygiene) so the
definitions are identical by construction, not by copy. Differences from the
gate extractor, all mechanical:
  - input: data/paper2/pull only (single source, single era — no dump track)
  - output: data/paper2/ticker_mentions.parquet, schema + `score` column
    (passthrough for the separately-registered engagement follow-up; no
    registered paper-2 readout uses it)
  - dedup scope is per (kind, shard file): within one pull era duplicates
    can only arise from cursor-resume re-fetches, which land in the same
    shard; global dedup would need a ~90M-id set for no additional benefit
    and risks cross-kind id collisions (t1_/t3_ namespaces share raw ids).

Outcome-blind: emits mentions only; no census, no statistic.
"""
import glob
import gzip
import json
import os
import sys

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_tickers import (  # noqa: E402  (frozen unit rules)
    CASHTAG, BARE, STOPLIST, GATE_SUBS, load_symbols)

PULL = "/Volumes/1TB NVME 1/antikythera/data/paper2/pull"
OUT = "/Volumes/1TB NVME 1/antikythera/data/paper2/ticker_mentions.parquet"


def main() -> None:
    symbols = load_symbols()
    print(f"SEC symbols: {len(symbols)}", flush=True)
    cols = {k: [] for k in ("author", "time", "subreddit", "ticker",
                            "unit_type", "kind", "item_id", "score")}
    n_items = n_rows = n_dup = 0
    for path in sorted(glob.glob(f"{PULL}/*.ndjson.gz")):
        base = os.path.basename(path)
        kind = "comment" if base.startswith("comments_") else "post"
        sub = base.split("_")[1]
        if sub not in GATE_SUBS:
            raise RuntimeError(f"unexpected sub in shard name: {base}")
        seen_ids: set[str] = set()   # per-shard: resume-duplicate scope
        with gzip.open(path, "rt", errors="replace") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                n_items += 1
                if n_items % 5_000_000 == 0:
                    print(f"  {n_items} items, {n_rows} mentions "
                          f"({n_dup} dups) at {base}", flush=True)
                author, ts, item_id = r.get("author"), r.get("created_utc"), r.get("id")
                if not author or author in ("[deleted]", "AutoModerator") \
                        or not ts:
                    continue
                if item_id in seen_ids:
                    n_dup += 1
                    continue
                seen_ids.add(item_id)
                text = (r.get("body") or "") if kind == "comment" else \
                    f"{r.get('title') or ''}\n{r.get('selftext') or ''}"
                found = {}
                for m in CASHTAG.finditer(text):
                    t = m.group(1).upper()
                    if t in symbols:
                        found[t] = "cashtag"
                for m in BARE.finditer(text):
                    t = m.group(1)
                    if t in symbols and t not in STOPLIST and t not in found:
                        found[t] = "bare"
                score = r.get("score")
                for t, unit in found.items():
                    cols["author"].append(author)
                    cols["time"].append(int(ts))
                    cols["subreddit"].append(sub)
                    cols["ticker"].append(t)
                    cols["unit_type"].append(unit)
                    cols["kind"].append(kind)
                    cols["item_id"].append(item_id)
                    cols["score"].append(None if score is None else int(score))
                    n_rows += 1
    table = pa.table({
        "author": cols["author"],
        "time": pa.array(cols["time"], pa.int64()),
        "subreddit": cols["subreddit"],
        "ticker": cols["ticker"],
        "unit_type": cols["unit_type"],
        "kind": cols["kind"],
        "item_id": cols["item_id"],
        "score": pa.array(cols["score"], pa.int64()),
    })
    pq.write_table(table, OUT, compression="zstd")
    print(f"items {n_items} | mentions {n_rows} | resume-dups {n_dup}",
          flush=True)


if __name__ == "__main__":
    main()
