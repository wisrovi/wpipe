"""
DEMO LEVEL 108: Wsqlite Múltiples Datos
-----------------------------------
Adds: Guardar múltiples datos.
Continues: L107.

DIAGRAM:
Wsqlite con varios registros
"""

from wpipe.sqlite import Wsqlite

if __name__ == "__main__":
    print(">>> Múltiples datos...")

    for i in range(3):
        with Wsqlite(db_name="output/multi108.db") as db:
            db.input = {"id": i, "valor": i * 10}
            db.output = {"resultado": i}
            print(f"  ✅ record {i}")

    print("✅ Completado!")
