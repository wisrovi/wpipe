# Uso como Microservicio

Este modulo contiene ejemplos para usar wpipe como microservicio, procesando mensajes de sistemas de mensajeria como Kafka.

## Concepto

Un microservicio basado en wpipe puede:
- Escuchar mensajes de Kafka u otro sistema de mensajeria
- Procesar cada mensaje usando un pipeline
- Guardar resultados en SQLite
- Reportar estado a la API (opcional)
- Mantener un health check continuo

## Estructura de un Microservicio

```
Microservicio
├── Configuracion (YAML)
├── Pipeline (pasos de procesamiento)
├── Health Checker (hilo de vida)
├── Mensajeria (Kafka u otro)
└── Persistencia (SQLite)
```

## Configuracion

Archivo `config.yaml`:
```yaml
name: Microservicio_1
version: v1.0
kafka_server: localhost:9092
pipeline_use: true
pipeline_server: http://localhost:8418
pipeline_token_server: mysecrettoken
sqlite_db_name: register.db
```

## Clases Principales

### Microservice
Clase base para crear microservicios:
```python
from examples.microservice.microservice import Microservice
from wkafka.controller import Wkafka

kafka = Wkafka(...)
microservice = Microservice(kafka, config_file="config.yaml")
microservice.set_steps([(step1, "Step1", "v1.0")])
microservice.start_healthchecker()
```

## Ejemplos Disponibles

### 01_basic_service.py
Estructura basica de microservicio sin Kafka.

```bash
python 01_basic_service.py
```

### 02_message_processor.py
Procesador de mensajes basico.

```bash
python 02_message_processor.py
```

### 03_service_with_pipeline.py
Microservicio completo con pipeline integrado.

```bash
python 03_service_with_pipeline.py
```

### 04_worker_health.py
Health checker y registro de worker.

```bash
python 04_worker_health.py
```

## Dependencias

Para usar microservicios:
```bash
pip install wkafka
```

## Ejecucion de Pruebas

```bash
# Ejecutar todos los ejemplos
pytest microservice/ -v

# Ejecutar un ejemplo especifico
python microservice/01_basic_service.py
```
