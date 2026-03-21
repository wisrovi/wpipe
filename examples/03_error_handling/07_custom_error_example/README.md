# Custom Error Handler Example

Shows implementing custom error handling logic.

## What It Does

Demonstrates how to handle errors in a pipeline step
and access error information in subsequent steps.

## Flow

```mermaid
graph LR
    A[Step with Error] -->|Fail| B[Error Handler]
    B --> C[Handle]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Step
    participant H as Handler
    
    P->>S: Run with fail=True
    S-->>P: ValueError
    P->>H: Pass Error
    H-->>P: Handled
```

```mermaid
graph TB
    subgraph Steps
        A[Step]
        B[Error Handler]
    end
    
    A -->|Error| B
    B --> C[Continue]
```

```mermaid
stateDiagram-v2
    [*] --> RunStep
    RunStep --> Error : ValueError
    RunStep --> Success : OK
    Error --> Handle
    Handle --> [*]
    Success --> [*]
```

```mermaid
flowchart LR
    S([Step]) -->|Success| C([Continue])
    S -->|Error| H([Handler])
```
