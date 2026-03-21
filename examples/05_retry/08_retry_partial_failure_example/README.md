# Partial Pipeline Failure Example

## What It Does

This example shows retry behavior when some steps in a multi-step pipeline fail while others succeed. The pipeline stops execution at the first failing step and retries only that step.

## Key Concepts

- Steps execute sequentially
- A failure stops subsequent steps temporarily
- Only the failed step is retried
- Successful steps do not re-execute after retry

## Example

```python
from wpipe import Pipeline

def step1(data):
    return {"step1": "done"}

def step2(data):
    raise ConnectionError("Network error")

def step3(data):
    return {"step3": "done"}

pipeline = Pipeline(
    max_retries=2,
    retry_delay=0.1,
    verbose=True,
)
pipeline.set_steps([
    (step1, "Step 1", "v1.0"),
    (step2, "Step 2", "v1.0"),
    (step3, "Step 3", "v1.0"),
])
try:
    result = pipeline.run({})
except Exception as e:
    print(f"Pipeline failed: {type(e).__name__}")
```

## Flow

```mermaid
graph LR
    A[Step 1] --> A1{OK}
    A1 -->|Yes| B[Step 2]
    A1 -->|No| Z[Fail]
    B --> B1{OK}
    B1 -->|Yes| C[Step 3]
    B1 -->|No| B2[Retry Step 2]
    B2 --> B1
    C --> C1{OK}
    C1 -->|Yes| D[Complete]
    C1 -->|No| Z
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S1 as Step 1
    participant S2 as Step 2
    participant S3 as Step 3
    P->>S1: Execute
    S1-->>P: {"step1": "done"}
    P->>S2: Execute
    S2-->>P: ConnectionError
    Note over P: Retrying Step 2...
    P->>S2: Retry 1
    S2-->>P: ConnectionError
    Note over P: Retrying Step 2...
    P->>S2: Retry 2
    S2-->>P: ConnectionError
    Note over P: Max retries reached
    P-->>P: Pipeline failed
    Note over S3: Step 3 never executed
```

## Retry Logic

```mermaid
graph TB
    START[Pipeline Start] --> S1[Step 1]
    S1 --> S1_OK{Success?}
    S1_OK -->|No| FAIL[Fail Pipeline]
    S1_OK -->|Yes| S2[Step 2]
    S2 --> S2_OK{Success?}
    S2_OK -->|No| RETRY[Retry Step 2]
    S2_OK -->|Yes| S3[Step 3]
    RETRY --> RETRY_COUNT{Retries left?}
    RETRY_COUNT -->|Yes| S2
    RETRY_COUNT -->|No| FAIL
    S3 --> S3_OK{Success?}
    S3_OK -->|Yes| SUCCESS[Complete]
    S3_OK -->|No| FAIL
```

## Partial Failure States

```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> Step1Ready
    Step1Ready --> Step1Running: Execute
    Step1Running --> Step1Success: OK
    Step1Running --> Step1Failed: Error
    Step1Success --> Step2Ready
    Step1Failed --> [*]: Pipeline failed
    Step2Ready --> Step2Running: Execute
    Step2Running --> Step2Success: OK
    Step2Running --> Step2Retrying: Error
    Step2Retrying --> Step2Running: Retry
    Step2Running --> Step2Failed: No retries
    Step2Success --> Step3Ready
    Step2Failed --> [*]: Pipeline failed
    Step3Ready --> Step3Running: Execute
    Step3Running --> Step3Success: OK
    Step3Running --> Step3Failed: Error
    Step3Success --> [*]: Pipeline complete
    Step3Failed --> [*]: Pipeline failed
```

## Process Overview

```mermaid
flowchart LR
    subgraph Pipeline["Pipeline Flow"]
        A1[Step 1] --> A2{Success?}
        A2 -->|Yes| A3[Step 2]
        A2 -->|No| A4[Fail]
        A3 --> A5{Success?}
        A5 -->|Yes| A6[Step 3]
        A5 -->|No| A7[Retry Step 2]
        A7 --> A3
        A6 --> A8{Success?}
        A8 -->|Yes| A9[Complete]
        A8 -->|No| A4
    end
```
