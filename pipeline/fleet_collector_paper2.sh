#!/bin/bash
# Paper-2 fleet collector: WSB 2019-01..2024-12 (72 month-nodes) + 5 DD
# control subs (one node each, all 72 months, monthly shards). Rolling queue
# capped at MAXBOX concurrent boxes: create from queue, bootstrap bare boxes,
# relaunch dead pulls (puller resumes from cursor), rsync complete boxes to
# the NVMe, destroy collected boxes, heartbeat WATCH lines. NO downstream
# trigger — acquisition only (registration must freeze before any analysis).
# Priority order: 2021 Q1 (multi-hour GME months) + DD subs first so long
# tails overlap the later waves. Adapted from fleet_collector.sh (gate run,
# 21 nodes, zero bans); both SSH landmines and alarm-timeouts preserved.
set -u
source ~/.config/antikythera/vultr.env
AUTH="Authorization: Bearer $VULTR_API_KEY"
SSHKEY_ID="7a23f40e-b96a-407e-a826-0aa991a75d10"
REGION="sea"; PLAN="vc2-1c-1gb"; OSID="2136"   # Debian 12
TAG="antikythera-paper2"
S="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=12 -o ServerAliveInterval=5 -o ServerAliveCountMax=3"
# macOS has no timeout(1); perl alarm bounds every remote call.
TO () { perl -e 'alarm shift @ARGV; exec @ARGV' "$@"; }
DEST="/Volumes/1TB NVME 1/antikythera/data/paper2/pull"
LOG="/Volumes/1TB NVME 1/antikythera/data/paper2/fleet_watch.log"
PULLER="$HOME/workspace/antikythera/pipeline/pull_reddit_paper2.py"
MAXBOX=20

MONTHS=""
for y in 2019 2020 2021 2022 2023 2024; do
  for m in 01 02 03 04 05 06 07 08 09 10 11 12; do MONTHS="$MONTHS $y-$m"; done
done
DD_SUBS="stocks investing StockMarket ValueInvesting SecurityAnalysis"

QUEUE="wsb-2021-01 wsb-2021-02 wsb-2021-03"
for s in $DD_SUBS; do QUEUE="$QUEUE dd-$s"; done
for m in $MONTHS; do
  case "$m" in 2021-01|2021-02|2021-03) continue;; esac
  QUEUE="$QUEUE wsb-$m"
done
N_SHARDS=$(echo "$QUEUE" | wc -w | tr -d ' ')

sub_of () { case "$1" in wsb-*) echo wallstreetbets;; dd-*) echo "${1#dd-}";; esac; }
months_of () { case "$1" in wsb-*) echo "${1#wsb-}";; dd-*) echo $MONTHS;; esac; }
expected_of () { case "$1" in wsb-*) echo 2;; dd-*) echo 144;; esac; }

done_local () {  # label -> all expected .ndjson.gz present in DEST
  local n
  case "$1" in
    wsb-*) n=$(ls "$DEST"/*_wallstreetbets_"${1#wsb-}".ndjson.gz 2>/dev/null | wc -l | tr -d ' ');;
    dd-*)  n=$(ls "$DEST"/*_"$(sub_of "$1")"_*.ndjson.gz 2>/dev/null | wc -l | tr -d ' ');;
  esac
  [ "${n:-0}" -ge "$(expected_of "$1")" ]
}

launch_on () {  # ip label — scp puller + setsid-launch (landmine-safe)
  local ip=$1 lb=$2
  TO 60 scp $S "$PULLER" root@"$ip":/root/pull.py >/dev/null 2>&1 || return 1
  TO 30 ssh -n $S root@"$ip" "mkdir -p /root/out; cd /root; (PULL_OUT=/root/out PULL_SLEEP=0.25 setsid nohup python3 -u pull.py $(sub_of "$lb") --month $(months_of "$lb") > pull.log 2>&1 < /dev/null &) ; exit 0" 2>/dev/null
}

create_box () {  # label
  curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" \
    "https://api.vultr.com/v2/instances" \
    -d "{\"region\":\"$REGION\",\"plan\":\"$PLAN\",\"os_id\":$OSID,
         \"label\":\"p2-$1\",\"sshkey_id\":[\"$SSHKEY_ID\"],
         \"tags\":[\"$TAG\"]}" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['instance']['id'])" 2>/dev/null
}

echo "$(date +%H:%M) START paper2 fleet: $N_SHARDS shards, cap $MAXBOX boxes" >> "$LOG"

while true; do
  INST=$(curl -s -H "$AUTH" "https://api.vultr.com/v2/instances?tag=$TAG&per_page=100" \
    | python3 -c "import json,sys; [print(i['id'],i['label'].replace('p2-','',1),i['main_ip']) for i in json.load(sys.stdin).get('instances',[])]")
  n_boxes=0; line=""; RUNNING=""
  while read -r id lb ip; do
    [ -z "${id:-}" ] && continue
    n_boxes=$((n_boxes+1)); RUNNING="$RUNNING $lb"
    if done_local "$lb"; then
      curl -s -X DELETE -H "$AUTH" "https://api.vultr.com/v2/instances/$id" >/dev/null
      n_boxes=$((n_boxes-1))
      echo "$(date +%H:%M) COLLECTED $lb — box destroyed" >> "$LOG"; continue
    fi
    [ "$ip" = "0.0.0.0" ] && { line="$line $lb:prov"; continue; }
    ST=$(TO 30 ssh -n $S root@"$ip" "ls /root/out/*.ndjson.gz 2>/dev/null | wc -l; pgrep -c python3 || true; tail -c 300 /root/pull.log 2>/dev/null | grep -oE '[0-9]+ rows' | tail -1" 2>/dev/null | tr '\n' '|')
    ngz=$(echo "$ST" | cut -d'|' -f1 | tr -d ' '); alive=$(echo "$ST" | cut -d'|' -f2 | tr -d ' '); rows=$(echo "$ST" | cut -d'|' -f3)
    if [ "${ngz:-0}" -ge "$(expected_of "$lb")" ] 2>/dev/null; then
      TO 600 rsync -az -e "ssh $S" root@"$ip":/root/out/ "$DEST/" >> "$LOG" 2>&1
      if done_local "$lb"; then
        curl -s -X DELETE -H "$AUTH" "https://api.vultr.com/v2/instances/$id" >/dev/null
        n_boxes=$((n_boxes-1))
        echo "$(date +%H:%M) COLLECTED $lb — box destroyed" >> "$LOG"
      else
        echo "$(date +%H:%M) STUCK $lb: rsync did not land files" >> "$LOG"
      fi
    elif [ "${alive:-0}" = "0" ]; then
      launch_on "$ip" "$lb" \
        && echo "$(date +%H:%M) RELAUNCH $lb on $ip" >> "$LOG" \
        || echo "$(date +%H:%M) STUCK $lb: cannot launch on $ip" >> "$LOG"
    else
      line="$line $lb:${rows:-0r}"
    fi
  done <<< "$INST"

  shards_home=0
  for lb in $QUEUE; do done_local "$lb" && shards_home=$((shards_home+1)); done

  created=0
  for lb in $QUEUE; do
    [ "$n_boxes" -ge "$MAXBOX" ] && break
    done_local "$lb" && continue
    case " $RUNNING " in *" $lb "*) continue;; esac
    NEWID=$(create_box "$lb")
    if [ -n "${NEWID:-}" ]; then
      n_boxes=$((n_boxes+1)); created=$((created+1)); RUNNING="$RUNNING $lb"
      echo "$(date +%H:%M) CREATED $lb -> $NEWID" >> "$LOG"
    else
      echo "$(date +%H:%M) STUCK create failed for $lb" >> "$LOG"
    fi
  done

  echo "$(date +%H:%M) WATCH shards_home=$shards_home/$N_SHARDS boxes_up=$n_boxes created=$created$line" >> "$LOG"

  if [ "$shards_home" = "$N_SHARDS" ]; then
    LEFT=$(curl -s -H "$AUTH" "https://api.vultr.com/v2/instances?tag=$TAG&per_page=100" \
      | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('instances',[])))")
    echo "$(date +%H:%M) ALL $N_SHARDS SHARDS HOME — teardown check: $LEFT boxes left by tag (must be 0)" >> "$LOG"
    exit 0
  fi
  sleep 180
done
