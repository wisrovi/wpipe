# Filter Exceptions Example

## What It Does

This example demonstrates selective retry behavior. The pipeline retries only specific exception types (e.g., `ConnectionError`) while immediately failing on other exception types (e.g., `ValueError`) without retrying.

## Key Concepts

- `retry_on_exceptions`: Tuple of exception types to retry on
- Only specified exceptions trigger retry logic
- Other exceptions propagate immediately

## Example

```python
from wpipe import Pipeline

def network_error_step(data):
    raise ConnectionError("Network timeout")

def validation_error_step(data):
    raise ValueError("Invalid input")

# ConnectionError will be retried
pipeline = Pipeline(
    max_retries=2,
    retry_delay=0.1,
    retry_on_exceptions=(ConnectionError,),
    verbose=True,
)
pipeline.set_steps([(network_error_step, "Network Step", "v1.0")])

# ValueError will NOT be retried (no retry_on_exceptions specified)
pipeline2 = Pipeline(
    max_retries=2,
    retry_delay=0.1,
    retry_on_exceptions=(ConnectionError,),
    verbose=True,
)
pipeline2.set_steps([(validation_error_step, "Validation Step", "v1.0")])
```

## Flow

```mermaid
graph LR
    A[Exception Raised] --> B{Is ConnectionError?}
    B -->|Yes| C[Retry]
    B -->|No| D[Fail Immediately]
    C --> E{Retries left?}
    E -->|Yes| A
    E -->|No| F[Fail]
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Network Step
    participant V as Validation Step
    Note over P,S: ConnectionError Path (Retried)
    P->>S: Attempt 1
    S-->>P: ConnectionError
    Note over P: Wait 0.1s
    P->>S: Attempt 2
    S-->>P: ConnectionError
    Note over P: Wait 0.1s
    P->>S: Attempt 3
    S-->>P: ConnectionError
    P-->>P: Fail after retries
    Note over P,V: ValueError Path (Not Retried)
    P->>V: Attempt 1
    V-->>P: ValueError
    P-->>P: Fail immediately (no retry)
```

## Retry Logic

```mermaid
graph TB
    START[Exception Raised] --> CHECK{Exception in retry_on_exceptions?}
    CHECK -->|Yes| RETRY[Retry step]
    CHECK -->|No| FAIL[Fail immediately]
    RETRY --> CHECK_RETRY{Retries left?}
    CHECK_RETRY -->|Yes| START
    CHECK_RETRY -->|No| FAIL
```

## Exception States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Executing: Run step
    Executing --> Retryable: ConnectionError raised
    Executing --> NonRetryable: ValueError raised
    Executing --> Success: No exception
    Retryable --> Retrying: Wait delay
    Retrying --> Executing: Next attempt
    Retryable --> Failed: Max retries reached
    NonRetryable --> [*]: Fail immediately
    Success --> [*]
    Failed --> [*]
```

## Process Overview

```mermaid
flowchart LR
    subgraph Exception Handling
        A1[Exception Occurs] --> A2{Type matches?}
        A2 -->|ConnectionError| A3[Retry]
        A2 -->|ValueError| A4[No Retry]
    end
    subgraph Retry Path
        B1[Retry] --> B2{Retries > 0?}
        B2 -->|Yes| B3[Execute]
        B2 -->|No| B4[Fail]
        B3 --> B5[Exception?]
        B5 --> A1
    end
    subgraph Immediate Fail
        C1[Fail] --> C2[Return Error]
    end
    A3 --> B2
    A4 --> C1
```
