#!/usr/bin/env python3
"""Variant gate: extract ticker mentions from the Reddit finance corpus.

Reads both acquisition tracks (monthly-dump filtered files and Arctic Shift
API shards), emits one row per (item, ticker) mention:
    author, time, subreddit, ticker, unit_type, kind, item_id

Unit rules (frozen in the gate registration before any eval):
  - CASHTAG (primary): $XYZ, case-insensitive, must resolve to a symbol in
    the SEC company_tickers table.
  - BARE (sensitivity lens): an uppercase 2-5 letter token in the SEC table
    and NOT in STOPLIST. Single letters are cashtag-only — 'A', 'F', 'T' are
    real symbols but overwhelmingly English in running text.
No LLM anywhere; deterministic and re-runnable.

Known caveat (disclosed in the registration): the SEC table lists CURRENT
registrants, so symbols delisted before the table snapshot are invisible.
This biases the census toward survivors; it does not affect whether a
suppressed pair among observed tickers forms.

Usage: extract_tickers.py [--limit N]
"""
import glob
import gzip
import json
import os
import re
import sys

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/Volumes/1TB NVME 1/antikythera/data/reddit_gate"
OUT = f"{BASE}/ticker_mentions.parquet"
SEC = f"{BASE}/company_tickers.json"

CASHTAG = re.compile(r"\$([A-Za-z]{1,5})\b")
BARE = re.compile(r"\b([A-Z]{2,5})\b")

# Uppercase tokens that are SEC symbols but read as English/finance jargon.
STOPLIST = {
    # pronouns / articles / prepositions / conjunctions
    "AN", "AND", "ANY", "ARE", "AS", "AT", "BE", "BY", "FOR", "IF", "IN",
    "IS", "IT", "ITS", "OF", "ON", "OR", "SO", "TO", "UP", "WE", "YOU",
    "HE", "ME", "MY", "NO", "NOT", "NOW", "ONE", "OUT", "THE", "ALL", "AM",
    "CAN", "DO", "GO", "HAS", "HOW", "NEW", "OLD", "SEE", "TWO", "WHO",
    "WHY", "YES", "GOOD", "BIG", "BUY", "MAX", "MIN", "NEXT", "OPEN",
    "REAL", "SAFE", "TRUE", "WELL", "BEST", "FREE", "FUN", "HOPE", "LOVE",
    "PLAY", "PLUS", "POST", "SAVE", "SO", "TECH", "TOP", "WIN", "WISH",
    # finance / forum jargon
    "ATH", "ATM", "CEO", "CFO", "CPI", "DD", "EOD", "EPS", "ETF", "EV",
    "FED", "FOMC", "FYI", "GDP", "IMO", "IMHO", "IPO", "IRA", "IV", "LEAP",
    "LOL", "NYSE", "OTC", "PE", "PM", "PT", "RSI", "SEC", "TA", "TLDR",
    "USA", "USD", "WSB", "YOLO", "YTD", "AMA", "TIL", "ELI", "EDIT", "PDT",
    "ROI", "P", "EBIT", "GAAP", "LLC", "INC", "ETH", "BTC", "NFT", "AI",
    "API", "CAGR", "DCF", "EBITDA", "FUD", "HODL", "ITM", "OTM", "QQQ",
    "SPY", "VIX", "YOY", "QOQ", "TTM", "AH", "PR", "SP", "US", "UK", "EU",
    "CA", "NY", "TX", "OK", "HI", "OH", "OR", "ID", "IN", "MA", "MD", "MI",
    "MN", "MO", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "PA", "RI",
    "SC", "SD", "TN", "UT", "VA", "VT", "WA", "WI", "WV", "WY", "AL", "AR",
    "AZ", "CO", "CT", "DE", "FL", "GA", "IA", "IL", "KS", "KY", "LA",
    # added 2026-08-30 after an outcome-blind audit of the top-100 bare hits:
    # tokens whose corpus usage is overwhelmingly not the company.
    "OP", "IRS", "TV", "WTF", "TD", "LINK", "RH", "CC", "PC", "UI", "DOW",
    "LOT", "WAY", "NYC", "VS", "JAN", "DEC", "HERE", "IP", "PS", "CPA",
    "ET", "WD", "SI", "DRS", "FCF", "DTE", "EOY", "COVID", "CBA", "GDPR",
    # Ambiguous but genuinely traded and heavily discussed (SHOP, BB, MU,
    # MS, SE, IQ, BYD, NET, ICE) are deliberately KEPT: excluding real
    # megacap/meme names would bias the census more than their noise does.
}


GATE_SUBS = {"wallstreetbets", "stocks", "investing", "SecurityAnalysis",
             "ValueInvesting", "StockMarket"}


def load_symbols() -> set[str]:
    return {r["ticker"].upper() for r in json.load(open(SEC)).values()
            if r.get("ticker")}


def iter_items():
    """Yield (author, ts, subreddit, item_id, text, kind) from both tracks."""
    for path in sorted(glob.glob(f"{BASE}/dump_filtered/filtered_*.ndjson.gz")):
        kind = "comment" if "_RC_" in path else "post"
        with gzip.open(path, "rt", errors="replace") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                text = (r.get("body") or "") if kind == "comment" else \
                    f"{r.get('title') or ''}\n{r.get('selftext') or ''}"
                yield (r.get("author"), r.get("created_utc"),
                       r.get("subreddit"), r.get("id"), text, kind)
    for path in sorted(glob.glob(f"{BASE}/pull/*.ndjson.gz")):
        base = os.path.basename(path)
        kind = "comment" if base.startswith("comments_") else "post"
        sub = base.split("_")[1]
        with gzip.open(path, "rt", errors="replace") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                text = (r.get("body") or "") if kind == "comment" else \
                    f"{r.get('title') or ''}\n{r.get('selftext') or ''}"
                yield (r.get("author"), r.get("created_utc"), sub,
                       r.get("id"), text, kind)


def main() -> None:
    symbols = load_symbols()
    print(f"SEC symbols: {len(symbols)}", flush=True)
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0
    cols = {k: [] for k in ("author", "time", "subreddit", "ticker",
                            "unit_type", "kind", "item_id")}
    n_items = n_rows = 0
    seen_ids: set[str] = set()
    for author, ts, sub, item_id, text, kind in iter_items():
        n_items += 1
        if n_items % 2_000_000 == 0:
            print(f"  {n_items} items, {n_rows} mentions", flush=True)
        if limit and n_items > limit:
            break
        if not author or author in ("[deleted]", "AutoModerator") or not ts:
            continue
        # The dump filter matches the subreddit field anywhere in the line, so
        # crossposts carrying a gate sub inside crosspost_parent_list leak in
        # (BBBY, WallStreetbetsELITE, ... — ~0.05% of rows). Require the
        # item's OWN subreddit to be a gate sub.
        if sub not in GATE_SUBS:
            continue
        if item_id in seen_ids:      # dump/API overlap -> keep one copy
            continue
        seen_ids.add(item_id)
        found = {}
        for m in CASHTAG.finditer(text):
            t = m.group(1).upper()
            if t in symbols:
                found[t] = "cashtag"
        for m in BARE.finditer(text):
            t = m.group(1)
            if t in symbols and t not in STOPLIST and t not in found:
                found[t] = "bare"
        for t, unit in found.items():
            cols["author"].append(author)
            cols["time"].append(int(ts))
            cols["subreddit"].append(sub)
            cols["ticker"].append(t)
            cols["unit_type"].append(unit)
            cols["kind"].append(kind)
            cols["item_id"].append(item_id)
            n_rows += 1
    table = pa.table({
        "author": cols["author"],
        "time": pa.array(cols["time"], pa.int64()),
        "subreddit": cols["subreddit"],
        "ticker": cols["ticker"],
        "unit_type": cols["unit_type"],
        "kind": cols["kind"],
        "item_id": cols["item_id"],
    })
    pq.write_table(table, OUT, compression="zstd")
    print(f"items {n_items} | mentions {n_rows} | unique items {len(seen_ids)}",
          flush=True)


if __name__ == "__main__":
    main()
