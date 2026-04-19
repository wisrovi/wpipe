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
    """
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_sns(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_sns(i) for i in data]
    return data


def object_to_dict(obj: Any) -> Any:
    """
    Recursively convert any object (Pydantic, Dataclass, etc.) to dict.
    """
    if obj is None:
        return {}
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


def to_obj(arg: Any = None) -> Callable:
    """
    Decorator that converts dict arguments to SimpleNamespace objects.
    Supports @to_obj and @to_obj(PipelineContextClass)
    """
    from wpipe.type_hinting.validators import TypeValidator

    def actual_decorator(func: Callable, schema: Any = None) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Identificamos el diccionario de datos (bodega)
            data_arg = None
            data_idx = -1
            
            for i, val in enumerate(args):
                if isinstance(val, dict):
                    data_arg = val
                    data_idx = i
                    break
            
            # 1. Validación de esquema
            if schema and data_arg is not None:
                TypeValidator.validate(data_arg, schema)

            # 2. Conversión a objeto
            new_args = list(args)
            if data_idx != -1:
                new_args[data_idx] = dict_to_sns(data_arg)
            
            # 3. Ejecución
            result = func(*new_args, **kwargs)
            
            # 4. Aseguramos que el retorno sea un dict no-nulo para WPipe
            if result is None:
                return data_arg if data_arg is not None else {}
                
            res_dict = object_to_dict(result)
            
            # Si el resultado es vacío pero la bodega no, devolvemos la bodega
            if not res_dict and data_arg is not None:
                return data_arg
                
            return res_dict if res_dict is not None else {}
        return wrapper

    # Si se usó como @to_obj (sin paréntesis)
    # Detectamos si 'arg' es una función normal y no una clase de contexto
    if callable(arg) and not isinstance(arg, type):
        return actual_decorator(arg)

    # Si se usó como @to_obj(Schema)
    def factory(f: Callable) -> Callable:
        return actual_decorator(f, schema=arg)

    return factory


def auto_dict_input(func: Callable) -> Callable:
    """
    Decorator that converts any object arguments to dicts.
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
    """
    def decorator(func: Callable) -> Any:
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
