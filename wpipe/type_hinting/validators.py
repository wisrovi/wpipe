"""
Type hinting validators for pipeline context and data.

Provides utilities for validating and enforcing type hints throughout the pipeline.
"""

from typing import Any, Dict, Generic, List, Type, TypeVar, get_args, get_origin

from pydantic import BaseModel, ValidationError
from typing_extensions import TypedDict

T = TypeVar("T")


class PipelineContext(TypedDict, total=False):
    """
    Base typed context for pipeline steps.

    Attributes:
        step_id: Unique identifier for the step.
        step_name: Human-readable name of the step.
        execution_id: ID of the current pipeline execution.
        timestamp: ISO formatted timestamp.
        metadata: Additional step metadata.
    """

    step_id: str
    step_name: str
    execution_id: str
    timestamp: str
    metadata: Dict[str, Any]


class TypeValidator:
    """
    Utility class for runtime type validation.

    Provides methods to validate values against Python types, TypedDicts,
    and Pydantic models.
    """

    @staticmethod
    def format_pydantic_error(err: ValidationError) -> str:
        """
        Format Pydantic ValidationError into a simple string.

        Args:
            err: The Pydantic ValidationError to format.

        Returns:
            A formatted error message string.
        """
        try:
            errors = err.errors()
            msg_parts = []
            for item in errors:
                loc = " -> ".join([str(x) for x in item.get("loc", [])])
                msg = item.get("msg", "Unknown error")
                err_type = item.get("type", "")

                if err_type == "missing":
                    msg_parts.append(f"Missing required variable: '{loc}'")
                elif "type" in err_type:
                    msg_parts.append(f"Incorrect data type in '{loc}': {msg}")
                else:
                    msg_parts.append(f"Error in '{loc}': {msg}")

            return " | ".join(msg_parts)
        except (AttributeError, KeyError, TypeError):
            return str(err)

    @staticmethod
    def validate(value: Any, expected_type: Type[T]) -> T:
        """
        Validate value against expected type.

        Supports standard types, TypedDict, and Pydantic models.

        Args:
            value: The value to validate.
            expected_type: The type to validate against.

        Returns:
            The validated value (possibly converted by Pydantic).

        Raises:
            TypeError: If validation fails.
        """
        # Support for Pydantic Models
        if isinstance(expected_type, type) and issubclass(expected_type, BaseModel):
            return TypeValidator._validate_pydantic(value, expected_type)

        origin = get_origin(expected_type)
        args = get_args(expected_type)

        # Special case for TypedDict
        if hasattr(expected_type, "__annotations__") and not isinstance(
            expected_type, type
        ):
            if not isinstance(value, dict):
                raise TypeError(
                    f"Expected dict for TypedDict, got {type(value).__name__}"
                )
            return TypeValidator.validate_dict(value, expected_type.__annotations__)

        if origin is None:
            return TypeValidator._validate_base_type(value, expected_type)

        if origin is dict:
            return TypeValidator._validate_dict_type(value, args)

        if origin is list:
            return TypeValidator._validate_list_type(value, args)

        return value

    @staticmethod
    def _validate_pydantic(value: Any, expected_type: Type[BaseModel]) -> Any:
        """Internal helper for Pydantic validation."""
        if isinstance(value, dict):
            try:
                return expected_type.model_validate(value)
            except ValidationError as e:
                simple_msg = TypeValidator.format_pydantic_error(e)
                raise TypeError(f"Pydantic validation failed: {simple_msg}") from e
            except (ValueError, RuntimeError) as e:
                raise TypeError(f"Pydantic validation error: {str(e)}") from e
        elif isinstance(value, expected_type):
            return value
        else:
            raise TypeError(
                f"Expected dict or {expected_type.__name__}, got {type(value).__name__}"
            )

    @staticmethod
    def _validate_base_type(value: Any, expected_type: Type[T]) -> T:
        """Internal helper for base type validation."""
        try:
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Expected {expected_type.__name__}, got {type(value).__name__}"
                )
        except TypeError:
            # Some special typing types might fail isinstance
            pass
        return value

    @staticmethod
    def _validate_dict_type(value: Any, args: tuple) -> Dict[Any, Any]:
        """Internal helper for dict type validation."""
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

    @staticmethod
    def _validate_list_type(value: Any, args: tuple) -> List[Any]:
        """Internal helper for list type validation."""
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

    @staticmethod
    def validate_dict(data: Dict[str, Any], schema: Dict[str, Type]) -> Dict[str, Any]:
        """
        Validate dictionary against schema.

        Args:
            data: Dictionary to validate.
            schema: Dictionary with type requirements.

        Returns:
            Validated dictionary.

        Raises:
            TypeError: If validation fails.
            KeyError: If required key is missing.
        """
        validated = {}

        for key, expected_type in schema.items():
            if key not in data:
                raise KeyError(f"Required key '{key}' not found in data")

            validated[key] = TypeValidator.validate(data[key], expected_type)

        return validated


class GenericPipeline(Generic[T]):
    """
    Generic pipeline with type parameters.

    Attributes:
        context_type: The type of context used in this pipeline.
    """

    def __init__(self, context_type: Type[T]):
        """
        Initialize generic pipeline.

        Args:
            context_type: Type of context flowing through pipeline.
        """
        self.context_type = context_type

    def validate_context(self, context: Any) -> T:
        """
        Validate context against pipeline type.

        Args:
            context: Context to validate.

        Returns:
            The validated context.

        Raises:
            TypeError: If context doesn't match expected type.
        """
        return TypeValidator.validate(context, self.context_type)
