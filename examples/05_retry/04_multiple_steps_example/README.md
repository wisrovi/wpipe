# Multiple Steps with Retry Example

## What It Does

This example demonstrates retry behavior in a multi-step pipeline. When a step in the middle fails, the pipeline retries that step. If retries are exhausted, the entire pipeline fails without executing subsequent steps.

## Key Concepts

- Steps execute sequentially
- A failed step triggers retries before moving on
- Subsequent steps are skipped if retries fail
- Each step can have independent retry behavior

## Example

```python
from wpipe import Pipeline

def step1(data):
    return {"step1": "done"}

def step2(data):
    raise ConnectionError("Step 2 failed")

def step3(data):
    return {"step3": "done"}

pipeline = Pipeline(max_retries=2, retry_delay=0.1, verbose=True)
pipeline.set_steps([
    (step1, "Step 1", "v1.0"),
    (step2, "Step 2", "v1.0"),
    (step3, "Step 3", "v1.0"),
])
result = pipeline.run({})
```

## Flow

```mermaid
graph LR
    A[Step 1] --> B{Success?}
    B -->|Yes| C[Step 2]
    B -->|No| D[Fail]
    C --> E{Success?}
    E -->|Yes| F[Step 3]
    E -->|No| G[Retry Step 2]
    G --> C
    F --> H[Complete]
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
    Note over P: Wait 0.1s
    P->>S2: Retry 1
    S2-->>P: ConnectionError
    Note over P: Wait 0.1s
    P->>S2: Retry 2
    S2-->>P: ConnectionError
    P-->>P: Pipeline failed
    Note over S3: Step 3 never executed
```

## Retry Logic

```mermaid
graph TB
    START[Pipeline Start] --> STEP1[Execute Step 1]
    STEP1 --> S1_OK{Success?}
    S1_OK -->|No| FAIL[Pipeline Failed]
    S1_OK -->|Yes| STEP2[Execute Step 2]
    STEP2 --> S2_OK{Success?}
    S2_OK -->|No| RETRY[Retry Step 2]
    S2_OK -->|Yes| STEP3[Execute Step 3]
    RETRY --> RETRY_COUNT{Retries left?}
    RETRY_COUNT -->|Yes| STEP2
    RETRY_COUNT -->|No| FAIL
    STEP3 --> SUCCESS[Pipeline Complete]
```

## Step States

```mermaid
stateDiagram-v2
    [*] --> Step1Ready
    Step1Ready --> Step1Running: Execute
    Step1Running --> Step1Success: Completed
    Step1Running --> Step1Failed: Exception
    Step1Success --> Step2Ready
    Step1Failed --> [*]: Pipeline failed
    Step2Ready --> Step2Running: Execute
    Step2Running --> Step2Success: Completed
    Step2Running --> Step2Retrying: Exception
    Step2Retrying --> Step2Running: Retry
    Step2Running --> Step2Failed: Max retries
    Step2Success --> Step3Ready
    Step2Failed --> [*]: Pipeline failed
    Step3Ready --> Step3Running: Execute
    Step3Running --> Step3Success: Completed
    Step3Success --> [*]: Pipeline complete
```

## Process Overview

```mermaid
flowchart LR
    subgraph Pipeline["Pipeline Execution"]
        A1[Step 1] --> A2{OK?}
        A2 -->|Yes| A3[Step 2]
        A2 -->|No| A4[Fail]
        A3 --> A5{OK?}
        A5 -->|Yes| A6[Step 3]
        A5 -->|No| A7[Retry]
        A7 --> A3
    end
    subgraph Result
        A4 --> A8[Error]
        A6 --> A9[Success]
        A7 --> A10[Max retries]
        A10 --> A8
    end
```
