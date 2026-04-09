"""
Basic export example.

Demonstrates exporting pipeline execution data to JSON and CSV.
"""

from wpipe import PipelineExporter
import json
from pathlib import Path

# Create sample export directory
export_dir = Path("exports")
export_dir.mkdir(exist_ok=True)

def setup_sample_data():
    """Setup sample execution data."""
    import sqlite3
    
    db_path = "export_example.db"
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create executions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY,
                pipeline_id TEXT,
                step_name TEXT,
                status TEXT,
                execution_time REAL,
                created_at TEXT
            )
        """)
        
        # Insert sample data
        sample_data = [
            ("pipeline_1", "step_1", "completed", 1.23, "2024-03-31 10:00:00"),
            ("pipeline_1", "step_2", "completed", 2.45, "2024-03-31 10:01:00"),
            ("pipeline_1", "step_3", "completed", 0.98, "2024-03-31 10:02:00"),
            ("pipeline_2", "step_1", "completed", 1.56, "2024-03-31 11:00:00"),
            ("pipeline_2", "step_2", "failed", 5.00, "2024-03-31 11:01:00"),
        ]
        
        cursor.executemany("""
            INSERT INTO executions (pipeline_id, step_name, status, execution_time, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, sample_data)
        
        conn.commit()
    
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
    print(f"✓ Exported {len(json.loads(json_output))} records")
    
    # Save to file
    json_path = export_dir / "all_logs.json"
    exporter.export_pipeline_logs(format="json", output_path=str(json_path))
    print(f"✓ Saved to {json_path}\n")
    
    # Example 2: Export logs as CSV
    print("--- Example 2: Export All Logs (CSV) ---")
    csv_output = exporter.export_pipeline_logs(format="csv")
    csv_lines = csv_output.strip().split("\n")
    print(f"✓ Exported {len(csv_lines) - 1} records (plus header)")
    
    # Save to file
    csv_path = export_dir / "all_logs.csv"
    exporter.export_pipeline_logs(format="csv", output_path=str(csv_path))
    print(f"✓ Saved to {csv_path}\n")
    
    # Example 3: Export filtered by pipeline
    print("--- Example 3: Filter by Pipeline ---")
    filtered_json = exporter.export_pipeline_logs(
        pipeline_id="pipeline_1",
        format="json"
    )
    filtered_records = json.loads(filtered_json)
    print(f"✓ Pipeline 1 has {len(filtered_records)} executions")
    
    pipeline_path = export_dir / "pipeline_1_logs.json"
    exporter.export_pipeline_logs(
        pipeline_id="pipeline_1",
        format="json",
        output_path=str(pipeline_path)
    )
    print(f"✓ Saved filtered logs to {pipeline_path}\n")
    
    # Example 4: Export statistics
    print("--- Example 4: Export Statistics ---")
    try:
        stats = exporter.export_statistics(format="json")
        stats_dict = json.loads(stats) if isinstance(stats, str) else stats
        print(f"✓ Statistics exported:")
        for key, value in stats_dict.items():
            print(f"  {key}: {value}")
        
        stats_path = export_dir / "statistics.json"
        exporter.export_statistics(format="json", output_path=str(stats_path))
        print(f"✓ Saved to {stats_path}\n")
    except Exception as e:
        print(f"Note: {e}\n")
    
    # Example 5: Show file contents
    print("--- Generated Files ---")
    for file in sorted(export_dir.glob("*")):
        size = file.stat().st_size
        print(f"  {file.name} ({size} bytes)")
    
    print("\n✓ Export examples completed!")
