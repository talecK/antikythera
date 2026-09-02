#!/usr/bin/env python3
"""Assemble the data release (Zenodo deposit) for papers 1 and 2.

Reads only. Every source file is opened read-only, its SHA-256 is recorded
before and after the build, and the script refuses to write to any path
that already exists (no overwrite, no rename, no delete anywhere).

Outputs, all under a fresh versioned folder on the NVMe:
  reddit_ticker_mentions_2019_2024.parquet   the paper-2 mention panel,
                                             author replaced by a salted
                                             SHA-256 (first 16 hex chars)
  hn_atlas/*.parquet, *.csv                  the HN atlas tables, copied
  paper2_runs/*.tsv                          registered-run outputs, copied
  stats.json                                 counts used by the datasheet
  CHECKSUMS.txt                              sha256 of every released file
  SOURCE_CHECKSUMS.txt                       sha256 of every source, before
                                             and after (must match)

The salt lives in private/release_salt.txt (gitignored). It is generated
on first run and never printed. Losing it means later versions get new
hashes; that is disclosed in the datasheet.

Usage: build_release.py --version v1
"""
import argparse
import hashlib
import json
import os
import secrets
import shutil
import sys

import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NVME = "/Volumes/1TB NVME 1/antikythera/data"
SALT_PATH = os.path.join(ROOT, "private", "release_salt.txt")

MENTIONS = f"{NVME}/paper2/ticker_mentions.parquet"
ATLAS = [
    "concept_freq_monthly.parquet", "concept_cooccurrence.parquet",
    "concept_first_seen.parquet", "title_claims_2006_2026.parquet",
    "concept_exposure_labels.csv", "claim_pair_verdicts.parquet",
]
RUNS = [
    "paper2_windows_z.tsv", "paper2_window_census.tsv",
    "paper2_placebo_reps.tsv", "paper2_volume_table.tsv",
    "paper2_windows_z_v1_superseded.tsv",
    "paper2_window_census_v1_superseded.tsv",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fresh(path):
    if os.path.exists(path):
        sys.exit(f"REFUSING to write over existing path: {path}")
    return path


def load_salt():
    if not os.path.exists(SALT_PATH):
        os.makedirs(os.path.dirname(SALT_PATH), exist_ok=True)
        with open(SALT_PATH, "w") as f:
            f.write(secrets.token_hex(32) + "\n")
        os.chmod(SALT_PATH, 0o600)
        print("salt: generated (kept in private/, not printed)", flush=True)
    else:
        print("salt: loaded from private/", flush=True)
    return open(SALT_PATH).read().strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    args = ap.parse_args()

    out = fresh(f"{NVME}/release/{args.version}")
    sources = [MENTIONS] + [f"{ROOT}/data/atlas/{a}" for a in ATLAS] \
        + [f"{ROOT}/reports/{r}" for r in RUNS]
    for s in sources:
        if not os.path.exists(s):
            sys.exit(f"missing source: {s}")
    before = {s: sha256(s) for s in sources}
    print(f"sources: {len(sources)} hashed", flush=True)

    os.makedirs(out)
    os.makedirs(f"{out}/hn_atlas")
    os.makedirs(f"{out}/paper2_runs")

    # 1. hashed-author ticker panel
    salt = load_salt()
    con = duckdb.connect()
    con.execute(f"create view m as select * from read_parquet('{MENTIONS}')")
    authors = [r[0] for r in con.execute(
        "select distinct author from m").fetchall()]
    table = [(a, hashlib.sha256((salt + a).encode()).hexdigest()[:16])
             for a in authors]
    con.execute("create table h(author varchar, author_hash varchar)")
    con.executemany("insert into h values (?, ?)", table)
    n_hash = con.execute("select count(distinct author_hash) from h").fetchone()[0]
    if n_hash != len(authors):
        sys.exit(f"hash collision: {len(authors)} authors -> {n_hash} hashes")
    panel = fresh(f"{out}/reddit_ticker_mentions_2019_2024.parquet")
    con.execute(f"""
        copy (
          select h.author_hash, m.time, m.subreddit, m.ticker, m.unit_type,
                 m.kind, m.item_id, m.score
          from m join h using (author)
          order by m.time, m.subreddit, m.item_id, m.ticker
        ) to '{panel}' (format parquet, compression zstd)
    """)
    n_src = con.execute("select count(*) from m").fetchone()[0]
    n_out = con.execute(
        f"select count(*) from read_parquet('{panel}')").fetchone()[0]
    if n_src != n_out:
        sys.exit(f"row count mismatch: {n_src} -> {n_out}")
    cols = [c[0] for c in con.execute(
        f"describe select * from read_parquet('{panel}')").fetchall()]
    if "author" in cols:
        sys.exit("author column leaked into release")
    print(f"panel: {n_out:,} rows, {n_hash:,} hashed authors", flush=True)

    stats = con.execute(f"""
        select count(*) as n_rows, count(distinct author_hash) as n_authors,
               count(distinct ticker) tickers,
               min(to_timestamp(time))::date first_day,
               max(to_timestamp(time))::date last_day
        from read_parquet('{panel}')
    """).fetchone()
    per_sub = con.execute(f"""
        select subreddit, count(*) as n_rows, count(distinct author_hash) as n_authors
        from read_parquet('{panel}') group by 1 order by 2 desc
    """).fetchall()
    per_kind = con.execute(f"""
        select kind, unit_type, count(*) from read_parquet('{panel}')
        group by 1, 2 order by 1, 2
    """).fetchall()

    # 2. copies
    copied = []
    for a in ATLAS:
        dst = fresh(f"{out}/hn_atlas/{a}")
        shutil.copyfile(f"{ROOT}/data/atlas/{a}", dst)
        copied.append(dst)
    for r in RUNS:
        dst = fresh(f"{out}/paper2_runs/{r}")
        shutil.copyfile(f"{ROOT}/reports/{r}", dst)
        copied.append(dst)
    print(f"copied: {len(copied)} files", flush=True)

    # 3. stats + checksums
    with open(fresh(f"{out}/stats.json"), "w") as f:
        json.dump({
            "panel": {"rows": stats[0], "authors": stats[1],
                      "tickers": stats[2], "first_day": str(stats[3]),
                      "last_day": str(stats[4])},
            "per_subreddit": [{"subreddit": s, "rows": n, "authors": a}
                              for s, n, a in per_sub],
            "per_kind_unit": [{"kind": k, "unit_type": u, "rows": n}
                              for k, u, n in per_kind],
        }, f, indent=2)

    released = [panel] + copied + [f"{out}/stats.json"]
    with open(fresh(f"{out}/CHECKSUMS.txt"), "w") as f:
        for p in released:
            f.write(f"{sha256(p)}  {os.path.relpath(p, out)}\n")

    after = {s: sha256(s) for s in sources}
    changed = [s for s in sources if before[s] != after[s]]
    def label(s):  # repo-relative labels; no local absolute paths in the release
        if s.startswith(NVME):
            return "data" + s[len(NVME):]
        return "repo:" + os.path.relpath(s, ROOT)
    with open(fresh(f"{out}/SOURCE_CHECKSUMS.txt"), "w") as f:
        for s in sources:
            f.write(f"{before[s]}  {after[s]}  {label(s)}\n")
    if changed:
        sys.exit(f"SOURCE CHANGED DURING BUILD: {changed}")
    print(f"sources unchanged: {len(sources)}/{len(sources)}", flush=True)
    print(f"release: {out}", flush=True)


if __name__ == "__main__":
    main()
