"""
DEMO LEVEL 106: Wsqlite Básico
-----------------------------
Adds: Base de datos SQLite.
Continues: Analysis de L105.

DIAGRAM:
Wsqlite(db_name) --> CRUD
"""

from wpipe.sqlite import Wsqlite

if __name__ == "__main__":
    print(">>> Wsqlite básico...")

    with Wsqlite(db_name="output/demo106.db") as db:
        db.input = {"speed": 120}
        db.output = {"resultado": "ok"}
        db.details = {"nota": "test"}

        print(f"✅ Guardado: {db.input}")

    print("✅ Completado!")
