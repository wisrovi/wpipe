# Example 10: Alert System

Configure alert thresholds and get notified when metrics exceed limits.

## Alert Flow

```mermaid
flowchart TD
    P[Pipeline] --> M[Measure Metrics]
    M --> C{Threshold Exceeded?}
    C -->|Yes| F[Fire Alert]
    C -->|No| E[Continue]
    F --> D[Store Alert]
    D --> N[Notify]
    D --> A[Dashboard Badge]
```

## Alert Configuration

```mermaid
classDiagram
    class AlertConfig {
        +str name
        +str metric
        +str condition  # >, <, ==
        +float value
        +str severity   # info, warning, critical
        +str message
    }
```

## Available Metrics

| Metric | Description |
|--------|-------------|
| pipeline_duration_ms | Total execution time |
| step_duration_ms | Individual step time |
| retry_count | Number of retries |
| error_count | Errors encountered |

## Severity Levels

```mermaid
pie
    title Alert Distribution
    "Info" : 20
    "Warning" : 50
    "Critical" : 30
```

## Run

```bash
cd examples/10_dashboard/10_alerts
python example.py
```
