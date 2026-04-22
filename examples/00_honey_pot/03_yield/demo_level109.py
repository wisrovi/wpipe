"""
DEMO LEVEL 109: Wsqlite Pipeline Integration
-------------------------------------
Añade: Wsqlite con tracking de Pipeline.
Continúa: L108.

DIAGRAMA:
Pipeline(tracking_db) + Wsqlite
"""

from wpipe import Pipeline, step
from wpipe.sqlite import Wsqlite


@step(name="proceso")
def proceso(data):
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Wsqlite + Pipeline integration...")

    db = "output/pipe109.db"
    pipe = Pipeline(pipeline_name="Viaje_L109", verbose=True, tracking_db=db)
    pipe.set_steps([proceso])
    pipe.run({})

    with Wsqlite(db_name=db) as wdb:
        wdb.details = {"pipeline": "L109", "status": "completado"}
        print("✅ Datos guardados en pipeline DB")
