"""
Decorators module for WPipe.

Provides @step decorator for inline step definitions.
"""

from .step import (
    AutoRegister,
    DecoratedStep,
    StepMetadata,
    StepRegistry,
    clear_registry,
    get_step_registry,
    step,
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
