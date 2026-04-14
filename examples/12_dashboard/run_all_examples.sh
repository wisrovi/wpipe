#!/bin/bash
# wpipe Dashboard - Run All Examples
# This script runs all examples and then starts the dashboard

cd "$(dirname "$0")"

echo "========================================"
echo "  wpipe - Running All Examples"
echo "========================================"
echo ""

# Clean previous database
rm -f wpipe_dashboard.db
mkdir -p configs logs

# Function to run an example
run_example() {
    local dir=$1
    local name=$2
    echo "----------------------------------------"
    echo "Running: $name"
    echo "----------------------------------------"
    cd "$dir"
    python example.py 2>&1 | tail -5
    cd ..
    echo ""
}

# Run all examples
run_example "01_pipeline_with_sqlite" "01 - Pipeline with SQLite"
run_example "04_basic_tracking" "04 - Basic Tracking"
run_example "05_error_handling" "05 - Error Handling"
run_example "06_retry_logic" "06 - Retry Logic"
run_example "07_conditions" "07 - Conditional Branching"
run_example "08_nested_pipelines" "08 - Nested Pipelines"
run_example "09_events_annotations" "09 - Events & Annotations"
run_example "10_alerts" "10 - Alert System"
run_example "11_pipeline_relations" "11 - Pipeline Relations"
run_example "12_performance_comparison" "12 - Performance Comparison"
run_example "13_complete_dashboard" "13 - Complete Dashboard (ALL FEATURES)"

echo "========================================"
echo "  All Examples Completed!"
echo "========================================"
# echo ""
# echo "Starting Dashboard..."
# echo ""

# Start dashboard
# python -m wpipe.dashboard \
#     --db wpipe_dashboard.db \
#     --config-dir configs \
#     --port 8035 \
#     --open
