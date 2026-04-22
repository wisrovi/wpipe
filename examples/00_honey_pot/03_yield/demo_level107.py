"""
DEMO LEVEL 107: Wsqlite con Pipeline
---------------------------------
Añade: Wsqlite integrado con Pipeline.
Continúa: L106.

DIAGRAMA:
Pipeline + Wsqlite
"""

from wpipe import Pipeline
from wpipe.sqlite import Wsqlite


def tarea(data):
    return {"resultado": "ok"}


if __name__ == "__main__":
    print(">>> Pipeline + Wsqlite...")

    db = "output/pipe107.db"
    pipe = Pipeline(pipeline_name="Viaje_L107", verbose=True, tracking_db=db)
    pipe.set_steps([tarea])
    pipe.run({})

    with Wsqlite(db_name=db) as wdb:
        wdb.input = {"test": "data"}
        print(f"✅ Datos guardados")
