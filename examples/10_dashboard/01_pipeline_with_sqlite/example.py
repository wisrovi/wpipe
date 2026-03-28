"""
Dashboard - Pipeline with SQLite Integration

This example demonstrates how to create a pipeline that automatically
stores execution data in SQLite, which can then be viewed in the dashboard.

Run this example first to generate data, then start the dashboard to view it.
"""

import os
from wpipe import Pipeline, Wsqlite


def fetch_data(data: dict) -> dict:
    """Simulate fetching data from an external source."""
    return {
        "source": "api",
        "records": [
            {"id": 1, "name": "Alice", "score": 95},
            {"id": 2, "name": "Bob", "score": 87},
            {"id": 3, "name": "Charlie", "score": 72},
        ],
    }


def process_records(data: dict) -> dict:
    """Process the fetched records."""
    records = data.get("records", [])
    processed = []

    for record in records:
        processed.append(
            {
                "id": record["id"],
                "name": record["name"],
                "score": record["score"],
                "grade": "A"
                if record["score"] >= 90
                else "B"
                if record["score"] >= 80
                else "C"
                if record["score"] >= 70
                else "F",
                "passed": record["score"] >= 70,
            }
        )

    return {"processed_records": processed, "total": len(processed)}


def calculate_stats(data: dict) -> dict:
    """Calculate statistics from processed records."""
    records = data.get("processed_records", [])
    scores = [r["score"] for r in records]

    return {
        "statistics": {
            "average": sum(scores) / len(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "min": min(scores) if scores else 0,
            "count": len(scores),
        },
        "passed_count": sum(1 for r in records if r["passed"]),
    }


def main() -> None:
    """Run the pipeline with SQLite integration."""
    db_path = "pipeline_data.db"

    if os.path.exists(db_path):
        os.remove(db_path)

    pipeline = Pipeline(verbose=True)
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

    with Wsqlite(db_name=db_path) as db:
        db.input = {"user_id": 123, "batch": "batch_001"}

        result = pipeline.run({})

        db.output = result
        db.details = {
            "pipeline_version": "1.0.0",
            "steps_executed": 3,
        }

    print("\n" + "=" * 50)
    print("Pipeline completed successfully!")
    print(f"Data saved to: {db_path}")
    print("\nTo view the dashboard, run:")
    print(f"  python -m wpipe.dashboard --db {db_path} --open")
    print("=" * 50)


if __name__ == "__main__":
    main()
