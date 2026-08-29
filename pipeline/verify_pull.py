#!/usr/bin/env python3
"""Verify the HN pull: file inventory, row counts, per-year sanity."""
import glob
import os
import sys

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw", "hn")

EXPECTED_STORY_YEARS = set(range(2006, 2027))

def main() -> int:
    con = duckdb.connect()
    ok = True

    stories = sorted(glob.glob(f"{RAW}/stories/stories_*.parquet"))
    comments = sorted(glob.glob(f"{RAW}/comments_top20/comments_*.parquet"))
    skeleton = sorted(glob.glob(f"{RAW}/comment_skeleton/skeleton_*.parquet"))
    print(f"files: {len(stories)} stories, {len(comments)} comments_top20, "
          f"{len(skeleton)} skeleton (expect 21 / 21 / 252)")
    got_years = {int(os.path.basename(p)[8:12]) for p in stories}
    missing = EXPECTED_STORY_YEARS - got_years
    if missing:
        print(f"MISSING story years: {sorted(missing)}")
        ok = False

    print("\nyear  stories  top20_rows  stories_w_comments  skel_rows")
    for year in sorted(got_years):
        n_s = con.sql(f"SELECT count(*) FROM '{RAW}/stories/stories_{year}.parquet'").fetchone()[0]
        n_c = sc = 0
        cf = f"{RAW}/comments_top20/comments_{year}.parquet"
        if os.path.exists(cf):
            n_c, sc = con.sql(f"SELECT count(*), count(DISTINCT story_id) FROM '{cf}'").fetchone()
        sk = con.sql(
            f"SELECT count(*) FROM read_parquet('{RAW}/comment_skeleton/skeleton_{year}_*.parquet', union_by_name=true)"
        ).fetchone()[0] if glob.glob(f"{RAW}/comment_skeleton/skeleton_{year}_*.parquet") else 0
        print(f"{year}  {n_s:7d}  {n_c:10d}  {sc:18d}  {sk:9d}")
        if n_c > 0 and sc > n_s:
            print(f"  ANOMALY {year}: more commented stories than stories")
            ok = False

    # duplicate story ids across years
    dup = con.sql(
        f"SELECT count(*) - count(DISTINCT id) FROM read_parquet('{RAW}/stories/stories_*.parquet')"
    ).fetchone()[0]
    print(f"\nduplicate story ids across all years: {dup}")
    if dup:
        ok = False

    # every top20 comment joins to a pulled story
    orphans = con.sql(f"""
        SELECT count(*) FROM read_parquet('{RAW}/comments_top20/comments_*.parquet') c
        LEFT JOIN read_parquet('{RAW}/stories/stories_*.parquet') s ON c.story_id = s.id
        WHERE s.id IS NULL
    """).fetchone()[0]
    print(f"top20 comments not joining to a pulled story: {orphans}")
    if orphans:
        ok = False

    print("\nVERIFY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
