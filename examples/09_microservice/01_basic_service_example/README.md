# Basic Microservice Example

Demonstrates the basic structure of a microservice using wpipe without requiring Kafka for local testing.

## What It Does

This example shows how to create a simple microservice with:
- A processing pipeline with multiple steps
- Message validation and enrichment
- Logging functionality
- Start/stop lifecycle management

## Service Flow

```mermaid
graph LR
    A[Receive Message] --> B[Validate]
    B --> C[Process]
    C --> D[Enrich]
    D --> E[Return Result]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Client
    participant Service as MicroserviceBasico
    participant Pipeline
    participant Steps

    Client->>Service: procesar_mensaje(msg)
    Service->>Pipeline: run(msg)
    Pipeline->>Steps: paso_validacion
    Steps-->>Pipeline: validated data
    Pipeline->>Steps: paso_procesamiento
    Steps-->>Pipeline: processed data
    Pipeline->>Steps: paso_enriquecimiento
    Steps-->>Pipeline: enriched data
    Pipeline-->>Service: result
    Service-->>Client: response
```

## Service Structure

```mermaid
graph TB
    subgraph MicroservicioBasico
        A[__init__] --> B[Logger]
        A --> C[Pipeline]
        C --> D[Step: Validation]
        C --> E[Step: Processing]
        C --> F[Step: Enrichment]
    end
    G[Client] --> H[procesar_mensaje]
    H --> I[iniciar/detener]
```

## Service States

```mermaid
stateDiagram-v2
    [*] --> Initialized
    Initialized --> Running: iniciar()
    Running --> Running: procesar_mensaje()
    Running --> Stopped: detener()
    Stopped --> [*]
```

## Processing Pipeline

```mermaid
flowchart LR
    subgraph Input
        A["{mensaje: 'text'}"]
    end
    subgraph Validation
        B[Check 'mensaje' exists]
    end
    subgraph Processing
        C[Convert to uppercase]
        D[Count length]
    end
    subgraph Enrichment
        E[Add timestamp]
        F[Add origin]
    end
    subgraph Output
        G["{validado, mensaje_upper, longitud, enriquecido}"]
    end
    
    A --> B --> C --> D --> E --> F --> G
```

## Usage

```bash
python example.py
```

## Expected Output

```
======================================
MICROSERVICIO BASICO
======================================

--- Creando Microservicio ---
[MICROSERVICIO] servicio_prueba iniciado
  Mensajes procesados: 0

--- Simulando Mensajes ---
[MENSAJE 1] Enviando: {'mensaje': 'hola mundo'}
[MSG-1] Procesando mensaje...
[MSG-1] Completado
[RESULTADO 1] {'validado': True, ...}

--- Deteniendo Microservicio ---
[MICROSERVICIO] servicio_prueba detenido
  Total mensajes procesados: 4
```
