"""
DEMO LEVEL 61: Pipeline con Retry y Delay
---------------------------------------
Adds: Configuración global de retry y delay a nivel de Pipeline.
Continues: Retry step-level de L22.

DIAGRAM:
[Pipeline: max_retries=3, retry_delay=1]
      |
      v
(paso_inestable) --[fallo]--> [espera 1s]--> retry 1
                       --> [espera 1s]--> retry 2
                       --> [success]   --> continuar
"""

import random

from wpipe import Pipeline, step

@step(name="conectar_api")
def conectar_api(data: dict) -> None:

    """Conectar api step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    if random.random() < 0.5:
        raise ConnectionError("API no disponible")
    print("✅ API conectada")
    return {"api": "ok"}

@step(name="procesar_respuesta")
def procesar_respuesta(data: dict) -> None:

    """Procesar respuesta step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📝 Procesando respuesta...")
    return {"procesado": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l61_pipelineretry",
        verbose=True,
        max_retries=3,
        retry_delay=1,
    )
    pipe.set_steps([conectar_api, procesar_respuesta])
    print("\n>>> Probando retry a nivel de Pipeline...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(e)
