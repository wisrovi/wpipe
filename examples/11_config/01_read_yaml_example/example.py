"""
Example 01: Reading YAML Configuration Files

This example demonstrates how to read configuration files
stored in YAML format.
"""

import os
import tempfile

from wpipe.util import escribir_yaml, leer_yaml


def crear_config_ejemplo() -> str:
    """Create an example configuration file.

    Returns:
        str: Path to the created temporary YAML configuration file.
    """
    config = {
        "servicio": "pipeline_procesamiento",
        "version": "1.0.0",
        "entorno": "desarrollo",
        "configuracion": {"timeout": 30, "reintentos": 3, "verbose": True},
        "api": {"base_url": "http://localhost:8418", "token": "token_secreto"},
        "base_datos": {"tipo": "sqlite", "nombre": "datos.db"},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        escribir_yaml(f.name, config)
        return f.name


def main() -> None:
    """Execute the YAML reading example workflow."""
    print("=" * 70)
    print("LECTURA DE ARCHIVOS YAML")
    print("=" * 70)

    print("\n--- Paso 1: Crear Archivo de Configuracion ---")
    config_path = crear_config_ejemplo()
    print(f"Archivo creado: {config_path}")

    print("\n--- Paso 2: Leer Configuracion Completa ---")

    config = leer_yaml(config_path)
    print("\nConfiguracion leida:")
    print(f"  Servicio: {config.get('servicio')}")
    print(f"  Version: {config.get('version')}")
    print(f"  Entorno: {config.get('entorno')}")

    print("\n--- Paso 3: Leer Secciones Especificas ---")

    configuracion = config.get("configuracion", {})
    print("\nConfiguracion:")
    print(f"  Timeout: {configuracion.get('timeout')}")
    print(f"  Reintentos: {configuracion.get('reintentos')}")
    print(f"  Verbose: {configuracion.get('verbose')}")

    api = config.get("api", {})
    print("\nAPI:")
    print(f"  Base URL: {api.get('base_url')}")
    print(f"  Token: {api.get('token')}")

    bd = config.get("base_datos", {})
    print("\nBase de Datos:")
    print(f"  Tipo: {bd.get('tipo')}")
    print(f"  Nombre: {bd.get('nombre')}")

    print("\n--- Paso 4: Usar Valores en Codigo ---")

    timeout = configuracion.get("timeout", 60)
    verbose = configuracion.get("verbose", False)

    print("\nUsando configuracion:")
    print(f"  Timeout configurado: {timeout} segundos")
    print(f"  Modo verbose: {verbose}")

    if verbose:
        print("  [VERBOSE] Mostrando logs detallados")

    print("\n--- Paso 5: Manejo de Valores por Defecto ---")

    config_minima = {"nombre": "test"}
    timeout_def = config_minima.get("timeout", 30)
    print(f"\nConfig sin timeout, usando valor por defecto: {timeout_def}")

    os.unlink(config_path)
    print("\n[OK] Archivo temporal eliminado")

    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print(
        """
Funciones disponibles:

1. leer_yaml(archivo)
   - Lee un archivo YAML y retorna un diccionario
   - Lanza error si el archivo no existe

2. escribir_yaml(archivo, datos)
   - Escribe un diccionario a un archivo YAML

3. get('clave', default)
   - Obtiene un valor con valor por defecto si no existe
"""
    )


if __name__ == "__main__":
    main()
