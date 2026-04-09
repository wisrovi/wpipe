# Export Examples

Examples demonstrating pipeline data export to JSON and CSV formats.

## Examples

### 01_json
Exporting pipeline data to JSON format.

**Run**: `python 01_json/export_json.py`

**What it shows**:
- Exporting logs as JSON
- Exporting metrics as JSON
- Saving to files
- Pretty formatting

### 02_csv
Exporting pipeline data to CSV format.

**What it shows**:
- Exporting logs as CSV
- Opening in Excel
- Data preparation for analysis

### 03_statistics
Computing and exporting statistics.

**What it shows**:
- Success rate calculation
- Average execution times
- Statistical summaries

### 04_integration
Integrating export with analysis tools.

**What it shows**:
- Pandas integration
- Data analysis examples
- Visualization prep

## Key Concepts

- **Multiple formats**: JSON for APIs, CSV for Excel
- **Flexible output**: Return as string or save to file
- **Filtering**: By pipeline ID
- **Aggregation**: Statistics computation

## Common Patterns

```python
# Export logs as JSON
json_data = exporter.export_pipeline_logs(
    pipeline_id="my_pipeline",
    format="json",
    output_path="logs.json"
)

# Export as CSV
csv_data = exporter.export_pipeline_logs(
    format="csv",
    output_path="logs.csv"
)

# Get statistics
stats = exporter.export_statistics(format="json")
print(f"Success rate: {stats['success_rate_percent']}%")
```

## Output Format

### JSON
```json
[
  {
    "pipeline_id": "my_pipeline",
    "step_name": "step_1",
    "status": "completed",
    "execution_time": 1.23,
    "created_at": "2024-03-31T10:00:00"
  }
]
```

### CSV
```
pipeline_id,step_name,status,execution_time,created_at
my_pipeline,step_1,completed,1.23,2024-03-31T10:00:00
```

## Use Cases

- **Analysis**: Import into Pandas/Excel
- **Reporting**: Generate reports
- **Debugging**: Investigate failures
- **Compliance**: Audit trails
- **Integration**: Send to monitoring systems

## Exported Metrics

- `total_executions`: Total count
- `successful_executions`: Success count
- `success_rate_percent`: Success percentage
- `average_execution_time_seconds`: Avg runtime
- `exported_at`: Timestamp

## See Also

- [Export Documentation](../../wpipe/export/README.md)
- [Phase 1 Features Guide](../../PHASE_1_FEATURES.md)
