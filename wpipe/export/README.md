# Export & Analytics

Export pipeline logs, metrics, and statistics to JSON or CSV formats.

## Features

- **Log export**: Export execution logs with filtering
- **Metrics export**: Export system metrics and statistics
- **Multiple formats**: JSON and CSV export
- **Flexible output**: Return as string or save to file
- **Statistics**: Calculate aggregate performance metrics

## Quick Start

```python
from wpipe import PipelineExporter

# Initialize exporter
exporter = PipelineExporter("pipeline.db")

# Export logs as JSON
json_logs = exporter.export_pipeline_logs(
    pipeline_id="my_pipeline",
    format="json",
    output_path="logs.json"
)

# Export logs as CSV
csv_logs = exporter.export_pipeline_logs(
    format="csv",
    output_path="logs.csv"
)

# Export metrics
metrics = exporter.export_metrics(
    format="json",
    output_path="metrics.json"
)

# Export statistics
stats = exporter.export_statistics(
    pipeline_id="my_pipeline",
    format="json",
    output_path="stats.json"
)
```

## API

### PipelineExporter

#### `__init__(db_path: str)`
Initialize exporter with database path.

#### `export_pipeline_logs(pipeline_id, format, output_path) -> str`
Export pipeline execution logs.

- `pipeline_id`: Optional filter by pipeline
- `format`: "json" or "csv"
- `output_path`: Optional file path to save

#### `export_metrics(pipeline_id, format, output_path) -> str`
Export system metrics data.

#### `export_statistics(pipeline_id, format, output_path) -> str`
Export pipeline statistics and summary.

Returns dictionary with:
- `total_executions`: Total number of executions
- `successful_executions`: Count of successful runs
- `success_rate_percent`: Success percentage
- `average_execution_time_seconds`: Average runtime
- `exported_at`: Export timestamp

## Output Formats

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

- **Analysis**: Data analysis in Excel or Python
- **Reporting**: Generate execution reports
- **Debugging**: Investigate pipeline failures
- **Compliance**: Audit trail for regulations
- **Integration**: Send data to external systems
