"""
DEMO LEVEL 140: Demo Final - Background Tasks
---------------------------------------------
Adds: Repaso completo de Background functionality.
Continues: L139.

DIAGRAM:
Pipeline con múltiples ejemplos de Background
"""

import time
import threading

from wpipe import Pipeline, step, Condition, Parallel
from wpipe.pipe.components.logic_blocks import Background


# Estado compartido para demostrar ejecución
execution_log = []


@step(name="start")
def start(data):
    print("=" * 50)
    print("🎉 DEMO FINAL - Background Tasks")
    print("=" * 50)
    print("\n📋 Características de Background:")
    print("  • Ejecución sin bloquear el pipeline")
    print("  • Retorno ignorado (no afecta datos)")
    print("  • capture_error=True para manejar fallos")
    print("  • Funciona con PipelineAsync")
    print("  • Acepta funciones, tuplas, y pipelines anidados")
    print()
    execution_log.clear()
    return {"started": True}


@step(name="log_task")
def log_task(data):
    """Tarea de logging en background."""
    print("📝 [BG] Enviando logs...")
    time.sleep(0.1)
    execution_log.append("log")


@step(name="telemetry_task")
def telemetry_task(data):
    """Tarea de telemetría en background."""
    print("📡 [BG] Enviando telemetría...")
    time.sleep(0.1)
    execution_log.append("telemetry")


@step(name="error_capture_handler")
def error_capture_handler(data, error_info):
    print(f"⚠️ [HANDLER] Error capturado: {error_info.get('error_message', 'Unknown')}")
    execution_log.append("error_handled")


@step(name="failing_bg")
def failing_bg(data):
    """Background que falla."""
    raise RuntimeError("Error simulado")


@step(name="normal_task")
def normal_task(data):
    print("✅ Tarea normal completada")
    execution_log.append("normal")


@step(name="finish")
def finish(data):
    print("\n" + "=" * 50)
    print("📊 Ejecución completada!")
    print(f"   Log: {execution_log}")
    print("=" * 50)


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="demo_140", verbose=True)
    pipe.add_error_capture([error_capture_handler])

    pipe.set_steps([
        start,
        # Múltiples backgrounds en paralelo
        Background(log_task),
        Background(telemetry_task),
        # Background que falla pero se captura
        Background(failing_bg, capture_error=True),
        # Tarea normal después de backgrounds
        normal_task,
        finish,
    ])

    result = pipe.run({})

    print("\n✅ Demo completado exitosamente!")
    print("   - Background tasks ejecutados en paralelo")
    print("   - Error capturado sin detener pipeline")
    print("   - Pipeline continuó normalmente")