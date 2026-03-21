# No Retry Example

## What It Does

This example demonstrates the default behavior when `max_retries` is not configured. Without explicit retry settings, the pipeline fails immediately on the first exception without any retry attempts.

## Key Concepts

- Default `max_retries=0` means no retries
- Pipeline fails immediately on first exception
- `retry_delay` has no effect without retries
- Useful for testing or non-critical operations

## Example

```python
from wpipe import Pipeline

def failing_step(data):
    raise ConnectionError("Network error")

pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (failing_step, "Failing Step", "v1.0"),
])
try:
    result = pipeline.run({})
except Exception as e:
    print(f"Failed without retry: {type(e).__name__}")
```

## Flow

```mermaid
graph LR
    A[Execute Step] --> B{Success?}
    B -->|Yes| C[Complete]
    B -->|No| D[Fail Immediately]
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Failing Step
    P->>S: Execute
    S-->>P: ConnectionError
    Note over P: No retries configured
    P-->>P: Fail immediately
    Note over P: Pipeline terminated
```

## Retry Logic

```mermaid
graph TB
    START[Execute Step] --> CHECK{Success?}
    CHECK -->|Yes| SUCCESS[Return Result]
    CHECK -->|No| FAIL[Fail Immediately]
    Note over FAIL: max_retries=0 by default
```

## States Without Retry

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Executing: Run pipeline
    Executing --> Success: No exception
    Executing --> Failed: Exception raised
    Success --> [*]
    Failed --> [*]
```

## Process Overview

```mermaid
flowchart LR
    subgraph Setup
        A1[Create Pipeline] --> A2[No max_retries set]
        A2 --> A3[max_retries = 0 by default]
    end
    subgraph Execution
        B1[Execute step] --> B2{Exception?}
        B2 -->|No| B3[Success]
        B2 -->|Yes| B4[Fail immediately]
    end
    A3 --> B1
```
