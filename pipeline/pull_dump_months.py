#!/usr/bin/env python3
"""Variant-gate fold-B acquisition from the monthly Reddit dumps torrent.

Per month: selectively download RC_/RS_ via aria2c, stream-filter to the six
gate subreddits (pipeline/dump_filter.py), gzip, delete the dump.

Two speedups over v1 (both measured 2026-08-30):
  - Python chunk filter at ~540MB/s replaces BSD `grep -aiE` at ~111MB/s.
  - The next month downloads (into an alternating dir, so aria2 control
    files never collide) while the current month filters.

Resume-safe per (kind, month); completed months are skipped.
Usage: pull_dump_months.py 2022-01 2024-12
"""
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/Volumes/1TB NVME 1/antikythera/data/reddit_gate"
TORRENT = f"{BASE}/3d426c47c767d40f82c7ef0f47c3acacedd2bf44.torrent"
FILT = f"{BASE}/dump_filtered"
FILTER_PY = f"{ROOT}/pipeline/dump_filter.py"
PY = f"{ROOT}/.venv/bin/python"
ARIA = "/usr/local/Cellar/aria2/1.37.0_2/bin/aria2c"
RC0, RS0, MONTH0 = 194, 441, (2022, 1)
MIN_FREE_GB = 60


def month_index(m: str) -> int:
    return (int(m[:4]) - MONTH0[0]) * 12 + (int(m[5:7]) - MONTH0[1])


def months_range(a: str, b: str) -> list[str]:
    out, i = [], month_index(a)
    while i <= month_index(b):
        y, mm = MONTH0[0] + (MONTH0[1] - 1 + i) // 12, (MONTH0[1] - 1 + i) % 12 + 1
        out.append(f"{y:04d}-{mm:02d}")
        i += 1
    return out


def paths(m: str, slot: int) -> dict:
    d = f"{BASE}/dl{slot}"
    return {"RC": (RC0 + month_index(m), f"{d}/reddit/comments/RC_{m}.zst"),
            "RS": (RS0 + month_index(m), f"{d}/reddit/submissions/RS_{m}.zst"),
            "dir": d}


def pending(m: str) -> list[str]:
    return [k for k in ("RC", "RS")
            if not os.path.exists(f"{FILT}/filtered_{k}_{m}.ndjson.gz")]


def start_download(m: str, slot: int):
    todo = pending(m)
    if not todo:
        return None
    p = paths(m, slot)
    idxs = ",".join(str(p[k][0]) for k in todo)
    os.makedirs(p["dir"], exist_ok=True)
    print(f"{m}: download start (slot {slot}, indices {idxs})", flush=True)
    return subprocess.Popen(
        [ARIA, f"--select-file={idxs}", "--torrent-file=" + TORRENT,
         "-d", p["dir"], "--seed-time=0", "--console-log-level=warn",
         "--summary-interval=0", "--file-allocation=none",
         "--bt-stop-timeout=14400"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def filter_month(m: str, slot: int) -> None:
    for k in pending(m):
        src = paths(m, slot)[k][1]
        if not os.path.exists(src):
            print(f"{m} {k}: MISSING after download — skipped", flush=True)
            continue
        sz = os.path.getsize(src) / 1e9
        out = f"{FILT}/filtered_{k}_{m}.ndjson.gz"
        t0 = time.time()
        with open(out + ".tmp", "wb") as fo:
            p1 = subprocess.Popen(["zstd", "-dc", "--long=31", src],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL)
            p2 = subprocess.Popen([PY, FILTER_PY], stdin=p1.stdout,
                                  stdout=subprocess.PIPE)
            p3 = subprocess.Popen(["gzip"], stdin=p2.stdout, stdout=fo)
            p1.stdout.close()
            p2.stdout.close()
            rc3, rc2, rc1 = p3.wait(), p2.wait(), p1.wait()
        if rc1 != 0 or rc2 != 0 or rc3 != 0:
            raise RuntimeError(f"filter failed {m} {k}: {rc1} {rc2} {rc3}")
        os.replace(out + ".tmp", out)
        print(f"{m} {k}: {sz:.1f}GB dump -> "
              f"{os.path.getsize(out)/1e6:.0f}MB kept "
              f"(filter {time.time()-t0:.0f}s)", flush=True)
        os.remove(src)


def main() -> None:
    os.makedirs(FILT, exist_ok=True)
    months = months_range(sys.argv[1], sys.argv[2])
    proc, slot = None, 0
    for i, m in enumerate(months):
        if not pending(m):
            print(f"{m}: done (cached)", flush=True)
            continue
        if proc is None:
            proc = start_download(m, slot)
        if proc is not None:
            proc.wait()
        # prefetch the next month into the other slot while this one filters
        nxt = next((x for x in months[i + 1:] if pending(x)), None)
        proc = start_download(nxt, 1 - slot) if nxt else None
        while shutil.disk_usage(BASE).free / 1e9 < MIN_FREE_GB:
            print(f"{m}: waiting for disk", flush=True)
            time.sleep(300)
        filter_month(m, slot)
        shutil.rmtree(f"{BASE}/dl{slot}", ignore_errors=True)
        slot = 1 - slot
    if proc is not None:
        proc.wait()
    print("ALL MONTHS DONE", flush=True)


if __name__ == "__main__":
    main()
