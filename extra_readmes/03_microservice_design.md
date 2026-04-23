# Microservice Design

## 1. Design Principles

### 1.1 Core Design Tenets

| Principle | Implementation |
|-----------|----------------|
| Single Responsibility | Each step in pipeline performs one transformation |
| Loose Coupling | Steps communicate via dictionaries |
| High Cohesion | Related transformations grouped in pipeline |
| Fault Tolerance | Retry logic and error handling per step |

### 1.2 Architecture Decisions

```mermaid
graph TB
    subgraph Design_Principles
        SRP[Single Responsibility]
        OCP[Open/Closed]
        LSP[Liskov Substitution]
        ISP[Interface Segregation]
        DIP[Dependency Inversion]
    end
    
    SRP --> Impl1[Step Functions]
    OCP --> Impl2[Pipeline Extension]
    LSP --> Impl3[Pipeline Subclasses]
    ISP --> Impl4[Specialized Services]
    DIP --> Impl5[Dependency Injection]
```

## 2. Service Structure

### 2.1 Class Diagram

```mermaid
classDiagram
    class MicroservicioBasico {
        +nombre: str
        +ejecutando: bool
        +contador_mensajes: int
        +logger: Logger
        +pipeline: Pipeline
        +__init__(nombre: str)
        +procesar_mensaje(mensaje: dict) dict
        +iniciar() None
        +detener() None
    }
    
    class Pipeline {
        +pipeline_name: str
        +verbose: bool
        +tasks_list: list
        +set_steps(steps: list) None
        +run(context: dict) dict
    }
    
    class Step {
        +func: Callable
        +name: str
        +version: str
        +run(context: dict) dict
    }
    
    MicroservicioBasico --> Pipeline : uses
    Pipeline --> Step : manages
```

### 2.2 Component Responsibilities

| Component | Responsibility | Public API |
|-----------|----------------|------------|
| `MicroservicioBasico` | Main service orchestrator | `procesar_mensaje()`, `iniciar()`, `detener()` |
| `Pipeline` | Step execution engine | `set_steps()`, `run()` |
| `Logger` | Structured logging | `info()`, `error()`, `debug()` |
| Step Functions | Data transformation | `func(data) -> dict` |

## 3. Design Patterns

### 3.1 Pipeline Pattern

```mermaid
flowchart LR
    subgraph Pipeline["Pipeline Pattern"]
        I[Input] --> S1[Step 1]
        S1 --> S2[Step 2]
        S2 --> S3[Step 3]
        S3 --> O[Output]
    end
    
    style Pipeline fill:#e1f5fe
    style I fill:#fff3e0
    style O fill:#e8f5e9
```

**Implementation:**
```python
@step(name="step_1")
def transform_1(data):
    return {"transformed": data["value"] * 2}

pipeline.set_steps([
    (transform_1, "Transform1", "v1.0"),
    (transform_2, "Transform2", "v1.0"),
])
```

### 3.2 Decorator Pattern

```mermaid
classDiagram
    class original_func {
        +__call__(data)
    }
    
    class step_decorator {
        +name: str
        +version: str
        +__call__(data)
    }
    
    class decorated_func {
        +NAME: str
        +VERSION: str
        +__call__(data)
    }
    
    original_func <-- step_decorator : wraps
    step_decorator <-- decorated_func : creates
```

### 3.3 State Pattern

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Running: start()
    Running --> Stopping: stop()
    Stopping --> Stopped: cleanup()
    Stopped --> [*]
    
    Running --> Processing: new message
    Processing --> Running: complete
```

## 4. Interface Design

### 4.1 Service Interface

```python
class MicroserviceInterface(ABC):
    """Abstract interface for all microservices."""
    
    @abstractmethod
    def procesar_mensaje(self, mensaje: dict) -> dict:
        """Process a single message."""
        pass
    
    @abstractmethod
    def iniciar(self) -> None:
        """Start the service."""
        pass
    
    @abstractmethod
    def detener(self) -> None:
        """Stop the service gracefully."""
        pass
    
    @abstractmethod
    def health_check(self) -> dict:
        """Return service health status."""
        pass
```

### 4.2 Pipeline Step Interface

```python
class PipelineStep(Protocol):
    """Protocol for pipeline steps."""
    
    def __call__(self, data: dict) -> dict:
        """Process input data and return transformed data."""
        ...
    
    @property
    def NAME(self) -> str:
        """Step name identifier."""
        ...
    
    @property
    def VERSION(self) -> str:
        """Step version."""
        ...
```

## 5. Configuration Design

### 5.1 YAML Configuration Schema

```yaml
service:
  name: string
  version: string
  log_level: INFO | DEBUG | WARNING | ERROR
  db_path: string (file path)

pipeline:
  retry_count: integer
  retry_delay: float (seconds)
  timeout: integer (seconds)
  verbose: boolean

queue:
  bootstrap_servers: string[]
  topic: string
  group_id: string
  auto_offset_reset: earliest | latest
```

### 5.2 Configuration Loading

```mermaid
flowchart TD
    A[Load YAML] --> B{Valid?}
    B -->|Yes| C[Parse Config]
    B -->|No| D[Raise Error]
    C --> E[Apply to Service]
    E --> F[Initialize Components]
```

## 6. Error Handling Design

### 6.1 Exception Hierarchy

```mermaid
classDiagram
    class PipelineError {
        +message: str
        +step: str
    }
    
    class ValidationError {
        +field: str
        +value: any
    }
    
    class ProcessingError {
        +original: Exception
    }
    
    class TimeoutError {
        +timeout_seconds: float
    }
    
    PipelineError <|-- ValidationError
    PipelineError <|-- ProcessingError
    PipelineError <|-- TimeoutError
```

### 6.2 Error Recovery Strategy

```mermaid
flowchart TD
    A[Error Occurs] --> B{Retryable?}
    B -->|Yes| C{Has Retries?}
    C -->|Yes| D[Wait Backoff]
    D --> E[Retry]
    E --> A
    C -->|No| F[Log Error]
    B -->|No| F
    F --> G[Return Error]
```

## 7. Data Models

### 7.1 Message Format

```python
from typing import TypedDict

class InputMessage(TypedDict, total=False):
    """Standard input message format."""
    message: str
    correlation_id: str
    timestamp: str
    metadata: dict

class ProcessingResult(TypedDict, total=False):
    """Standard processing result format."""
    processed: bool
    result: dict
    error: str | None
    timestamp: str
```

### 7.2 Service State

```python
class ServiceState(TypedDict):
    """Service runtime state."""
    nombre: str
    ejecutando: bool
    contador_mensajes: int
    mensajes_exitosos: int
    mensajes_fallidos: int
    uptime_seconds: float
```

## 8. Component Wiring

### 8.1 Dependency Injection

```mermaid
flowchart TB
    subgraph Container["Service Container"]
        Svc[Microservice]
    end
    
    subgraph Dependencies["Injected Dependencies"]
        Log[Logger]
        Pipe[Pipeline]
        DB[Database]
    end
    
    subgraph Config["Configuration"]
        Yaml[YAML Config]
        Env[Environment]
    end
    
    Config --> Container
    Dependencies --> Container
```

### 8.2 Initialization Sequence

```mermaid
sequenceDiagram
    participant Main
    participant Config
    participant Logger
    participant Pipeline
    participant Service
    
    Main->>Config: Load YAML
    Config-->>Main: config_dict
    Main->>Logger: Initialize
    Logger-->>Main: logger_instance
    Main->>Pipeline: Create instance
    Pipeline-->>Main: pipeline
    Main->>Service: Create with deps
    Service-->>Main: service_instance
    Main->>Service: Start
```

## 9. Extensibility Points

### 9.1 Custom Step Types

```python
# Extend with custom validation
@step(name="custom_validation")
def custom_validator(data):
    # Custom logic
    return validated_data

# Extend with external calls
@step(name="external_api")
def call_external_api(data):
    response = requests.post(API_URL, json=data)
    return response.json()
```

### 9.2 Pipeline Composition

```python
# Nested pipelines
sub_pipeline = Pipeline("sub_processing")
sub_pipeline.set_steps([step_a, step_b])

main_pipeline = Pipeline("main")
main_pipeline.set_steps([
    step_1,
    sub_pipeline,  # Include as step
    step_3
])
```

## 10. Quality Attributes

### 10.1 Non-Functional Requirements

| Attribute | Target | Verification |
|-----------|--------|--------------|
| Performance | < 10ms avg latency | Load testing |
| Availability | 99.9% | Uptime monitoring |
| Scalability | 1000 msg/sec | Stress testing |
| Maintainability | < 5 min MTTR | Incident logs |

### 10.2 Code Quality Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Cyclomatic Complexity | < 10 | SonarQube |
| Coupling | Low | CodeScene |
| Cohesion | High | CodeScene |
| Test Coverage | > 80% | pytest-cov |