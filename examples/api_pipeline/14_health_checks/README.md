# 14 Health Checks

Demonstrates implementing health check functionality.
Pipeline can be used to verify service dependencies are healthy.

## What it evaluates

- Health check step in pipeline
- Service dependency verification
- Status reporting for monitoring

## Flow

```mermaid
graph LR
    A[Health Check] --> B[DB Check]
    A --> C[Cache Check]
    A --> D[API Check]
    B --> E[Aggregate]
    C --> E
    D --> E
    E --> F[Status Report]
```

```mermaid
sequenceDiagram
    participant Monitor
    participant Pipeline
    participant DB
    participant Cache
    participant API
    
    Monitor->>Pipeline: Run health check pipeline
    Pipeline->>DB: Check connectivity
    Pipeline->>Cache: Check status
    Pipeline->>API: Check availability
    DB-->>Pipeline: db_status
    Cache-->>Pipeline: cache_status
    API-->>Pipeline: api_status
    Pipeline->>Pipeline: Aggregate results
    Pipeline-->>Monitor: overall_status
```

```mermaid
graph TB
    subgraph CHECKS
        C1[check_database]
        C2[check_cache]
        C3[check_api]
    end
    
    subgraph RESULTS
        R1[db_status: healthy]
        R2[cache_status: healthy]
        R3[api_status: healthy]
    end
    
    subgraph AGGREGATION
        A1[All healthy?]
        A1 -->|Yes| A2[overall: healthy]
        A1 -->|No| A3[overall: unhealthy]
    end
    
    C1 --> R1
    C2 --> R2
    C3 --> R3
    R1 --> A1
    R2 --> A1
    R3 --> A1
```

```mermaid
stateDiagram-v2
    [*] --> CheckDB
    CheckDB --> CheckCache: DB healthy
    CheckDB --> Failed: DB down
    CheckCache --> CheckAPI: Cache healthy
    CheckCache --> Failed: Cache down
    CheckAPI --> Aggregate: API healthy
    CheckAPI --> Failed: API down
    Aggregate --> [*]: Report status
    Failed --> [*]: Report failure
```

```mermaid
flowchart TB
    subgraph STEP_1_DB
        S1[Check database connectivity]
        S2[Return db_status, latency]
    end
    
    subgraph STEP_2_CACHE
        S3[Check cache service]
        S4[Return cache_status, hits]
    end
    
    subgraph STEP_3_API
        S5[Check external API]
        S6[Return api_status, version]
    end
    
    subgraph STEP_4_AGGREGATE
        S7[Collect all statuses]
        S8[Check if all healthy]
        S9[Return overall_status]
    end
    
    S1 --> S3 --> S5 --> S7 --> S8 --> S9
```
