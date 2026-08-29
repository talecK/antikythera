#!/usr/bin/env python3
"""Pilot 1 extraction conveyor: full docs (title + self-text + top comments)
for the pre-registered fold years, one doc per call.

Extractor: deepseek-v4-flash, thinking disabled, prompt v2 — SAME extractor
id as the smoke test (deepseek-v4-flash-nothink_pv2_sv1), so its cache
namespace and record shape ({doc_id, raw, stop_reason, usage}) carry over;
already-extracted docs are skipped.

Usage: pilot1_extract.py --years 2015 2016 2017 [--budget-usd 60]
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import threading
import time

import duckdb
import jsonschema
import openai

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTOR_ID = "deepseek-v4-flash-nothink_pv2_sv1"
MODEL = "deepseek-v4-flash"
PRICE_IN, PRICE_OUT = 0.14, 0.28
SCHEMA = json.load(open(os.path.join(ROOT, "schema", "extraction.schema.json")))
PROMPT = open(os.path.join(ROOT, "prompts", "extraction_v2.md")).read().split("---\n", 1)[1].strip()
FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)

lock = threading.Lock()
spend = {"in": 0, "out": 0, "docs": 0, "parse_fail": 0}


def load_env() -> None:
    for line in open(os.path.join(ROOT, ".env")):
        line = line.split("#")[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def parses(raw: str) -> bool:
    m = FENCE.match(raw)
    try:
        jsonschema.validate(json.loads(m.group(1) if m else raw), SCHEMA)
        return True
    except (json.JSONDecodeError, jsonschema.ValidationError):
        # lenient normalizer path: drop unexpected top-level keys / null quotes
        try:
            data = json.loads((FENCE.match(raw) or re.match(r"(.*)", raw, re.S)).group(1))
            return isinstance(data, dict) and isinstance(data.get("claims"), list)
        except Exception:
            return False


def extract_doc(client: openai.OpenAI, doc_id: int, text: str) -> None:
    if cache.has(EXTRACTOR_ID, doc_id):
        return
    record = None
    for attempt, suffix in enumerate(("", "\n\nREMINDER: raw JSON only, exactly as specified.")):
        try:
            r = client.chat.completions.create(
                model=MODEL, max_tokens=2000,
                extra_body={"thinking": {"type": "disabled"}},
                messages=[{"role": "system", "content": PROMPT + suffix},
                          {"role": "user", "content": text}])
        except openai.APIStatusError as e:
            if e.status_code == 402:
                raise SystemExit("402 Insufficient Balance — top up and re-run")
            time.sleep(5 * (attempt + 1))
            continue
        except openai.APIError:
            time.sleep(5 * (attempt + 1))
            continue
        with lock:
            spend["in"] += r.usage.prompt_tokens
            spend["out"] += r.usage.completion_tokens
        raw = r.choices[0].message.content or ""
        record = {"doc_id": doc_id, "raw": raw,
                  "stop_reason": r.choices[0].finish_reason,
                  "usage": {"in": r.usage.prompt_tokens, "out": r.usage.completion_tokens}}
        if parses(raw):
            break
    if record is None:
        with lock:
            spend["parse_fail"] += 1
        return
    if not parses(record["raw"]):
        with lock:
            spend["parse_fail"] += 1
    cache.put(EXTRACTOR_ID, doc_id, record)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs="+", type=int, required=True)
    ap.add_argument("--budget-usd", type=float, default=60.0)
    ap.add_argument("--workers", type=int, default=48)
    args = ap.parse_args()
    load_env()
    client = openai.OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                           base_url="https://api.deepseek.com", max_retries=3)
    con = duckdb.connect()
    files = ", ".join(f"'{ROOT}/data/docs/docs_{y}.parquet'" for y in args.years)
    docs = con.sql(f"SELECT doc_id, text FROM read_parquet([{files}]) ORDER BY doc_id").fetchall()
    todo = [(d, t) for d, t in docs if not cache.has(EXTRACTOR_ID, d)]
    print(f"{EXTRACTOR_ID}: {len(todo)} of {len(docs)} docs to extract", flush=True)

    stop = threading.Event()
    done = [0]

    def run(dt):
        if stop.is_set():
            return
        extract_doc(client, dt[0], dt[1])
        with lock:
            done[0] += 1
            cost = spend["in"] / 1e6 * PRICE_IN + spend["out"] / 1e6 * PRICE_OUT
            if done[0] % 2000 == 0:
                print(f"{done[0]}/{len(todo)} docs | ${cost:.2f} | "
                      f"{spend['parse_fail']} parse-fail", flush=True)
            if cost > args.budget_usd:
                stop.set()
                print(f"BUDGET STOP at ${cost:.2f}", flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(run, todo))
    cost = spend["in"] / 1e6 * PRICE_IN + spend["out"] / 1e6 * PRICE_OUT
    print(f"DONE: {done[0]} docs, {spend['in']} in / {spend['out']} out, "
          f"${cost:.2f}, {spend['parse_fail']} parse-fail", flush=True)


if __name__ == "__main__":
    main()
