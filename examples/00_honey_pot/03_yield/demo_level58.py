"""
DEMO LEVEL 58: Retry con Excepciones Específicas
------------------------------------------------
Añade: Control granular de reintentos por tipo de excepción.
Continúa: Retry de L22.

DIAGRAMA:
(operacion_inestable)
      |
      +-- NetworkError   --> [retry 3 veces]
      +-- ValueError  --> [NO reintentar - falla inmediatamente]
      +-- Success    --> [continúa]
"""

import random

from wpipe import Pipeline, step


class NetworkError(Exception):
    pass


@step(
    name="operacion_inestable",
    retry_count=3,
    retry_delay=0.1,
    retry_on_exceptions=(NetworkError,),
)
def operacion_inestable(data):
    val = random.random()
    if val < 0.3:
        raise NetworkError("Conexión perdue")
    elif val < 0.5:
        raise ValueError("Error de valor inválido")
    print("✅ Operación completada exitosamente")
    return {"status": "ok"}


@step(name="verificar_sistema")
def verificar_sistema(data):
    print("✅ Sistema verificado")
    return {"verificado": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L58_SelectiveRetry", verbose=True)
    pipe.set_steps([operacion_inestable, verificar_sistema])
    print("\n>>> Probando retry selectivo...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(f"Error esperado: {e}")
