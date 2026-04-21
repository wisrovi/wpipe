# Usage & Test Documentation

## 1. Quick Start

### 1.1 Installation

```bash
# Install wpipe
pip install wpipe

# Verify installation
python -c "from wpipe import Pipeline; print('OK')"
```

### 1.2 Basic Usage Example

```python
from wpipe import Pipeline

# Define processing steps
@step(name="process")
def my_step(data):
    return {"processed": True, "data": data}

# Create and configure pipeline
pipeline = Pipeline(pipeline_name="my_service")
pipeline.set_steps([(my_step, "Process", "v1.0")])

# Execute
result = pipeline.run({"input": "value"})
```

## 2. Usage Examples

### 2.1 Basic Microservice Example

**File:** `examples/24_microservice/01_basic_service_example/example.py`

**Code:**
```python
from wpipe import Pipeline
from wpipe.log import new_logger

class MicroservicioBasico:
    def __init__(self, nombre: str = "microservicio_basico"):
        self.nombre = nombre
        self.ejecutando = False
        self.contador_mensajes = 0
        self.logger = new_logger(process_name=nombre)
        self.pipeline = Pipeline(verbose=True)
        self.pipeline.set_steps([
            (paso_validacion, "Validacion", "v1.0"),
            ( paso_procesamiento, "Procesamiento", "v1.0"),
            (paso_enriquecimiento, "Enriquecimiento", "v1.0"),
        ])
    
    def procesar_mensaje(self, mensaje: dict) -> dict:
        self.contador_mensajes += 1
        try:
            resultado = self.pipeline.run(mensaje)
            return resultado
        except Exception as e:
            return {"error": str(e)}
    
    def iniciar(self):
        self.ejecutando = True
    
    def detener(self):
        self.ejecutando = False

# Usage
servicio = MicroservicioBasico("mi_servicio")
servicio.iniciar()
result = servicio.procesar_mensaje({"mensaje": "hola"})
servicio.detener()
```

### 2.2 Health Check Example

**File:** `examples/24_microservice/05_health_check_example/example.py`

**Code:**
```python
from wpipe import Pipeline, step

@step(name="process")
def process_step(data):
    return {"status": "ok", "processed": True}

pipeline = Pipeline(pipeline_name="test_service")
pipeline.set_steps([process_step])

# Execute pipeline
result = pipeline.run({"test": "data"})
print(f"Process result: {result}")
```

## 3. Test Evidence

### 3.1 Basic Microservice Test

**Command:**
```bash
cd examples/24_microservice/01_basic_service_example
python example.py
```

**Output:**
```
======================================================================
MICROSERVICIO BASICO
======================================================================

--- Creando Microservicio ---

[MICROSERVICIO] servicio_prueba iniciado
  Mensajes procesados: 0

--- Simulando Mensajes ---

[MENSAJE 1] Enviando: {'mensaje': 'hola mundo'}

[PASO] Validando mensaje...
[PASO] Procesando datos...
[PASO] Enriqueciendo datos...

[RESULTADO 1] {'mensaje': 'hola mundo', 'origen': 'servicio_prueba', 'validado': True, 'procesado': True, 'mensaje_upper': 'HOLA MUNDO', 'longitud': 10, 'enriquecido': True, 'timestamp': '2026-04-20T10:09:15.969863'}

[MENSAJE 2] Enviando: {'mensaje': 'procesando datos'}
[RESULTADO 2] {'mensaje': 'procesando datos', 'origen': 'servicio_prueba', 'validado': True, 'procesado': True, 'mensaje_upper': 'PROCESANDO DATOS', 'longitud': 16, 'enriquecido': True, 'timestamp': '2026-04-20T10:09:15.971870'}

[MENSAJE 3] Enviando: {'mensaje': 'mensaje de prueba'}
[RESULTADO 3] {'mensaje': 'mensaje de prueba', 'origen': 'servicio_prueba', 'validado': True, 'procesado': True, 'mensaje_upper': 'MENSAJE DE PRUEBA', 'longitud': 17, 'enriquecido': True, 'timestamp': '2026-04-20T10:09:15.973863'}

[MENSAJE 4] Enviando: {'mensaje': 'otro mensaje'}
[RESULTADO 4] {'mensaje': 'otro mensaje', 'origen': 'servicio_prueba', 'validado': True, 'procesado': True, 'mensaje_upper': 'OTRO MENSAJE', 'longitud': 12, 'enriquecido': True, 'timestamp': '2026-04-20T10:09:15.976461'}

--- Deteniendo Microservicio ---

[MICROSERVICIO] servicio_prueba detenido
  Total mensajes procesados: 4
```

**Analysis:**
- ✅ Service initialized successfully
- ✅ 4 messages processed
- ✅ All validations passed
- ✅ All transformations applied
- ✅ All enrichments added
- ✅ Graceful shutdown completed

### 3.2 Health Check Test

**Command:**
```bash
cd examples/24_microservice/05_health_check_example
python example.py
```

**Output:**
```
Health check: {'service': 'test_service', 'status': 'healthy', 'pipeline_ready': True}
Process result: {'test': 'data', 'status': 'ok', 'processed': True}
```

**Analysis:**
- ✅ Health check endpoint returns healthy status
- ✅ Pipeline is ready for processing
- ✅ Processing returns expected result

### 3.3 Metrics Test

**Command:**
```bash
cd examples/24_microservice/08_service_metrics_example
python example.py
```

**Output:**
```
Metrics: {'requests': 3, 'avg_time': 0.0021452903747558594}
```

**Analysis:**
- ✅ Metrics collection working
- ✅ Average time calculated correctly
- ✅ Request count tracked

### 3.4 Graceful Shutdown Test

**Command:**
```bash
cd examples/24_microservice
python 10_service_graceful_shutdown.py
```

**Output:**
```
Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Before shutdown: {'id': 1, 'processed': True}
Service shutting down gracefully
After shutdown: {'error': 'Service stopped'}
```

**Analysis:**
- ✅ Processing completed before shutdown
- ✅ Graceful shutdown triggered
- ✅ Service stopped correctly

## 4. API Usage Reference

### 4.1 Creating a Pipeline

```python
from wpipe import Pipeline

# Simple pipeline
pipeline = Pipeline(pipeline_name="my_pipeline")
pipeline.set_steps([
    (step_function, "StepName", "v1.0"),
])

# Execute
result = pipeline.run({"input": "data"})
```

### 4.2 Adding Steps

```python
# Single step
pipeline.set_steps([
    (my_function, "MyStep", "v1.0"),
])

# Multiple steps
pipeline.set_steps([
    (step_1, "Step1", "v1.0"),
    (step_2, "Step2", "v1.0"),
    (step_3, "Step3", "v1.0"),
])

# Conditional steps
from wpipe import Condition

pipeline.set_steps([
    Condition(
        expression="value > 10",
        branch_true=[step_a],
        branch_false=[step_b]
    )
])

# Parallel execution
from wpipe import Parallel

pipeline.set_steps([
    Parallel(
        steps=[step_a, step_b, step_c],
        max_workers=3
    )
])

# Loop execution
from wpipe import For

pipeline.set_steps([
    For(
        iterations=5,
        steps=[process_step]
    )
])
```

### 4.3 Using @step Decorator

```python
from wpipe import step

@step(name="mi_paso", version="v1.0", retry_count=3)
def mi_paso(data):
    # Processing logic
    return {"result": data["value"] * 2}

# Use in pipeline
pipeline.set_steps([mi_paso])
```

## 5. Configuration Examples

### 5.1 Basic Configuration

```yaml
service:
  name: my_microservice
  version: v1.0
  log_level: INFO
```

### 5.2 Pipeline Configuration

```yaml
pipeline:
  retry_count: 3
  retry_delay: 1.0
  timeout: 30
  verbose: true
```

### 5.3 Queue Configuration (Kafka)

```yaml
queue:
  bootstrap_servers:
    - localhost:9092
  topic: my_topic
  group_id: my_group
  auto_offset_reset: earliest
```

## 6. Common Patterns

### 6.1 Validation Pattern

```python
@step(name="validate")
def validate_input(data):
    required_fields = ["mensaje"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    return {"validado": True, **data}
```

### 6.2 Transformation Pattern

```python
@step(name="transform")
def transform_data(data):
    return {
        **data,
        "transformed_value": transform_function(data["value"])
    }
```

### 6.3 Error Handling Pattern

```python
@step(name="safe_process")
def safe_process(data):
    try:
        return process(data)
    except Exception as e:
        return {"error": str(e), "processed": False}
```

### 6.4 Logging Pattern

```python
from wpipe.log import new_logger

logger = new_logger(
    process_name="my_service",
    path_file="logs/service_{time}.log"
)

logger.info("Starting process")
logger.debug("Processing data")
logger.error(f"Error: {e}")
```

## 7. Troubleshooting

### 7.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| ImportError | Missing dependencies | `pip install wpipe` |
| ValidationError | Missing required field | Check input message structure |
| TimeoutError | Step took too long | Increase timeout or optimize step |
| SQLite Error | Database locked | Use WAL mode or single connection |

### 7.2 Debug Mode

```python
# Enable verbose logging
pipeline = Pipeline(pipeline_name="debug", verbose=True)

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 8. Performance Tips

1. **Use Parallel for Independent Steps**
   ```python
   # Good: Parallel for independent operations
   Parallel(steps=[step_a, step_b, step_c], max_workers=3)
   ```

2. **Keep Steps Small and Focused**
   ```python
   # Good: Single responsibility
   @step(name="validate")
   def validate(data): ...
   
   @step(name="transform")
   def transform(data): ...
   ```

3. **Use Caching for Expensive Operations**
   ```python
   @step(name="fetch")
   @cache(timeout=300)  # Cache for 5 minutes
   def fetch_data(data): ...
   ```

## 9. Integration Examples

### 9.1 With Flask

```python
from flask import Flask, request, jsonify
from wpipe import Pipeline

app = Flask(__name__)
pipeline = Pipeline()
pipeline.set_steps([process_step])

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    result = pipeline.run(data)
    return jsonify(result)
```

### 9.2 With FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel
from wpipe import Pipeline

app = FastAPI()
pipeline = Pipeline()
pipeline.set_steps([process_step])

class Input(BaseModel):
    data: str

@app.post("/process")
def process(input: Input):
    return pipeline.run(input.dict())
```

### 9.3 With Celery

```python
from celery import Celery
from wpipe import Pipeline

app = Celery('tasks')

@app.task
def process_message(data):
    pipeline = Pipeline()
    pipeline.set_steps([process_step])
    return pipeline.run(data)
```