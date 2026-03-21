# Multiple Steps in Branch

Demonstrates running multiple steps within each conditional branch.

## What It Does

This example shows how to define multiple steps in both the true and false branches of a condition. When a branch is selected, all steps within that branch execute sequentially, accumulating their results in the pipeline state.

## Flow

```mermaid
graph LR
    A[Get Value] --> B{value > 0?}
    B -->|True| C[Step 1] --> D[Step 2]
    B -->|False| E[Step 3] --> F[Step 4]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant G as Get Value
    participant C as Condition
    participant S1 as Step 1
    participant S2 as Step 2

    P->>G: Run get_value
    G-->>P: {value: 10}
    P->>C: Evaluate value > 0
    C-->>P: True
    P->>S1: Run step1
    S1-->>P: {step1: 'done'}
    P->>S2: Run step2
    S2-->>P: {step2: 'done'}
```

```mermaid
graph TB
    subgraph Pipeline
        A1[get_value<br/>returns: value]
        A2[Condition<br/>value > 0]
        A3[step1<br/>step1: done]
        A4[step2<br/>step2: done]
        A5[step3<br/>step3: done]
        A6[step4<br/>step4: done]
    end
    A1 --> A2
    A2 -->|True| A3
    A3 --> A4
    A2 -->|False| A5
    A5 --> A6
```

```mermaid
stateDiagram-v2
    [*] --> GetValue
    GetValue --> EvaluateCondition: value = 10
    EvaluateCondition --> ExecuteTrueBranch: value > 0 = True
    EvaluateCondition --> ExecuteFalseBranch: value <= 0
    ExecuteTrueBranch --> Step1
    Step1 --> Step2
    Step2 --> [*]
    ExecuteFalseBranch --> Step3
    Step3 --> Step4
    Step4 --> [*]
```

```mermaid
flowchart LR
    subgraph Input
        I["value = 10"]
    end
    subgraph True Branch
        T1[Step 1] --> T2[Step 2]
    end
    subgraph False Branch
        F1[Step 3] --> F2[Step 4]
    end
    I --> C{value > 0?}
    C -->|True| T1
    C -->|False| F1
```
