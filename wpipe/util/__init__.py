"""
Utility functions and decorators for pipeline steps.

Transform decorators:
- to_obj: Convert dict arguments to SimpleNamespace objects
- auto_dict_input: Convert object arguments to dicts
- state: Create structured state classes from functions
"""

from .transform import auto_dict_input, object_to_dict, state, to_obj
from .utils import escribir_yaml, leer_yaml

__all__ = [
    # Transform decorators
    "to_obj",
    "auto_dict_input",
    "state",
    "object_to_dict",
    # YAML utilities
    "leer_yaml",
    "escribir_yaml",
]
