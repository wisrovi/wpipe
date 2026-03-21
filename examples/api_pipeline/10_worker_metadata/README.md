# 10 Worker Metadata

Demonstrates passing custom metadata to the worker registration.
Metadata can include version info, environment, tags, etc.

## What it evaluates

- worker_metadata parameter in api_config
- Metadata is sent during worker registration
- Pipeline can track worker properties

## Flow

```mermaid
graph LR
    A[Input Data] --> B[Process Step]
    B --> C[Result with Worker Info]
```

```mermaid
sequenceDiagram
    participant Client
    participant Pipeline
    participant API
    
    Client->>Pipeline: Run with metadata
    Pipeline->>API: Register worker with metadata
    API-->>Pipeline: Worker ID
    Pipeline->>Pipeline: Execute steps
    Pipeline-->>Client: Result
```

```mermaid
graph TB
    subgraph API_CONFIG
        M1[base_url]
        M2[token]
        M3[worker_metadata]
    end
    
    subgraph METADATA_FIELDS
        V1[version]
        V2[environment]
        V3[tags]
    end
    
    M3 --> V1
    M3 --> V2
    M3 --> V3
```

```mermaid
stateDiagram-v2
    [*] --> Registering
    Registering --> Registered: with metadata
    Registered --> Executing: run()
    Executing --> [*]: Complete
```

```mermaid
flowchart LR
    subgraph SETUP
        A1[api_config] --> A2[worker_metadata]
    end
    
    subgraph REGISTRATION
        A2 --> B1[Worker Register]
        B1 --> B2[Worker ID]
    end
    
    subgraph EXECUTION
        B2 --> C1[Process Step]
        C1 --> C2[Return Result]
    end
```
