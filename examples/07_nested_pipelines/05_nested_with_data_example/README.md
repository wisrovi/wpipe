# Passing Custom Data to Nested Pipelines

Demonstrates passing custom input data to nested pipelines and using the results in outer steps.

## What It Does

- Passes custom data (value: 5) to an outer pipeline
- Inner pipeline processes the value and returns inner_result
- Outer pipeline uses inner_result to compute outer_result

## Nested Flow

```mermaid
graph LR
    A[{value: 5}] --> B[Inner Pipeline]
    B --> C[{inner_result: 10}]
    C --> D[outer_step]
    D --> E[{outer_result: 20}]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant O as Outer Pipeline
    participant I as Inner Pipeline
    participant OS as outer_step

    O->>I: Run with {value: 5}
    I-->>O: Return {inner_result: 10}
    O->>OS: Execute with {value: 5, inner_result: 10}
    OS-->>O: Return {outer_result: 20}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Outer["Outer Pipeline"]
        I[Inner Pipeline]
        OS[outer_step]
    end
    subgraph Inner["Inner Pipeline"]
        IS[inner_step]
    end
    I --> IS
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> InnerRun: run inner pipeline
    InnerRun --> InnerDone: inner complete
    InnerDone --> OuterRun: run outer step
    OuterRun --> Done: complete
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{value: 5}] --> B[inner_step]
    B --> C[{inner_result: 10}]
    C --> D[outer_step]
    D --> E[{outer_result: 20}]
```
