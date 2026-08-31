#!/bin/bash
# Fleet watcher/collector: every ~3 min, ensure every gate-fill box is
# progressing (bootstrap if bare, relaunch if dead — the puller resumes from
# its cursor), collect finished months, destroy collected boxes, and when all
# 21 months are local run extraction + the final gate. One WATCH line per
# cycle; event lines (COLLECTED/RELAUNCH/READY/STUCK) for the monitor.
set -u
source ~/.config/pricemole/vultr.env
AUTH="Authorization: Bearer $VULTR_API_KEY"
S="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=12 -o ServerAliveInterval=5 -o ServerAliveCountMax=3"
# macOS has no timeout(1); perl alarm gives every remote call a hard bound so
# one hung ssh can never stall the sweep (it did: 30 min on a held channel).
TO () { perl -e 'alarm shift @ARGV; exec @ARGV' "$@"; }
DEST="/Volumes/1TB NVME 1/antikythera/data/reddit_gate/pull"
LOG="/Volumes/1TB NVME 1/antikythera/data/reddit_gate/fleet_watch.log"
PULLER="/Users/andrej/workspace/antikythera/pipeline/pull_reddit_gate.py"
PY="/Users/andrej/workspace/antikythera/.venv/bin/python"

have_month () { [ "$(ls "$DEST"/*wallstreetbets_"$1".ndjson.gz 2>/dev/null | wc -l | tr -d ' ')" = "2" ]; }

while true; do
  INST=$(curl -s -H "$AUTH" "https://api.vultr.com/v2/instances?tag=antikythera-gate&per_page=50" \
    | python3 -c "import json,sys; [print(i['id'],i['label'].replace('gate-fill-',''),i['main_ip']) for i in json.load(sys.stdin).get('instances',[])]")
  n_boxes=0; n_done=0; line=""
  while read -r id m ip; do
    [ -z "${id:-}" ] && continue
    n_boxes=$((n_boxes+1))
    if have_month "$m"; then
      curl -s -X DELETE -H "$AUTH" "https://api.vultr.com/v2/instances/$id" >/dev/null
      echo "$(date +%H:%M) COLLECTED $m — box destroyed" >> "$LOG"; continue
    fi
    [ "$ip" = "0.0.0.0" ] && { line="$line $m:prov"; continue; }
    ST=$(TO 30 ssh -n $S root@"$ip" "ls /root/out/*.ndjson.gz 2>/dev/null | wc -l; pgrep -c python3 || true; tail -c 300 /root/pull.log 2>/dev/null | grep -oE '[0-9]+ rows' | tail -1" 2>/dev/null | tr '\n' '|')
    ngz=$(echo "$ST" | cut -d'|' -f1 | tr -d ' '); alive=$(echo "$ST" | cut -d'|' -f2 | tr -d ' '); rows=$(echo "$ST" | cut -d'|' -f3)
    if [ "${ngz:-0}" = "2" ]; then
      TO 300 rsync -az -e "ssh $S" root@"$ip":/root/out/ "$DEST/" >> "$LOG" 2>&1
      if have_month "$m"; then
        curl -s -X DELETE -H "$AUTH" "https://api.vultr.com/v2/instances/$id" >/dev/null
        echo "$(date +%H:%M) COLLECTED $m — box destroyed" >> "$LOG"
      else
        echo "$(date +%H:%M) STUCK $m: rsync did not land files" >> "$LOG"
      fi
    elif [ "${alive:-0}" = "0" ]; then
      TO 60 scp $S "$PULLER" root@"$ip":/root/pull.py >/dev/null 2>&1
      TO 30 ssh -n $S root@"$ip" "mkdir -p /root/out; cd /root; (PULL_OUT=/root/out PULL_SLEEP=0.25 setsid nohup python3 -u pull.py wallstreetbets --month $m > pull.log 2>&1 < /dev/null &) ; exit 0" 2>/dev/null \
        && echo "$(date +%H:%M) RELAUNCH $m on $ip" >> "$LOG" \
        || echo "$(date +%H:%M) STUCK $m: cannot launch on $ip" >> "$LOG"
    else
      line="$line $m:${rows:-0r}"
    fi
  done <<< "$INST"
  # count months home
  local_done=0
  for m in 2023-04 2023-05 2023-06 2023-07 2023-08 2023-09 2023-10 2023-11 2023-12 2024-01 2024-02 2024-03 2024-04 2024-05 2024-06 2024-07 2024-08 2024-09 2024-10 2024-11 2024-12; do
    have_month "$m" && local_done=$((local_done+1))
  done
  echo "$(date +%H:%M) WATCH months_home=$local_done/21 boxes_up=$n_boxes$line" >> "$LOG"
  if [ "$local_done" = "21" ]; then
    echo "$(date +%H:%M) ALL 21 MONTHS HOME — extract + gate" >> "$LOG"
    "$PY" -u /Users/andrej/workspace/antikythera/pipeline/extract_tickers.py >> "/Volumes/1TB NVME 1/antikythera/data/reddit_gate/extract.log" 2>&1 \
      && "$PY" -u /Users/andrej/workspace/antikythera/eval/run_gate.py >> "/Volumes/1TB NVME 1/antikythera/data/reddit_gate/gate_final.log" 2>&1 \
      && echo "$(date +%H:%M) FINAL GATE TABLE READY" >> "$LOG" \
      || echo "$(date +%H:%M) PIPELINE FAILED — see extract.log/gate_final.log" >> "$LOG"
    exit 0
  fi
  sleep 180
done
