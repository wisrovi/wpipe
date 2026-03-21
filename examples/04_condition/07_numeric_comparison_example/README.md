# Numeric Comparisons

Demonstrates various numeric comparison operators in conditions.

## What It Does

This example shows how to use numeric comparison operators like `>=`, `>`, `<`, `<=`, `==`, and `!=` in condition expressions. The pipeline evaluates `value >= 70` and routes to different steps based on whether the value meets the threshold.

## Flow

```mermaid
graph LR
    A[Get Value] --> B{value >= 70?}
    B -->|True| C[Greater or Equal]
    B -->|False| D[Less]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant G as Get Value
    participant C as Condition
    participant S as Step GT/LT

    P->>G: Run get_value
    G-->>P: {value: 75}
    P->>C: Evaluate value >= 70
    Note over C: 75 >= 70 = True
    C-->>P: True
    P->>S: Run step_gt
    S-->>P: {result: 'greater'}
```

```mermaid
graph TB
    subgraph Input
        A1[get_value<br/>returns: value = 75]
    end
    subgraph Comparison
        C1[Condition<br/>value >= 70]
        V1[75 >= 70 = True]
    end
    subgraph Branches
        T1[step_gt<br/>result: greater]
        F1[step_lt<br/>result: less]
    end
    A1 --> C1
    C1 --> V1
    V1 -->|True| T1
    V1 -->|False| F1
```

```mermaid
stateDiagram-v2
    [*] --> GetValue
    GetValue --> CompareValue: value = 75
    CompareValue --> GreaterOrEqual: value >= 70
    CompareValue --> LessThan: value < 70
    GreaterOrEqual --> [*]: {result: 'greater'}
    LessThan --> [*]: {result: 'less'}
```

```mermaid
flowchart LR
    subgraph Test Values
        V1["value = 75"]
        V2["value = 65"]
        V3["value = 70"]
    end
    subgraph Results
        R1["result: greater"]
        R2["result: less"]
    end
    V1 --> C{value >= 70?}
    V2 --> C
    V3 --> C
    C -->|True| R1
    C -->|False| R2
```
