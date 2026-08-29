#!/usr/bin/env bash
# Pull the filtered HN slice from the ClickHouse public playground.
# Idempotent: skips files that already exist and are non-empty.
# Playground caps results at 1M rows -> comment skeleton is pulled monthly.
# Playground quota: 100 queries/hour per normalized query hash (all monthly
# skeleton queries share one hash). Bulk runs stall after ~100 chunks; re-run
# in a later hour to continue (idempotent). Do not engineer around this.
# Usage: pull_hn.sh [first_year] [last_year]
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENDPOINT="https://play.clickhouse.com/?user=play"
OUT="$ROOT/data/raw/hn"
SQL="$ROOT/sql"
FIRST="${1:-2006}"
LAST="${2:-2026}"

mkdir -p "$OUT/stories" "$OUT/comments_top20" "$OUT/comment_skeleton"

fetch() { # $1=query $2=outfile
    local q="$1" out="$2"
    if [[ -s "$out" ]]; then
        echo "skip  $(basename "$out")"
        return 0
    fi
    local attempt
    for attempt in 1 2 3; do
        if curl -sS --fail --max-time 300 "$ENDPOINT" --data-binary "$q" -o "$out.tmp"; then
            # Parquet magic bytes check: an error page is not a parquet file
            if head -c4 "$out.tmp" | grep -q PAR1; then
                mv "$out.tmp" "$out"
                echo "ok    $(basename "$out") $(du -h "$out" | cut -f1 | tr -d ' ')"
                return 0
            fi
            echo "bad payload for $(basename "$out") (attempt $attempt): $(head -c200 "$out.tmp")"
        else
            echo "curl fail for $(basename "$out") (attempt $attempt)"
        fi
        rm -f "$out.tmp"
        sleep $((attempt * 10))
    done
    echo "FAIL  $(basename "$out")"
    return 1
}

year_query() { # $1=template $2=year
    sed -e "s/{YEAR}/$2/g" -e "s/{NEXT_YEAR}/$(($2 + 1))/g" "$1"
}

month_query() { # $1=template $2=year $3=month
    local y=$2 m=$3 ny nm
    if [[ $m -eq 12 ]]; then ny=$((y + 1)); nm=1; else ny=$y; nm=$((m + 1)); fi
    sed -e "s/{START}/$(printf '%04d-%02d-01' "$y" "$m")/g" \
        -e "s/{END}/$(printf '%04d-%02d-01' "$ny" "$nm")/g" "$1"
}

fails=0
for year in $(seq "$FIRST" "$LAST"); do
    fetch "$(year_query "$SQL/stories_filtered.sql.tmpl" "$year")" \
          "$OUT/stories/stories_$year.parquet" || fails=$((fails+1))
    fetch "$(year_query "$SQL/comments_top20.sql.tmpl" "$year")" \
          "$OUT/comments_top20/comments_$year.parquet" || fails=$((fails+1))
    for month in $(seq 1 12); do
        # don't query months that haven't happened yet
        if [[ $(printf '%04d%02d' "$year" "$month") -gt $(date +%Y%m) ]]; then
            continue
        fi
        fetch "$(month_query "$SQL/comment_skeleton.sql.tmpl" "$year" "$month")" \
              "$OUT/comment_skeleton/skeleton_$(printf '%04d_%02d' "$year" "$month").parquet" || fails=$((fails+1))
    done
done

echo "done. failures: $fails"
exit $((fails > 0))
