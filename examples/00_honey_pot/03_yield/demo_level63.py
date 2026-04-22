"""
DEMO LEVEL 63: Retry Específico por Tipo de Excepción
------------------------------------------------------
Añade: Filtrar qué excepciones se reintentan a nivel de Pipeline.
Continúa: L62.

DIAGRAMA:
[Pipeline: retry_on_exceptions=(NetworkError, TimeoutError)]
      |
      v
(paso_inestable)
      |
      +-- NetworkError --> [retry]
      +-- ValueError --> [NO retry - falla]
      +-- OK         --> [continuar]
"""

import random

from wpipe import Pipeline, step


class NetworkError(Exception):
    pass


class ValidationError(Exception):
    pass


@step(name="validar_y_conectar")
def validar_y_conectar(data):
    val = random.random()
    if val < 0.3:
        raise NetworkError("Red no disponible")
    elif val < 0.5:
        raise ValidationError("Datos inválidos")
    print("✅ Conexión establecida")
    return {"connected": True}


@step(name="finalizar")
def finalizar(data):
    print("🏁 Proceso finalizado")
    return {"finalizado": True}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L63_PipelineRetryExcept",
        verbose=True,
        max_retries=3,
        retry_delay=0.1,
        retry_on_exceptions=(NetworkError,),
    )
    pipe.set_steps([validar_y_conectar, finalizar])
    print("\n>>> Probando retry filter por excepción...\n")
    pipe.run({})
