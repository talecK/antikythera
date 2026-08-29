#!/usr/bin/env python3
"""Schema-hygiene smoke test (action item 5): N docs through one extractor,
measure native JSON/schema discipline. No provider-side format enforcement —
the test measures the model's own output hygiene so results are comparable
across future candidates (Qwen/DeepSeek/Gemini).

Usage: smoke_test.py --extractor haiku-4-5 [--n-per-year 5]
Raw responses cached immutably via cache.py (same namespace the conveyor
would use: these docs never need re-extraction).
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import statistics
import sys

import anthropic
import duckdb
import jsonschema

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, "schema", "extraction.schema.json")))

EXTRACTORS = {
    # extractor_id -> (provider, model id, prompt file). Prompt/schema versions
    # are part of the id: changing either mints a new cache namespace.
    "haiku-4-5_pv1_sv1": ("anthropic", "claude-haiku-4-5", "extraction_v1.md"),
    "haiku-4-5_pv2_sv1": ("anthropic", "claude-haiku-4-5", "extraction_v2.md"),
}


def load_prompt(name: str) -> str:
    return open(os.path.join(ROOT, "prompts", name)).read().split("---\n", 1)[1].strip()

FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)


def load_env() -> None:
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path):
            line = line.split("#")[0].strip()
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def sample_docs(n_per_year: int) -> list[tuple[int, str]]:
    con = duckdb.connect()
    return con.sql(f"""
        SELECT doc_id, text FROM (
            SELECT doc_id, text,
                   row_number() OVER (
                       PARTITION BY year(time)
                       ORDER BY (doc_id * 2654435761) % 4294967296
                   ) AS rn
            FROM read_parquet('{ROOT}/data/docs/docs_*.parquet')
        ) WHERE rn <= {n_per_year} ORDER BY doc_id
    """).fetchall()


def extract_one(client: anthropic.Anthropic, model: str, extractor_id: str,
                prompt: str, doc_id: int, text: str) -> dict:
    cached = cache.get(extractor_id, doc_id)
    if cached is not None:
        return cached
    response = client.messages.create(
        model=model,
        max_tokens=2000,
        system=prompt,
        messages=[{"role": "user", "content": text}],
    )
    raw = next((b.text for b in response.content if b.type == "text"), "")
    record = {
        "doc_id": doc_id,
        "raw": raw,
        "stop_reason": response.stop_reason,
        "usage": {"in": response.usage.input_tokens, "out": response.usage.output_tokens},
    }
    cache.put(extractor_id, doc_id, record)
    return record


def grade(record: dict) -> dict:
    raw = record["raw"]
    fenced = bool(FENCE.match(raw))
    body = FENCE.match(raw).group(1) if fenced else raw
    out = {"doc_id": record["doc_id"], "fenced": fenced, "json_ok": False,
           "schema_ok": False, "n_claims": 0, "claims": []}
    try:
        data = json.loads(body)
        out["json_ok"] = True
    except json.JSONDecodeError:
        return out
    try:
        jsonschema.validate(data, SCHEMA)
        out["schema_ok"] = True
        out["n_claims"] = len(data["claims"])
        out["claims"] = [c["claim"] for c in data["claims"]]
    except jsonschema.ValidationError as e:
        out["error"] = e.message[:120]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extractor", default="haiku-4-5_pv1_sv1", choices=EXTRACTORS)
    ap.add_argument("--n-per-year", type=int, default=5)
    args = ap.parse_args()
    load_env()
    provider, model, prompt_file = EXTRACTORS[args.extractor]
    assert provider == "anthropic", "only anthropic wired up so far"
    prompt = load_prompt(prompt_file)
    client = anthropic.Anthropic()

    docs = sample_docs(args.n_per_year)
    print(f"{args.extractor}: {len(docs)} docs")
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(
            lambda d: extract_one(client, model, args.extractor, prompt, d[0], d[1]), docs))

    graded = [grade(r) for r in records]
    n = len(graded)
    json_ok = sum(g["json_ok"] for g in graded)
    schema_ok = sum(g["schema_ok"] for g in graded)
    fenced = sum(g["fenced"] for g in graded)
    counts = [g["n_claims"] for g in graded if g["schema_ok"]]
    tok_in = sum(r["usage"]["in"] for r in records)
    tok_out = sum(r["usage"]["out"] for r in records)
    print(f"json_ok    {json_ok}/{n}")
    print(f"schema_ok  {schema_ok}/{n}")
    print(f"fenced     {fenced}/{n} (fences tolerated but counted against hygiene)")
    if counts:
        print(f"claims/doc min {min(counts)} / median {statistics.median(counts)} / max {max(counts)}")
        print(f"zero-claim docs: {sum(1 for c in counts if c == 0)}")
    print(f"tokens: {tok_in} in / {tok_out} out "
          f"(haiku cost ≈ ${tok_in / 1e6 * 1 + tok_out / 1e6 * 5:.2f})")
    for g in graded:
        if g["schema_ok"] is False:
            print(f"  BAD doc {g['doc_id']}: json_ok={g['json_ok']} {g.get('error', '')}")
    print("\n-- sample claims (granularity eyeball) --")
    for g in graded[:60]:
        for c in g["claims"][:2]:
            print(f"  {c}")


if __name__ == "__main__":
    main()
