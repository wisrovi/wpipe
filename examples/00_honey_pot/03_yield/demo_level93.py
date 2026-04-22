"""
DEMO LEVEL 93: TaskTimer Async
--------------------------
Añade: TaskTimer con PipelineAsync.
Continúa: L92.

DIAGRAMA:
TaskTimer + PipelineAsync
"""

import asyncio

from wpipe import PipelineAsync, TaskTimer


async def tarea(data):
    print("⚡ Tarea async...")
    await asyncio.sleep(0.05)
    return {"ok": True}


async def main():
    with TaskTimer("async93", timeout_seconds=1) as timer:
        pipe = PipelineAsync(pipeline_name="Viaje_L93", verbose=True)
        pipe.set_steps([tarea])
        await pipe.run({})

    print(f"\n⏱️ Tiempo: {timer.elapsed_seconds:.3f}s")


if __name__ == "__main__":
    print(">>> TaskTimer async...")
    asyncio.run(main())
