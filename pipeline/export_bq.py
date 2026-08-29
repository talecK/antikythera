#!/usr/bin/env python3
"""Export the staged antikythera_hn tables to local parquet via the
BigQuery Storage Read API. Streams Arrow batches; constant memory.

Auth: mints an access token from the gcloud credential store per table
(no ADC needed).
"""
import os
import subprocess
import sys

import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud.bigquery_storage import BigQueryReadClient, types
from google.oauth2.credentials import Credentials

PROJECT = "pricemole-g4a"
DATASET = "antikythera_hn"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "raw", "hn_bq")
TABLES = ["stories_filtered", "comments_top20", "comment_skeleton"]


def gcloud_token() -> str:
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def export(table: str) -> None:
    dest = os.path.join(OUT, f"{table}.parquet")
    if os.path.exists(dest):
        print(f"skip  {table}")
        return
    client = BigQueryReadClient(credentials=Credentials(token=gcloud_token()))
    session = client.create_read_session(
        parent=f"projects/{PROJECT}",
        read_session=types.ReadSession(
            table=f"projects/{PROJECT}/datasets/{DATASET}/tables/{table}",
            data_format=types.DataFormat.ARROW,
        ),
        max_stream_count=1,
    )
    reader = client.read_rows(session.streams[0].name)
    writer = None
    rows = 0
    tmp = dest + ".tmp"
    for page in reader.rows(session).pages:
        batch = page.to_arrow()
        if writer is None:
            writer = pq.ParquetWriter(tmp, batch.schema, compression="zstd")
        writer.write_batch(batch)
        rows += batch.num_rows
    if writer is None:
        print(f"EMPTY {table}")
        sys.exit(1)
    writer.close()
    os.replace(tmp, dest)
    print(f"ok    {table}: {rows} rows, {os.path.getsize(dest) / 1e6:.0f} MB")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for table in TABLES:
        export(table)


if __name__ == "__main__":
    main()
