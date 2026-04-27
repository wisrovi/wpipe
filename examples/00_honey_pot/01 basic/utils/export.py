import json
import os
from pathlib import Path

from wpipe import PipelineExporter

db_path = "output/wpipe_dashboard.db"


def export_logs_to_json(exporter: PipelineExporter, output_path: str) -> None:
    """Export logs to JSON format."""
    print("\n" + "=" * 70)
    print("JSON EXPORT")
    print("=" * 70)

    try:
        json_data = exporter.export_pipeline_logs(export_format="json")

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
        csv_data = exporter.export_pipeline_logs(export_format="csv")

        if csv_data:
            # Fix path for CSV
            csv_path = output_path.replace(".json", ".csv")
            Path(csv_path).write_text(csv_data)
            print(f"✓ Exported to: {csv_path}")

            lines = csv_data.split("\n")
            print(f"  File size: {len(csv_data)} bytes")
            print(f"  Records: {len(lines) - 1}")  # Exclude header
            print(f"  Columns: {len(lines[0].split(','))}")
            print(f"  Header: {lines[0]}")
        else:
            print("ℹ No execution data to export yet")
    except Exception as e:
        print(f"ℹ CSV export: {e}")


def exporter_data():
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
    output_dir = "output/export_output"

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Initialize exporter
    exporter = PipelineExporter(db_path)

    print("=" * 70)
    print("EXPORTING DATA")
    print("=" * 70 + "\n")

    # Export statistics
    print("1. Exporting statistics to JSON...")
    stats_path = os.path.join(output_dir, "pipeline_statistics.json")
    try:
        exporter.export_statistics(export_format="json", output_path=stats_path)
        print(f"   ✓ Saved to: {stats_path}\n")

        with open(stats_path) as f:
            stats = json.load(f)
            print("   Statistics:")
            for key, value in stats.items():
                print(f"     - {key}: {value}")
    except Exception as e:
        print(f"   ⚠ Stats export note: {e}\n")

    # Export logs
    print("\n2. Exporting pipeline logs...")
    logs_json_path = os.path.join(output_dir, "pipeline_logs.json")
    export_logs_to_json(exporter, logs_json_path)
    export_logs_to_csv(exporter, logs_json_path)

    # Show available files
    print("\n" + "=" * 70)
    print("AVAILABLE EXPORTS")
    print("=" * 70 + "\n")

    if Path(output_dir).exists():
        for file in Path(output_dir).glob("*"):
            size = file.stat().st_size
            print(f"✓ {file.name} ({size} bytes)")
    else:
        print("Output directory not yet created")

    print("\n✓ Export demo completed!")
