"""
Example demonstrating metrics and statistics export functionality.

Shows how to export pipeline execution metrics, logs, and statistics
to JSON and CSV formats for analysis and reporting.
"""

import os
import time
from pathlib import Path

from wpipe import Pipeline, PipelineExporter


def step_1_fetch_data(data: dict) -> dict:
    """Simulate data fetching."""
    print("[Step 1] Fetching data from API...")
    time.sleep(0.5)
    return {"fetched_records": 1500}


def step_2_validate(data: dict) -> dict:
    """Simulate data validation."""
    print("[Step 2] Validating records...")
    time.sleep(0.3)
    records = data.get("fetched_records", 0)
    return {"validated_records": int(records * 0.95)}


def step_3_transform(data: dict) -> dict:
    """Simulate data transformation."""
    print("[Step 3] Transforming data...")
    time.sleep(0.4)
    records = data.get("validated_records", 0)
    return {"transformed_records": records, "transformation_time": 0.4}


def demo_metrics_export() -> None:
    """Demonstrate metrics export functionality."""
    print("\n" + "=" * 70)
    print("METRICS AND STATISTICS EXPORT DEMO")
    print("=" * 70 + "\n")

    db_path = "metrics_demo.db"
    output_dir = "export_output"

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Create and run pipeline with tracking
    pipeline = Pipeline(
        tracking_db=db_path,
        pipeline_name="metrics_export_demo",
        verbose=False,
        collect_system_metrics=True,  # Enable metrics collection
    )

    pipeline.set_steps(
        [
            (step_1_fetch_data, "fetch_data", "v1.0"),
            (step_2_validate, "validate_data", "v1.0"),
            (step_3_transform, "transform_data", "v1.0"),
        ]
    )

    # Run pipeline
    print("Running pipeline with metrics collection...\n")
    result = pipeline.run({})

    print(f"\n✓ Pipeline completed!")
    print(f"  Result: {result}\n")

    # Initialize exporter
    exporter = PipelineExporter(db_path)

    print("=" * 70)
    print("EXPORTING DATA")
    print("=" * 70 + "\n")

    # Export statistics
    print("1. Exporting statistics to JSON...")
    stats_path = os.path.join(output_dir, "pipeline_statistics.json")
    try:
        exporter.export_statistics(format="json", output_path=stats_path)
        print(f"   ✓ Saved to: {stats_path}\n")

        with open(stats_path) as f:
            import json

            stats = json.load(f)
            print("   Statistics:")
            for key, value in stats.items():
                print(f"     - {key}: {value}")
    except Exception as e:
        print(f"   ⚠ Stats export note: {e}\n")

    # Export metrics (simulated)
    print("\n2. Exporting pipeline logs...")
    logs_path = os.path.join(output_dir, "pipeline_logs.json")
    print(f"   → Output location: {logs_path}")
    print(f"   → Logs would be exported from tracking database\n")

    # Show available files
    print("=" * 70)
    print("AVAILABLE EXPORTS")
    print("=" * 70 + "\n")

    if Path(output_dir).exists():
        for file in Path(output_dir).glob("*"):
            size = file.stat().st_size
            print(f"✓ {file.name} ({size} bytes)")
    else:
        print("Output directory not yet created")

    print("\n✓ Export demo completed!")
    print("  These files can be sent to support or analyzed in Excel/Python\n")


def demo_export_formats() -> None:
    """Demonstrate different export formats."""
    print("\n" + "=" * 70)
    print("SUPPORTED EXPORT FORMATS")
    print("=" * 70 + "\n")

    print("JSON Export:")
    print("  - Human readable")
    print("  - Best for nested/complex data")
    print("  - Supported by: Python, JavaScript, most tools")
    print("  - Usage: exporter.export_pipeline_logs(format='json')\n")

    print("CSV Export:")
    print("  - Spreadsheet compatible")
    print("  - Best for tabular data")
    print("  - Supported by: Excel, Google Sheets, Pandas")
    print("  - Usage: exporter.export_pipeline_logs(format='csv')\n")


if __name__ == "__main__":
    demo_metrics_export()
    demo_export_formats()
