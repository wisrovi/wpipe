"""
DEMO LEVEL 126: API + PipelineAsync
----------------------------------
Adds: API con PipelineAsync.
Continues: L125.

DIAGRAM:
PipelineAsync + APIClient
"""

import asyncio

from wpipe import PipelineAsync

async def task(data):
    print("⚡ Tarea async...")
    return {"ok": True}

async def main():
    print(">>> API + async...")

    pipe = PipelineAsync(pipeline_name="viaje_l126", verbose=True)
    pipe.set_steps([task])
    await pipe.run({})

if __name__ == "__main__":
    asyncio.run(main())
