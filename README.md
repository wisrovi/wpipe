# 🚀 WPipe v1.6.1

**El motor de orquestación de pipelines más rápido, resiliente y puro para Python.**

WPipe es una librería industrial diseñada para automatizar flujos de trabajo complejos, garantizando que tus datos viajen seguros, tus procesos sean ultra-rápidos y tus fallos sean fáciles de diagnosticar.

[![PyPI version](https://badge.fury.io/py/wpipe.svg)](https://badge.fury.io/py/wpipe)
[![Documentation Status](https://readthedocs.org/projects/wpipe/badge/?version=latest)](https://wpipe.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 💎 ¿Por qué WPipe?

Diferénciate de los scripts lineales. WPipe te ofrece superpoderes:

- ⚡ **Modo Relámpago**: Optimización extrema de SQLite (WAL Mode) y monitorización de hardware sin bloqueos. ¡Velocidad de ráfaga real!
- 🧵 **Paralelismo Nativo**: Ejecuta tareas en Hilos o Procesos con un solo comando. Bypass del GIL para tareas pesadas de CPU.
- 🛡️ **Checkpoints Inteligentes**: Define hitos basados en expresiones lógicas. Si el sistema cae, WPipe reanuda exactamente donde se quedó.
- 🔍 **Captura de Errores Forense**: Olvídate de los errores genéricos. Recibe notificaciones detalladas con el archivo y la línea exacta del fallo.
- 🧬 **Contratos de Datos (TypeValidator)**: Valida tu "Bodega" de datos automáticamente con esquemas estrictos pero extensibles.
- 🔄 **Paridad Síncrona/Asíncrona**: Elige entre `Pipeline` o `PipelineAsync` con el 100% de las mismas funcionalidades.

---

## 🛠️ Instalación Instantánea

```bash
pip install wpipe
```

---

## 🚀 Ejemplo de Poder: El Viaje Resiliente

```python
from wpipe import Pipeline, For, Condition, Parallel, step, PipelineContext

# 1. Definimos el contrato de nuestra Bodega
class MiContexto(PipelineContext):
    motor: str
    temperatura: float

# 2. Creamos estados inteligentes
@step(name="Verificar", retry_count=3)
def verificar_motor(ctx: MiContexto):
    return {"temperatura": 85.5}

# 3. Orquestación de Alto Nivel
viaje = Pipeline(pipeline_name="Viaje_LTS", verbose=True)

# Añadimos hitos inteligentes
viaje.add_checkpoint("arranque", expression="temperatura > 0")

viaje.set_steps([
    verificar_motor,
    Parallel(
        steps=[revisar_luces, hechar_gasolina],
        max_workers=2
    ),
    For(iterations=10, steps=[conducir_paso])
])

results = viaje.run({"motor": "V8"})
```

---

## 📊 Observabilidad y Análisis

WPipe no solo ejecuta, **entiende** tu proceso.

- **AnalysisManager**: Obtén estadísticas de éxito, tiempos medios y detecta cuellos de botella automáticamente.
- **ResourceMonitor**: Controla el pico de RAM y el consumo de CPU de cada ejecución.
- **PipelineExporter**: Exporta tus reportes de ejecución a **JSON o CSV** listos para auditoría.

---

## 🌐 Dashboard Web

Visualiza tus pipelines en tiempo real con el dashboard integrado:

```python
from wpipe import start_dashboard

start_dashboard(db_path="mi_tracking.db", port=8000)
```

---

## 🛡️ Soporte y Calidad

- **LTS Policy**: WPipe v1.6+ cuenta con soporte a largo plazo.
- **95% Test Coverage**: Probado rigurosamente en entornos síncronos y asíncronos.
- **Arquitectura Pura**: Unificación total bajo `wsqlite`, eliminando SQL crudo del núcleo.

---

Diseñado con ❤️ por **William Rodriguez** (wisrovi) para ingenieros que no aceptan menos que la perfección.
