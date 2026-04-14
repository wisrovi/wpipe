# Example 01: Pipeline with SQLite

This example demonstrates how to create a pipeline that automatically stores execution data in SQLite, which can then be viewed in the dashboard.

## What it does

The pipeline performs data processing tasks and automatically tracks:
- Pipeline execution status
- Input and output data
- Step-by-step execution details
- Timestamps and duration

## Pipeline Flow

```mermaid
graph LR
    A[Fetch Data] --> B[Process Records]
    B --> C[Calculate Stats]
    C --> D[Complete]
    
    subgraph SQLite Storage
        S[(wpipe_dashboard.db)]
    end
    
    A -.-> S
    B -.-> S
    C -.-> S
```

## Execution Timeline

```mermaid
gantt
    title Pipeline Execution Timeline
    dateFormat X
    axisFormat %s
    
    Fetch Data       :0, 5
    Process Records  :5, 15
    Calculate Stats  :15, 20
```

## Architecture

```mermaid
flowchart TB
    subgraph Pipeline
        P[Pipeline] --> S1[Step 1: fetch_data]
        S1 --> S2[Step 2: process_records]
        S2 --> S3[Step 3: calculate_stats]
    end
    
    subgraph Tracking
        P --> T[PipelineTracker]
        T --> DB[(SQLite DB)]
    end
    
    subgraph Dashboard
        DB --> D[Dashboard UI]
    end
```

## Run the Example

```bash
cd examples/10_dashboard/01_pipeline_with_sqlite
python example.py
```

## View Dashboard

```bash
cd ..
python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open
```

## Key Features Demonstrated

- ✅ Automatic SQLite tracking
- ✅ Input/output data capture
- ✅ Step-level metrics
- ✅ Dashboard visualization
