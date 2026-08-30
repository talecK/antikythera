#!/usr/bin/env python3
"""Run 5 intermediate: attribute cached extraction concepts to comment authors.

For every cached (doc, claim) of the primary extractor, match the claim's
verbatim quote to exactly one cleaned comment (or the title/self-text) and
attribute the claim's concepts to that comment's author (or story author).
Claims with no quote, an unmatched quote, or an ambiguous quote are dropped
(coverage measured in the run-5 feasibility check: 82% attributed).

Output: data/registry/run5_author/author_concepts.parquet
  doc_id, time (story ts), author, concept   (one row per attribution)
Deterministic; touches no eval outcome.
"""
import glob
import html
import json
import os
import re

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = os.path.join(ROOT, "data", "extractions", "deepseek-v4-flash-nothink_pv2_sv1")
RAW = os.path.join(ROOT, "data", "raw", "hn_bq")
OUT = os.path.join(ROOT, "data", "registry", "run5_author")

TAG_BREAK = re.compile(r"<p>|<br ?/?>", re.I)
TAG_ANY = re.compile(r"<[^>]+>")
WS = re.compile(r"[ \t]+")


def clean(raw):
    if not raw:
        return ""
    s = TAG_BREAK.sub("\n", raw)
    s = TAG_ANY.sub("", s)
    s = html.unescape(s)
    return WS.sub(" ", s).strip()


def norm(s):
    return WS.sub(" ", s.replace("\n", " ")).strip().lower()


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    con = duckdb.connect()
    print("loading raw comments/stories (2015-2017 only) …", flush=True)
    comments = con.sql(f"""
        SELECT c.story_id, c."by", c.text
        FROM '{RAW}/comments_top20.parquet' c
        JOIN '{RAW}/stories_filtered.parquet' s ON c.story_id = s.id
        WHERE year(s.time) BETWEEN 2015 AND 2017""").fetchall()
    by_story = {}
    for sid, by, text in comments:
        if by:
            by_story.setdefault(sid, []).append((by, norm(clean(text))[:1200]))
    stories = con.sql(f"""
        SELECT id, "by", time, title, COALESCE(text,'')
        FROM '{RAW}/stories_filtered.parquet'
        WHERE year(time) BETWEEN 2015 AND 2017""").fetchall()
    story_meta = {sid: (by, ts, norm(clean(t)), norm(clean(st)))
                  for sid, by, ts, t, st in stories}
    print(f"{len(by_story)} stories with comments; {len(story_meta)} stories",
          flush=True)

    files = sorted(glob.glob(f"{EXT}/*/*.json"))
    print(f"{len(files)} cached extractions", flush=True)
    rows_doc, rows_ts, rows_auth, rows_conc = [], [], [], []
    stats = {"claims": 0, "attributed": 0}
    for n, f in enumerate(files):
        if n % 200000 == 0:
            print(f"  {n}/{len(files)} ({stats['attributed']} attributed)",
                  flush=True)
        did = int(f.rsplit("/", 1)[1][:-5])
        meta = story_meta.get(did)
        if meta is None:
            continue
        s_by, s_ts, title_n, self_n = meta
        try:
            claims = json.loads(json.load(open(f))["raw"])["claims"]
        except Exception:
            continue
        cs = by_story.get(did, [])
        for c in claims:
            if not isinstance(c, dict):
                continue
            stats["claims"] += 1
            q = c.get("quote")
            if not q:
                continue
            qn = norm(q)
            if not qn:
                continue
            hits = [by for by, t in cs if qn in t]
            if len(hits) == 1:
                author = hits[0]
            elif len(hits) == 0 and s_by and (qn in title_n or (self_n and qn in self_n)):
                author = s_by
            else:
                continue
            stats["attributed"] += 1
            for concept in c.get("concepts", []):
                cc = concept.strip().lower()
                if len(cc) >= 2:
                    rows_doc.append(did); rows_ts.append(s_ts)
                    rows_auth.append(author); rows_conc.append(cc)

    table = pa.table({
        "doc_id": pa.array(rows_doc, pa.int64()),
        "time": pa.array(rows_ts, pa.timestamp("us")),
        "author": rows_auth,
        "concept": rows_conc,
    })
    pq.write_table(table, os.path.join(OUT, "author_concepts.parquet"),
                   compression="zstd")
    print(f"claims {stats['claims']} | attributed {stats['attributed']} "
          f"({stats['attributed']/max(stats['claims'],1):.0%}) | "
          f"concept rows {table.num_rows}", flush=True)


if __name__ == "__main__":
    main()
