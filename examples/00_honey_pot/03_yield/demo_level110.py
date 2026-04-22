"""
DEMO LEVEL 110: Wsqlite Async
-------------------------------
Añade: Wsqlite con PipelineAsync.
Continúa: L109.

DIAGRAMA:
PipelineAsync + Wsqlite
"""

import asyncio

from wpipe import PipelineAsync
from wpipe.sqlite import Wsqlite


async def proceso(data):
    return {"ok": True}


async def main():
    print(">>> Wsqlite + async...")

    db = "output/async110.db"
    pipe = PipelineAsync(pipeline_name="Viaje_L110", verbose=True, tracking_db=db)
    pipe.set_steps([proceso])
    await pipe.run({})

    with Wsqlite(db_name=db) as wdb:
        wdb.details = {"async": "test"}
        print("✅ Async + Wsqlite")


if __name__ == "__main__":
    asyncio.run(main())
