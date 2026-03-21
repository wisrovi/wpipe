# Parallel Nested Pipelines

Demonstrates multiple nested pipelines executed in sequence within a main pipeline.

## What It Does

- Creates two pipelines that process the same input differently
- Pipeline A passes through the value unchanged
- Pipeline B doubles the value
- Final step combines results from both pipelines

## Nested Flow

```mermaid
graph LR
    A[{value: 10}] --> B[Pipeline A]
    A --> C[Pipeline B]
    B --> D[{a: 10}]
    C --> E[{b: 20}]
    D --> F[combine]
    E --> F
    F --> G[{combined: 30}]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant M as Main Pipeline
    participant PA as Pipeline A
    participant PB as Pipeline B
    participant C as combine

    M->>PA: Run with {value: 10}
    PA-->>M: Return {a: 10}
    M->>PB: Run with {value: 10}
    PB-->>M: Return {b: 20}
    M->>C: Execute with {a: 10, b: 20}
    C-->>M: Return {combined: 30}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Main["Main Pipeline"]
        PA[Pipeline A]
        PB[Pipeline B]
        C[combine]
    end
    subgraph PA_"Pipeline A"
        PCA[process_a]
    end
    subgraph PB_"Pipeline B"
        PCB[process_b]
    end
    PA --> PCA
    PB --> PCB
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> RunA: run pipeline A
    RunA --> DoneA: pipeline A complete
    DoneA --> RunB: run pipeline B
    RunB --> DoneB: pipeline B complete
    DoneB --> Combine: combine results
    Combine --> Done: complete
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{value: 10}] --> B[process_a]
    A --> C[process_b]
    B --> D[{a: 10}]
    C --> E[{b: 20}]
    D --> F[combine]
    E --> F
    F --> G[{combined: 30}]
```
