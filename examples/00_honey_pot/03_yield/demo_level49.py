"""
DEMO LEVEL 49: Async Tracking
--------------------------------------
Añade: Tracking en pipeline async.
Continúa: L48.

DIAGRAMA:
(async iniciar) --> [tracked]
"""

import asyncio

from wpipe import PipelineAsync


async def iniciar_motor(data):
    await asyncio.sleep(0.05)
    print("🔑 [ASYNC] Motor iniciado y trackeado")
    return {"motor": "on"}


async def main():
    db_path = "output/async_tracking.db"
    pipe = PipelineAsync(
        pipeline_name="Viaje_L49_AsyncTracking",
        verbose=True,
        tracking_db=db_path,
    )
    pipe.set_steps([iniciar_motor])
    print("\n>>> Probando async con tracking...\n")
    result = await pipe.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
