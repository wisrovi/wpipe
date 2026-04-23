"""
DEMO LEVEL 109: Wsqlite Pipeline Integration
-------------------------------------
Adds: Wsqlite con tracking de Pipeline.
Continues: L108.

DIAGRAM:
Pipeline(tracking_db) + Wsqlite
"""

from wpipe import Pipeline, step
from wpipe.sqlite import Wsqlite

@step(name="proceso")
def proceso(data: dict) -> None:

    """Proceso step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Wsqlite + Pipeline integration...")

    db = "output/pipe109.db"
    pipe = Pipeline(pipeline_name="viaje_l109", verbose=True, tracking_db=db)
    pipe.set_steps([proceso])
    pipe.run({})

    with Wsqlite(db_name=db) as wdb:
        wdb.details = {"pipeline": "L109", "status": "completado"}
        print("✅ Datos guardados en pipeline DB")
