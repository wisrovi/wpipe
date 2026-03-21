# Health Check Example

Demonstrates implementing a health check endpoint for microservice monitoring.

## What It Does

This example shows how to create a service with:
- Health check endpoint for monitoring
- Service status reporting
- Basic pipeline processing
- Simple architecture

## Service Flow

```mermaid
graph LR
    A[Health Check Request] --> B[Check Service Status]
    B --> C[Check Pipeline]
    C --> D[Return Status]
    
    E[Process Request] --> F[Run Pipeline]
    F --> G[Return Result]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Client
    participant Service as HealthCheckService
    participant Pipeline

    Client->>Service: health_check()
    Service-->>Client: {status: healthy, pipeline_ready: true}

    Client->>Service: process(data)
    Service->>Pipeline: run(data)
    Pipeline->>Service: result
    Service-->>Client: {status: ok, processed: true}
```

## Service Structure

```mermaid
graph TB
    subgraph HealthCheckService
        A[__init__] --> B[Logger]
        A --> C[Pipeline]
        C --> D[process_step]
    end
    
    E[health_check] --> F[Status Check]
    G[process] --> C
```

## Service States

```mermaid
stateDiagram-v2
    [*] --> Initialized: __init__
    Initialized --> Ready: Service created
    Ready --> HealthCheck: health_check()
    HealthCheck --> Ready: Return status
    Ready --> Processing: process()
    Processing --> Ready: Return result
```

## Processing Flow

```mermaid
flowchart LR
    subgraph Input
        A["{test: 'data'}"]
    end
    
    subgraph Process Step
        B[process_step]
        B --> C["{status: ok}"]
        B --> D["{processed: true}"]
    end
    
    subgraph Output
        E["{status: ok, processed: true}"]
    end
    
    A --> B --> E
```

## Usage

```bash
python example.py
```

## Expected Output

```
Health check: {'service': 'test_service', 'status': 'healthy', 'pipeline_ready': True}
Process result: {'status': 'ok', 'processed': True}
```
