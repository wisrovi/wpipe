"""
DEMO LEVEL 42: Step Decorator Async
--------------------------------------
Añade: Funciones async dentro del pipeline.
Continúa: L41.

DIAGRAMA:
(async verificar_bateria) --> [bateria: 85%]
       |
       v
(async iniciar_sistema) --> [sistema: 'ON']
"""

import asyncio

from wpipe import PipelineAsync


async def verificar_bateria(data):
    await asyncio.sleep(0.05)
    print("🔋 [ASYNC] Batería al 85%")
    return {"bateria": 85}


async def iniciar_sistema(data):
    await asyncio.sleep(0.05)
    print("🟢 [ASYNC] Sistema iniciado")
    return {"sistema": "ON"}


if __name__ == "__main__":

    async def main():
        pipe = PipelineAsync(pipeline_name="Viaje_L42_AsyncStep", verbose=True)
        pipe.set_steps([verificar_bateria, iniciar_sistema])
        print("\n>>> Probando funciones async...\n")
        await pipe.run({})

    asyncio.run(main())
