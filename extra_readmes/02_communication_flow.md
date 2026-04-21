# Communication Flow

## 1. Internal Communication

### 1.1 Message Processing Flow

```mermaid
sequenceDiagram
    participant Ext as External Client
    participant Gateway as Message Gateway
    participant Pipeline as Pipeline Engine
    participant Steps as Processing Steps
    participant Logger as Logging System
    participant DB as SQLite Database

    Ext->>Gateway: POST /process {message}
    Gateway->>Logger: INFO: Received message
    Gateway->>Pipeline: execute(message)
    Pipeline->>Logger: DEBUG: Starting pipeline
    Pipeline->>Steps: step_1.validate()
    Steps-->>Pipeline: validation_result
    Pipeline->>Steps: step_2.transform()
    Steps-->>Pipeline: transformed_data
    Pipeline->>Steps: step_3.enrich()
    Steps-->>Pipeline: enriched_data
    Pipeline->>Logger: DEBUG: Pipeline completed
    Pipeline->>DB: INSERT result
    DB-->>Pipeline: row_id
    Pipeline-->>Gateway: result_dict
    Gateway-->>Ext: 200 OK {result}
```

### 1.2 Pipeline Execution Flow

```mermaid
sequenceDiagram
    participant Service as Microservice
    participant Pipeline as Pipeline Instance
    participant Step1 as Validation Step
    participant Step2 as Processing Step
    participant Step3 as Enrichment Step
    participant DB as Result Storage

    Service->>Pipeline: run(input_data)
    Pipeline->>Step1: execute(input_data)
    Step1->>Step1: Validate message structure
    Step1-->>Pipeline: validated_data
    Pipeline->>Step2: execute(validated_data)
    Step2->>Step2: Transform data
    Step2-->>Pipeline: processed_data
    Pipeline->>Step3: execute(processed_data)
    Step3->>Step3: Add metadata
    Step3-->>Pipeline: enriched_data
    Pipeline->>DB: Store result
    DB-->>Pipeline: confirmation
    Pipeline-->>Service: final_result
```

## 2. External Communication

### 2.1 Health Check Endpoint

```mermaid
sequenceDiagram
    participant LB as Load Balancer
    participant HC as Health Check Endpoint
    participant Pipeline as Pipeline Status
    participant DB as Database Connection
    participant State as Service State

    LB->>HC: GET /health
    HC->>State: is_running()
    State-->>HC: True
    HC->>Pipeline: is_ready()
    Pipeline-->>HC: True
    HC->>DB: ping()
    DB-->>HC: OK
    HC-->>LB: 200 OK {status: healthy}
```

### 2.2 Metrics Collection

```mermaid
sequenceDiagram
    participant Monitor as Monitoring System
    participant Metrics as Metrics Collector
    participant Pipeline as Pipeline Metrics
    participant DB as Historical Data

    Monitor->>Metrics: GET /metrics
    Metrics->>Pipeline: get_execution_stats()
    Pipeline-->>Metrics: stats_dict
    Metrics->>DB: get_historical()
    Metrics-->>Metrics: Calculate averages
    Metrics->>Metrics: Format Prometheus/Grafana
    Metrics-->>Monitor: 200 OK {metrics}
```

### 2.3 Graceful Shutdown Flow

```mermaid
sequenceDiagram
    participant Signal as OS Signal (SIGINT)
    participant Handler as Signal Handler
    participant Service as Microservice
    participant Pipeline as Pipeline
    participant Queue as Message Queue

    Signal->>Handler: SIGINT received
    Handler->>Service: stop()
    Service->>Pipeline: finish_current()
    Pipeline-->>Service: completed
    Service->>Queue: wait_for_ack()
    Queue-->>Service: all_acked
    Service->>Service: cleanup_resources()
    Service-->>Signal: Exit 0
```

## 3. Kafka Integration Flow

### 3.1 Message Consumption

```mermaid
sequenceDiagram
    participant Kafka as Kafka Cluster
    participant Consumer as Message Consumer
    participant Service as Microservice
    participant Pipeline as Pipeline
    participant DB as Result DB

    Kafka->>Consumer: poll()
    Consumer->>Service: process_message(msg)
    Service->>Pipeline: execute(msg.value)
    Pipeline->>DB: Store result
    DB-->>Pipeline: success
    Pipeline-->>Service: processed
    Service->>Consumer: commit offset
    Consumer-->>Kafka: ack()
```

### 3.2 Error Handling with Retry

```mermaid
flowchart TD
    A[Receive Message] --> B{Process Message}
    B -->|Success| C[Commit Offset]
    B -->|Error| D{Retry Count < Max?}
    D -->|Yes| E[Wait Backoff]
    E --> B
    D -->|No| F[Log Error]
    F --> G[Send to DLQ]
    G --> C
```

## 4. Service-to-Service Communication

### 4.1 Upstream Service

```mermaid
flowchart LR
    subgraph Upstream
        API[REST API]
    end
    
    subgraph This Service
        GW[Gateway]
        PL[Pipeline]
    end
    
    subgraph Downstream
        DB[(SQLite)]
        EXT[External API]
    end
    
    API --> GW
    GW --> PL
    PL --> DB
    PL --> EXT
```

### 4.2 Configuration-based Service Dependencies

```mermaid
sequenceDiagram
    participant Config as Config Service
    participant Service as Microservice
    participant Dep1 as Dependency A
    participant Dep2 as Dependency B

    Service->>Config: Load configuration
    Config-->>Service: dependencies_config
    Service->>Dep1: Health check
    Dep1-->>Service: OK
    Service->>Dep2: Health check
    Dep2-->>Service: OK
    Service->>Service: Start processing
```

## 5. State Management

### 5.1 Service Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> Initialized
    
    Initialized --> Starting: start()
    Starting --> Running: Ready
    Running --> Stopping: stop() / SIGINT
    Stopping --> Stopped: Cleanup complete
    
    Running --> Processing: Process message
    Processing --> Running: Complete
    
    Running --> Error: Exception
    Error --> Running: Retry success
    Error --> Stopping: Retry failed
    
    Stopped --> [*]
```

### 5.2 Message Counter State

```mermaid
sequenceDiagram
    participant Client
    participant Service
    participant Counter
    participant Pipeline
    
    Client->>Service: process(msg_1)
    Service->>Counter: increment()
    Counter-->>Service: count = 1
    Service->>Pipeline: run(msg_1)
    Pipeline-->>Service: result_1
    Service-->>Client: result_1
    
    Client->>Service: process(msg_2)
    Service->>Counter: increment()
    Counter-->>Service: count = 2
    Service->>Pipeline: run(msg_2)
    Pipeline-->>Service: result_2
    Service-->>Client: result_2
```

## 6. Data Flow

### 6.1 Input to Output Transformation

```mermaid
flowchart LR
    subgraph Input
        JSON[JSON Message]
    end
    
    subgraph Validation
        V[Validate Schema]
    end
    
    subgraph Processing
        T1[Transform]
        T2[Enrich]
        T3[Aggregate]
    end
    
    subgraph Output
        RES[Result Object]
        DB[(SQLite)]
        API[Response]
    end
    
    JSON --> V
    V --> T1
    T1 --> T2
    T2 --> T3
    T3 --> RES
    RES --> DB
    RES --> API
```

### 6.2 Error Data Flow

```mermaid
flowchart TD
    A[Process Message] --> B{Success?}
    B -->|Yes| C[Store Success Result]
    B -->|No| D{Retry Available?}
    D -->|Yes| E[Wait Backoff]
    E --> A
    D -->|No| F[Log Error Details]
    F --> G[Store Error Result]
    G --> H{Is Critical?}
    H -->|Yes| I[Alert On-Call]
    H -->|No| J[Continue]
    I --> J
```

## 7. Communication Protocols

### 7.1 REST API Interface

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/health` | GET | Health check | `{status, pipeline_ready}` |
| `/process` | POST | Process message | `{result}` |
| `/metrics` | GET | Get metrics | `{requests, avg_time}` |
| `/stop` | POST | Graceful shutdown | `{status}` |

### 7.2 Message Queue Protocol

| Topic | Message Format | Ack Mode |
|-------|---------------|----------|
| `input_queue` | JSON | After processing |
| `output_queue` | JSON | Immediate |
| `error_queue` | JSON + Error | After DLQ |

## 8. Logging Context

### 8.1 Logged Events

```mermaid
sequenceDiagram
    participant Client
    participant Service
    participant Logger
    participant File
    
    Client->>Service: POST /process
    Service->>Logger: [MSG-1] Received message
    Service->>Logger: [MSG-1] Starting pipeline
    Service->>Logger: [PASO] Validating
    Service->>Logger: [PASO] Processing
    Service->>Logger: [PASO] Enriching
    Service->>Logger: [MSG-1] Completed
    Logger->>File: Write logs
    Service-->>Client: Response
```