# State Preservation

Demonstrates state preservation and mutation between nested pipelines.

## What It Does

- Inner pipeline initializes state and increments counter
- State persists across steps within the inner pipeline
- Outer pipeline can access the final state after inner pipeline completes

## Nested Flow

```mermaid
graph LR
    A[{}] --> B[Inner Pipeline]
    B --> C[init_state]
    C --> D[{state: {count: 0}}]
    D --> E[increment]
    E --> F[{state: {count: 1}}]
    F --> G[get_state]
    G --> H[{final_count: 1}]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant O as Outer Pipeline
    participant I as Inner Pipeline
    participant Init as init_state
    participant Inc as increment
    participant GS as get_state

    O->>I: Run with {}
    I->>Init: Execute init_state
    Init-->>I: Return {state: {count: 0}}
    I->>Inc: Execute increment
    Inc-->>I: Return {state: {count: 1}}
    I-->>O: Return {state: {count: 1}}
    O->>GS: Execute get_state
    GS-->>O: Return {final_count: 1}
```

## Pipeline Hierarchy

```mermaid
graph TB
    subgraph Outer["Outer Pipeline"]
        I[Inner Pipeline]
        GS[get_state]
    end
    subgraph Inner["Inner Pipeline"]
        Init[init_state]
        Inc[increment]
    end
    I --> Init --> Inc
```

## Execution States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> InitState: run init_state
    InitState --> StateReady: state initialized
    StateReady --> Increment: run increment
    Increment --> InnerDone: count = 1
    InnerDone --> GetState: run get_state
    GetState --> Done: final result
    Done --> [*]
```

## Data Flow

```mermaid
flowchart LR
    A[{}] --> B[init_state]
    B --> C[{state: {count: 0}}]
    C --> D[increment]
    D --> E[{state: {count: 1}}]
    E --> F[get_state]
    F --> G[{final_count: 1}]
```
