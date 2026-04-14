# Example 12: Performance Comparison

Compare two pipeline executions to identify performance regressions or improvements.

## Comparison Flow

```mermaid
flowchart TD
    A[Run A] --> P1[Pipeline A]
    B[Run B] --> P2[Pipeline B]
    P1 --> C[Compare Metrics]
    P2 --> C
    C --> R[Results]
    
    R --> D{Duration Diff}
    D -->|Positive| I[Improvement]
    D -->|Negative| Rg[Regression]
```

## Comparison Metrics

```mermaid
classDiagram
    class Comparison {
        +str comparison_id
        +str pipeline_a_id
        +str pipeline_b_id
        +dict comparison_data
        +float duration_diff_ms
        +str status_diff
    }
```

## Results Display

```mermaid
pie
    title "Performance Changes"
    "Improved" : 45
    "No Change" : 30
    "Regressed" : 25
```

## Run

```bash
cd examples/10_dashboard/12_performance_comparison
python example.py
```
