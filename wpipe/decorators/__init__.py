"""
Decorators module for WPipe.

Provides @step decorator for inline step definitions.
"""

from typing import Any

_LAZY_MAP = {
    "step": (".step", "step"),
    "StepRegistry": (".step", "StepRegistry"),
    "AutoRegister": (".step", "AutoRegister"),
    "DecoratedStep": (".step", "DecoratedStep"),
    "StepMetadata": (".step", "StepMetadata"),
    "get_step_registry": (".step", "get_step_registry"),
    "clear_registry": (".step", "clear_registry"),
}

def __getattr__(name: str) -> Any:
    """Handle lazy loading of modules."""
    if name in _LAZY_MAP:
        module_path, attr_name = _LAZY_MAP[name]
        import importlib
        module = importlib.import_module(module_path, __package__)
        attr = getattr(module, attr_name)
        globals()[name] = attr
        return attr
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = list(_LAZY_MAP.keys())
