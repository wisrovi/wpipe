"""
Dashboard - Pipeline with SQLite Integration

This example demonstrates how to create a pipeline that automatically
stores execution data in SQLite, which can then be viewed in the dashboard.

Run this example first to generate data, then start the dashboard to view it.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wpipe import Pipeline
from states import fetch_data, process_records, calculate_stats


def main() -> None:
    """Run the pipeline with SQLite integration."""
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    # Remove old database to start fresh (optional)
    # if os.path.exists(db_path):
    #     os.remove(db_path)

    pipeline = Pipeline(
        verbose=True,
        tracking_db=db_path,
        config_dir=config_dir,
    )
    pipeline.set_steps(
        [
            (fetch_data, "Fetch Data", "v1.0"),
            (process_records, "Process Records", "v1.0"),
            (calculate_stats, "Calculate Stats", "v1.0"),
        ]
    )

    print("\n" + "=" * 50)
    print("Running pipeline with SQLite integration...")
    print("=" * 50 + "\n")

    result = pipeline.run({"user_id": 123, "batch": "batch_001"})

    print("\n" + "=" * 50)
    print("Pipeline completed successfully!")
    print(f"Data saved to: {db_path}")
    print("\nTo view the dashboard, run:")
    print(
        f"  cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )
    print("=" * 50)


if __name__ == "__main__":
    main()
