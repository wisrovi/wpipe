# 02 Class-Based Steps

Using classes as pipeline steps with state.

## What It Does

- Creates pipeline with class instances
- Classes maintain state via __call__
- Chains class instances as steps

## Flow

```mermaid
graph LR
    A[Input] --> B[Pipeline]
    B --> C[Register Worker]
    C --> D{Check API}
    D -->|Yes| E[Run with API]
    D -->|No| F[Run Local]
    E --> G[Result]
    F --> G
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant C1 as DoubleValue
    participant C2 as AddFive
    participant C3 as FormatOutput
    
    P->>C1: run({value: 10})
    C1-->>P: {doubled: 20}
    P->>C2: run({doubled: 20})
    C2-->>P: {added: 25}
    P->>C3: run({added: 25})
    C3-->>P: {output: "Result: 25"}
```

```mermaid
graph TB
    subgraph Setup
        A[Input]
        B[Pipeline]
    end
    
    subgraph Execution
        C[DoubleValue]
        D[AddFive]
        E[FormatOutput]
    end
    
    subgraph Result
        F[Output]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
```

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Running
    Running --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    I([Input]) --> P([Process])
    P --> O([Output])
```
