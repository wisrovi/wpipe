"""
Example demonstrating pipeline log export to JSON and CSV formats.

Shows how to export execution logs for analysis, debugging, and reporting
to various formats that can be used in Excel, Python, or web dashboards.
"""

import csv
import json
import time
from pathlib import Path

from wpipe import Pipeline, PipelineExporter


def step_1_collect(data: dict) -> dict:
    """Collect data from source."""
    print("[Collect] Gathering data...")
    time.sleep(0.5)
    return {"collected": 500}


def step_2_filter(data: dict) -> dict:
    """Filter data."""
    print("[Filter] Removing duplicates...")
    time.sleep(0.3)
    collected = data.get("collected", 0)
    return {"filtered": int(collected * 0.92)}


def step_3_enrich(data: dict) -> dict:
    """Enrich data with metadata."""
    print("[Enrich] Adding metadata...")
    time.sleep(0.4)
    return {"enriched": True, "metadata_fields": 5}


def export_logs_to_json(exporter: PipelineExporter, output_path: str) -> None:
    """Export logs to JSON format."""
    print("\n" + "=" * 70)
    print("JSON EXPORT")
    print("=" * 70)

    try:
        json_data = exporter.export_pipeline_logs(format="json")

        if json_data:
            Path(output_path).write_text(json_data)
            print(f"✓ Exported to: {output_path}")
            print(f"  File size: {len(json_data)} bytes")

            # Show sample
            data = json.loads(json_data)
            if isinstance(data, list) and data:
                print(f"  Records: {len(data)}")
                print(f"  Sample record keys: {list(data[0].keys())}")
        else:
            print("ℹ No execution data to export yet")
    except Exception as e:
        print(f"ℹ JSON export: {e}")


def export_logs_to_csv(exporter: PipelineExporter, output_path: str) -> None:
    """Export logs to CSV format."""
    print("\n" + "=" * 70)
    print("CSV EXPORT")
    print("=" * 70)

    try:
        csv_data = exporter.export_pipeline_logs(format="csv")

        if csv_data:
            Path(output_path).write_text(csv_data)
            print(f"✓ Exported to: {output_path}")

            lines = csv_data.split("\n")
            print(f"  File size: {len(csv_data)} bytes")
            print(f"  Records: {len(lines) - 1}")  # Exclude header
            print(f"  Columns: {len(lines[0].split(','))}")
            print(f"  Header: {lines[0]}")
        else:
            print("ℹ No execution data to export yet")
    except Exception as e:
        print(f"ℹ CSV export: {e}")


def demo_log_export() -> None:
    """Demonstrate log export functionality."""
    print("\n" + "=" * 70)
    print("PIPELINE LOG EXPORT DEMO")
    print("=" * 70 + "\n")

    db_path = "log_export_demo.db"
    output_dir = "exported_logs"

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Create and run pipeline
    pipeline = Pipeline(
        tracking_db=db_path,
        pipeline_name="log_export_demo",
        verbose=False,
    )

    pipeline.set_steps(
        [
            (step_1_collect, "collect_data", "v1.0"),
            (step_2_filter, "filter_data", "v1.0"),
            (step_3_enrich, "enrich_data", "v1.0"),
        ]
    )

    print("Running pipeline...\n")
    result = pipeline.run({})

    print(f"\n✓ Pipeline completed with result: {result}\n")

    # Initialize exporter
    exporter = PipelineExporter(db_path)

    # Export to different formats
    json_path = str(Path(output_dir) / "pipeline_logs.json")
    csv_path = str(Path(output_dir) / "pipeline_logs.csv")

    export_logs_to_json(exporter, json_path)
    export_logs_to_csv(exporter, csv_path)

    # Show summary
    print("\n" + "=" * 70)
    print("EXPORT SUMMARY")
    print("=" * 70 + "\n")

    print("✓ Logs exported successfully!")
    print("  Use cases:")
    print("    - Send to support team for debugging")
    print("    - Load in Excel for analysis")
    print("    - Import to Python for data processing")
    print("    - Upload to cloud storage for archiving\n")


def demo_export_use_cases() -> None:
    """Show real-world export use cases."""
    print("\n" + "=" * 70)
    print("EXPORT USE CASES")
    print("=" * 70 + "\n")

    print("1. DEBUGGING:")
    print("   → Export JSON")
    print("   → Look for error_message fields")
    print("   → Check timestamps and execution_time\n")

    print("2. ANALYTICS:")
    print("   → Export CSV")
    print("   → Load in Excel/Google Sheets")
    print("   → Create pivot tables and charts\n")

    print("3. REPORTING:")
    print("   → Export statistics")
    print("   → Generate PDF reports")
    print("   → Track KPIs over time\n")

    print("4. COMPLIANCE:")
    print("   → Export full logs")
    print("   → Archive for audit trail")
    print("   → Verify all steps completed\n")


if __name__ == "__main__":
    demo_log_export()
    demo_export_use_cases()
