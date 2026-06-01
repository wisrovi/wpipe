"""
DEMO LEVEL 135: Background para Logging/Telemetría
-------------------------------------------------
Adds: Uso práctico: logging sin bloquear pipeline.
Continues: L134.

DIAGRAM:
Pipeline → Background(telemetry) → main_continues
"""

import time

from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background


@step(name="process_data")
def process_data(data):
    """Procesa datos."""
    print("📊 Procesando datos...")
    data["processed"] = True
    return data


@step(name="telemetry")
def telemetry(data):
    """Envía telemetría (background)."""
    print("📡 [TELEMETRY] Enviando métricas a servidor...")
    time.sleep(0.15)
    print("📡 [TELEMETRY] ✓ Métricas enviadas: cpu=45%, mem=2GB")
    return {}


@step(name="save_result")
def save_result(data):
    """Guarda resultado."""
    print("💾 Guardando resultado...")
    return data


if __name__ == "__main__":
    print(">>> DEMO 135: Background para Logging/Telemetría")
    print("=" * 50)

    start = time.time()

    pipe = Pipeline(pipeline_name="demo_135", verbose=False)
    pipe.set_steps([
        process_data,
        Background(telemetry),
        save_result,
    ])

    result = pipe.run({})

    elapsed = time.time() - start
    print(f"\n⏱️ Pipeline: {elapsed*1000:.0f}ms")
    print("💡 La telemetría se envió SIN bloquear el pipeline!")