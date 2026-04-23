"""
DEMO LEVEL 58: Retry con Excepciones Específicas
------------------------------------------------
Adds: Control granular de reintentos por tipo de excepción.
Continues: Retry de L22.

DIAGRAM:
(operacion_inestable)
      |
      +-- NetworkError   --> [retry 3 veces]
      +-- ValueError  --> [NO reintentar - failure inmediatamente]
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
def operacion_inestable(data: dict) -> None:

    """Operacion inestable step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    val = random.random()
    if val < 0.3:
        raise NetworkError("Conexión perdue")
    elif val < 0.5:
        raise ValueError("Error de valor inválido")
    print("✅ Operación completada exitosamente")
    return {"status": "ok"}

@step(name="verificar_sistema")
def verificar_sistema(data: dict) -> None:

    """Verificar sistema step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("✅ Sistema verificado")
    return {"verificado": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l58_selectiveretry", verbose=True)
    pipe.set_steps([operacion_inestable, verificar_sistema])
    print("\n>>> Probando retry selectivo...\n")
    try:
        pipe.run({})
    except Exception as e:
        print(f"Error esperado: {e}")
