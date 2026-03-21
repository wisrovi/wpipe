# Basic Conditional Branch

Demonstrates the simplest form of conditional branching in a pipeline using the `Condition` class.

## What It Does

This example shows how to create a pipeline that evaluates a condition expression and routes execution to different branches based on the result. The condition checks if `value > 50` and executes either `step_a` or `step_b` accordingly.

## Flow

```mermaid
graph LR
    A[Fetch Data] --> B{value > 50?}
    B -->|True| C[Step A]
    B -->|False| D[Step B]
    C --> E[Final Step]
    D --> E
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant F as Fetch Data
    participant C as Condition
    participant S as Step A/B
    participant L as Final Step

    P->>F: Run fetch_data
    F-->>P: {value: 80}
    P->>C: Evaluate value > 50
    C-->>P: True (value=80)
    P->>S: Run step_a
    S-->>P: {branch: A, result: 160}
    P->>L: Run final_step
    L-->>P: {final: "Processed by A"}
```

```mermaid
graph TB
    subgraph Pipeline
        A1[fetch_data<br/>returns: value, type]
        A2[Condition<br/>expression: value > 50]
        A3[step_a<br/>branch: A]
        A4[step_b<br/>branch: B]
        A5[final_step<br/>final message]
    end
    A1 --> A2
    A2 -->|True| A3
    A2 -->|False| A4
    A3 --> A5
    A4 --> A5
```

```mermaid
stateDiagram-v2
    [*] --> FetchData
    FetchData --> Condition: data={value: 80}
    Condition --> StepA: value > 50 = True
    Condition --> StepB: value > 50 = False
    StepA --> FinalStep
    StepB --> FinalStep
    FinalStep --> [*]
```

```mermaid
flowchart LR
    subgraph Inputs
        V80["value = 80"]
        V30["value = 30"]
    end
    subgraph Outputs
        R1["Result: branch=A"]
        R2["Result: branch=B"]
    end
    V80 --> C1{value > 50?}
    V30 --> C2{value > 50?}
    C1 -->|True| R1
    C2 -->|False| R2
```
