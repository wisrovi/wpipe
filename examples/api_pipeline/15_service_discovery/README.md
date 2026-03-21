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
    participant P as Pipeline
    participant R as Registry
    
    P->>R: Discover services
    R-->>P: Endpoints
    P->>P: Configure
    P->>P: Test
```

```mermaid
graph TB
    subgraph Discovery
        A[Query registry]
    end
    
    subgraph Services
        B[API]
        C[Database]
        D[Cache]
    end
    
    subgraph Config
        E[Configure]
    end
    
    subgraph Test
        F[Test]
    end
    
    A --> B
    A --> C
    A --> D
    B --> E
    C --> E
    D --> E
    E --> F
```

```mermaid
stateDiagram-v2
    [*] --> Discover
    Discover --> Configure
    Configure --> Test
    Test --> [*]
```

```mermaid
flowchart LR
    D([Discover]) --> S([Services])
    S --> C([Configure])
    C --> T([Test])
    
    style D fill:#e1f5fe
    style T fill:#c8e6c9
```
