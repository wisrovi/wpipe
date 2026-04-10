# Basic Error Example

Shows the simplest error handling pattern - catching a ValueError in a pipeline step.

## What It Does

Demonstrates how to create a pipeline where one step intentionally fails.
The error is captured in the pipeline result, allowing graceful handling.

## Flow

```mermaid
graph LR
    A[Valid Step] --> B[Failing Step]
    B --> C[Error Captured]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant V as Valid Step
    participant F as Failing Step
    
    P->>V: Run
    V-->>P: Success
    P->>F: Run
    F-->>P: ValueError
```

```mermaid
graph TB
    subgraph Pipeline
        A[Start]
        B[Valid Step]
        C[Failing Step]
        D[Error]
    end
    
    A --> B
    B --> C
    C --> D
```

```mermaid
stateDiagram-v2
    [*] --> RunValid
    RunValid --> ValidSuccess
    ValidSuccess --> RunFailing
    RunFailing --> Error
    Error --> [*]
```

```mermaid
flowchart LR
    V([Valid]) --> F([Failing])
    F --> E([Error])
```
