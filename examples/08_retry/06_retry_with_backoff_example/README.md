# Exponential Backoff Retry Example

## What It Does

This example demonstrates retry with exponential backoff. While the basic delay is fixed, the retry mechanism ensures a pause between attempts, simulating backoff behavior for transient failures.

## Key Concepts

- `retry_delay`: Fixed delay between retry attempts
- Exponential backoff pattern can be implemented with increasing delays
- Retry delays help prevent overwhelming failing services
- Verbose mode logs each retry attempt with timing

## Example

```python
from wpipe import Pipeline

def failing_step(data):
    raise ConnectionError("Network error")

pipeline = Pipeline(
    max_retries=3,
    retry_delay=0.2,
    verbose=True,
)
pipeline.set_steps([(failing_step, "Failing", "v1.0")])
try:
    result = pipeline.run({})
except Exception as e:
    print(f"Failed after retries: {type(e).__name__}")
```

## Flow

```mermaid
graph LR
    A[Attempt 1] --> B{Fail?}
    B -->|Yes| C[Wait 0.2s]
    B -->|No| D[Complete]
    C --> E[Attempt 2]
    E --> F{Fail?}
    F -->|Yes| G[Wait 0.2s]
    F -->|No| D
    G --> H[Attempt 3]
    H --> I{Fail?}
    I -->|Yes| J[Wait 0.2s]
    I -->|No| D
    J --> K[Attempt 4]
    K --> L{Fail?}
    L -->|Yes| M[Fail]
    L -->|No| D
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Failing Step
    P->>S: Attempt 1
    S-->>P: ConnectionError
    Note over P: Wait 0.2s
    P->>S: Attempt 2
    S-->>P: ConnectionError
    Note over P: Wait 0.2s
    P->>S: Attempt 3
    S-->>P: ConnectionError
    Note over P: Wait 0.2s
    P->>S: Attempt 4
    S-->>P: ConnectionError
    P-->>P: Retries exhausted
```

## Retry Logic

```mermaid
graph TB
    START[Start] --> ATTEMPT[Attempt N]
    ATTEMPT --> CHECK{Success?}
    CHECK -->|Yes| SUCCESS[Return Result]
    CHECK -->|No| RETRY_CHECK{Retries left?}
    RETRY_CHECK -->|Yes| WAIT[Wait retry_delay]
    WAIT --> ATTEMPT
    RETRY_CHECK -->|No| FAIL[Fail Pipeline]
```

## Retry States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Attempting: Start execution
    Attempting --> Waiting: Exception raised
    Attempting --> Complete: Success
    Waiting --> Attempting: Delay elapsed
    Attempting --> Exhausted: No retries left
    Complete --> [*]
    Exhausted --> [*]
```

## Process Overview

```mermaid
flowchart LR
    subgraph Configuration
        A1[max_retries=3] --> A2[retry_delay=0.2]
        A2 --> A3[verbose=True]
    end
    subgraph Execution
        B1[Execute] --> B2{Success?}
        B2 -->|No| B3[Decrement retries]
        B2 -->|Yes| B4[Done]
        B3 --> B5{Retries > 0?}
        B5 -->|Yes| B6[Wait delay]
        B5 -->|No| B7[Fail]
        B6 --> B1
    end
    A3 --> B1
```
