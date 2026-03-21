"""
Ejemplo 03: Pipeline con Configuracion YAML

Este ejemplo demonstra como usar archivos de configuracion YAML
para configurar y ejecutar un pipeline.
"""

import os
import tempfile
from wpipe import Pipeline
from wpipe.util import leer_yaml, escribir_yaml


def paso_validacion(data: dict) -> dict:
    """Paso de validacion de datos."""
    return {"validado": True, "datos_validos": "datos" in data}


def paso_procesamiento(data: dict) -> dict:
    """Paso de procesamiento."""
    multiplicador = data.get("multiplicador", 1)
    return {"procesado": True, "resultado": data.get("valor", 0) * multiplicador}


def paso_formateo(data: dict) -> dict:
    """Paso de formateo de salida."""
    return {"formateado": True, "salida": f"Resultado: {data.get('resultado', 0)}"}


def crear_config_pipeline():
    """Crea archivo de configuracion para pipeline."""
    config = {
        "pipeline": {
            "nombre": "pipeline_ejemplo",
            "descripcion": "Pipeline de ejemplo con configuracion YAML",
        },
        "parametros": {"valor": 42, "multiplicador": 10, "verbose": True},
        "pasos": {
            "validacion": {"habilitado": True},
            "procesamiento": {"habilitado": True},
            "formateo": {"habilitado": True},
        },
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        escribir_yaml(f.name, config)
        return f.name


def main():
    print("=" * 70)
    print("PIPELINE CON CONFIGURACION YAML")
    print("=" * 70)

    print("\n--- Paso 1: Crear Configuracion ---")
    config_path = crear_config_pipeline()
    print(f"Configuracion creada: {config_path}")

    print("\n--- Paso 2: Leer Configuracion ---")
    config = leer_yaml(config_path)
    print(f"\nConfiguracion cargada:")
    print(f"  Nombre: {config['pipeline']['nombre']}")
    print(f"  Valor: {config['parametros']['valor']}")
    print(f"  Multiplicador: {config['parametros']['multiplicador']}")
    print(f"  Verbose: {config['parametros']['verbose']}")

    print("\n--- Paso 3: Crear Pipeline con Configuracion ---")

    verbose = config["parametros"]["verbose"]
    pipeline = Pipeline(verbose=verbose)

    pasos_habilitados = []
    if config["pasos"]["validacion"]["habilitado"]:
        pasos_habilitados.append((paso_validacion, "Validacion", "v1.0"))
    if config["pasos"]["procesamiento"]["habilitado"]:
        pasos_habilitados.append((paso_procesamiento, "Procesamiento", "v1.0"))
    if config["pasos"]["formateo"]["habilitado"]:
        pasos_habilitados.append((paso_formateo, "Formateo", "v1.0"))

    pipeline.set_steps(pasos_habilitados)
    print(f"Pasos configurados: {len(pasos_habilitados)}")

    print("\n--- Paso 4: Ejecutar Pipeline ---")

    datos_ejecucion = {
        "datos": "datos_ejemplo",
        "valor": config["parametros"]["valor"],
        "multiplicador": config["parametros"]["multiplicador"],
    }

    print(f"Datos de entrada: {datos_ejecucion}")

    resultado = pipeline.run(datos_ejecucion)

    print("\n--- Paso 5: Resultado ---")
    print(f"\nResultado del pipeline:")
    print(f"  Validado: {resultado.get('validado', False)}")
    print(f"  Procesado: {resultado.get('procesado', False)}")
    print(f"  Resultado: {resultado.get('resultado', 'N/A')}")
    print(f"  Formateado: {resultado.get('formateado', False)}")
    print(f"  Salida: {resultado.get('salida', 'N/A')}")

    os.unlink(config_path)
    print(f"\n[OK] Archivo temporal eliminado")

    print("\n" + "=" * 70)
    print("FLUJO DE TRABAJO")
    print("=" * 70)
    print("""
1. Crear archivo de configuracion YAML
2. Leer configuracion con leer_yaml()
3. Extraer parametros de configuracion
4. Crear pipeline con parametros leidos
5. Configurar pasos basados en habilitadores
6. Ejecutar pipeline con datos
""")


if __name__ == "__main__":
    main()
