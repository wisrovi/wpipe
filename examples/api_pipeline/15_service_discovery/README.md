# 15 Service Discovery

Demonstrates dynamic service discovery and configuration.
Pipeline discovers services and configures connections dynamically.

## What it evaluates

- Dynamic service discovery
- Configuration based on discovered services
- Flexible service routing

## Flow

```mermaid
graph LR
    A[Discover] --> B[Services Found]
    B --> C[Configure]
    C --> D[Test Connections]
    D --> E[Result]
```

```mermaid
sequenceDiagram
    participant Pipeline
    participant Discovery
    participant Registry
    participant Services
    
    Pipeline->>Discovery: Discover services
    Discovery->>Registry: Query available services
    Registry-->>Discovery: Service endpoints
    Discovery-->>Pipeline: Discovered services
    Pipeline->>Pipeline: Configure connections
    Pipeline->>Services: Test connections
    Services-->>Pipeline: Test results
    Pipeline-->>Pipeline: Final status
```

```mermaid
graph TB
    subgraph DISCOVERY
        D1[Discover services]
        D2[Service registry]
        D3[Service endpoints]
    end
    
    subgraph SERVICES
        S1[api: http://...]
        S2[database: postgresql://...]
        S3[cache: redis://...]
    end
    
    subgraph CONFIG
        C1[Configure URLs]
        C2[Connection pools]
    end
    
    subgraph TEST
        T1[Test connections]
        T2[Report status]
    end
    
    D1 --> D2 --> D3
    D3 --> S1 & S2 & S3
    S1 & S2 & S3 --> C1 --> C2 --> T1 --> T2
```

```mermaid
stateDiagram-v2
    [*] --> Discover
    Discover --> Configure: Services found
    Discover --> [*]: No services
    Configure --> Test: Connections configured
    Test --> Success: All pass
    Test --> Warning: Some fail
    Success --> [*]: Ready
    Warning --> [*]: Degraded
```

```mermaid
flowchart TB
    subgraph STEP_1_DISCOVER
        S1[Query service registry]
        S2[Return service_map]
        S3[api, database, cache]
    end
    
    subgraph STEP_2_CONFIGURE
        S4[Build config from services]
        S5[Create connection URLs]
        S6[Return configured object]
    end
    
    subgraph STEP_3_TEST
        S7[Test each connection]
        S8[Collect test results]
        S9[Return all_passed status]
    end
    
    S1 --> S2 --> S3
    S3 --> S4 --> S5 --> S6
    S6 --> S7 --> S8 --> S9
```
