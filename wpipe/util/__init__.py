"""
Utility functions and decorators for pipeline steps.

Transform decorators:
- to_obj: Convert dict arguments to SimpleNamespace objects
- auto_dict_input: Convert object arguments to dicts
"""

from .transform import auto_dict_input, dict_to_sns, object_to_dict, to_obj
from .utils import escribir_yaml, leer_yaml, read_yaml, write_yaml

__all__ = [
    # Transform decorators
    "to_obj",
    "auto_dict_input",
    "dict_to_sns",
    "object_to_dict",
    # YAML utilities
    "read_yaml",
    "write_yaml",
    "leer_yaml",
    "escribir_yaml",
]
