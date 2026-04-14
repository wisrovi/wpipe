# Exception Types Example

Shows handling different types of exceptions in pipeline steps.

## What It Does

Demonstrates how the pipeline handles various exception types:
TypeError, KeyError, and AssertionError are all captured uniformly.

## Flow

```mermaid
graph LR
    A[TypeError] --> B[Pipeline]
    C[KeyError] --> B
    D[AssertionError] --> B
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant T as TypeError
    participant K as KeyError
    
    P->>T: Raise
    T-->>P: Catch
    P->>K: Raise
    K-->>P: Catch
```

```mermaid
graph TB
    subgraph Exceptions
        A[TypeError]
        B[KeyError]
        C[AssertionError]
    end
    
    subgraph Handling
        D[Capture]
    end
    
    A --> D
    B --> D
    C --> D
```

```mermaid
stateDiagram-v2
    [*] --> RaiseType
    RaiseType --> CaptureType
    CaptureType --> RaiseKey
    RaiseKey --> CaptureKey
    CaptureKey --> [*]
```

```mermaid
flowchart LR
    T([TypeError]) --> P([Pipeline])
    K([KeyError]) --> P
    A([Assertion]) --> P
```
