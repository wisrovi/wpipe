# TaskError Example

Shows using TaskError exception directly for custom error handling.

## What It Does

Demonstrates creating a validation step that uses TaskError
with error codes to indicate validation failures.

## Flow

```mermaid
graph LR
    A[Input Data] --> B[Validate]
    B --> C[Process]
    B -->|Invalid| D[TaskError]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant V as Validate
    participant T as TaskError
    
    P->>V: Run validation
    V-->>P: Valid
    P->>T: Raise TaskError
```

```mermaid
graph TB
    subgraph Validation
        A[Check Value]
        B[Positive?]
    end
    
    subgraph Result
        C[Success]
        D[TaskError]
    end
    
    A --> B
    B -->|Yes| C
    B -->|No| D
```

```mermaid
stateDiagram-v2
    [*] --> Validate
    Validate --> Valid : Positive
    Validate --> Invalid : Negative
    Valid --> Process
    Invalid --> Error
    Error --> [*]
    Process --> [*]
```

```mermaid
flowchart LR
    V([Validate]) -->|Valid| P([Process])
    V -->|Invalid| E([TaskError])
```
