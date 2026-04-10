# Basic Retry Example

## What It Does

This example demonstrates the simplest retry behavior in wpipe. When a step fails, the pipeline automatically retries it up to a specified number of attempts with a configurable delay between retries.

## Key Concepts

- `max_retries`: Maximum number of retry attempts
- `retry_delay`: Time in seconds to wait between retries
- `verbose`: Enables detailed logging of retry attempts

## Example

```python
from wpipe import Pipeline

def unreliable_step(data):
    raise ConnectionError("Network error!")

pipeline = Pipeline(max_retries=3, retry_delay=0.1, verbose=True)
pipeline.set_steps([(unreliable_step, "Unreliable Step", "v1.0")])
result = pipeline.run({})
```

## Flow

```mermaid
graph LR
    A[Start] --> B[Execute Step]
    B --> C{Success?}
    C -->|Yes| D[Complete]
    C -->|No| E[Retry?]
    E -->|Yes| B
    E -->|No| F[Fail]
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Step
    P->>S: Attempt 1
    S-->>P: ConnectionError
    Note over P: Wait 0.1s
    P->>S: Attempt 2
    S-->>P: ConnectionError
    Note over P: Wait 0.1s
    P->>S: Attempt 3
    S-->>P: ConnectionError
    Note over P: Retries exhausted
    P-->>P: Raise Exception
```

## Retry Logic

```mermaid
graph TB
    START[Start] --> CHECK{Attempts < max_retries}
    CHECK -->|Yes| EXECUTE[Execute Step]
    CHECK -->|No| FAIL[Fail Pipeline]
    EXECUTE -->|Success| SUCCESS[Return Result]
    EXECUTE -->|Failure| WAIT[Wait delay]
    WAIT --> INCREMENT[Increment attempt]
    INCREMENT --> CHECK
```

## Retry States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Executing: Run pipeline
    Executing --> Waiting: Exception raised
    Executing --> Success: Step completed
    Waiting --> Executing: Retry delay elapsed
    Executing --> Failed: Max retries reached
    Success --> [*]
    Failed --> [*]
```

## Process Overview

```mermaid
flowchart LR
    subgraph Setup["Pipeline Setup"]
        direction TB
        A1[Create Pipeline] --> A2[Set max_retries]
        A2 --> A3[Set retry_delay]
        A3 --> A4[Add Steps]
    end
    subgraph Execution["Execution Flow"]
        direction TB
        B1[Run Pipeline] --> B2{Step Fails?}
        B2 -->|No| B3[Next Step]
        B2 -->|Yes| B4{Retries Left?}
        B4 -->|Yes| B5[Wait & Retry]
        B4 -->|No| B6[Fail]
        B5 --> B2
        B3 --> B7[Complete]
    end
    A4 --> B1
```
