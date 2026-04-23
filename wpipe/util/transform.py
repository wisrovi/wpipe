"""
Transform decorators for pipeline steps.

Provides decorators for converting between dicts and objects,
and for creating structured state classes from functions.
"""

from dataclasses import asdict, is_dataclass
from functools import wraps
from types import SimpleNamespace
from typing import Any, Callable, Set, Optional

from pydantic import BaseModel


def dict_to_sns(data: Any, _seen: Optional[Set[int]] = None) -> Any:
    """Recursively convert a dictionary to SimpleNamespace.

    Args:
        data: Data to convert.
        _seen: Set of seen object IDs to prevent infinite recursion.

    Returns:
        Converted object.
    """
    # Initialize seen set for cycle detection
    if _seen is None:
        _seen = set()

    # Prevent infinite recursion by tracking object identity
    data_id = id(data)
    if data_id in _seen:
        return f"<Circular Reference to {type(data).__name__}>"
    _seen.add(data_id)

    try:
        if isinstance(data, dict):
            return SimpleNamespace(**{k: dict_to_sns(v, _seen) for k, v in data.items()})
        if isinstance(data, list):
            return [dict_to_sns(i, _seen) for i in data]
        return data
    finally:
        # Remove from seen set when done processing this branch
        _seen.discard(data_id)


def object_to_dict(obj: Any, _seen: Optional[Set[int]] = None) -> Any:
    """Recursively convert any object (Pydantic, Dataclass, etc.) to dict.

    Args:
        obj: Object to convert.
        _seen: Set of seen object IDs to prevent infinite recursion.

    Returns:
        Converted dictionary or original object if not convertible.
    """
    # Initialize seen set for cycle detection
    if _seen is None:
        _seen = set()

    # Handle None
    if obj is None:
        return {}

    # Prevent infinite recursion by tracking object identity
    obj_id = id(obj)
    if obj_id in _seen:
        return f"<Circular Reference to {type(obj).__name__}>"
    _seen.add(obj_id)

    try:
        # Handle dict
        if isinstance(obj, dict):
            return {k: object_to_dict(v, _seen) for k, v in obj.items()}

        # Handle list
        if isinstance(obj, list):
            return [object_to_dict(i, _seen) for i in obj]

        # Handle Pydantic models
        if isinstance(obj, BaseModel):
            return obj.model_dump()

        # Handle dataclasses
        if is_dataclass(obj):
            return asdict(obj)

        # Handle objects with __dict__
        if hasattr(obj, "__dict__"):
            return {k: object_to_dict(v, _seen) for k, v in obj.__dict__.items()}

        # Return primitive types as-is
        return obj
    finally:
        # Remove from seen set when done processing this branch
        _seen.discard(obj_id)


def to_obj(arg: Any = None) -> Callable:
    """Decorator that converts dict arguments to SimpleNamespace objects.

    Supports @to_obj and @to_obj(PipelineContextClass).

    Args:
        arg: Optional schema or function to decorate.

    Returns:
        Decorated function or decorator factory.
    """
    # pylint: disable=import-outside-toplevel
    from wpipe.type_hinting.validators import TypeValidator

    def actual_decorator(func: Callable, schema: Any = None) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Identify the data dictionary (store)
            data_arg = None
            data_idx = -1

            for i, val in enumerate(args):
                if isinstance(val, dict):
                    data_arg = val
                    data_idx = i
                    break

            # 1. Schema validation
            if schema and data_arg is not None:
                TypeValidator.validate(data_arg, schema)

            # 2. Convert to object
            new_args = list(args)
            if data_idx != -1:
                new_args[data_idx] = dict_to_sns(data_arg)

            # 3. Execution
            result = func(*new_args, **kwargs)

            # 4. Ensure return is a non-null dict for WPipe
            if result is None:
                return data_arg if data_arg is not None else {}

            res_dict = object_to_dict(result)

            # If result is empty but store is not, return the store
            if not res_dict and data_arg is not None:
                return data_arg

            return res_dict if res_dict is not None else {}
        return wrapper

    # If used as @to_obj (without parentheses)
    # Detect if 'arg' is a normal function and not a context class
    if callable(arg) and not isinstance(arg, type):
        return actual_decorator(arg)

    # If used as @to_obj(Schema)
    def factory(func: Callable) -> Callable:
        return actual_decorator(func, schema=arg)

    return factory


def auto_dict_input(func: Callable) -> Callable:
    """Decorator that converts any object arguments to dicts.

    Args:
        func: Function to decorate.

    Returns:
        Decorated function.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        new_args = [object_to_dict(arg) for arg in args]
        new_kwargs = {k: object_to_dict(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)

    return wrapper
