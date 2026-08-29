#!/usr/bin/env python3
"""Assemble extraction-ready documents from the canonical HN pull.

Document = story title + self-text + top-N comments (already ranked in the
pull: reply-count desc, time asc). HTML entities decoded, tags stripped —
this is derived data; the raw pull stays immutable.

Output: data/docs/docs_YYYY.parquet with
  doc_id, time, title, url, n_comments, authors (story+comment authors),
  text (the extractor input), n_chars
Deterministic for a given raw pull + parameters; parameters are embedded in
the parquet's key-value metadata for cache-keying.
"""
import argparse
import html
import json
import os
import re

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "hn_bq")
OUT = os.path.join(ROOT, "data", "docs")

PARAMS = {
    "builder_version": "v1",
    "max_comments": 20,
    "max_chars_per_comment": 1200,
    "max_doc_chars": 20000,
}

TAG_BREAK = re.compile(r"<p>|<br ?/?>", re.I)
TAG_ANY = re.compile(r"<[^>]+>")
WS = re.compile(r"[ \t]+")


def clean(raw: str | None) -> str:
    if not raw:
        return ""
    s = TAG_BREAK.sub("\n", raw)
    s = TAG_ANY.sub("", s)
    s = html.unescape(s)
    return WS.sub(" ", s).strip()


def build_year(con: duckdb.DuckDBPyConnection, year: int) -> dict:
    stories = con.sql(f"""
        SELECT id, time, "by", title, url, text
        FROM '{RAW}/stories_filtered.parquet'
        WHERE year(time) = {year}
        ORDER BY id
    """).fetchall()
    comments = con.sql(f"""
        SELECT c.story_id, c."by", c.text
        FROM '{RAW}/comments_top20.parquet' c
        JOIN '{RAW}/stories_filtered.parquet' s ON c.story_id = s.id
        WHERE year(s.time) = {year}
        ORDER BY c.story_id, c.n_replies DESC, c.time ASC
    """).fetchall()

    by_story: dict[int, list] = {}
    for sid, author, text in comments:
        by_story.setdefault(sid, []).append((author, text))

    rows = []
    for sid, ts, author, title, url, selftext in stories:
        title_c, self_c = clean(title), clean(selftext)
        parts = [f"TITLE: {title_c}"]
        if self_c:
            parts.append(self_c)
        authors = [author] if author else []
        n_comments = 0
        for c_author, c_text in by_story.get(sid, [])[: PARAMS["max_comments"]]:
            c_clean = clean(c_text)[: PARAMS["max_chars_per_comment"]]
            if not c_clean:
                continue
            parts.append(f"COMMENT: {c_clean}")
            if c_author:
                authors.append(c_author)
            n_comments += 1
        text = "\n\n".join(parts)[: PARAMS["max_doc_chars"]]
        rows.append((sid, ts, title_c, url or "", n_comments,
                     sorted(set(authors)), text, len(text)))

    table = pa.table(
        {
            "doc_id": pa.array([r[0] for r in rows], pa.int64()),
            "time": pa.array([r[1] for r in rows], pa.timestamp("us")),
            "title": [r[2] for r in rows],
            "url": [r[3] for r in rows],
            "n_comments": pa.array([r[4] for r in rows], pa.int32()),
            "authors": pa.array([r[5] for r in rows], pa.list_(pa.string())),
            "text": [r[6] for r in rows],
            "n_chars": pa.array([r[7] for r in rows], pa.int64()),
        }
    ).replace_schema_metadata({"build_params": json.dumps(PARAMS)})
    os.makedirs(OUT, exist_ok=True)
    pq.write_table(table, f"{OUT}/docs_{year}.parquet", compression="zstd")
    return {
        "year": year,
        "docs": len(rows),
        "mchars": sum(r[7] for r in rows) / 1e6,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("years", nargs="+", type=int)
    args = ap.parse_args()
    con = duckdb.connect()
    total_docs = total_mchars = 0.0
    for year in args.years:
        st = build_year(con, year)
        total_docs += st["docs"]
        total_mchars += st["mchars"]
        print(f"{st['year']}: {st['docs']} docs, {st['mchars']:.0f} Mchars")
    print(f"total: {total_docs:.0f} docs, {total_mchars:.0f} Mchars "
          f"(~{total_mchars / 4:.0f}M tokens at 4 chars/token)")


if __name__ == "__main__":
    main()
