# Example 05: Error Handling

Demonstrates how errors are tracked, stored, and displayed in the dashboard.

## Error Tracking Flow

```mermaid
flowchart TD
    A[Pipeline] --> B{Execute Step}
    B -->|Success| C[Next Step]
    B -->|Error| D[Capture Error]
    D --> E[Store in DB]
    E --> F[Mark Pipeline Failed]
    F --> G[Dashboard Error Panel]
    
    D --> ET[Error Type]
    D --> EM[Error Message]
    D --> ES[Error Step]
```

## Error Data Captured

```mermaid
classDiagram
    class ErrorData {
        +str error_message
        +str error_step
        +str error_traceback
        +str status
        +timestamp fired_at
    }
```

## Dashboard Error Display

```mermaid
graph LR
    DB[(SQLite)] --> API[/api/pipelines/{id}\]
    API --> D[Dashboard]
    D --> EP[Error Panel]
    D --> EL[Error List]
    D --> EA[Alert Badge]
```

## What Gets Tracked

- ✅ Error message
- ✅ Error step name
- ✅ Full traceback
- ✅ Pipeline status
- ✅ Timestamp

## Run

```bash
cd examples/10_dashboard/05_error_handling
python example.py
```
