#!/usr/bin/env python3
"""Pilot 0 extraction conveyor: claims from ALL filtered-story titles,
batched ~45 titles/call (amortizes prompt overhead ~15x on short inputs).

Extractor: DeepSeek V4 Flash, thinking disabled.
Cache: per-doc parsed claims under extractor id (immutable, resume-safe);
raw batch responses under data/extractions_raw/<extractor>/ for audit.
Failed batches: one retry with a corrective suffix, then logged + skipped
(missing docs re-batched on the next run).

Usage: pilot0_extract.py [--limit-batches N] [--budget-usd 35]
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
EXTRACTOR_ID = "deepseek-v4-flash-nothink_ptitles1_svt1"
MODEL = "deepseek-v4-flash"
BATCH = 45
PRICE_IN, PRICE_OUT = 0.14, 0.28  # $/M tokens
SCHEMA = json.load(open(os.path.join(ROOT, "schema", "extraction_titles.schema.json")))
PROMPT = open(os.path.join(ROOT, "prompts", "extraction_titles_v1.md")).read().split("---\n", 1)[1].strip()
RAW_DIR = os.path.join(ROOT, "data", "extractions_raw", EXTRACTOR_ID)
FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)

spend_lock = threading.Lock()
spend = {"in": 0, "out": 0, "calls": 0, "failed_batches": 0}


def load_env() -> None:
    for line in open(os.path.join(ROOT, ".env")):
        line = line.split("#")[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def pending_docs() -> list[tuple[int, str]]:
    con = duckdb.connect()
    rows = con.sql(f"""
        SELECT doc_id, title FROM read_parquet('{ROOT}/data/docs/docs_*.parquet')
        WHERE length(title) > 0 ORDER BY doc_id
    """).fetchall()
    return [(d, t) for d, t in rows if not cache.has(EXTRACTOR_ID, d)]


def call_batch(client: openai.OpenAI, batch: list[tuple[int, str]], corrective: str = "") -> dict:
    lines = "\n".join(f"{i}|{title}" for i, (_, title) in enumerate(batch))
    r = client.chat.completions.create(
        model=MODEL, max_tokens=6000,
        extra_body={"thinking": {"type": "disabled"}},
        messages=[{"role": "system", "content": PROMPT + corrective},
                  {"role": "user", "content": lines}])
    with spend_lock:
        spend["in"] += r.usage.prompt_tokens
        spend["out"] += r.usage.completion_tokens
        spend["calls"] += 1
    return {"raw": r.choices[0].message.content or "", "stop": r.choices[0].finish_reason}


def parse_batch(raw: str, n: int) -> list[list[str]] | None:
    m = FENCE.match(raw)
    try:
        data = json.loads(m.group(1) if m else raw)
        jsonschema.validate(data, SCHEMA)
    except (json.JSONDecodeError, jsonschema.ValidationError):
        return None
    by_i = {item["i"]: item["claims"] for item in data["items"]}
    if set(by_i) != set(range(n)):
        return None
    return [by_i[i] for i in range(n)]


def process_batch(client: openai.OpenAI, batch_no: int, batch: list[tuple[int, str]]) -> bool:
    for attempt, corrective in enumerate((
            "",
            "\n\nREMINDER: raw JSON only; every index 0..N-1 exactly once.")):
        try:
            result = call_batch(client, batch, corrective)
        except openai.APIStatusError as e:
            if e.status_code == 402:  # out of balance: halt run, don't grind
                raise SystemExit("402 Insufficient Balance — top up and re-run")
            time.sleep(5 * (attempt + 1))
            continue
        except openai.APIError:
            time.sleep(5 * (attempt + 1))
            continue
        claims = parse_batch(result["raw"], len(batch))
        if claims is not None:
            os.makedirs(RAW_DIR, exist_ok=True)
            with open(os.path.join(RAW_DIR, f"batch_{batch[0][0]}.json"), "w") as f:
                json.dump({"docs": [d for d, _ in batch], **result}, f)
            for (doc_id, title), doc_claims in zip(batch, claims):
                if not cache.has(EXTRACTOR_ID, doc_id):
                    cache.put(EXTRACTOR_ID, doc_id, {"doc_id": doc_id, "claims": doc_claims})
            return True
    with spend_lock:
        spend["failed_batches"] += 1
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-batches", type=int, default=0)
    ap.add_argument("--budget-usd", type=float, default=35.0)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()
    load_env()
    client = openai.OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                           base_url="https://api.deepseek.com", max_retries=3)

    docs = pending_docs()
    batches = [docs[i:i + BATCH] for i in range(0, len(docs), BATCH)]
    if args.limit_batches:
        batches = batches[: args.limit_batches]
    print(f"{EXTRACTOR_ID}: {len(docs)} pending docs, {len(batches)} batches", flush=True)

    done = 0
    stop = threading.Event()

    def run(i_b):
        i, b = i_b
        if stop.is_set():
            return
        process_batch(client, i, b)
        nonlocal done
        with spend_lock:
            done += 1
            cost = spend["in"] / 1e6 * PRICE_IN + spend["out"] / 1e6 * PRICE_OUT
            if done % 200 == 0:
                print(f"{done}/{len(batches)} batches | ${cost:.2f} | "
                      f"{spend['failed_batches']} failed", flush=True)
        if cost > args.budget_usd:
            stop.set()
            print(f"BUDGET STOP at ${cost:.2f}", flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(run, enumerate(batches)))

    cost = spend["in"] / 1e6 * PRICE_IN + spend["out"] / 1e6 * PRICE_OUT
    print(f"DONE: {done} batches, {spend['calls']} calls, "
          f"{spend['in']} in / {spend['out']} out tokens, ${cost:.2f}, "
          f"{spend['failed_batches']} failed batches", flush=True)


if __name__ == "__main__":
    main()
