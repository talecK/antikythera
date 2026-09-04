# Runbook: parallel Reddit API pull on disposable Vultr nodes

Written 2026-08-31 after the variant-gate fleet (21 nodes, 21 WSB months,
~2.5h wall, ~$1, zero API bans). Assumes the repo and zero session context.
Target example throughout: WSB 2019-01..2024-12 continuous (72 months).

## 0. Decisions to make BEFORE launching (cannot be fixed after)
- **Field set.** `pipeline/pull_reddit_gate.py` FIELDS pulls ONLY
  `id,author,created_utc,body,link_id` (comments) /
  `id,author,created_utc,title,selftext` (posts). No `score`, no flair.
  If the analysis needs engagement (score) or any other field, EDIT the
  FIELDS dict FIRST — a re-pull later costs the full job again. Score
  settles ~36h after posting (per Arctic Shift docs); pulling months
  younger than that under-counts it.
- **Month list.** One node per month is the sharding unit. For the 72-month
  example: 72 nodes at once is rude and unnecessary; run waves of ~20.
- **2021 warning.** WSB volume is violently non-uniform:
  2017 ≈ 65K/mo avg, 2019 ≈ 285K/mo, 2022-06 = 1.13M, 2023-09 = 510K
  (the lull), 2024-03 = 962K. 2021-01..03 (GME) are the extreme outliers —
  plan for several MILLION comments in 2021-01 alone; that node runs
  3-5h, not 40min. Do NOT interpret a small completed month as failure:
  check the volume against neighbours (see §5) before suspecting truncation.

## 1. Node spin-up
- Plan `vc2-1c-1gb` ($5/mo ≈ $0.007/h), region `sea`, os_id 2136
  (Debian 12), tag every instance (e.g. `antikythera-pull`) — the tag is
  how the collector finds them and how you verify teardown.
- Key: `~/.config/antikythera/vultr.env` (VULTR_API_KEY); account ssh key id
  `7a23f40e-b96a-407e-a826-0aa991a75d10` (local `~/.ssh/id_ed25519`).
- Create via API (see `pipeline/fleet_pull.sh` for the exact curl; ignore
  its launch loop — buggy, superseded by the collector, kept for the
  create/IP-wait snippets). Boxes are ACTIVE with an IP in ~60-90s.
- Cost math: a 20-node wave for 2h ≈ $0.30. Never worth optimizing.

## 2. Bootstrap + launch (the two SSH landmines)
The puller is STDLIB-ONLY — bootstrap is literally one scp, no pip:
    scp pipeline/pull_reddit_gate.py root@IP:/root/pull.py
    ssh -n root@IP "mkdir -p /root/out; cd /root; \
      (PULL_OUT=/root/out PULL_SLEEP=0.25 setsid nohup \
       python3 -u pull.py wallstreetbets --month 2021-01 \
       > pull.log 2>&1 < /dev/null &) ; exit 0"
- **Landmine 1:** `ssh host "a && b && nohup x &"` can hold the SSH channel
  open until the REMOTE JOB EXITS (cost us 45 min serialized + a 30-min
  hang). The `setsid` + subshell + explicit `exit 0` pattern above is the
  fix. Do not "simplify" it.
- **Landmine 2:** macOS has no `timeout(1)`. Wrap EVERY remote call in
  `perl -e 'alarm shift @ARGV; exec @ARGV' 30 ssh ...` or one wedged box
  stalls your whole orchestration loop (it did).

## 3. Sharding, state, resume
- Shard = (kind, sub, month) → files `comments_<sub>_<YYYY-MM>.ndjson.gz`
  and `posts_...`. `--month` accepts a list; one month per node is the
  clean unit.
- The puller checkpoints per shard: `<tag>.part` (rows so far) +
  `<tag>.cursor` (created_utc high-water mark, DESC pagination). Kill it
  anywhere; relaunching the same command RESUMES from the cursor. A shard
  is complete only when the `.ndjson.gz` exists (atomic rename); `.part`
  present = in-flight.
- A fresh session resumes a partial FLEET by just running the collector
  (§4): it discovers boxes by tag, relaunches dead pulls (resume-safe),
  collects finished ones. No other state needed.

## 4. The collector (use it, don't reinvent)
`pipeline/fleet_collector.sh` — sweep every ~3 min: bootstrap bare boxes,
relaunch dead pulls, rsync finished months to the NVMe, DESTROY collected
boxes, heartbeat `WATCH months_home=N/M` lines, and (as written) trigger
downstream processing when all months are home — EDIT that tail section
for a new job (month list is hardcoded; downstream = extract+gate today).
All remote calls already carry alarm-timeouts and the setsid launch.

## 5. Integrity checks (each one exists because it caught a real bug)
- **Never trust file size.** BitTorrent-style sparse files report full
  logical size while containing pure zeros (`RC_2023-04.zst`, 27GB of
  0x00). API-side equivalent: check ROWS, not bytes.
- **Volume sanity per month** against neighbours + the table in §0; a
  month at 0 or at 5% of its neighbours is a failure, not a small month.
  (Root causes seen: JSON format drift breaking a filter — dumps switched
  `"k":"v"` to `"k": "v"` at 2023-04 — and truncated downloads.)
- **Timestamp span** must be [1st 00:00, last day 23:59] UTC —
  `pipeline/validate_month.py output <file> <YYYY-MM> <RC|RS>` does span +
  parse + floor checks (its own-subreddit check is meaningless for API
  files: they carry no subreddit field; sub comes from the filename).
- **Dedup downstream by item id** (`extract_tickers.py` does this) — makes
  source overlap harmless; measured API/dump agreement 0.9996 with
  API-only = 0 (`pipeline/provenance_check.py`, results in
  preregistration_gate.md A1'), i.e. API-filling is sparser-never-denser.
- **Teardown verification is mandatory:** instances list by tag must be
  EMPTY at the end (`GET /v2/instances?tag=...` → 0). Collector destroys
  as it collects, but verify.

## 6. Rate etiquette (kept us unbanned across 21 concurrent nodes)
- `PULL_SLEEP=0.25` → ~1.7 req/s per node — inside Arctic Shift's stated
  "couple requests per second" per client. Do not lower the sleep.
- `limit=auto` returns what the server is comfortable with (~300 rows/req
  observed; it self-throttles under load). Observed sustainable throughput:
  ~28K rows/min/node; a 900K-row month ≈ 35-40 min.
- Exponential backoff on ANY error is built into the puller (1s→120s).
  Zero 429s observed at 21 nodes. Do not run more than ~20-25 nodes.
- Their docs: bulk belongs on the monthly dumps. The dumps' per-subreddit
  torrents are DELISTED and the big archive swarm (~16 seeders) has holes;
  that is why the API fleet exists. For non-WSB-scale subs, one local
  process is plenty — the fleet is for many-months × big-sub jobs.

## 7. Output schema and landing zone
- Land in `/Volumes/1TB NVME 1/antikythera/data/reddit_gate/pull/`
  (symlinked under repo `data/`): gzip ndjson, one JSON object/line,
  exactly the FIELDS keys. Naming: `comments_wallstreetbets_2021-01.ndjson.gz`.
- Posts and comments are separate shards; both needed per month.
- ~55-60MB gz per 900K-comment month. 72 WSB months ≈ 4-5GB total.

## 8. Known gotchas that each cost ≥30 minutes tonight
1. The two SSH landmines (§2).
2. Sparse-zeros files passing size checks (§5).
3. Dump JSON format seam at 2023-04 silently zeroing a fast filter —
   differential-validate any regex filter against json.loads
   (`validate_month.py preflight`).
4. This harness's shell aliases `grep` to ugrep — benchmark `/usr/bin/grep`
   explicitly or your perf numbers are fiction.
5. Backgrounding a heredoc (`python -u - <<EOF ... &`) detaches stdin →
   instant silent exit. Write a real file, then nohup it.
6. `crosspost_parent_list` makes line-level subreddit matching
   over-inclusive on dump data; the extractor's own-field check is the
   authoritative filter.
