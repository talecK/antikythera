#!/bin/bash
# Bootstrap the Vultr bench box and launch the batched cluster run.
# Usage: box_bootstrap.sh <ip>
set -euo pipefail
IP="$1"
SSH="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 root@$IP"
SRC="/Users/andrej/workspace/antikythera"
REG="/Volumes/1TB NVME 1/antikythera/data/registry/pilot1"

echo "== wait for ssh =="
for i in $(seq 1 30); do $SSH true 2>/dev/null && break; sleep 10; done
$SSH true

echo "== install deps =="
$SSH "apt-get -qq update && apt-get -qq install -y python3-venv rsync >/dev/null && python3 -m venv /root/venv && /root/venv/bin/pip -q install faiss-cpu numpy pyarrow duckdb"

echo "== ship code + data =="
$SSH "mkdir -p /root/antikythera/pipeline /root/antikythera/data/registry/pilot1_box"
rsync -az -e "ssh -o StrictHostKeyChecking=accept-new" \
  "$SRC/pipeline/build_registry.py" root@"$IP":/root/antikythera/pipeline/
rsync -az --progress -e "ssh -o StrictHostKeyChecking=accept-new" \
  "$REG/claims.parquet" "$REG/embeddings.npy" "$REG/claim_texts.json" \
  root@"$IP":/root/antikythera/data/registry/pilot1_box/

echo "== launch batched cluster (logged, unpiped) =="
$SSH "cd /root/antikythera && REGISTRY_OUT=/root/antikythera/data/registry/pilot1_box CLUSTER_BATCH=2048 OMP_NUM_THREADS=64 nohup /root/venv/bin/python pipeline/build_registry.py cluster > /root/cluster.log 2>&1 & echo launched pid \$!"

echo "== BOOTSTRAP DONE =="
