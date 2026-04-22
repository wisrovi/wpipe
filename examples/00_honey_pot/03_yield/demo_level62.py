"""
DEMO LEVEL 62: on_exception Callback
-------------------------------------
Añade: Callback ejecutado cuando ocurre una excepción.
Continúa: Retry de L61.

DIAGRAMA:
[Pipeline: add_error_capture(handler)]
      |
      v
(paso_fallido) --[Error]--> handler() --> [log, notificar]
"""

import random

from wpipe import Pipeline, step


@step(name="operacion_peligrosa")
def operacion_peligrosa(data):
    if random.random() < 0.4:
        raise RuntimeError("Operación falló")
    print("✅ Operación completada")
    return {"status": "ok"}


def manejador_errores(context, error):
    print(f"🔴 [CALLBACK] Error capturado: {error['error_message']}")
    print("📧 Enviando notificación...")
    return {"notificado": True}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L62_OnException",
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
