# Request Validation Example

Demonstrates validating incoming requests before processing.

## What It Does

This example shows how to create a validating service with:
- Request validation step
- Pipeline-based validation
- Error handling for invalid requests
- Processing after validation

## Service Flow

```mermaid
graph LR
    A[Receive Request] --> B[Validate]
    B --> C{Valid?}
    C -->|Yes| D[Process Data]
    C -->|No| E[Raise Error]
    D --> F[Return Result]
    E --> G[Return Error]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Client
    participant Service as ValidatingService
    participant Pipeline

    Client->>Service: handle(data)
    Service->>Pipeline: run(data)
    Pipeline->>Pipeline: validate_request()
    Note over Pipeline: Check required_field
    alt required_field present
        Pipeline->>Pipeline: process()
        Pipeline-->>Service: result
    else required_field missing
        Pipeline-->>Service: ValueError
    end
    Service-->>Client: response
```

## Service Structure

```mermaid
graph TB
    subgraph ValidatingService
        A[__init__] --> B[Pipeline]
        B --> C[validate_request]
        B --> D[process]
    end
    
    E[handle] --> F[Run pipeline]
    F --> G[Return result]
```

## Validation States

```mermaid
stateDiagram-v2
    [*] --> Idle: __init__
    Idle --> Validating: handle()
    Validating --> Valid: required_field exists
    Validating --> Invalid: required_field missing
    Invalid --> Error: Raise ValueError
    Valid --> Processing: Continue pipeline
    Processing --> Complete: Return result
    Error --> Idle: Catch and return
    Complete --> Idle
```

## Validation Flow

```mermaid
flowchart LR
    subgraph Valid Request
        A1["{required_field: 'present'}"] --> B1[validate_request]
        B1 --> C1["{validated: True}"]
        C1 --> D1[process]
        D1 --> E1["{processed: True}"]
    end
    
    subgraph Invalid Request
        A2["{other_field: 'x'}"] --> B2[validate_request]
        B2 --> C2{required_field?}
        C2 -->|No| D2[ValueError]
    end
```

## Usage

```bash
python example.py
```

## Expected Output

```
Valid request result: {'validated': True, 'processed': True}
```
