#!/usr/bin/env python3
"""Adjudicate gray-zone merge candidates (SAME/DISTINCT/UNSURE) and emit the
merged registry v2. Runs under the x86 .venv (API work, no torch/faiss).

Input:  REGISTRY_OUT/{gray_pairs.json, registry.json, claims.parquet, assignments.npy}
Output: REGISTRY_OUT/{verdicts.json, registry_v2.json, report_v2.txt}

Verdict application: SAME -> claim's idea merges into the matched idea
(union-find over idea ids, so chains collapse transitively). UNSURE/DISTINCT
-> stays separate (brief: UNSURE = DISTINCT until next rebuild).
Calls cached in data/extractions/<adjudicator_id>/ keyed by pair hash batch.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import sys
import threading
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("REGISTRY_OUT", os.path.join(ROOT, "data", "registry", "pilot0"))
PAIRS_PER_CALL = 20
FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)

PROMPT = open(os.path.join(ROOT, "prompts", "adjudication_v1.md")).read().split("---\n", 1)[1].strip()

ADJUDICATORS = {
    "deepseek": ("deepseek-v4-flash", 0.14, 0.28),
    "haiku": ("claude-haiku-4-5", 1.0, 5.0),
}

spend_lock = threading.Lock()
spend = {"in": 0, "out": 0, "bad": 0}


def load_env():
    for line in open(os.path.join(ROOT, ".env")):
        line = line.split("#")[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def make_caller(provider: str):
    model, _, _ = ADJUDICATORS[provider]
    if provider == "haiku":
        import anthropic
        client = anthropic.Anthropic()

        def call(user: str) -> str:
            r = client.messages.create(model=model, max_tokens=3000,
                                       system=PROMPT,
                                       messages=[{"role": "user", "content": user}])
            with spend_lock:
                spend["in"] += r.usage.input_tokens
                spend["out"] += r.usage.output_tokens
            return next((b.text for b in r.content if b.type == "text"), "")
        return call
    import openai
    client = openai.OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                           base_url="https://api.deepseek.com", max_retries=3)

    def call(user: str) -> str:
        r = client.chat.completions.create(
            model=model, max_tokens=3000,
            extra_body={"thinking": {"type": "disabled"}},
            messages=[{"role": "system", "content": PROMPT},
                      {"role": "user", "content": user}])
        with spend_lock:
            spend["in"] += r.usage.prompt_tokens
            spend["out"] += r.usage.completion_tokens
        return r.choices[0].message.content or ""
    return call


def format_batch(batch: list[dict]) -> str:
    lines = []
    for p in batch:
        lines.append(f"PAIR {p['pid']}")
        lines.append(f"A: {p['a']}")
        lines.append(f"B: {p['b']}")
    return "\n".join(lines)


def parse_verdicts(raw: str, expected: set[str]) -> dict | None:
    m = FENCE.match(raw)
    try:
        data = json.loads(m.group(1) if m else raw)
        out = {v["pair"]: v["verdict"] for v in data["verdicts"]
               if v.get("verdict") in ("SAME", "DISTINCT", "UNSURE")}
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    return out if set(out) == expected else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="deepseek", choices=ADJUDICATORS)
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--limit", type=int, default=0, help="cap pairs (0=all)")
    args = ap.parse_args()
    load_env()
    _, price_in, price_out = ADJUDICATORS[args.provider]

    import pyarrow.parquet as pq
    gray = json.load(open(os.path.join(OUT, "gray_pairs.json")))
    ideas = json.load(open(os.path.join(OUT, "registry.json")))
    claims = pq.read_table(os.path.join(OUT, "claims.parquet"))["claim"].to_pylist()
    assign = np.load(os.path.join(OUT, "assignments.npy"))
    if args.limit:
        gray = gray[: args.limit]

    cache_dir = os.path.join(ROOT, "data", "extractions",
                             f"adjudicate-{args.provider}_av1")
    os.makedirs(cache_dir, exist_ok=True)

    pairs = []
    for row, idea_id, cos in gray:
        a, b = claims[row], ideas[idea_id]["canonical"]
        pid = hashlib.sha1(f"{a}||{b}".encode()).hexdigest()[:12]
        pairs.append({"pid": pid, "a": a, "b": b, "row": row, "idea": idea_id})
    # dedupe identical text pairs
    uniq = {p["pid"]: p for p in pairs}
    todo = [p for p in uniq.values()
            if not os.path.exists(os.path.join(cache_dir, p["pid"] + ".json"))]
    print(f"{len(gray)} gray pairs -> {len(uniq)} unique, {len(todo)} to call "
          f"({args.provider})", flush=True)

    call = make_caller(args.provider)
    batches = [todo[i:i + PAIRS_PER_CALL] for i in range(0, len(todo), PAIRS_PER_CALL)]
    done = [0]

    def run(batch):
        expected = {p["pid"] for p in batch}
        for attempt in range(2):
            try:
                raw = call(format_batch(batch))
            except Exception as e:
                if "402" in str(e) or "Insufficient Balance" in str(e):
                    raise SystemExit("402 Insufficient Balance — top up and re-run")
                time.sleep(5 * (attempt + 1))
                continue
            verdicts = parse_verdicts(raw, expected)
            if verdicts:
                for p in batch:
                    with open(os.path.join(cache_dir, p["pid"] + ".json"), "w") as f:
                        json.dump({"pid": p["pid"], "verdict": verdicts[p["pid"]]}, f)
                break
        else:
            with spend_lock:
                spend["bad"] += 1
        done[0] += 1
        if done[0] % 100 == 0:
            cost = spend["in"] / 1e6 * price_in + spend["out"] / 1e6 * price_out
            print(f"{done[0]}/{len(batches)} batches | ${cost:.2f} | {spend['bad']} bad",
                  flush=True)

    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(run, batches))

    # apply verdicts: union-find over idea ids
    parent = list(range(len(ideas)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    merged = 0
    for p in uniq.values():
        vf = os.path.join(cache_dir, p["pid"] + ".json")
        if not os.path.exists(vf):
            continue
        if json.load(open(vf))["verdict"] == "SAME":
            a, b = find(int(assign[p["row"]])), find(p["idea"])
            if a != b:
                parent[max(a, b)] = min(a, b)
                merged += 1

    roots: dict[int, int] = {}
    for i in range(len(ideas)):
        roots.setdefault(find(i), 0)
    for row in range(len(assign)):
        roots[find(int(assign[row]))] = roots.get(find(int(assign[row])), 0) + 1

    v2 = []
    for root, n in roots.items():
        rec = dict(ideas[root])
        rec["n"] = n
        v2.append(rec)
    json.dump(v2, open(os.path.join(OUT, "registry_v2.json"), "w"))

    cost = spend["in"] / 1e6 * price_in + spend["out"] / 1e6 * price_out
    ns = sorted((i["n"] for i in v2), reverse=True)
    singles = sum(1 for n in ns if n == 1)
    lines = [
        f"adjudicated {len(uniq)} unique pairs, {merged} SAME merges applied, ${cost:.2f}",
        f"registry v2: {len(v2)} ideas (was {len(ideas)}) | singletons {singles} ({singles / len(v2):.0%})",
        f"top-10 sizes: {ns[:10]}",
    ]
    print("\n".join(lines), flush=True)
    open(os.path.join(OUT, "report_v2.txt"), "w").write("\n".join(lines) + "\n")
    print("\n-- top ideas v2 --", flush=True)
    for i in sorted(v2, key=lambda x: -x["n"])[:25]:
        print(f"  [{i['n']:5d}] {i['canonical'][:100]}", flush=True)


if __name__ == "__main__":
    main()
