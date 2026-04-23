"""
DEMO LEVEL 107: Wsqlite con Pipeline
---------------------------------
Adds: Wsqlite integrado con Pipeline.
Continues: L106.

DIAGRAM:
Pipeline + Wsqlite
"""

from wpipe import Pipeline
from wpipe.sqlite import Wsqlite

def task(data):
    return {"resultado": "ok"}

if __name__ == "__main__":
    print(">>> Pipeline + Wsqlite...")

    db = "output/pipe107.db"
    pipe = Pipeline(pipeline_name="viaje_l107", verbose=True, tracking_db=db)
    pipe.set_steps([task])
    pipe.run({})

    with Wsqlite(db_name=db) as wdb:
        wdb.input = {"test": "data"}
        print(f"✅ Datos guardados")
