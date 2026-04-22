"""
DEMO LEVEL 108: Wsqlite Múltiples Datos
-----------------------------------
Añade: Guardar múltiples datos.
Continúa: L107.

DIAGRAMA:
Wsqlite con varios registros
"""

from wpipe.sqlite import Wsqlite


if __name__ == "__main__":
    print(">>> Múltiples datos...")

    for i in range(3):
        with Wsqlite(db_name="output/multi108.db") as db:
            db.input = {"id": i, "valor": i * 10}
            db.output = {"resultado": i}
            print(f"  ✅ registro {i}")

    print("✅ Completado!")
