"""
DEMO LEVEL 126: API + PipelineAsync
----------------------------------
Añade: API con PipelineAsync.
Continúa: L125.

DIAGRAMA:
PipelineAsync + APIClient
"""

import asyncio

from wpipe import PipelineAsync


async def tarea(data):
    print("⚡ Tarea async...")
    return {"ok": True}


async def main():
    print(">>> API + async...")

    pipe = PipelineAsync(pipeline_name="Viaje_L126", verbose=True)
    pipe.set_steps([tarea])
    await pipe.run({})


if __name__ == "__main__":
    asyncio.run(main())
