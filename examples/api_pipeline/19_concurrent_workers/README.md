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
    participant Pool
    participant W1[Worker 1]
    participant W2[Worker 2]
    participant W3[Worker 3]
    
    Pool->>W1: Execute concurrently
    Pool->>W2: Execute concurrently
    Pool->>W3: Execute concurrently
    W1-->>Pool: Result 1
    W2-->>Pool: Result 2
    W3-->>Pool: Result 3
```

```mermaid
graph TB
    subgraph THREADS
        T1[Worker 1: task_a]
        T2[Worker 2: task_b]
        T3[Worker 3: task_c]
    end
    
    subgraph TASKS
        P1[Process 10 -> 20]
        P2[Process 20 -> 40]
        P3[Process 30 -> 60]
    end
    
    T1 --> P1
    T2 --> P2
    T3 --> P3
```

```mermaid
stateDiagram-v2
    [*] --> SubmitTasks
    SubmitTasks --> Running: ThreadPool
    Running --> Complete1: Worker 1
    Running --> Complete2: Worker 2
    Running --> Complete3: Worker 3
    Complete1 & Complete2 & Complete3 --> [*]: All done
```

```mermaid
flowchart LR
    subgraph INDEPENDENT
        I1[Pipeline 1]
        I2[Pipeline 2]
        I3[Pipeline 3]
    end
    
    subgraph COORDINATION
        C1[ThreadPoolExecutor]
        C2[concurrent.futures]
    end
    
    I1 & I2 & I3 --> C1
    C1 --> C2
```
