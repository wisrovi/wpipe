"""
DEMO LEVEL 64: Delay Exponencial Backoff
-----------------------------------------
Adds: Delay que aumenta exponencialmente en cada retry.
Continues: L59.

DIAGRAM:
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
def llamar_api(data: dict) -> None:

    """Llamar api step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    if random.random() < 0.7:
        raise APIError("API temporalmente no disponible")
    print("✅ API respondiendo")
    return {"response": "ok"}

@step(name="process")
def process(data: dict) -> None:

    """Process step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📊 Processing data...")
    return {"procesado": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l64_exponentialbackoff",
        verbose=True,
    )
    pipe.set_steps([llamar_api, process])
    print("\n>>> Probando exponential backoff...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(f"Error: {e}")
