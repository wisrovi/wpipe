#!/bin/bash
# wpipe Dashboard Launcher
# This script runs the wpipe dashboard with the shared database

cd "$(dirname "$0")"

echo "========================================"
echo "  wpipe Dashboard Launcher"
echo "========================================"
echo ""
echo "Starting dashboard..."
echo "Database: wpipe_dashboard.db"
echo "Config:   configs/"
echo ""
echo "Dashboard will open at: http://127.0.0.1:8035"
echo ""

python -m wpipe.dashboard \
    --db wpipe_dashboard.db \
    --config-dir configs \
    --port 8036 \
    --open
