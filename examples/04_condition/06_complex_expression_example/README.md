# Complex Expression

Demonstrates using complex boolean expressions with multiple conditions.

## What It Does

This example shows how to create conditions that combine multiple comparisons using boolean operators like `and`. The expression `x > 5 and y > 10 and z < 10` evaluates all three conditions and only returns true if all are satisfied.

## Flow

```mermaid
graph LR
    A[Get Data] --> B{x>5 and y>10 and z<10?}
    B -->|True| C[Step A]
    B -->|False| D[Step B]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant G as Get Data
    participant C as Condition
    participant S as Step A/B

    P->>G: Run get_data
    G-->>P: {x: 10, y: 20, z: 5}
    P->>C: Evaluate x>5 and y>10 and z<10
    Note over C: 10>5=True, 20>10=True, 5<10=True
    C-->>P: True (all conditions met)
    P->>S: Run step_a
    S-->>P: {branch: 'A'}
```

```mermaid
graph TB
    subgraph Data
        A1[get_data<br/>returns: x=10, y=20, z=5]
    end
    subgraph Expression Components
        E1[x > 5<br/>10 > 5 = True]
        E2[y > 10<br/>20 > 10 = True]
        E3[z < 10<br/>5 < 10 = True]
    end
    subgraph Condition
        C1[AND]
    end
    subgraph Result
        R1[step_a<br/>branch: A]
        R2[step_b<br/>branch: B]
    end
    A1 --> E1
    A1 --> E2
    A1 --> E3
    E1 --> C1
    E2 --> C1
    E3 --> C1
    C1 -->|True| R1
    C1 -->|False| R2
```

```Mermaid
stateDiagram-v2
    [*] --> GetData
    GetData --> EvaluateAll: data received
    EvaluateAll --> CheckX: x > 5?
    CheckX --> CheckY: True
    CheckX --> Fail: False
    CheckY --> CheckZ: y > 10?
    CheckY --> Fail: False
    CheckZ --> StepA: z < 10 = True
    CheckZ --> Fail: z < 10 = False
    StepA --> [*]
    Fail --> StepB
    StepB --> [*]
```

```mermaid
flowchart LR
    subgraph Inputs
        I["x=10, y=20, z=5"]
    end
    subgraph Checks
        C1[x > 5?]
        C2[y > 10?]
        C3[z < 10?]
    end
    subgraph Outputs
        O1["branch: A"]
        O2["branch: B"]
    end
    I --> C1 --> C2 --> C3
    C3 -->|True| O1
    C3 -->|False| O2
```
