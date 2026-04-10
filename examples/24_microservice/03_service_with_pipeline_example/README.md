# Microservice with Pipeline Example

Demonstrates a complete microservice with integrated pipeline, YAML configuration, and worker registration.

## What It Does

This example shows how to create a full-featured microservice with:
- YAML-based configuration management
- Worker registration with API server
- Multi-step pipeline processing
- State management
- SQLite persistence support

## Service Flow

```mermaid
graph LR
    A[Load Config] --> B[Register Worker]
    B --> C[Process Message]
    C --> D[Validate]
    D --> E[Process Data]
    E --> F[Save Result]
    F --> G[Return Response]
```

## Service Communication

```mermaid
sequenceDiagram
    participant Config
    participant Service as MicroservicioConPipeline
    participant API as Pipeline Server
    participant Worker
    participant SQLite

    Config->>Service: Load YAML config
    Service->>API: worker_register()
    API-->>Worker: Return worker_id
    Worker-->>Service: Store worker info
    Service->>SQLite: Save worker_id
    loop Process Messages
        Service->>Service: ejecutar(msg)
        Service->>Service: Validate
        Service->>Service: Process
        Service->>Service: Save
    end
    Service-->>SQLite: Store results
```

## Service Structure

```mermaid
graph TB
    subgraph Configuration
        A[YAML Config] --> B[leer_yaml]
    end
    subgraph MicroservicioConPipeline
        B --> C[Logger]
        C --> D[Pipeline]
        D --> E[Worker Registry]
        E --> F[SQLite DB]
    end
    subgraph Pipeline Steps
        G[Validate]
        H[Process]
        I[Save]
    end
    D --> G
    D --> H
    D --> I
```

## Service States

```mermaid
stateDiagram-v2
    [*] --> Loading: __init__
    Loading --> Initialized: Config loaded
    Initialized --> Registering: registrar_worker()
    Registering --> Registered: API response
    Registering --> Offline: API unavailable
    Registered --> Processing: execute()
    Offline --> Processing: execute() (offline mode)
    Processing --> Registered: Complete
    Registered --> Shutdown: detroy
    Shutdown --> [*]
```

## Component Architecture

```mermaid
flowchart TB
    subgraph Core Components
        A[Config (YAML)] 
        B[Pipeline (wpipe)]
        C[Worker (API)]
        D[SQLite (Persistence)]
        E[Logger]
    end
    
    subgraph Pipeline Steps
        F[paso_validar]
        G[paso_procesar]
        H[paso_guardar]
    end
    
    subgraph Methods
        I[registrar_worker]
        J[ejecutar]
        K[obtener_estado]
    end
    
    A --> B
    C --> D
    B --> F
    B --> G
    B --> H
    
    J --> B
    I --> C
    K --> A
```

## Usage

```bash
python example.py
```

## Expected Output

```
======================================
MICROSERVICIO CON PIPELINE INTEGRADO
======================================

--- Creando Microservicio ---
Configuracion:
  Nombre: microservicio_ejemplo
  Version: 1.0.0

--- Registrando Worker ---
  Worker registrado: worker-xxx

--- Procesando Mensajes ---
[MENSAJE 1] Tipo: usuario
  Validado: True
  Procesado: True
  Guardado: True
```
