# Example 04: Basic Tracking

Simple example demonstrating core pipeline tracking functionality.

## Pipeline Flow

```mermaid
graph LR
    A[Generate Numbers] --> B[Double Values]
    B --> C[Calculate Sum]
    C --> D[Complete]
    
    A -.-> T[Tracker]
    B -.-> T
    C -.-> T
    T --> DB[(SQLite)]
```

## Execution Steps

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant T as Tracker
    participant DB as SQLite
    
    P->>T: start_pipeline()
    T->>DB: INSERT pipeline
    P->>T: start_step("generate_numbers")
    T->>DB: INSERT step
    P->>T: complete_step()
    T->>DB: UPDATE step
    P->>T: start_step("double_values")
    T->>DB: INSERT step
    P->>T: complete_step()
    T->>DB: UPDATE step
    P->>T: complete_pipeline()
    T->>DB: UPDATE pipeline
```

## Key Tracking Data

| Data Type | Stored |
|-----------|--------|
| Pipeline ID | ✅ Unique matrícula |
| Status | ✅ completed/error/running |
| Duration | ✅ milliseconds |
| Input Data | ✅ JSON |
| Output Data | ✅ JSON |
| Timestamps | ✅ started/completed |

## Run

```bash
cd examples/10_dashboard/04_basic_tracking
python example.py
```
