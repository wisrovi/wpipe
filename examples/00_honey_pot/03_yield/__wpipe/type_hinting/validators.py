"""
Type hinting validators for pipeline context and data.

Provides utilities for validating and enforcing type hints throughout the pipeline.
"""

from typing import Any, Dict, Generic, Type, TypeVar, get_args, get_origin

from typing_extensions import TypedDict

T = TypeVar("T")


class PipelineContext(TypedDict, total=False):
    """Base typed context for pipeline steps."""

    step_id: str
    step_name: str
    execution_id: str
    timestamp: str
    metadata: Dict[str, Any]


class TypeValidator:
    """Validate types at runtime."""

    @staticmethod
    def format_pydantic_error(e) -> str:
        """Format Pydantic ValidationError into a simple string."""
        try:
            errors = e.errors()
            msg_parts = []
            for err in errors:
                loc = " -> ".join([str(x) for x in err.get("loc", [])])
                msg = err.get("msg", "Unknown error")
                err_type = err.get("type", "")
                
                if err_type == "missing":
                    msg_parts.append(f"Ausencia de variable obligatoria: '{loc}'")
                elif "type" in err_type:
                    msg_parts.append(f"Tipo de dato incorrecto en '{loc}': {msg}")
                else:
                    msg_parts.append(f"Error en '{loc}': {msg}")
            
            return " | ".join(msg_parts)
        except Exception:
            return str(e)

    @staticmethod
    def validate(value: Any, expected_type: Type[T]) -> T:
        """
        Validate value against expected type.
        Supports standard types, TypedDict, and Pydantic models.
        """
        from pydantic import BaseModel, ValidationError

        # SOPORTE PARA PYDANTIC MODELS
        if isinstance(expected_type, type) and issubclass(expected_type, BaseModel):
            if isinstance(value, dict):
                try:
                    # Intentamos validar y devolver el modelo
                    return expected_type.model_validate(value)
                except ValidationError as e:
                    simple_msg = TypeValidator.format_pydantic_error(e)
                    raise TypeError(f"Validación Pydantic fallida: {simple_msg}") from e
                except Exception as e:
                    raise TypeError(f"Pydantic validation failed: {str(e)}") from e
            elif isinstance(value, expected_type):
                return value
            else:
                raise TypeError(f"Expected dict or {expected_type.__name__}, got {type(value).__name__}")

        origin = get_origin(expected_type)
        args = get_args(expected_type)

        # Caso especial para PipelineContext (TypedDict)
        if hasattr(expected_type, "__annotations__") and not isinstance(expected_type, type):
            if not isinstance(value, dict):
                raise TypeError(f"Expected dict for TypedDict, got {type(value).__name__}")
            # Validamos contra las anotaciones del TypedDict
            return TypeValidator.validate_dict(value, expected_type.__annotations__)

        if origin is None:
            # Si es una clase normal (no genérica)
            try:
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Expected {expected_type.__name__}, got {type(value).__name__}"
                    )
            except TypeError:
                # Algunos tipos especiales de typing pueden fallar en isinstance
                pass
            return value

        if origin is dict:
            if not isinstance(value, dict):
                raise TypeError(f"Expected dict, got {type(value).__name__}")

            if args:
                key_type, val_type = args
                for k, v in value.items():
                    if not isinstance(k, key_type):
                        raise TypeError(
                            f"Dict key must be {key_type.__name__}, got {type(k).__name__}"
                        )
                    if not isinstance(v, val_type):
                        raise TypeError(
                            f"Dict value must be {val_type.__name__}, got {type(v).__name__}"
                        )

            return value

        if origin is list:
            if not isinstance(value, list):
                raise TypeError(f"Expected list, got {type(value).__name__}")

            if args:
                item_type = args[0]
                for item in value:
                    if not isinstance(item, item_type):
                        raise TypeError(
                            f"List item must be {item_type.__name__}, got {type(item).__name__}"
                        )

            return value

        return value

    @staticmethod
    def validate_dict(data: Dict[str, Any], schema: Dict[str, Type]) -> Dict[str, Any]:
        """
        Validate dictionary against schema.

        Args:
            data: Dictionary to validate
            schema: Dictionary with type requirements

        Returns:
            Validated dictionary

        Raises:
            TypeError: If validation fails
            KeyError: If required key is missing
        """
        validated = {}

        for key, expected_type in schema.items():
            if key not in data:
                raise KeyError(f"Required key '{key}' not found in data")

            validated[key] = TypeValidator.validate(data[key], expected_type)

        return validated


class GenericPipeline(Generic[T]):
    """Generic pipeline with type parameters."""

    def __init__(self, context_type: Type[T]):
        """
        Initialize generic pipeline.

        Args:
            context_type: Type of context flowing through pipeline
        """
        self.context_type = context_type

    def validate_context(self, context: Any) -> T:
        """
        Validate context against pipeline type.

        Args:
            context: Context to validate

        Returns:
            Validated context

        Raises:
            TypeError: If context doesn't match expected type
        """
        return TypeValidator.validate(context, self.context_type)
