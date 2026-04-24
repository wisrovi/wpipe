"""
DEMO LEVEL 132: Background con Capture Error
-------------------------------------------
Adds: Background con captura de errores.
Continues: L131.

DIAGRAM:
Background(failing_task, capture_error=True) → error_handler
"""

import time

from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background


@step(name="start")
def start(data):
    """Inicio."""
    print("📌 Iniciando...")
    return {"started": True}


@step(name="failing_background")
def failing_background(data):
    """Tarea que falla en background."""
    print("🔄 [BACKGROUND] Iniciando tarea que fallará...")
    time.sleep(0.05)
    raise RuntimeError("¡Error simulado en background!")
    return {}


@step(name="error_handler")
def error_handler(data, error_info):
    """Manejador de errores."""
    print(f"⚠️ [ERROR CAPTURE] Error capturado: {error_info.get('error_message', 'Unknown')}")
    return data


@step(name="continue_after_error")
def continue_after_error(data):
    """Continúa después del error."""
    print("✅ Pipeline continúa a pesar del error en background!")
    return data


if __name__ == "__main__":
    print(">>> DEMO 132: Background con Capture Error")
    print("=" * 50)

    pipe = Pipeline(pipeline_name="demo_132", verbose=True)
    pipe.add_error_capture([error_handler])

    pipe.set_steps([
        start,
        Background(failing_background, capture_error=True),
        continue_after_error,
    ])

    result = pipe.run({})

    print("\n✅ El pipeline NO se detuvo por el error!")