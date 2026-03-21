# Custom Exception Retry Example

## What It Does

This example demonstrates how to configure the pipeline to retry on custom exception types. Instead of built-in exceptions, you can define your own exception classes and specify them for retry behavior.

## Key Concepts

- Custom exception classes inherit from `Exception`
- `retry_on_exceptions` accepts any exception type tuple
- Custom exceptions can carry domain-specific error information
- Retry logic works identically to built-in exceptions

## Example

```python
from wpipe import Pipeline

class CustomError(Exception):
    pass

def failing_step(data):
    raise CustomError("Custom error")

pipeline = Pipeline(
    max_retries=2,
    retry_delay=0.1,
    retry_on_exceptions=(CustomError,),
    verbose=True,
)
pipeline.set_steps([(failing_step, "Failing", "v1.0")])
try:
    result = pipeline.run({})
except CustomError as e:
    print(f"Custom error caught: {e}")
```

## Flow

```mermaid
graph LR
    A[Execute Step] --> B{Exception?}
    B -->|No| C[Success]
    B --> D{CustomError?}
    D -->|Yes| E[Retry]
    D -->|No| F[Fail]
    E --> G{Retries left?}
    G -->|Yes| A
    G -->|No| F
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Custom Step
    P->>S: Attempt 1
    S-->>P: CustomError("Custom error")
    Note over P: Wait 0.1s
    P->>S: Attempt 2
    S-->>P: CustomError("Custom error")
    Note over P: Wait 0.1s
    P->>S: Attempt 3
    S-->>P: CustomError("Custom error")
    P-->>P: Retries exhausted
    P-->>P: Raise CustomError
```

## Retry Logic

```mermaid
graph TB
    START[Execute Step] --> CHECK{Exception Type}
    CHECK --> CUSTOM{CustomError?}
    CHECK --> OTHER{Other Exception}
    CUSTOM --> RETRY[Retry Step]
    OTHER --> FAIL[Fail Immediately]
    RETRY --> COUNT{Remaining retries?}
    COUNT -->|Yes| START
    COUNT -->|No| FAIL
```

## Custom Exception States

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Executing: Run
    Executing --> CustomRetryable: CustomError raised
    Executing --> NonRetryable: Other error
    Executing --> Success: No exception
    CustomRetryable --> Retrying: Wait delay
    Retrying --> Executing: Next attempt
    CustomRetryable --> CustomFailed: No retries left
    Success --> [*]
    NonRetryable --> [*]
    CustomFailed --> [*]
```

## Process Overview

```mermaid
flowchart LR
    subgraph CustomException
        A1[Define CustomError] --> A2[Extend Exception]
        A2 --> A3[Configure retry_on_exceptions]
    end
    subgraph Execution
        B1[Execute step] --> B2{Exception?}
        B2 -->|No| B3[Success]
        B2 --> B4{Type matches?}
        B4 -->|CustomError| B5[Retry]
        B4 -->|Other| B6[Fail]
        B5 --> B7{Remaining?}
        B7 -->|Yes| B1
        B7 -->|No| B6
    end
    A3 --> B1
```
