"""
Ejemplo 04: Consultas Avanzadas

Este ejemplo demonstra consultas avanzadas usando SQLite
y analisis de datos con Pandas.
"""

import os
import json
import pandas as pd
from wpipe import Pipeline
from wpipe.sqlite import Wsqlite
from wpipe.sqlite.Sqlite import SQLite


def paso_basico(data: dict) -> dict:
    """Paso basico."""
    return {
        "procesado": True,
        "categoria": data.get("categoria", "general"),
        "valor": data.get("valor", 0),
        "status": "completado",
    }


def crear_dataset_completo():
    """Crea un dataset con diferentes categorias y valores."""
    db_nombre = "ejemplo_avanzado.db"

    if os.path.exists(db_nombre):
        os.remove(db_nombre)

    pipeline = Pipeline(verbose=False)
    pipeline.set_steps([(paso_basico, "Basico", "v1.0")])

    datos = [
        {"categoria": "A", "valor": 100, "region": "norte"},
        {"categoria": "B", "valor": 200, "region": "sur"},
        {"categoria": "A", "valor": 150, "region": "norte"},
        {"categoria": "C", "valor": 300, "region": "este"},
        {"categoria": "B", "valor": 250, "region": "sur"},
        {"categoria": "A", "valor": 120, "region": "oeste"},
        {"categoria": "C", "valor": 350, "region": "este"},
        {"categoria": "B", "valor": 220, "region": "norte"},
    ]

    for datos_entrada in datos:
        with Wsqlite(db_name=db_nombre) as db:
            db.input = datos_entrada
            resultado = pipeline.run(datos_entrada)
            db.output = resultado
            db.details = {"timestamp": pd.Timestamp.now().isoformat()}

    return db_nombre


def main():
    print("=" * 70)
    print("CONSULTAS AVANZADAS")
    print("=" * 70)

    print("\n--- Paso 1: Crear Dataset Completo ---")
    db_nombre = crear_dataset_completo()
    print("[OK] Dataset creado")

    print("\n--- Paso 2: Leer Todos los Datos como DataFrame ---")

    with SQLite(db_nombre) as db:
        df = db.export_to_dataframe()
        print(f"\nTotal de registros: {len(df)}")

        df_input = pd.DataFrame()
        df_output = pd.DataFrame()

        for idx, row in df.iterrows():
            if row["input"]:
                df_input = pd.concat(
                    [df_input, pd.DataFrame([json.loads(row["input"])])],
                    ignore_index=True,
                )
            if row["output"]:
                df_output = pd.concat(
                    [df_output, pd.DataFrame([json.loads(row["output"])])],
                    ignore_index=True,
                )

        print("\nInputs:")
        print(df_input)

        print("\nOutputs:")
        print(df_output)

    print("\n--- Paso 3: Analisis por Categoria ---")

    df_input["output_valor"] = df_output["valor"]

    print("\nEstadisticas por categoria:")
    estadisticas = df_input.groupby("categoria")["output_valor"].agg(
        ["count", "sum", "mean"]
    )
    print(estadisticas)

    print("\n--- Paso 4: Analisis por Region ---")

    print("\nEstadisticas por region:")
    por_region = df_input.groupby("region")["output_valor"].agg(
        ["count", "sum", "mean"]
    )
    print(por_region)

    print("\n--- Paso 5: Filtrado de Registros ---")

    print("\nRegistros con valor > 200:")
    filtrado = df_input[df_input["output_valor"] > 200]
    print(filtrado)

    print("\nRegistros de categoria 'A':")
    categoria_a = df_input[df_input["categoria"] == "A"]
    print(categoria_a)

    print("\n--- Paso 6: Agregacion Multiple ---")

    print("\nResumen completo:")
    resumen = df_input.groupby(["categoria", "region"])["output_valor"].agg(
        [
            ("count", "count"),
            ("sum", "sum"),
            ("mean", "mean"),
            ("min", "min"),
            ("max", "max"),
        ]
    )
    print(resumen)

    print("\n--- Paso 7: Exportar Analisis a CSV ---")

    resumen.to_csv("analisis_resumen.csv")
    print("[OK] Analisis exportado a analisis_resumen.csv")

    print("\n--- Paso 8: Estadisticas Generales ---")

    print("\nEstadisticas generales:")
    print(f"  Total registros: {len(df_input)}")
    print(f"  Valor total: {df_input['output_valor'].sum()}")
    print(f"  Valor promedio: {df_input['output_valor'].mean():.2f}")
    print(f"  Valor minimo: {df_input['output_valor'].min()}")
    print(f"  Valor maximo: {df_input['output_valor'].max()}")

    print("\n" + "=" * 70)
    print("TIPS PARA CONSULTAS AVANZADAS")
    print("=" * 70)
    print("""
1. Usar export_to_dataframe() para obtener todos los datos
2. Parsear campos JSON (input, output, details) con json.loads()
3. Usar Pandas para analisis y filtrado avanzado
4. groupby() para agregaciones por categoria
5. export_to_csv() para guardar analisis
6. count_records() para conteo rapido
7. get_records_by_date_range() para filtrado temporal
""")


if __name__ == "__main__":
    main()
