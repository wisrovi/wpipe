"""
Dashboard - Full Example with Conditional Pipeline

This comprehensive example demonstrates:
1. Creating a complex pipeline with conditional branches
2. Executing multiple runs to generate historical data
3. Starting the dashboard to visualize everything

The pipeline simulates a data processing workflow with:
- Validation step
- Conditional processing based on data type
- Error handling
- Statistics calculation
"""

import os
import random
from wpipe import Pipeline, Condition


def validate_input(data: dict) -> dict:
    """Validate input data."""
    data_type = data.get("type", "unknown")
    return {
        "valid": True,
        "type": data_type,
        "message": f"Data type '{data_type}' validated",
    }


def process_numbers(data: dict) -> dict:
    """Process numeric data."""
    numbers = data.get("numbers", [])
    return {
        "processed": numbers,
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers) if numbers else 0,
        "count": len(numbers),
    }


def process_text(data: dict) -> dict:
    """Process text data."""
    text = data.get("text", "")
    words = text.split()
    return {
        "processed": text,
        "word_count": len(words),
        "char_count": len(text),
        "uppercase": text.upper(),
    }


def process_records(data: dict) -> dict:
    """Process record data."""
    records = data.get("records", [])
    return {
        "processed": records,
        "count": len(records),
        "ids": [r.get("id") for r in records],
    }


def calculate_metrics(data: dict) -> dict:
    """Calculate final metrics."""
    metrics = {}

    if "sum" in data:
        metrics["numeric_sum"] = data["sum"]
    if "word_count" in data:
        metrics["total_words"] = data["word_count"]
    if "count" in data:
        metrics["total_records"] = data["count"]

    return {"metrics": metrics, "status": "completed"}


def run_pipeline_batch(db_path: str, config_dir: str, batch_id: int) -> None:
    """Run a single pipeline execution."""
    data_types = ["numbers", "text", "records"]
    data_type = random.choice(data_types)

    if data_type == "numbers":
        input_data = {
            "type": "numbers",
            "numbers": [random.randint(1, 100) for _ in range(5)],
        }
    elif data_type == "text":
        input_data = {
            "type": "text",
            "text": "Hello world this is a sample text for processing",
        }
    else:
        input_data = {
            "type": "records",
            "records": [
                {"id": i, "name": f"User_{i}", "score": random.randint(50, 100)}
                for i in range(3)
            ],
        }

    pipeline = Pipeline(
        verbose=False,
        tracking_db=db_path,
        config_dir=config_dir,
    )

    if data_type == "numbers":
        pipeline.set_steps(
            [
                (validate_input, "Validate Input", "v1.0"),
                (process_numbers, "Process Numbers", "v1.0"),
                (calculate_metrics, "Calculate Metrics", "v1.0"),
            ]
        )
    elif data_type == "text":
        pipeline.set_steps(
            [
                (validate_input, "Validate Input", "v1.0"),
                (process_text, "Process Text", "v1.0"),
                (calculate_metrics, "Calculate Metrics", "v1.0"),
            ]
        )
    else:
        pipeline.set_steps(
            [
                (validate_input, "Validate Input", "v1.0"),
                (process_records, "Process Records", "v1.0"),
                (calculate_metrics, "Calculate Metrics", "v1.0"),
            ]
        )

    try:
        result = pipeline.run(input_data)
    except Exception as e:
        pass


def main():
    """Run the full example."""
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    if os.path.exists(db_path):
        os.remove(db_path)

    print("\n" + "=" * 60)
    print("WPIPE DASHBOARD - FULL EXAMPLE")
    print("=" * 60)
    print("\nGenerating historical pipeline data...")

    num_runs = 10
    for i in range(num_runs):
        print(f"  Running pipeline {i + 1}/{num_runs}...", end=" ")
        run_pipeline_batch(db_path, config_dir, i + 1)
        print("✓")

    print(f"\nGenerated {num_runs} pipeline executions")
    print(f"Database: {db_path}")

    print("\n" + "=" * 60)
    print("To view the dashboard, run:")
    print(
        "  cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
