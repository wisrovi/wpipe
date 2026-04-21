# 🚀 WPipe v1.6.17

**El motor de orquestación de pipelines más rápido, resiliente y puro para Python.**

WPipe es una librería profesional diseñada para automatizar flujos de trabajo complejos, garantizando que tus datos viajen seguros, tus procesos sean ultra-rápidos y tus fallos sean fáciles de diagnosticar.

[![PyPI version](https://badge.fury.io/py/wpipe.svg)](https://badge.fury.io/py/wpipe)
[![Python versions](https://img.shields.io/pypi/pyversions/wpipe.svg)](https://pypi.org/project/wpipe/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/wpipe/badge/?version=latest)](https://wpipe.readthedocs.io/en/latest/?badge=latest)

---

## 💎 ¿Por qué WPipe?

Diferénciate de los scripts lineales. WPipe te ofrece superpoderes:

| Superpoder | Descripción |
|------------|-------------|
| ⚡ **Modo Relámpago** | Optimización extrema de SQLite (WAL Mode) y sincronización thread-safe para ejecuciones paralelas. |
| 🧵 **Paralelismo Nativo** | Ejecuta tareas en Hilos o Procesos con un solo comando. Bypass del GIL para tareas pesadas de CPU. |
| 🛡️ **Checkpoints Inteligentes** | Resiliencia ante objetos no serializables y referencias circulares. Si el sistema cae, WPipe reanuda exactamente donde se quedó. |
| 🔍 **Captura de Errores Forense** | Olvídate de los errores genéricos. Recibe notificaciones detalladas con el archivo y la línea exacta del fallo. |
| 🧬 **Contratos de Datos** | Valida tu "Bodega" de datos automáticamente con esquemas estrictos pero extensibles. |
| 🔄 **Paridad Síncrona/Asíncrona** | Elige entre `Pipeline` o `PipelineAsync` con el 100% de las mismas funcionalidades. |

---

## 📊 Features (24 Features)

| Feature | Descripción |
|---------|-------------|
| 🔗 Pipeline Orchestration | Crear pipelines con funciones y clases como pasos |
| 🌳 Conditional Branches | Ejecutar diferentes rutas basadas en condiciones de datos |
| 🔄 Retry Logic | Reintentos automáticos con estrategias configurables |
| 🌐 API Integration | Conectar a APIs externas, registrar workers |
| 💾 SQLite Storage | Persistir resultados de ejecución a base de datos |
| ⚠️ Error Handling | Excepciones personalizadas y códigos de error detallados |
| 📋 YAML Configuration | Cargar y gestionar configuraciones |
| 🔀 Nested Pipelines | Componer flujos de trabajo complejos |
| 📊 Progress Tracking | Salida rica en terminal |
| 🧪 Type Hints | Anotaciones de tipo completas |
| 🔒 Memory Control | Utilidades integradas de memoria |
| 🧩 Composable | Componentes reutilizables de pipeline |
| ⚡ Parallel Execution | Ejecutar pasos en paralelo (I/O o CPU bound) |
| 📂 Pipeline Composition | Usar pipelines como pasos de otros pipelines |
| 🎯 Step Decorators | Definir pasos en línea con @step decorator |
| 💾 Checkpointing | Guardar y resumir desde checkpoints |
| ⏱️ Timeouts | Prevenir tareas colgadas con soporte de timeout |
| 📈 Resource Monitoring | Rastrear RAM y CPU durante ejecución |
| 📤 Export | Exportar logs, métricas y estadísticas a JSON/CSV |
| 🎪 Events & Hooks | Eventos pre/post ejecución y hooks personalizados |
| 📉 Alerts | Alertas configurables basadas en métricas |
| 🔐 Type Validation | Validación de esquemas con PipelineContext |
| 🔄 Async Pipeline | Soporte completo para pipelines asíncronos |
| 🏗️ DAG Scheduling | Programación basada en grafos acíclicos dirigida |
| 🌐 Dashboard Web | Dashboard visual en tiempo real |

---

## 🚀 Instalación

```bash
pip install wpipe
```

---

## 📖 Guía Completa

### 1. Conceptos Fundamentales

WPipe se basa en **4 pilares** que puedes combinar libremente:

```python
from wpipe import Pipeline, step, Condition, For, Parallel
```

| Pilar | Uso |
|-------|-----|
| **`step`** | Decorador para definir funciones como pasos del pipeline |
| **`Pipeline`** | Contenedor principal que orquesta la ejecución |
| **`Condition`** | Ramificación condicional basada en expresiones |
| **`For`** | Bucles con validación de parada |
| **`Parallel`** | Ejecución paralela de múltiples pasos |

### 2. Tu Primer Pipeline

```python
from wpipe import Pipeline, step

@step(name="saludar")
def saludar(name):
    return {"mensaje": f"Hola, {name}!"}

pipeline = Pipeline(pipeline_name="miPrimero")
pipeline.set_steps([saludar])

result = pipeline.run({"name": "Mundo"})
# {'mensaje': 'Hola, Mundo!'}
```

### 3. Pipeline con Validación de Tipos

```python
from wpipe import Pipeline, step, PipelineContext

class Usuario(PipelineContext):
    nombre: str
    edad: int
    email: str

@step(name="validar_usuario")
def validar(usuario: Usuario):
    if usuario.edad < 18:
        return {"validado": False, "razon": "menor de edad"}
    return {"validado": True}

pipeline = Pipeline(pipeline_name="validacion")
pipeline.set_steps([validar])

result = pipeline.run({"nombre": "Ana", "edad": 25, "email": "ana@ejemplo.com"})
# {'validado': True}
```

### 4. Ramificaciones Condicionales

```python
from wpipe import Pipeline, step, Condition

@step(name="procesar")
def procesar(data):
    return {"resultado": "procesado"}

@step(name="alerta")
def alertar(data):
    return {"alerta": "¡Datos críticos!"}

pipeline = Pipeline(pipeline_name="condicional")
pipeline.set_steps([
    Condition(
        expression="valor > 100",
        branch_true=[procesar],
        branch_false=[alertar]
    )
])

pipeline.run({"valor": 50})  # Ejecuta alertar
pipeline.run({"valor": 150})  # Ejecuta procesar
```

### 5. Ejecución Paralela

```python
from wpipe import Pipeline, step, Parallel

@step(name="tarea_a")
def tarea_a(data):
    return {"a": "listo"}

@step(name="tarea_b")
def tarea_b(data):
    return {"b": "listo"}

@step(name="tarea_c")
def tarea_c(data):
    return {"c": "listo"}

pipeline = Pipeline(pipeline_name="paralelo")
pipeline.set_steps([
    Parallel(
        steps=[tarea_a, tarea_b, tarea_c],
        max_workers=3
    )
])

result = pipeline.run({})
# Las 3 tareas se ejecutan simultáneamente
```

### 6. Checkpoints (Resiliencia)

```python
from wpipe import Pipeline, step, CheckpointManager

pipeline = Pipeline(pipeline_name="resiliente")

# Definir checkpoint basado en expresión lógica
pipeline.add_checkpoint(
    checkpoint_name="datos_listos",
    expression="temperatura > 0"
)

@step(name="procesar")
def procesar(data):
    return {"status": "completado"}

pipeline.set_steps([procesar])

# Si el sistema cae, WPipe reanuda automáticamente
chk = CheckpointManager("mi_db.db")
if chk.can_resume("resiliente"):
    pipeline.resume()
else:
    pipeline.run({"temperatura": 25})
```

### 7. Reintentos Automáticos

```python
from wpipe import Pipeline, step

@step(name="conexion_api", retry_count=3, retry_delay=1)
def conexion_api(data):
    # Simulamos posible fallo
    if not data.get("disponible"):
        raise ConnectionError("API no disponible")
    return {"conectado": True}

pipeline = Pipeline(pipeline_name="retry")
pipeline.set_steps([conexion_api])
pipeline.run({"disponible": False})  # Reintenta 3 veces antes de fallar
```

### 8. Timeouts

```python
from wpipe import Pipeline, step, timeout_sync

@timeout_sync(seconds=5)
@step(name="tarea_lenta")
def tarea_lenta(data):
    import time
    time.sleep(10)  # Simula tarea lenta
    return {"status": "ok"}

pipeline = Pipeline(pipeline_name="timeout")
pipeline.set_steps([tarea_lenta])
# Si tarda más de 5 segundos, lanza TimeoutError
```

### 9. Pipeline Asíncrono

```python
import asyncio
from wpipe import PipelineAsync, step

@step(name="async_task")
async def async_task(data):
    await asyncio.sleep(1)
    return {"result": "async done"}

async def main():
    pipeline = PipelineAsync(pipeline_name="async_demo")
    pipeline.set_steps([async_task])
    result = await pipeline.run({"data": "test"})
    return result

asyncio.run(main())
```

### 10. Pipelines Anidados

```python
from wpipe import Pipeline, step

# Pipeline hijo
sub_pipeline = Pipeline(pipeline_name="hijo")
sub_pipeline.set_steps([step_a, step_b])

# Pipeline padre que usa el hijo
parent_pipeline = Pipeline(pipeline_name="padre")
parent_pipeline.set_steps([
    paso_inicial,
    sub_pipeline,  # ¡Se ejecuta como un paso más!
    paso_final
])
```

### 11. Exportar Resultados

```python
from wpipe import PipelineExporter

exporter = PipelineExporter("tracking.db")

# Exportar a JSON
json_data = exporter.export_pipeline_logs(format="json")

# Exportar a CSV
csv_data = exporter.export_pipeline_logs(format="csv")

# Exportar estadísticas
stats = exporter.export_statistics(format="json")
```

### 12. Dashboard Web

```python
from wpipe import start_dashboard

# Inicia el dashboard en http://localhost:5000
start_dashboard(db_path="tracking.db", port=5000)
```

---

## 🎯 Uso Avanzado: El Viaje Resiliente

Este ejemplo combina **todas las características** de WPipe:

```python
from wpipe import (
    Pipeline, For, Condition, Parallel, step, to_obj,
    PipelineContext, CheckpointManager, Metric, Severity
)

# 1. Definimos el contrato de datos
class MiContexto(PipelineContext):
    motor: str
    temperatura: float
    nivel_gasolina: str

# 2. Creamos pasos con validación automática
@step(name="VerificarMotor", retry_count=3)
@to_obj(MiContexto)
def verificar_motor(ctx: MiContexto):
    print(f"Chequeando motor: {ctx.motor}")
    return {"temperatura": 85.5}

@step(name="CargarCombustible")
def cargar_combustible(data):
    return {"nivel_gasolina": "completo"}

@step(name="Conducir")
def conducir(data):
    return {"distancia": 100}

# 3. Orquestación de Alto Nivel
viaje = Pipeline(pipeline_name="ViajeLTS", verbose=True)

# Añadimos checkpoint inteligente
viaje.add_checkpoint(
    checkpoint_name="arranque",
    expression="temperatura > 0"
)

# Añadimos alertas
viaje.tracker.add_alert_threshold(
    metric=Metric.PIPELINE_DURATION,
    expression=">5000",
    severity=Severity.WARNING,
    steps=[lambda d: print("⚠ Pipeline lento!")]
)

# 4. Configuramos los pasos
viaje.set_steps([
    verificar_motor,
    Parallel(
        steps=[cargar_combustible, revisar_neumaticos],
        max_workers=2
    ),
    For(
        iterations=10,
        validation_expression="nivel_gasolina != 'vacío'",
        steps=[conducir]
    )
])

# 5. Ejecutamos
results = viaje.run({"motor": "V8", "temperatura": 20})
```

---

## 📊 Observabilidad Completa

WPipe no solo ejecuta, **entiende** tu proceso:

```python
# Análisis de rendimiento
analysis = pipeline.tracker.analysis
stats = analysis.get_stats()

# Estadísticas globales
print(f"Total ejecuciones: {stats['total_pipelines']}")
print(f"Tasa de éxito: {stats['success_rate']}%")
print(f"Duración media: {stats['avg_duration_ms']}ms")

# Detectar cuellos de botella
slow_steps = analysis.get_top_slow_steps(limit=5)
for step in slow_steps:
    print(f"{step['step_name']}: {step['avg_duration_ms']}ms")

# Exportar a JSON/CSV para auditorías
exporter = PipelineExporter("tracking.db")
exporter.export_pipeline_logs(format="json", output_path="reporte.json")
```

---

## 📋 API Reference (Resumen)

| Clase/Función | Descripción |
|--------------|------------|
| `Pipeline` | Pipeline síncrono principal |
| `PipelineAsync` | Pipeline asíncrono |
| `@step(name, version, retry_count, ...)` | Decorador para definir pasos |
| `Condition(expression, branch_true, branch_false)` | Ramificación condicional |
| `For(iterations, validation_expression, steps)` | Bucle con validación |
| `Parallel(steps, max_workers, use_processes)` | Ejecución paralela |
| `CheckpointManager` | Gestor de checkpoints |
| `PipelineExporter` | Exportador de logs/métricas |
| `start_dashboard(port)` | Dashboard web |
| `ResourceMonitor` | Monitor de RAM/CPU |
| `PipelineContext` | TypedDict para validación de tipos |

---

## 🛡️ Calidad y Soporte

| Aspecto | Detalle |
|--------|---------|
| **LTS** | WPipe v1.6+ cuenta con soporte a largo plazo |
| **Test Coverage** | 95%+ pruebas en entornos síncronos y asíncronos |
| **Arquitectura** | Unificación bajo `wsqlite`, sin SQL crudo en el núcleo |
| **Python** | Compatible con Python 3.9+ |

---

## 📄 Licencia

MIT License - Libre para usar, modificar y distribuir.

---

## 🏢 ¿Usas WPipe? (Opcional)

¡Nos encantaría saberlo! Si usas WPipe en producción, nos motiva mucho saberlo.

** badge opcional:**

```markdown
[![Built with WPipe](https://img.shields.io/badge/Built%20with-WPipe-blue)](https://github.com/wisrovi/wpipe)
```

📧 **Contáctanos:** wisrovi.rodriguez@gmail.com

Consulta **USERS.md** para ver la lista completa de usuarios reconocidos.

---

 Diseñado con ❤️ por **William Rodriguez** (wisrovi) para ingenieros que no aceptan menos que la excelencia.