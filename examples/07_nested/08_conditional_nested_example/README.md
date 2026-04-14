# Conditional Nested Pipelines

Demonstrates selecting different nested pipelines based on conditions.

## What It Does

- Creates two inner pipelines for different types (A and B)
- Runs inner_a pipeline for type A processing
- Runs inner_b pipeline for type B processing
- Shows how to choose the appropriate pipeline based on input

## Nested Flow

```mermaid
graph LR
    A[{type: A}] --> B[Inner A Pipeline]
    B --> C[{processed: A}]
    A'[{type: B}] --> D[Inner B Pipeline]
    D --> E[{processed: B}]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant Caller
    participant I_A as Inner A
    participant I_B as Inner B

    Caller->>I_A: Run with {type: A}
    I_A-->>Caller: Return {processed: A}
    Caller->>I_B: Run with {type: B}
    I_B-->>Caller: Return {processed: B}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Inner_A["Inner A Pipeline"]
        PA[process_a]
    end
    subgraph Inner_B["Inner B Pipeline"]
        PB[process_b]
    end
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Decision: check type
    Decision --> ProcessA: type = A
    Decision --> ProcessB: type = B
    ProcessA --> DoneA: process_a complete
    ProcessB --> DoneB: process_b complete
    DoneA --> [*]
    DoneB --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{type: A}] --> B[process_a]
    B --> C[{processed: A}]

    A2[{type: B}] --> D[process_b]
    D --> E[{processed: B}]
```
