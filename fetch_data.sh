#!/bin/bash
# Requires FOOTBALL_DATA_API_TOKEN env var set (free key from football-data.org)
set -e

fetch() {
  # $1 = competition code, $2 = output file
  curl -s -H "X-Auth-Token: $FOOTBALL_DATA_API_TOKEN" "https://api.football-data.org/v4/competitions/$1/standings" -o "$2"
  if grep -q '"errorCode"' "$2"; then
    echo "ERROR: fetch for $1 failed — $(cat "$2")" >&2
    exit 1
  fi
  sleep 7
}

fetch PL pl_standings.json
fetch ELC elc_standings.json
fetch PD pd_standings.json
fetch BL1 bl1_standings.json
fetch SA sa_standings.json
fetch FL1 fl1_standings.json
fetch CL cl_standings.json
python3 build_dashboard.py
echo "Rebuilt index.html"
