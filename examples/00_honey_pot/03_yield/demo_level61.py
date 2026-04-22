"""
DEMO LEVEL 61: Pipeline con Retry y Delay
---------------------------------------
Añade: Configuración global de retry y delay a nivel de Pipeline.
Continúa: Retry step-level de L22.

DIAGRAMA:
[Pipeline: max_retries=3, retry_delay=1]
      |
      v
(paso_inestable) --[fallo]--> [espera 1s]--> retry 1
                       --> [espera 1s]--> retry 2
                       --> [éxito]   --> continuar
"""

import random

from wpipe import Pipeline, step


@step(name="conectar_api")
def conectar_api(data):
    if random.random() < 0.5:
        raise ConnectionError("API no disponible")
    print("✅ API conectada")
    return {"api": "ok"}


@step(name="procesar_respuesta")
def procesar_respuesta(data):
    print("📝 Procesando respuesta...")
    return {"procesado": True}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L61_PipelineRetry",
        verbose=True,
        max_retries=3,
        retry_delay=1,
    )
    pipe.set_steps([conectar_api, procesar_respuesta])
    print("\n>>> Probando retry a nivel de Pipeline...\n")
    pipe.run({})
