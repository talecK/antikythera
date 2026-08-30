#!/usr/bin/env python3
"""Wind-down: materialize the reusable derived tables ("HN atlas") from the
project's caches into data/atlas/. Each table is standalone parquet/csv with
a documented schema (see data/atlas/README.md).
"""
import json
import os
from collections import defaultdict

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(ROOT, "data", "registry", "pilot1_concepts")
OUT = os.path.join(ROOT, "data", "atlas")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    con = duckdb.connect()

    # 1. concept frequency by month (2015-2017 docs corpus)
    con.sql(f"""
        COPY (SELECT claim AS concept, date_trunc('month', time) AS month,
                     count(*) AS mentions, count(DISTINCT doc_id) AS docs
              FROM read_parquet('{C}/claims.parquet')
              GROUP BY 1, 2 ORDER BY 1, 2)
        TO '{OUT}/concept_freq_monthly.parquet' (FORMAT parquet, COMPRESSION zstd)
    """)

    # 2. concept co-occurrence edges (doc-level, 2015-2017)
    con.sql(f"""
        COPY (
          WITH dc AS (SELECT DISTINCT doc_id, claim FROM read_parquet('{C}/claims.parquet'))
          SELECT a.claim AS concept_a, b.claim AS concept_b,
                 count(*) AS co_docs, min(d.time) AS first_seen
          FROM dc a JOIN dc b ON a.doc_id = b.doc_id AND a.claim < b.claim
          JOIN (SELECT doc_id, any_value(time) AS time
                FROM read_parquet('{C}/claims.parquet') GROUP BY doc_id) d
            ON d.doc_id = a.doc_id
          GROUP BY 1, 2 HAVING count(*) >= 2 ORDER BY co_docs DESC)
        TO '{OUT}/concept_cooccurrence.parquet' (FORMAT parquet, COMPRESSION zstd)
    """)

    # 3. first-seen index: concepts (2015-17) and title-claims (2006-26)
    con.sql(f"""
        COPY (SELECT claim AS concept, min(time) AS first_seen, count(*) AS total_mentions
              FROM read_parquet('{C}/claims.parquet') GROUP BY 1 ORDER BY 2)
        TO '{OUT}/concept_first_seen.parquet' (FORMAT parquet, COMPRESSION zstd)
    """)
    P0 = os.path.join(ROOT, "data", "registry", "pilot0")
    if os.path.exists(os.path.join(P0, "registry.json")):
        ideas = json.load(open(os.path.join(P0, "registry.json")))
        import pyarrow as pa
        import pyarrow.parquet as pq
        pq.write_table(pa.table({
            "claim": [i["canonical"] for i in ideas],
            "first_seen": [i["first_seen"] for i in ideas],
            "n_title_mentions": [i["n"] for i in ideas],
        }), f"{OUT}/title_claims_2006_2026.parquet", compression="zstd")

    # 4. exposure labels
    exposed = {l.strip() for l in open(f"{C}/exposed_concepts.txt")}
    universe = [l.strip() for l in open(f"{C}/concepts_to_classify.txt") if l.strip()]
    with open(f"{OUT}/concept_exposure_labels.csv", "w") as f:
        f.write("concept,economically_exposed\n")
        for c in universe:
            f.write(f'"{c}",{1 if c in exposed else 0}\n')

    # 5. adjudication verdict pairs (paraphrase dataset)
    import glob
    import hashlib
    rows = []
    for reg_dir in ("pilot0", "pilot1_box"):
        R = os.path.join(ROOT, "data", "registry", reg_dir)
        gp = os.path.join(R, "gray_pairs.json")
        if not os.path.exists(gp):
            continue
        gray = json.load(open(gp))
        ideas = json.load(open(os.path.join(R, "registry.json")))
        import pyarrow.parquet as pq2
        claims = pq2.read_table(os.path.join(R, "claims.parquet"))["claim"].to_pylist()
        cd = os.path.join(ROOT, "data", "extractions", "adjudicate-deepseek_av1")
        for row, idea_id, cos in gray:
            a, b = claims[int(row)], ideas[int(idea_id)]["canonical"]
            pid = hashlib.sha1(f"{a}||{b}".encode()).hexdigest()[:12]
            p = os.path.join(cd, pid + ".json")
            if os.path.exists(p):
                rows.append((a, b, float(cos), json.load(open(p))["verdict"], reg_dir))
    import pyarrow as pa
    import pyarrow.parquet as pq3
    pq3.write_table(pa.table({
        "text_a": [r[0] for r in rows], "text_b": [r[1] for r in rows],
        "cosine": [r[2] for r in rows], "verdict": [r[3] for r in rows],
        "source": [r[4] for r in rows],
    }), f"{OUT}/claim_pair_verdicts.parquet", compression="zstd")

    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)) // 1024, "KB")


if __name__ == "__main__":
    main()
