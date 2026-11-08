#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || true
HOST="${1:-0.0.0.0}"
PORT="${2:-5000}"
if [ -n "${PYTHON:-}" ]; then
    :
elif command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi
echo "[*] Serving on http://$HOST:$PORT"
"$PYTHON" cli.py serve --host "$HOST" --port "$PORT"
