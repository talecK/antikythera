#!/usr/bin/env python3
"""Rebuild #1 (granularity iteration): concept-level units.

Pulls the `concepts` arrays from the cached doc extractions (pv2_sv1),
normalizes (lowercase, strip, collapse whitespace), and writes a
claims.parquet-compatible table where each row is one (doc, concept)
mention — the registry/eval machinery then runs unchanged with
REGISTRY_OUT pointed here (concept text plays the role of claim text).
"""
import glob
import json
import os
import re
import sys

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTOR_ID = "deepseek-v4-flash-nothink_pv2_sv1"
OUT = os.environ.get("REGISTRY_OUT", os.path.join(ROOT, "data", "registry", "pilot1_concepts"))
FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)
WS = re.compile(r"\s+")


def rec_concepts(rec: dict) -> list[str]:
    m = FENCE.match(rec.get("raw", ""))
    try:
        data = json.loads(m.group(1) if m else rec["raw"])
    except (json.JSONDecodeError, KeyError):
        return []
    out = []
    for c in data.get("claims", []) if isinstance(data, dict) else []:
        if isinstance(c, dict):
            for k in c.get("concepts", []) or []:
                if isinstance(k, str) and 2 <= len(k) <= 60:
                    out.append(WS.sub(" ", k.strip().lower()))
    return sorted(set(out))          # per-doc distinct concepts


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    shards = glob.glob(os.path.join(ROOT, "data", "extractions", EXTRACTOR_ID, "*", "*.json"))
    rows = []
    for path in shards:
        rec = json.load(open(path))
        for k in rec_concepts(rec):
            rows.append((rec["doc_id"], k))
    print(f"{len(rows)} concept mentions from {len(shards)} docs")
    con = duckdb.connect()
    t = pa.table({"doc_id": [r[0] for r in rows], "claim": [r[1] for r in rows]})
    con.register("c", t)
    out = con.sql(f"""
        SELECT c.doc_id, c.claim, d.time FROM c
        JOIN read_parquet('{ROOT}/data/docs/docs_*.parquet') d ON c.doc_id = d.doc_id
        WHERE year(d.time) IN (2015, 2016, 2017)
        ORDER BY d.time, c.doc_id
    """).arrow()
    if hasattr(out, "read_all"):
        out = out.read_all()
    pq.write_table(out, os.path.join(OUT, "claims.parquet"), compression="zstd")
    uniq = con.sql(f"SELECT count(DISTINCT claim) FROM read_parquet('{OUT}/claims.parquet')").fetchone()[0]
    print(f"fold rows: {out.num_rows} | unique concepts: {uniq}")


if __name__ == "__main__":
    main()
