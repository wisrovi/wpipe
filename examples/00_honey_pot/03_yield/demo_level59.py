"""
DEMO LEVEL 59: Retry con Delay Variable
--------------------------------------
Añade: delay_delay dinámico basado en número de intento.
Continúa: Retry selectivo de L58.

DIAGRAMA:
(operacion_red) --[Fallo]--> delay=1s --> retry
                 --[Fallo]--> delay=2s --> retry
                 --[Fallo]--> delay=3s --> retry
                 --[OK]     --> continuar
"""

import random

from wpipe import Pipeline, step


@step(name="conectar_servidor", retry_count=5, retry_delay=1)
def conectar_servidor(data):
    if random.random() < 0.6:
        raise ConnectionError("Servidor no responde")
    print("✅ Conectado al servidor")
    return {"connected": True}


@step(name="descargar_datos")
def descargar_datos(data):
    print("📥 Descargando datos...")
    return {"datos": "descargados"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L59_RetryDelay", verbose=True)
    pipe.set_steps([conectar_servidor, descargar_datos])
    print("\n>>> Probando retry con delay...\n")
    pipe.run({})
