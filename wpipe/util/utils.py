"""
YAML utilities for reading and writing configuration files.
"""

from pathlib import Path
from typing import Any, Union, Dict

import yaml


def clean_for_json(obj: Any) -> Any:
    """Recursively convert non-serializable objects to strings for JSON compatibility.

    Args:
        obj: Object to clean.

    Returns:
        Cleaned object (dict, list, or basic type).
    """
    if isinstance(obj, dict):
        return {str(k): clean_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    # Fallback for complex objects like StepMetadata
    return str(obj)


def read_yaml(file_path: Union[str, Path], verbose: bool = False) -> Dict[str, Any]:
    """Read a YAML file.

    Args:
        file_path: Path to the YAML file.
        verbose: Enable verbose output.

    Returns:
        Dictionary with YAML contents, or empty dict on error.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            content = yaml.safe_load(file)
            return content or {}
    except FileNotFoundError:
        if verbose:
            print(f"File {file_path} not found.")
    except yaml.YAMLError as error:
        if verbose:
            print(f"Error reading YAML file: {error}")
    return {}


def write_yaml(
    file_path: Union[str, Path],
    data: Dict[str, Any],
    verbose: bool = False,
) -> None:
    """Write data to a YAML file.

    Args:
        file_path: Path to the output file.
        data: Dictionary to write.
        verbose: Enable verbose output.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
            if verbose:
                print(f"YAML file successfully created at {file_path}")
    except OSError as error:
        if verbose:
            print(f"Error writing YAML file: {error}")


# Backward compatibility aliases
leer_yaml = read_yaml
escribir_yaml = write_yaml
