"""
Ejemplo 02: Escribir Archivos de Configuracion YAML

Este ejemplo demonstra como crear y escribir configuraciones
en archivos YAML.
"""

import os
import tempfile
from wpipe.util import leer_yaml, escribir_yaml


def main():
    print("=" * 70)
    print("ESCRITURA DE ARCHIVOS YAML")
    print("=" * 70)

    print("\n--- Paso 1: Crear Configuracion Simple ---")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config_path = f.name

    config_simple = {"nombre": "mi_pipeline", "version": "1.0.0"}

    escribir_yaml(config_path, config_simple)
    print(f"Archivo creado: {config_path}")

    config_leida = leer_yaml(config_path)
    print(f"Contenido: {config_leida}")

    print("\n--- Paso 2: Crear Configuracion Compleja ---")

    config_compleja = {
        "servicio": "procesamiento_datos",
        "version": "2.0.0",
        "ambiente": "produccion",
        "parametros": {"timeout": 60, "reintentos": 5, " workers": 4},
        "conexiones": {
            "api": {"url": "https://api.ejemplo.com", "key": "clave_secreta"},
            "base_datos": {"host": "localhost", "puerto": 5432, "nombre": "mydb"},
        },
        "caracteristicas": ["feature_a", "feature_b", "feature_c"],
    }

    config_path_compleja = config_path.replace(".yaml", "_compleja.yaml")
    escribir_yaml(config_path_compleja, config_compleja)
    print(f"Archivo complejo creado: {config_path_compleja}")

    print("\n--- Paso 3: Verificar Contenido ---")

    verificacion = leer_yaml(config_path_compleja)
    print("\nVerificacion de escritura:")
    print(f"  Servicio: {verificacion.get('servicio')}")
    print(f"  Parametros timeout: {verificacion.get('parametros', {}).get('timeout')}")
    print(f"  API URL: {verificacion.get('conexiones', {}).get('api', {}).get('url')}")
    print(f"  Caracteristicas: {verificacion.get('caracteristicas')}")

    print("\n--- Paso 4: Actualizar Configuracion Existente ---")

    config_existente = leer_yaml(config_path_compleja)
    config_existente["version"] = "2.1.0"
    config_existente["parametros"]["timeout"] = 120

    escribir_yaml(config_path_compleja, config_existente)

    config_actualizada = leer_yaml(config_path_compleja)
    print("\nConfiguracion actualizada:")
    print(f"  Nueva version: {config_actualizada.get('version')}")
    print(f"  Nuevo timeout: {config_actualizada.get('parametros', {}).get('timeout')}")

    print("\n--- Paso 5: Escribir Configuracion de Pipeline ---")

    config_pipeline = {
        "pipeline": {
            "nombre": "etl_pipeline",
            "pasos": [
                {"nombre": "extraccion", "funcion": "extraer_datos"},
                {"nombre": "transformacion", "funcion": "transformar_datos"},
                {"nombre": "carga", "funcion": "cargar_datos"},
            ],
        },
        "logging": {"nivel": "INFO", "archivo": "pipeline.log"},
    }

    config_pipeline_path = config_path.replace(".yaml", "_pipeline.yaml")
    escribir_yaml(config_pipeline_path, config_pipeline)
    print(f"Configuracion de pipeline: {config_pipeline_path}")

    pipeline_leida = leer_yaml(config_pipeline_path)
    print("\nPasos del pipeline:")
    for paso in pipeline_leida.get("pipeline", {}).get("pasos", []):
        print(f"  - {paso.get('nombre')}: {paso.get('funcion')}")

    print("\n--- Limpieza ---")
    os.unlink(config_path)
    os.unlink(config_path_compleja)
    os.unlink(config_pipeline_path)
    print("[OK] Archivos temporales eliminados")

    print("\n" + "=" * 70)
    print("PATRONES DE ESCRITURA YAML")
    print("=" * 70)
    print("""
Patrones comunes:

1. Crear desde cero:
   config = {"clave": "valor"}
   escribir_yaml("archivo.yaml", config)

2. Actualizar existente:
   config = leer_yaml("archivo.yaml")
   config["nueva_clave"] = valor
   escribir_yaml("archivo.yaml", config)

3. Estructura de pipeline:
   config = {
       "pipeline": {
           "nombre": "...",
           "pasos": [{"nombre": "...", "funcion": "..."}]
       }
   }
""")


if __name__ == "__main__":
    main()
