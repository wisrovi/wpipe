"""
YAML utilities for reading and writing configuration files.
"""

from pathlib import Path
from typing import Any, Union

import yaml


def clean_for_json(obj: Any) -> Any:
    """
    Recursively convert non-serializable objects to strings for JSON compatibility.
    
    Args:
        obj: Object to clean.
        
    Returns:
        Cleaned object (dict, list, or basic type).
    """
    if isinstance(obj, dict):
        return {str(k): clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        # Fallback para objetos complejos como StepMetadata
        return str(obj)


def leer_yaml(archivo: Union[str, Path], verbose: bool = False) -> dict:
    """
    Read a YAML file.

    Args:
        archivo: Path to the YAML file.
        verbose: Enable verbose output.

    Returns:
        Dictionary with YAML contents, or empty dict on error.
    """
    try:
        with open(archivo, encoding="utf-8") as file:
            contenido = yaml.safe_load(file)
            return contenido or {}
    except FileNotFoundError:
        if verbose:
            print(f"El archivo {archivo} no se encontró.")
    except yaml.YAMLError as e:
        if verbose:
            print(f"Error al leer el archivo YAML: {e}")
    return {}


def escribir_yaml(
    archivo: Union[str, Path],
    datos: dict,
    verbose: bool = False,
) -> None:
    """
    Write data to a YAML file.

    Args:
        archivo: Path to the output file.
        datos: Dictionary to write.
        verbose: Enable verbose output.
    """
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            yaml.dump(datos, file, default_flow_style=False, allow_unicode=True)
            if verbose:
                print(f"Archivo YAML creado exitosamente en {archivo}")
    except OSError as e:
        if verbose:
            print(f"Error al escribir el archivo YAML: {e}")
