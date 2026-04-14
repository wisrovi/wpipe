# Retry Counter Example

## What It Does

This example demonstrates how to track retry attempts within a step. The `counting_step` uses a global counter to track how many times it has been executed, succeeding only after a specified number of failures.

## Key Concepts

- Global variables can track state across retries
- `verbose=True` shows attempt numbers in logs
- Steps can make decisions based on attempt count
- Retry count includes the initial attempt

## Example

```python
from wpipe import Pipeline

retry_count = 0

def counting_step(data):
    global retry_count
    retry_count += 1
    if retry_count < 3:
        raise ConnectionError(f"Attempt {retry_count}")
    return {"success": True, "attempts": retry_count}

pipeline = Pipeline(
    max_retries=3,
    retry_delay=0.1,
    verbose=True,
)
pipeline.set_steps([(counting_step, "Counting Step", "v1.0")])
result = pipeline.run({})
print(f"Result: {result}")
```

## Flow

```mermaid
graph LR
    A[Attempt 1] --> B{count < 3?}
    B -->|Yes| C[Raise Error]
    B -->|No| D[Return Success]
    C --> E[Attempt 2]
    E --> F{count < 3?}
    F -->|Yes| G[Raise Error]
    F -->|No| D
    G --> H[Attempt 3]
    H --> I{count < 3?}
    I -->|Yes| J[Raise Error]
    I -->|No| D
    J --> K[Final]
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Counting Step
    Note over S: retry_count = 0
    P->>S: Attempt 1
    Note over S: retry_count = 1, 1 < 3
    S-->>P: ConnectionError (Attempt 1)
    Note over P: Wait 0.1s
    P->>S: Attempt 2
    Note over S: retry_count = 2, 2 < 3
    S-->>P: ConnectionError (Attempt 2)
    Note over P: Wait 0.1s
    P->>S: Attempt 3
    Note over S: retry_count = 3, 3 >= 3
    S-->>P: {"success": True, "attempts": 3}
    P-->>P: Pipeline complete
```

## Retry Logic

```mermaid
graph TB
    START[Execute Step] --> INCREMENT[retry_count += 1]
    INCREMENT --> CHECK{retry_count < 3?}
    CHECK -->|Yes| FAIL[Raise ConnectionError]
    CHECK -->|No| SUCCESS[Return Result]
    FAIL --> RETRY[Wait & Retry]
    RETRY --> START
```

## Counter States

```mermaid
stateDiagram-v2
    [*] --> Initial
    Initial --> Counting: retry_count = 0
    Counting --> Attempting: Execute step
    Attempting --> Failing: retry_count < 3
    Attempting --> Succeeded: retry_count >= 3
    Failing --> Waiting: Wait delay
    Waiting --> Counting: Increment
    Succeeded --> [*]
```

## Process Overview

```mermaid
flowchart LR
    subgraph Tracking["Retry Tracking"]
        A1[Initialize retry_count=0] --> A2[Set max_retries=3]
        A2 --> A3[retry_delay=0.1]
    end
    subgraph Execution["Execution Loop"]
        B1[Execute step] --> B2[retry_count++]
        B2 --> B3{retry_count < 3?}
        B3 -->|Yes| B4[Raise Error]
        B3 -->|No| B5[Return Success]
        B4 --> B6[Wait & Retry]
        B6 --> B1
    end
    A3 --> B1
```
