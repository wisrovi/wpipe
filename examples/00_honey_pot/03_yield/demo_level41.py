"""
DEMO LEVEL 41: Pipeline Asíncrono Básico
--------------------------------------
Añade: PipelineAsync para ejecución asíncrona.
Acumula: Pipeline básico de L1.

DIAGRAMA:
(async iniciar_motor) --> [motor: 'ON']
      |
      v
(async verificar_sensores) --> [sensores: 'OK']
"""

import asyncio

from wpipe import PipelineAsync


def iniciar_motor(data):
    print("🔑 [ASYNC] Motor iniciado")
    return {"motor": "ON", "gasolina": 100}


def verificar_sensores(data):
    print("📡 [ASYNC] Sensores verificados")
    return {"sensores": "OK"}


if __name__ == "__main__":

    async def main():
        pipe = PipelineAsync(pipeline_name="Viaje_L41_AsyncBasic", verbose=True)
        pipe.set_steps([iniciar_motor, verificar_sensores])
        print("\n>>> Iniciando pipeline asíncrono...\n")
        await pipe.run({})

    asyncio.run(main())
