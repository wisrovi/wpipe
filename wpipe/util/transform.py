"""
Transform decorators for pipeline steps.

Provides decorators for converting between dicts and objects,
and for creating structured state classes from functions.
"""

from dataclasses import asdict, is_dataclass
from functools import wraps
from types import SimpleNamespace
from typing import Any, Callable, Optional

from pydantic import BaseModel


def dict_to_sns(data: Any) -> Any:
    """
    Recursively convert a dictionary to SimpleNamespace.

    Args:
        data: Data to convert.

    Returns:
        SimpleNamespace if dict, original type otherwise.
    """
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_sns(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_sns(i) for i in data]
    return data


def object_to_dict(obj: Any) -> Any:
    """
    Recursively convert any object (Pydantic, Dataclass, etc.) to dict.

    Args:
        obj: Object to convert.

    Returns:
        Dict representation of the object.
    """
    if isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [object_to_dict(i) for i in obj]
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if is_dataclass(obj):
        return asdict(obj)
    if hasattr(obj, "__dict__"):
        return {k: object_to_dict(v) for k, v in obj.__dict__.items()}
    return obj


def to_obj(func: Callable) -> Callable:
    """
    Decorator that converts dict arguments to SimpleNamespace objects.

    This allows accessing dict keys as attributes (e.g., data.name instead of
    data['name']) inside the decorated function.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function that converts dict arguments to objects.

    Example:
        @to_obj
        def process(data):
            print(data.name)  # data is now an object, not a dict
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        new_args = [dict_to_sns(arg) for arg in args]
        new_kwargs = {k: dict_to_sns(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)

    return wrapper


def auto_dict_input(func: Callable) -> Callable:
    """
    Decorator that converts any object arguments to dicts.

    This automatically converts Pydantic models, dataclasses, or any object
    with __dict__ to plain dictionaries before passing to the function.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function that converts object arguments to dicts.

    Example:
        @auto_dict_input
        def process(data):
            print(data)  # data is always a plain dict
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        new_args = [object_to_dict(arg) for arg in args]
        new_kwargs = {k: object_to_dict(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)

    return wrapper


def state(name: str, version: str = "v1.0") -> Callable:
    """
    Decorator that transforms a function into a structured State class.

    The decorated function becomes a callable class with NAME and VERSION
    attributes, useful for pipeline steps that need metadata.

    Args:
        name: The name identifier for the state.
        version: The version string (default: "v1.0").

    Returns:
        A decorator that wraps a function in a StateWrapper class.

    Example:
        @state(name="ProcessData", version="v1.0")
        def process_data(data):
            return {"result": data["value"] * 2}

        # Now can be used as:
        # process_data.NAME -> "ProcessData"
        # process_data.VERSION -> "v1.0"
        # process_data(data) -> calls the original function
    """

    def decorator(func: Callable) -> "StateWrapper":
        class StateWrapper:
            NAME = name
            VERSION = version

            def __init__(self, original_func: Callable):
                self.original_func = original_func
                wraps(original_func)(self)

            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                return self.original_func(*args, **kwargs)

            def __repr__(self) -> str:
                return f"<State: {self.NAME} {self.VERSION}>"

        return StateWrapper(func)

    return decorator
