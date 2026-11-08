#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || true
HOST="${1:-0.0.0.0}"
PORT="${2:-5000}"
echo "[*] Serving on http://$HOST:$PORT"
python3 cli.py serve --host "$HOST" --port "$PORT"
