# Success After Retries Example

## What It Does

This example shows how a step can fail initially but succeed after several retry attempts. The `FlakyStep` class tracks the number of attempts and only succeeds after a configurable number of failures.

## Key Concepts

- Steps can be classes with state (callable objects)
- Retry mechanism allows transient failures to be recovered
- Successful completion returns the accumulated result

## Example

```python
from wpipe import Pipeline

class FlakyStep:
    def __init__(self, fail_count=2):
        self.attempts = 0
        self.fail_count = fail_count

    def __call__(self, data):
        self.attempts += 1
        if self.attempts <= self.fail_count:
            raise ConnectionError(f"Attempt {self.attempts} failed")
        return {"success": True, "attempts": self.attempts}

pipeline = Pipeline(max_retries=3, retry_delay=0.1, verbose=True)
pipeline.set_steps([(FlakyStep(fail_count=2), "Flaky Step", "v1.0")])
result = pipeline.run({})
```

## Flow

```mermaid
graph LR
    A[Start] --> B[Attempt 1]
    B --> C{Fail 1}
    C -->|Yes| D[Wait & Retry]
    D --> E[Attempt 2]
    E --> F{Fail 2}
    F -->|Yes| G[Wait & Retry]
    G --> H[Attempt 3]
    H --> I[Success]
    I --> J[Complete]
```

## Attempt Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as FlakyStep
    P->>S: Attempt 1
    S-->>P: ConnectionError (fail_count=2)
    Note over P: Wait 0.1s
    P->>S: Attempt 2
    S-->>P: ConnectionError (fail_count=2)
    Note over P: Wait 0.1s
    P->>S: Attempt 3
    S-->>P: {"success": True, "attempts": 3}
    P-->>P: Pipeline complete
```

## Retry Logic

```mermaid
graph TB
    START[Start] --> INIT[Initialize FlakyStep]
    INIT --> CHECK{attempts < fail_count}
    CHECK -->|Yes| FAIL[Raise ConnectionError]
    CHECK -->|No| SUCCESS[Return success result]
    FAIL --> WAIT[Wait retry_delay]
    WAIT --> INCREMENT[attempts += 1]
    INCREMENT --> CHECK
```

## Retry States

```mermaid
stateDiagram-v2
    [*] --> Initial
    Initial --> Ready: Initialize
    Ready --> Failing: Call step
    Failing --> Retrying: attempts < fail_count
    Retrying --> Failing: Next attempt
    Failing --> Succeeded: attempts >= fail_count
    Succeeded --> [*]
```

## Process Overview

```mermaid
flowchart LR
    subgraph Initialization
        A1[Create FlakyStep] --> A2[Set fail_count=2]
        A2 --> A3[Create Pipeline]
    end
    subgraph Retry Loop
        B1[Call step] --> B2{attempts < 2?}
        B2 -->|Yes| B3[Raise Error]
        B2 -->|No| B4[Return Result]
        B3 --> B5[Wait & Increment]
        B5 --> B1
    end
    A3 --> B1
```
