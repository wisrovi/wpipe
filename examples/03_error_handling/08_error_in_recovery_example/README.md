# Recovery After Error Example

Shows recovery mechanism after step failure.

## What It Does

Demonstrates how to recover from errors and access
error information in subsequent pipeline steps.

## Flow

```mermaid
graph LR
    A[Failing Step] -->|Error| B[Recovery Step]
    B --> C[Continue]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant F as Failing
    participant R as Recovery
    
    P->>F: Run
    F-->>P: RuntimeError
    P->>R: Continue
    R-->>P: Recovered
```

```mermaid
graph TB
    subgraph Flow
        A[Failing Step]
        B[Recovery Step]
        C[Continue]
    end
    
    A -->|Error| B
    B --> C
```

```mermaid
stateDiagram-v2
    [*] --> RunStep
    RunStep --> Error
    Error --> Recover
    Recover --> Continue
    Continue --> [*]
```

```mermaid
flowchart LR
    F([Failing]) -->|Error| R([Recovery])
    R --> C([Continue])
```
