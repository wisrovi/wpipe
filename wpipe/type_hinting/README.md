# Type Hinting & Validation

Runtime type validation for pipeline context and data flowing between steps.

## Features

- **TypeValidator**: Runtime type checking at step boundaries
- **PipelineContext**: Typed context TypedDict for pipeline data
- **GenericPipeline**: Generic pipeline with type parameters
- **Schema validation**: Validate dictionaries against schemas

## Quick Start

```python
from typing import TypedDict, Dict
from wpipe import PipelineContext, TypeValidator

# Define typed context
class MyContext(TypedDict):
    user_id: int
    username: str
    email: str

# Validate context
context = {"user_id": 123, "username": "john", "email": "john@example.com"}
validated = TypeValidator.validate(context, MyContext)

# Validate dictionary against schema
schema = {
    "user_id": int,
    "username": str,
    "email": str,
}
validated = TypeValidator.validate_dict(context, schema)

# Use generic pipeline
from wpipe import GenericPipeline
pipeline = GenericPipeline[MyContext](MyContext)
validated_ctx = pipeline.validate_context(context)
```

## API

### TypeValidator

Static utility for runtime type validation.

#### `validate(value: Any, expected_type: Type[T]) -> T`
Validate a value against expected type.

```python
validated = TypeValidator.validate(value, int)
validated = TypeValidator.validate(data, Dict[str, int])
validated = TypeValidator.validate(items, List[str])
```

#### `validate_dict(data: Dict, schema: Dict[str, Type]) -> Dict`
Validate dictionary against schema.

```python
schema = {"id": int, "name": str, "values": list}
validated = TypeValidator.validate_dict(data, schema)
```

### PipelineContext

Base TypedDict for pipeline execution context.

```python
class MyContext(PipelineContext):
    result: str
    error_count: int
```

### GenericPipeline

Generic pipeline with type parameters.

```python
pipeline = GenericPipeline[MyContext](MyContext)
ctx = pipeline.validate_context(data)
```

## Exceptions

- `TypeError`: When type validation fails
- `KeyError`: When required key is missing in schema validation

## Use Cases

- **Type safety**: Catch type errors before production
- **IDE support**: Full type hints for autocomplete
- **Documentation**: Context structure is self-documenting
- **Testing**: Validate mock data matches schema
