#!/bin/bash
# Parallel API fill: one cheap Vultr box per WSB month. Stdlib-only puller,
# so bootstrap is just scp. Results rsync back to the NVMe pull dir with
# month-granular shard names; boxes are destroyed at the end regardless.
set -uo pipefail
source ~/.config/pricemole/vultr.env
KEY="Authorization: Bearer $VULTR_API_KEY"
SSHKEY_ID="7a23f40e-b96a-407e-a826-0aa991a75d10"
REGION="sea"; PLAN="vc2-1c-1gb"; OSID="2136"   # Debian 12
SRC="/Users/andrej/workspace/antikythera/pipeline/pull_reddit_gate.py"
DEST="/Volumes/1TB NVME 1/antikythera/data/reddit_gate/pull"
LOG="/Volumes/1TB NVME 1/antikythera/data/reddit_gate/fleet.log"
MONTHS=("$@")
echo "$(date +%H:%M) fleet: ${#MONTHS[@]} months: ${MONTHS[*]}" >> "$LOG"

declare -a IDS IPS
for i in "${!MONTHS[@]}"; do
  R=$(curl -s -X POST -H "$KEY" -H "Content-Type: application/json" \
    "https://api.vultr.com/v2/instances" \
    -d "{\"region\":\"$REGION\",\"plan\":\"$PLAN\",\"os_id\":$OSID,
         \"label\":\"gate-fill-${MONTHS[$i]}\",\"sshkey_id\":[\"$SSHKEY_ID\"],
         \"tags\":[\"antikythera-gate\"]}")
  IDS[$i]=$(echo "$R" | python3 -c "import json,sys; print(json.load(sys.stdin)['instance']['id'])")
  echo "$(date +%H:%M) created ${MONTHS[$i]} -> ${IDS[$i]}" >> "$LOG"
done

for i in "${!MONTHS[@]}"; do
  for t in $(seq 1 60); do
    R=$(curl -s -H "$KEY" "https://api.vultr.com/v2/instances/${IDS[$i]}")
    IP=$(echo "$R" | python3 -c "import json,sys; d=json.load(sys.stdin)['instance']; print(d['main_ip'] if d['status']=='active' and d['main_ip']!='0.0.0.0' else '')")
    [ -n "$IP" ] && { IPS[$i]="$IP"; break; }
    sleep 10
  done
  echo "$(date +%H:%M) ${MONTHS[$i]} ip=${IPS[$i]:-FAILED}" >> "$LOG"
done

SSH="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"
for i in "${!MONTHS[@]}"; do
  IP="${IPS[$i]:-}"; [ -z "$IP" ] && continue
  for t in $(seq 1 30); do $SSH root@"$IP" true 2>/dev/null && break; sleep 10; done
  scp -o StrictHostKeyChecking=accept-new "$SRC" root@"$IP":/root/pull.py
  $SSH root@"$IP" "mkdir -p /root/out && cd /root && PULL_OUT=/root/out PULL_SLEEP=0.25 nohup python3 -u pull.py wallstreetbets --month ${MONTHS[$i]} > pull.log 2>&1 & echo started"
  echo "$(date +%H:%M) ${MONTHS[$i]} launched on $IP" >> "$LOG"
done

echo "$(date +%H:%M) fleet launched; polling for completion" >> "$LOG"
for t in $(seq 1 200); do
  ALLDONE=1
  for i in "${!MONTHS[@]}"; do
    IP="${IPS[$i]:-}"; [ -z "$IP" ] && continue
    N=$($SSH root@"$IP" "ls /root/out/*.ndjson.gz 2>/dev/null | wc -l" 2>/dev/null | tr -d ' ')
    [ "$N" = "2" ] || ALLDONE=0
  done
  [ "$ALLDONE" = "1" ] && break
  sleep 120
done

for i in "${!MONTHS[@]}"; do
  IP="${IPS[$i]:-}"; [ -z "$IP" ] && continue
  rsync -az -e "ssh -o StrictHostKeyChecking=accept-new" \
    root@"$IP":/root/out/ "$DEST/" >> "$LOG" 2>&1
  $SSH root@"$IP" "tail -2 /root/pull.log" >> "$LOG" 2>&1
done

for i in "${!IDS[@]}"; do
  curl -s -X DELETE -H "$KEY" "https://api.vultr.com/v2/instances/${IDS[$i]}"
  echo "$(date +%H:%M) destroyed ${IDS[$i]} (${MONTHS[$i]})" >> "$LOG"
done
echo "$(date +%H:%M) FLEET DONE" >> "$LOG"
