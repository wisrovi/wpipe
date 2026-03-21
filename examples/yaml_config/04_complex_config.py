"""
Ejemplo 04: Configuracion Compleja con Múltiples Secciones

Este ejemplo demonstra configuraciones complejas con múltiples
secciones y perfiles de configuración.
"""

import os
import tempfile
from wpipe import Pipeline
from wpipe.util import leer_yaml, escribir_yaml


def paso_extraccion(data: dict) -> dict:
    """Paso de extraccion."""
    return {"extraido": True, "datos": data.get("fuente", "unknown")}


def paso_transformacion(data: dict) -> dict:
    """Paso de transformacion."""
    return {"transformado": True, "procesado": True}


def paso_carga(data: dict) -> dict:
    """Paso de carga."""
    return {"cargado": True, "destino": data.get("destino", "unknown")}


def crear_config_multientorno():
    """Crea configuracion con multiples entornos."""
    config = {
        "aplicacion": {"nombre": "etl_multientorno", "version": "1.0.0"},
        "entornos": {
            "desarrollo": {
                "base_url": "http://localhost:8418",
                "debug": True,
                "workers": 1,
            },
            "pruebas": {
                "base_url": "http://test-api.ejemplo.com",
                "debug": True,
                "workers": 2,
            },
            "produccion": {
                "base_url": "https://api.ejemplo.com",
                "debug": False,
                "workers": 8,
            },
        },
        "pipeline": {
            "timeout": 300,
            "reintentos": 3,
            "pasos": ["extraccion", "transformacion", "carga"],
        },
        "conexiones": {
            "oracle": {"host": "oracle.db.local", "puerto": 1521, "sid": "ORCL"},
            "postgresql": {"host": "pg.db.local", "puerto": 5432, "base_datos": "mydb"},
        },
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        escribir_yaml(f.name, config)
        return f.name


def main():
    print("=" * 70)
    print("CONFIGURACION COMPLEJA MULTIENTORNO")
    print("=" * 70)

    print("\n--- Paso 1: Crear Configuracion Multientorno ---")
    config_path = crear_config_multientorno()
    print(f"Configuracion creada: {config_path}")

    print("\n--- Paso 2: Leer Configuracion Completa ---")
    config = leer_yaml(config_path)
    print(f"\nAplicacion: {config['aplicacion']['nombre']}")
    print(f"Version: {config['aplicacion']['version']}")

    print("\n--- Paso 3: Seleccionar Entorno ---")

    entorno_actual = "desarrollo"
    entorno_config = config["entornos"][entorno_actual]

    print(f"\nEntorno seleccionado: {entorno_actual}")
    print(f"  Base URL: {entorno_config['base_url']}")
    print(f"  Debug: {entorno_config['debug']}")
    print(f"  Workers: {entorno_config['workers']}")

    print("\n--- Paso 4: Configurar Pipeline por Entorno ---")

    pipeline_config = config["pipeline"]
    api_config = entorno_config

    print(f"\nConfiguracion del pipeline:")
    print(f"  Timeout: {pipeline_config['timeout']}")
    print(f"  Reintentos: {pipeline_config['reintentos']}")
    print(f"  Pasos: {pipeline_config['pasos']}")

    print("\n--- Paso 5: Crear Pipelines Segun Pasos ---")

    pasos_disponibles = {
        "extraccion": paso_extraccion,
        "transformacion": paso_transformacion,
        "carga": paso_carga,
    }

    pipeline_pasos = []
    for paso_nombre in pipeline_config["pasos"]:
        if paso_nombre in pasos_disponibles:
            pipeline_pasos.append(
                (pasos_disponibles[paso_nombre], paso_nombre.capitalize(), "v1.0")
            )

    pipeline = Pipeline(verbose=api_config["debug"])
    pipeline.set_steps(pipeline_pasos)

    print(f"Pipeline configurado con {len(pipeline_pasos)} pasos")

    print("\n--- Paso 6: Ejecutar Pipeline ---")

    datos = {"fuente": "oracle", "destino": "postgresql", "entorno": entorno_actual}

    resultado = pipeline.run(datos)

    print(f"\nResultado:")
    for clave, valor in resultado.items():
        print(f"  {clave}: {valor}")

    print("\n--- Paso 7: Cambiar a Entorno de Produccion ---")

    entorno_produccion = "produccion"
    prod_config = config["entornos"][entorno_produccion]

    print(f"\nEntorno: {entorno_produccion}")
    print(f"  Base URL: {prod_config['base_url']}")
    print(f"  Debug: {prod_config['debug']}")
    print(f"  Workers: {prod_config['workers']}")

    print("\n--- Paso 8: Conectar a Base de Datos ---")

    db_oracle = config["conexiones"]["oracle"]
    db_pg = config["conexiones"]["postgresql"]

    print(f"\nOracle:")
    print(f"  Host: {db_oracle['host']}")
    print(f"  Puerto: {db_oracle['puerto']}")
    print(f"  SID: {db_oracle['sid']}")

    print(f"\nPostgreSQL:")
    print(f"  Host: {db_pg['host']}")
    print(f"  Puerto: {db_pg['puerto']}")
    print(f"  Base de datos: {db_pg['base_datos']}")

    os.unlink(config_path)
    print(f"\n[OK] Archivo temporal eliminado")

    print("\n" + "=" * 70)
    print("BENEFICIOS DE CONFIGURACION COMPLEJA")
    print("=" * 70)
    print("""
Ventajas de configuracion multientorno:

1. Un solo archivo de configuracion
2. Cambio rapido entre entornos
3. Parametros especificos por entorno
4. Secciones organizadas (app, pipeline, conexiones)
5. Reutilizacion de configuraciones

Estructura recomendada:
- aplicacion: metadatos
- entornos: configuracion por ambiente
- pipeline: parametros de ejecucion
- conexiones: cadenas de conexion
""")


if __name__ == "__main__":
    main()
