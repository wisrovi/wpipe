from dataclasses import asdict, is_dataclass
from functools import wraps

from pydantic import BaseModel  # pip install pydantic


def object_to_dict(obj):
    """Convierte cualquier objeto (Pydantic, Dataclass, etc.) a dict recursivamente."""
    if isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [object_to_dict(i) for i in obj]
    if isinstance(obj, BaseModel):
        return obj.model_dump()  # Pydantic v2 (usa .dict() si es v1)
    if is_dataclass(obj):
        return asdict(obj)
    if hasattr(obj, "__dict__"):
        return {k: object_to_dict(v) for k, v in obj.__dict__.items()}
    return obj


def auto_dict_input(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Transformamos todos los argumentos posicionales
        new_args = [object_to_dict(arg) for arg in args]
        # Transformamos todos los argumentos de nombre (kwargs)
        new_kwargs = {k: object_to_dict(v) for k, v in kwargs.items()}
        
        return func(*new_args, **new_kwargs)
    return wrapper
