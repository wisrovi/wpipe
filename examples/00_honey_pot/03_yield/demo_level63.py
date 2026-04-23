"""
DEMO LEVEL 63: Retry Específico por Tipo de Excepción
------------------------------------------------------
Adds: Filtrar qué excepciones se reintentan a nivel de Pipeline.
Continues: L62.

DIAGRAM:
[Pipeline: retry_on_exceptions=(NetworkError, TimeoutError)]
      |
      v
(paso_inestable)
      |
      +-- NetworkError --> [retry]
      +-- ValueError --> [NO retry - failure]
      +-- OK         --> [continuar]
"""

import random

from wpipe import Pipeline, step

class NetworkError(Exception):
    pass

class ValidationError(Exception):
    pass

@step(name="validar_y_conectar")
def validar_y_conectar(data: dict) -> None:

    """Validar y conectar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    val = random.random()
    if val < 0.3:
        raise NetworkError("Red no disponible")
    elif val < 0.5:
        raise ValidationError("Datos inválidos")
    print("✅ Conexión establecida")
    return {"connected": True}

@step(name="finish")
def finish(data: dict) -> None:

    """Finish step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🏁 Proceso finalizado")
    return {"finalizado": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l63_pipelineretryexcept",
        verbose=True,
        max_retries=3,
        retry_delay=0.1,
        retry_on_exceptions=(NetworkError,),
    )
    pipe.set_steps([validar_y_conectar, finish])
    print("\n>>> Probando retry filter por excepción...\n")
    pipe.run({})
