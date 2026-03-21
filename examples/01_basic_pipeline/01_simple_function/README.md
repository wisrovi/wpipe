# 01 Simple Function

Sequential function execution in a pipeline.

## What It Does

- Creates a Pipeline instance
- Adds three functions as sequential steps
- Runs pipeline with input data
- Transforms data through each step

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
    participant S1 as multiply_by_two
    participant S2 as add_ten
    participant S3 as square
    
    P->>S1: run({input: 5})
    S1-->>P: {value: 10}
    P->>S2: run({value: 10})
    S2-->>P: {value: 20}
    P->>S3: run({value: 20})
    S3-->>P: {result: 400}
```

```mermaid
graph TB
    subgraph Setup
        A[Input]
        B[Pipeline]
    end
    
    subgraph Execution
        C[multiply_by_two]
        D[add_ten]
        E[square]
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
