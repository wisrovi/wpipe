"""
DEMO LEVEL 62: on_exception Callback
-------------------------------------
Adds: Callback ejecutado cuando ocurre una excepción.
Continues: Retry de L61.

DIAGRAM:
[Pipeline: add_error_capture(handler)]
      |
      v
(paso_fallido) --[Error]--> handler() --> [log, notificar]
"""

import random

from wpipe import Pipeline, step

@step(name="operacion_peligrosa")
def operacion_peligrosa(data: dict) -> None:

    """Operacion peligrosa step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    if random.random() < 0.4:
        raise RuntimeError("Operación falló")
    print("✅ Operación completada")
    return {"status": "ok"}

def manejador_errores(context, error: dict) -> dict:

    """Operacion peligrosa step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print(f"🔴 [CALLBACK] Error capturado: {error['error_message']}")
    print("📧 Enviando notificación...")
    return {"notificado": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l62_onexception",
        verbose=True,
        max_retries=2,
    )
    pipe.add_error_capture([manejador_errores])
    pipe.set_steps([operacion_peligrosa])
    print("\n>>> Probando callback de excepciones...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(f"Error: {e}")
