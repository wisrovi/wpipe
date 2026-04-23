"""
DEMO LEVEL 65: Combinación Retry + Delay + on_exception
---------------------------------------------------------
Adds: Todas las opciones de recuperación combinadas.
Continues: L64.

DIAGRAM:
[Pipeline: max_retries=3, retry_delay=1, add_error_capture(handler)]
      |
      v
(paso_inestable) --[Error]--> handler --> [espera 1s]--> retry
"""

import random

from wpipe import Pipeline, step

@step(name="sincronizar_datos")
def sincronizar_datos(data: dict) -> None:

    """Sincronizar datos step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    if random.random() < 0.4:
        raise ConnectionError("Sincronización falló")
    print("✅ Datos sincronizados")
    return {"sync": "ok"}

def error_handler(context, error: dict) -> dict:

    """Sincronizar datos step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print(f"⚠️ [MANEJADOR] Error: {error.get('error_message')}")
    return {"manejado": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l65_fullrecovery",
        verbose=True,
        max_retries=3,
        retry_delay=0.5,
    )
    pipe.add_error_capture([error_handler])
    pipe.set_steps([sincronizar_datos])
    print("\n>>> Probando recuperación completa...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(f"Error: {e}")
