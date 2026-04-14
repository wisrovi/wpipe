# Continue After Error Example

Shows that pipeline continues even when errors occur.

## What It Does

Demonstrates the finally block behavior - cleanup steps
always execute regardless of errors in previous steps.

## Flow

```mermaid
graph LR
    A[Step 1] --> B[Failing]
    B -->|Error| C[Final Step]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S as Step 1
    participant F as Failing
    participant Fi as Final
    
    P->>S: Run
    S-->>P: Success
    P->>F: Run
    F-->>P: Error
    P->>Fi: Always Run
```

```mermaid
graph TB
    subgraph Execution
        A[Step 1]
        B[Failing Step]
        C[Final Step]
    end
    
    A --> B
    B -->|Error| C
```

```mermaid
stateDiagram-v2
    [*] --> Step1
    Step1 --> Failing
    Failing --> Error
    Error --> Final
    Final --> [*]
```

```mermaid
flowchart LR
    S1([Step 1]) --> F([Failing])
    F -->|Error| Fi([Final])
    Fi --> D([Done])
```
