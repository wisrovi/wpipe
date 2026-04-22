"""
DEMO LEVEL 45: Async con Checkpoints
--------------------------------------
Añade: Checkpoints en pipeline async.
Continúa: L44.

DIAGRAMA:
(async iniciar_motor)
      |
      +-- [Checkpoint: engine_on]
      |
      v
(async conducir)
"""

import asyncio

from wpipe import PipelineAsync, step


async def iniciar_motor(data):
    await asyncio.sleep(0.05)
    print("🔑 [ASYNC] Motor iniciado")
    return {"engine": "on"}


async def conducir(data):
    await asyncio.sleep(0.05)
    print("🚗 [ASYNC] Conduciendo...")
    return {"driving": True}


if __name__ == "__main__":

    async def main():
        pipe = PipelineAsync(pipeline_name="Viaje_L45_AsyncCheckpoint", verbose=True)

        pipe.add_checkpoint(
            checkpoint_name="engine_on",
            expression="engine == 'on'",
        )

        pipe.set_steps([iniciar_motor, conducir])
        print("\n>>> Probando async con checkpoints...\n")
        try:
            await pipe.run({})
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
