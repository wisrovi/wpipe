# 19 Concurrent Workers

Demonstrates multiple workers running concurrently with API tracking.
Each worker should have unique ID and operate independently.

## What it evaluates

- Multiple concurrent pipelines
- Unique worker identification
- Independent execution
- Thread-safe operations

## Flow

```mermaid
graph LR
    A[Worker 1] --> E[Result 1]
    B[Worker 2] --> F[Result 2]
    C[Worker 3] --> G[Result 3]
```

```mermaid
sequenceDiagram
    participant P as Pool
    participant W1 as Worker 1
    participant W2 as Worker 2
    participant W3 as Worker 3
    
    P->>W1: Execute
    P->>W2: Execute
    P->>W3: Execute
    W1-->>P: Result
    W2-->>P: Result
    W3-->>P: Result
```

```mermaid
graph TB
    subgraph Pool
        P[ThreadPool]
    end
    
    subgraph Workers
        W1[Worker 1]
        W2[Worker 2]
        W3[Worker 3]
    end
    
    subgraph Results
        R1[Result 1]
        R2[Result 2]
        R3[Result 3]
    end
    
    P --> W1
    P --> W2
    P --> W3
    W1 --> R1
    W2 --> R2
    W3 --> R3
```

```mermaid
stateDiagram-v2
    [*] --> Submit
    Submit --> Running
    Running --> Complete
    Complete --> [*]
```

```mermaid
flowchart LR
    P([Pool]) --> W1([Worker 1])
    P --> W2([Worker 2])
    P --> W3([Worker 3])
    
    style P fill:#e1f5fe
```
