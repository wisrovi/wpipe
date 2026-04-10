# Service State Management Example

Demonstrates managing service state across multiple requests.

## What It Does

This example shows how to create a stateful service with:
- Request counting across calls
- State persistence during service lifetime
- Pipeline processing per request
- Logging of request numbers

## Service Flow

```mermaid
graph LR
    A[Process Request] --> B[Increment Counter]
    B --> C[Log Request]
    C --> D[Run Pipeline]
    D --> E[Return Result]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Client
    participant Service as StatefulService

    Client->>Service: process({id: 1})
    Service->>Service: request_count++
    Service->>Service: log Request #1
    Service->>Pipeline: run(data)
    Pipeline-->>Service: result
    Service-->>Client: {processed: true}

    Client->>Service: process({id: 2})
    Service->>Service: request_count++
    Service->>Service: log Request #2
    Service->>Pipeline: run(data)
    Pipeline-->>Service: result
    Service-->>Client: {processed: true}
```

## Service Structure

```mermaid
graph TB
    subgraph StatefulService
        A[__init__] --> B[Logger]
        A --> C[request_count: 0]
    end
    
    D[process] --> E[Increment counter]
    E --> F[Log info]
    F --> G[Create Pipeline]
    G --> H[process_step]
    H --> I[Return result]
```

## Service States

```mermaid
stateDiagram-v2
    [*] --> Initialized: __init__
    Initialized --> Ready: request_count = 0
    Ready --> Processing: process()
    Processing --> Ready: Complete
    Ready --> Ready: process() again
    Ready --> Shutdown: destroy
    Shutdown --> [*]
```

## Request Counter Flow

```mermaid
flowchart LR
    subgraph Request 1
        A1[Start] --> B1[count = 0]
        B1 --> C1[count++ = 1]
        C1 --> D1[Log #1]
    end
    
    subgraph Request 2
        A2[Start] --> B2[count = 1]
        B2 --> C2[count++ = 2]
        C2 --> D2[Log #2]
    end
    
    subgraph Request N
        AN[Start] --> BN[count = N-1]
        BN --> CN[count++ = N]
        CN --> DN[Log #N]
    end
```

## Usage

```bash
python example.py
```

## Expected Output

```
Total requests: 2
```
