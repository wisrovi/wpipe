"""
04 SQLite - Advanced Queries

Demonstrates reading and analyzing SQLite data.
"""

import json
import os
from typing import Any

from wpipe import Pipeline
from wpipe.sqlite import Wsqlite, SQLite


def paso_basico(data: dict[str, Any]) -> dict[str, Any]:
    """Process basic data step."""
    return {
        "procesado": True,
        "categoria": data.get("categoria", "general"),
        "valor": data.get("valor", 0),
        "status": "completado",
    }


def crear_dataset() -> str:
    """Create a dataset with different categories and values."""
    db_nombre: str = "ejemplo_avanzado.db"

    if os.path.exists(db_nombre):
        os.remove(db_nombre)

    pipeline: Pipeline = Pipeline(verbose=False)
    pipeline.set_steps([(paso_basico, "Basico", "v1.0")])

    datos: list[dict[str, Any]] = [
        {"categoria": "A", "valor": 100, "region": "norte"},
        {"categoria": "B", "valor": 200, "region": "sur"},
        {"categoria": "A", "valor": 150, "region": "norte"},
        {"categoria": "C", "valor": 300, "region": "este"},
        {"categoria": "B", "valor": 250, "region": "sur"},
    ]

    for datos_entrada in datos:
        with Wsqlite(db_name=db_nombre) as db:
            db.input = datos_entrada
            resultado: dict[str, Any] = pipeline.run(datos_entrada)
            db.output = resultado

    return db_nombre


def main() -> None:
    """Run the advanced queries example."""
    print("=" * 50)
    print("CONSULTAS AVANZADAS")
    print("=" * 50)

    print("\n--- Paso 1: Crear Dataset ---")
    db_nombre: str = crear_dataset()
    print("[OK] Dataset creado")

    print("\n--- Paso 2: Leer Registros ---")

    with SQLite(db_nombre) as db:
        total = db.count_records()
        print(f"Total de registros: {total}")

        records = []
        for i in range(1, total + 1):
            rec = db.read_by_id(i)
            records.append(rec)
            print(f"  ID {i}: {rec.get('input')}")

    print("\n--- Paso 3: Analisis Simple ---")

    valores = []
    categorias = {}
    for rec in records:
        input_data = json.loads(rec.get("input", "{}"))
        output_data = json.loads(rec.get("output", "{}"))
        valor = output_data.get("valor", 0)
        valores.append(valor)
        cat = input_data.get("categoria", "unknown")
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(valor)

    print("\nEstadisticas por categoria:")
    for cat, vals in categorias.items():
        cuenta = len(vals)
        suma = sum(vals)
        promedio = suma / cuenta if cuenta > 0 else 0
        print(f"  {cat}: count={cuenta}, sum={suma}, mean={promedio:.1f}")

    total_valor = sum(valores)
    promedio_total = total_valor / len(valores) if valores else 0
    print(f"\nTotal valor: {total_valor}")
    print(f"Promedio: {promedio_total:.1f}")

    print("\n--- Paso 4: Filtrado ---")

    print("\nRegistros con valor > 150:")
    for rec in records:
        output_data = json.loads(rec.get("output", "{}"))
        if output_data.get("valor", 0) > 150:
            print(f"  {output_data}")

    if os.path.exists(db_nombre):
        os.remove(db_nombre)

    print("\n[OK] Ejemplo completado")


if __name__ == "__main__":
    main()