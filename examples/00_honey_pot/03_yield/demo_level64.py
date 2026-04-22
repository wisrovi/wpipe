"""
DEMO LEVEL 64: Delay Exponencial Backoff
-----------------------------------------
Añade: Delay que aumenta exponencialmente en cada retry.
Continúa: L59.

DIAGRAMA:
(operacion) --[fallo]--> delay=1s --> retry
                 --[fallo]--> delay=2s --> retry
                 --[fallo]--> delay=4s --> retry
                 --[OK]    --> continuar
"""

import random

from wpipe import Pipeline, step


class APIError(Exception):
    pass


@step(name="llamar_api", retry_count=4, retry_delay=1)
def llamar_api(data):
    if random.random() < 0.7:
        raise APIError("API temporalmente no disponible")
    print("✅ API respondiendo")
    return {"response": "ok"}


@step(name="procesar")
def procesar(data):
    print("📊 Procesando datos...")
    return {"procesado": True}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L64_ExponentialBackoff",
        verbose=True,
    )
    pipe.set_steps([llamar_api, procesar])
    print("\n>>> Probando exponential backoff...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(f"Error: {e}")
