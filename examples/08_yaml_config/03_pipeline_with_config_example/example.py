"""
Example 03: Pipeline with YAML Configuration

This example demonstrates how to use YAML configuration files
to configure and execute a pipeline.
"""

import os
import tempfile

from wpipe import Pipeline
from wpipe.util import escribir_yaml, leer_yaml


def paso_validacion(data: dict) -> dict:
    """Validation step for input data.

    Args:
        data: Input data dictionary containing validation parameters.

    Returns:
        dict: Validation result with validado and datos_validos flags.
    """
    return {"validado": True, "datos_validos": "datos" in data}


def paso_procesamiento(data: dict) -> dict:
    """Data processing step.

    Args:
        data: Input data dictionary with valor and multiplicador.

    Returns:
        dict: Processing result with procesado flag and calculated resultado.
    """
    multiplicador = data.get("multiplicador", 1)
    return {"procesado": True, "resultado": data.get("valor", 0) * multiplicador}


def paso_formateo(data: dict) -> dict:
    """Output formatting step.

    Args:
        data: Input data dictionary with resultado.

    Returns:
        dict: Formatted output with formateado flag and salida string.
    """
    return {"formateado": True, "salida": f"Resultado: {data.get('resultado', 0)}"}


def crear_config_pipeline() -> str:
    """Create a pipeline configuration YAML file.

    Returns:
        str: Path to the created temporary configuration file.
    """
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


def main() -> None:
    """Execute the pipeline with YAML configuration example."""
    print("=" * 70)
    print("PIPELINE CON CONFIGURACION YAML")
    print("=" * 70)

    print("\n--- Paso 1: Crear Configuracion ---")
    config_path = crear_config_pipeline()
    print(f"Configuracion creada: {config_path}")

    print("\n--- Paso 2: Leer Configuracion ---")
    config = leer_yaml(config_path)
    print("\nConfiguracion cargada:")
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
    print("\nResultado del pipeline:")
    print(f"  Validado: {resultado.get('validado', False)}")
    print(f"  Procesado: {resultado.get('procesado', False)}")
    print(f"  Resultado: {resultado.get('resultado', 'N/A')}")
    print(f"  Formateado: {resultado.get('formateado', False)}")
    print(f"  Salida: {resultado.get('salida', 'N/A')}")

    os.unlink(config_path)
    print("\n[OK] Archivo temporal eliminado")

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
