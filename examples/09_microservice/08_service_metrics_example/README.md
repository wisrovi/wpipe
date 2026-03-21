# Metrics Collection Example

Demonstrates collecting service performance metrics.

## What It Does

This example shows how to create a metrics service with:
- Request counting
- Processing time tracking
- Average time calculation
- Metrics retrieval

## Service Flow

```mermaid
graph LR
    A[Receive Request] --> B[Start Timer]
    B --> C[Run Pipeline]
    C --> D[Stop Timer]
    D --> E[Update Metrics]
    E --> F[Return Result]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Client
    participant Service as MetricsService
    participant Pipeline

    Client->>Service: handle(data)
    Service->>Service: start = time.time()
    Service->>Pipeline: run(data)
    Pipeline-->>Service: result
    Service->>Service: elapsed = time.time() - start
    Service->>Service: total_requests++
    Service->>Service: total_time += elapsed
    Service-->>Client: result

    loop Multiple requests
        Client->>Service: handle({})
        Service-->>Client: result
    end

    Client->>Service: get_metrics()
    Service-->>Client: {requests: N, avg_time: X}
```

## Service Structure

```mermaid
graph TB
    subgraph MetricsService
        A[__init__] --> B[total_requests: 0]
        A --> C[total_time: 0]
    end
    
    D[handle] --> E[Start timer]
    E --> F[Create Pipeline]
    F --> G[Run pipeline]
    G --> H[Stop timer]
    H --> I[Update metrics]
    I --> J[Return result]
    
    K[get_metrics] --> L[Calculate avg]
    L --> M[Return metrics]
```

## Metrics States

```mermaid
stateDiagram-v2
    [*] --> Initialized: __init__
    Initialized --> Ready: Service ready
    Ready --> Handling: handle()
    Handling --> Measure: Record time
    Measure --> Ready: Return result
    Ready --> Querying: get_metrics()
    Querying --> Ready: Return metrics
```

## Metrics Collection Flow

```mermaid
flowchart LR
    subgraph Request 1
        A1[start time] --> B1[run pipeline]
        B1 --> C1[end time]
        C1 --> D1[elapsed = X]
        D1 --> E1[total_requests = 1]
        E1 --> F1[total_time = X]
    end
    
    subgraph Request 2
        A2[start time] --> B2[run pipeline]
        B2 --> C2[end time]
        C2 --> D2[elapsed = Y]
        D2 --> E2[total_requests = 2]
        E2 --> F2[total_time = X+Y]
    end
    
    F1 --> G[avg = total / requests]
    F2 --> G
```

## Usage

```bash
python example.py
```

## Expected Output

```
Metrics: {'requests': 3, 'avg_time': 0.001234}
```
