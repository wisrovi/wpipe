"""
Decorators module for WPipe.

Provides @step decorator for inline step definitions.
"""

from .step import (
    step,
    StepRegistry,
    AutoRegister,
    DecoratedStep,
    StepMetadata,
    get_step_registry,
    clear_registry,
)

__all__ = [
    "step",
    "StepRegistry",
    "AutoRegister",
    "DecoratedStep",
    "StepMetadata",
    "get_step_registry",
    "clear_registry",
]
