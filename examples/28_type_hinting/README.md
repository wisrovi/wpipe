# Type Hinting Examples

Examples demonstrating type validation and static typing in pipelines.

## Examples

### 01_basic
Basic type hinting and validation.

**Run**: `python 01_basic/basic_typing.py`

**What it shows**:
- Defining typed contexts with TypedDict
- TypeValidator for type checking
- Catching type errors early

### 02_typed_dict
Advanced TypedDict patterns.

**What it shows**:
- Complex nested types
- Optional fields
- Union types

### 03_generic
Generic pipelines with type parameters.

**What it shows**:
- GenericPipeline[T] usage
- Type-safe pipeline composition
- Generic context inheritance

### 04_validation
Advanced validation patterns.

**What it shows**:
- Custom validators
- Schema-based validation
- Conditional type checking

## Key Concepts

- **TypedDict**: Runtime-checkable data structure types
- **TypeValidator**: Runtime type enforcement
- **GenericPipeline**: Type-safe pipeline composition
- **IDE support**: Full autocomplete with type hints

## Common Patterns

```python
# Define typed context
class MyContext(PipelineContext):
    user_id: int
    username: str

# Validate dictionary
validated = TypeValidator.validate_dict(data, {
    "user_id": int,
    "username": str,
})

# Validate single value
user_id = TypeValidator.validate(value, int)

# Generic pipeline
pipeline = GenericPipeline[MyContext](MyContext)
ctx = pipeline.validate_context(data)
```

## Best Practices

1. **Define types early**: Before the pipeline runs
2. **Validate inputs**: At step boundaries
3. **Use generics**: For reusable components
4. **Document schemas**: In TypedDict definitions

## Common Errors

- **TypeError**: Value doesn't match expected type
- **KeyError**: Missing required field in schema
- **AttributeError**: Field not defined in TypedDict

## See Also

- [Type Hinting Documentation](../../wpipe/type_hinting/README.md)
- [Phase 1 Features Guide](../../PHASE_1_FEATURES.md)
