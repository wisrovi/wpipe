# Architecture & Backend Core

## 1. Executive Summary

This microservice module provides a flexible framework for building message-driven microservices using the WPipe pipeline orchestration library. The architecture enables processing messages from queuing systems (Kafka, RabbitMQ, SQS), executing complex data transformation pipelines, persisting results to SQLite, and exposing health check endpoints.

## 2. System Overview

### 2.1 High-Level Architecture

```mermaid
flowchart TB
    subgraph External_Layers["External Interfaces"]
        API[REST API / Health Endpoints]
        MQ[Message Queue / Kafka]
        EXT[External Services]
    end

    subgraph Core["Microservice Core"]
        MG[Message Gateway]
        PC[Pipeline Coordinator]
        ST[State Manager]
        LG[Logger]
    end

    subgraph Processing["Processing Layer"]
        VAL[Validation]
        TX[Transformation]
        ENR[Enrichment]
        VAL[Validation]
    end

    subgraph Persistence["Data Layer"]
        SQL[(SQLite DB)]
        CAC[(Cache)]
        QUE[(Queue)]
    end

    MQ --> MG
    API --> MG
    MG --> PC
    PC --> ST
    PC --> LG
    PC --> VAL
    VAL --> TX
    TX --> ENR
    ENR --> SQL
    SQL --> CAC
    CAC --> QUE
```

### 2.2 Core Components

| Component | Responsibility | Key APIs |
|-----------|----------------|----------|
| Message Gateway | Receive and validate incoming messages | `receive()`, `validate_message()` |
| Pipeline Coordinator | Orchestrate execution flow | `execute()`, `add_step()` |
| State Manager | Track service lifecycle | `start()`, `stop()`, `get_status()` |
| Logger | Structured logging with context | `info()`, `error()`, `debug()` |

## 3. Technical Architecture

### 3.1 Layered Architecture

```mermaid
graph TB
    subgraph Presentation["Presentation Layer"]
        API[REST Endpoints]
        HC[Health Checks]
        MET[Metrics]
    end

    subgraph Application["Application Layer"]
        MG[Message Gateway]
        PC[Pipeline Controller]
        SM[State Machine]
    end

    subgraph Domain["Domain Layer"]
        PIP[Pipeline Engine]
        VAL[ validators]
        TX[Transformers]
    end

    subgraph Infrastructure["Infrastructure Layer"]
        SQ[(SQLite)]
        LO[(Logger)]
        KF[(Kafka)]
    end

    API --> MG
    MG --> PC
    PC --> SM
    SM --> PIP
    PIP --> VAL
    VAL --> TX
    TX --> SQ
    PC --> LO
    MG --> KF
```

### 3.2 Design Patterns

| Pattern | Implementation | Usage |
|--------|----------------|-------|
| Pipeline | `wpipe.Pipeline` | Orchestrate processing steps |
| Decorator | `@step` | Define reusable processing functions |
| State Machine | Service lifecycle | Manage startup/shutdown |
| Factory | `MicroservicioBasico` | Create service instances |
| Repository | SQLite | Persist processing results |

## 4. Integration Points

### 4.1 External Communication

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Gateway
    participant Pipeline
    participant DB
    participant Queue

    Client->>API: POST /process
    API->>Gateway: Route message
    Gateway->>Pipeline: Execute steps
    Pipeline->>Pipeline: Validate input
    Pipeline->>Pipeline: Transform data
    Pipeline->>Pipeline: Enrich data
    Pipeline->>DB: Persist result
    Pipeline->>Queue: Confirm completion
    Queue-->>Client: Acknowledgment
```

### 4.2 Message Queue Integration

```mermaid
flowchart LR
    subgraph Producers
        P1[Producer 1]
        P2[Producer N]
    end

    subgraph Queue["Message Queue"]
        Q[Kafka / RabbitMQ]
    end

    subgraph Consumers
        C1[Consumer 1]
        C2[Consumer N]
    end

    P1 --> Q
    P2 --> Q
    Q --> C1
    Q --> C2
```

## 5. Technical Specifications

### 5.1 Dependencies

| Dependency | Version | Purpose |
|------------|---------|----------|
| wpipe | 1.6.4 | Pipeline orchestration |
| sqlite3 | Built-in | Data persistence |
| logging | Built-in | Logging infrastructure |
| signal | Built-in | Graceful shutdown |

### 5.2 Configuration

```yaml
service:
  name: microservice_example
  version: v1.0
  log_level: INFO
  db_path: service.db

pipeline:
  retry_count: 3
  timeout: 30

queue:
  bootstrap_servers: localhost:9092
  topic: processing_queue
  group_id: service_group
```

### 5.3 Database Schema

```sql
CREATE TABLE processing_logs (
    id INTEGER PRIMARY KEY,
    service_name TEXT,
    message_id TEXT,
    status TEXT,
    input_data TEXT,
    output_data TEXT,
    error TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 6. Scalability Considerations

### 6.1 Horizontal Scaling

```mermaid
flowchart TB
    subgraph LoadBalancer["Load Balancer"]
        LB[Round Robin / IP Hash]
    end

    subgraph Instances["Service Instances"]
        S1[Instance 1]
        S2[Instance 2]
        S3[Instance N]
    end

    subgraph Shared["Shared Resources"]
        DB[(SQLite)]
        QC[Queue Cluster]
    end

    LB --> S1
    LB --> S2
    LB --> S3
    S1 --> DB
    S2 --> DB
    S3 --> DB
    S1 --> QC
    S2 --> QC
    S3 --> QC
```

### 6.2 Performance Metrics

| Metric | Target | Measurement |
|--------|--------|------------|
| Latency P50 | < 10ms | Pipeline execution |
| Latency P99 | < 100ms | End-to-end |
| Throughput | 1000 msg/s | Message processing |
| Availability | 99.9% | Service uptime |

## 7. Error Handling

### 7.1 Error Classification

```mermaid
flowchart TD
    E[Error Occurs] --> T{Error Type}
    T -->|Validation| V[Return Error Response]
    T -->|Processing| P{Has Retry?}
    P -->|Yes| R[Retry N Times]
    P -->|No| F[Log and Continue]
    R -->|Success| S[Continue]
    R -->|Failure| F
    T -->|System| SYS[Graceful Shutdown]
```

### 7.2 Retry Strategy

| Error Type | Retry Count | Backoff |
|-----------|-------------|---------|
| Transient | 3 | Exponential |
| Validation | 0 | None |
| System | 1 | Linear |

## 8. Monitoring & Observability

### 8.1 Metrics Collection

```python
# Key metrics collected
metrics = {
    "requests_total": int,
    "requests_success": int,
    "requests_failed": int,
    "avg_latency_ms": float,
    "p50_latency_ms": float,
    "p99_latency_ms": float,
}
```

### 8.2 Health Check Protocol

```mermaid
sequenceDiagram
    participant Client
    participant Health
    participant Pipeline
    participant DB

    Client->>Health: GET /health
    Health->>Pipeline: Check status
    Pipeline-->>Health: READY
    Health->>DB: Check connection
    DB-->>Health: OK
    Health-->>Client: 200 OK
```

## 9. File Structure

```
24_microservice/
├── 01_basic_service_example/
│   └── example.py           # Core microservice structure
├── 02_message_processor_example/
├── 03_service_with_pipeline_example/
├── 05_health_check_example/
│   └── example.py           # Health check implementation
├── 06_service_state_example/
├── 07_service_validation_example/
├── 08_service_metrics_example/
│   └── example.py           # Metrics collection
├── 09_service_config_example/
├── 09_service_dependencies_example/
├── 10_service_graceful_shutdown.py
└── README.md
```

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.6.4 | 2026-04-20 | Current version, @step decorator replacement |
| 1.6.3 | 2026-xx-xx | Previous stable release |