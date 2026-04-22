"""
DEMO LEVEL 44: Async Parallel
--------------------------------------
Añade: Pasos async en paralelo.
Continúa: L43.

DIAGRAMA:
Parallel(async pasos) {
  |-- (async camara_frontal)
  |-- (async camara_trasera)
  |-- (async radar)
}
"""

import asyncio

from wpipe import PipelineAsync, Parallel


async def camara_frontal(data):
    await asyncio.sleep(0.05)
    print("📷 [ASYNC] Cámara frontal activada")
    return {"frontal": "activa"}


async def camara_trasera(data):
    await asyncio.sleep(0.05)
    print("📷 [ASYNC] Cámara trasera activada")
    return {"trasera": "activa"}


async def radar(data):
    await asyncio.sleep(0.05)
    print("📡 [ASYNC] Radar activado")
    return {"radar": "activo"}


async def main():
    pipe = PipelineAsync(pipeline_name="Viaje_L44_AsyncParallel", verbose=True)
    pipe.set_steps(
        [Parallel(steps=[camara_frontal, camara_trasera, radar], max_workers=3)]
    )
    print("\n>>> Probando async paralelo...\n")
    await pipe.run({})


if __name__ == "__main__":
    asyncio.run(main())
