"""
Basic export example using WSQLite models.

Demonstrates exporting pipeline execution data to JSON and CSV.
"""

import json
from pathlib import Path
from wsqlite import WSQLite
from wpipe import PipelineExporter
from wpipe.sqlite.tables_dto.tracker_models import PipelineModel

# Create sample export directory
export_dir = Path("exports")
export_dir.mkdir(exist_ok=True)


def setup_sample_data():
    """Setup sample execution data using WSQLite."""
    db_path = "export_example.db"
    # Forzamos el nombre de tabla 'pipelines' para que el Exporter lo encuentre
    db = WSQLite(PipelineModel, db_path)
    db.table_name = "pipelines"

    # Insert sample data using PipelineModel
    sample_data = [
        PipelineModel(id="pipeline_1", name="viaje", status="completed", started_at="2024-03-31T10:00:00", total_duration_ms=5000),
        PipelineModel(id="pipeline_2", name="viaje", status="completed", started_at="2024-03-31T11:00:00", total_duration_ms=6000),
        PipelineModel(id="pipeline_3", name="analisis", status="error", started_at="2024-03-31T12:00:00", error_message="Fatal error"),
    ]

    for item in sample_data:
        db.insert(item)

    return db_path


if __name__ == "__main__":
    print("=== Basic Export Example ===\n")

    # Setup sample data
    db_path = setup_sample_data()
    print(f"✓ Sample database created: {db_path}\n")

    # Create exporter
    exporter = PipelineExporter(db_path)

    # Example 1: Export all logs as JSON
    print("--- Example 1: Export All Logs (JSON) ---")
    json_output = exporter.export_pipeline_logs(format="json")
    if json_output:
        print(f"✓ Exported {len(json.loads(json_output))} records")

        # Save to file
        json_path = export_dir / "all_logs.json"
        exporter.export_pipeline_logs(format="json", output_path=str(json_path))
        print(f"✓ Saved to {json_path}\n")

    # Example 2: Export logs as CSV
    print("--- Example 2: Export All Logs (CSV) ---")
    csv_output = exporter.export_pipeline_logs(format="csv")
    if csv_output:
        csv_lines = csv_output.strip().split("\n")
        print(f"✓ Exported {len(csv_lines) - 1} records (plus header)")

        # Save to file
        csv_path = export_dir / "all_logs.csv"
        exporter.export_pipeline_logs(format="csv", output_path=str(csv_path))
        print(f"✓ Saved to {csv_path}\n")

    # Example 5: Show file contents
    print("--- Generated Files ---")
    for file in sorted(export_dir.glob("*")):
        size = file.stat().st_size
        print(f"  {file.name} ({size} bytes)")

    print("\n✓ Export examples completed!")
