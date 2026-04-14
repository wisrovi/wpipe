# Step Decorators

Define pipeline steps inline using the `@step()` decorator for cleaner, more Pythonic code.

## Features

- **@step() decorator**: Inline step definition
- **Automatic registration**: Steps auto-register in global registry
- **Metadata attachment**: Timeout, dependencies, tags, description
- **Auto-discovery**: Find and register all decorated steps
- **Tag-based filtering**: Register steps by category

## Quick Start

```python
from wpipe import Pipeline
from wpipe.decorators import step, AutoRegister

@step(timeout=30, description="Fetch user data")
def fetch_users(context):
    return {"users": [...]}

@step(depends_on=["fetch_users"], description="Validate users")
def validate_users(context):
    return {"valid_users": [...]}

@step(depends_on=["validate_users"], description="Save to database")
def save_users(context):
    return {"saved_count": 3}

# Auto-register all decorated steps
pipeline = Pipeline()
AutoRegister.register_all(pipeline)

# Execute
result = pipeline.run({})
```

## Decorator Parameters

```python
@step(
    name="my_step",           # Override function name
    timeout=30,               # Timeout in seconds
    depends_on=["fetch"],     # Dependency list
    retry_count=3,            # Retries on failure
    parallel=False,           # Allow parallel execution
    description="...",        # Step description
    tags=["prod", "critical"] # Tag list
)
def my_step(context):
    return {}
```

## Registry Operations

### Get Registry

```python
from wpipe.decorators import get_step_registry

registry = get_step_registry()

# Get all steps
all_steps = registry.get_all()

# Get specific step
step = registry.get("step_name")
```

### Auto-Register All

```python
from wpipe.decorators import AutoRegister

pipeline = Pipeline()
AutoRegister.register_all(pipeline)
```

### Register by Tag

```python
# Register only production steps
AutoRegister.register_by_tag(pipeline, "prod")

# Register only critical steps
AutoRegister.register_by_tag(pipeline, "critical")
```

### Manual Registration

```python
from wpipe.decorators import StepRegistry

registry = StepRegistry()

# Register function
registry.register_func(
    my_func,
    name="my_step",
    timeout=30,
)
```

## Metadata Access

```python
@step(description="Test step", tags=["test"])
def my_step(context):
    return {}

# Access metadata
metadata = my_step._wpipe_metadata
print(metadata.name)        # "my_step"
print(metadata.timeout)     # None
print(metadata.tags)        # ["test"]
print(metadata.func)        # <function my_step>
```

## Advanced Patterns

### Tag Organization

```python
@step(tags=["etl", "extract"])
def extract(): pass

@step(tags=["etl", "transform"])
def transform(): pass

@step(tags=["etl", "load"])
def load(): pass

@step(tags=["analytics"])
def analyze(): pass

# Create ETL pipeline
etl_pipeline = Pipeline()
AutoRegister.register_by_tag(etl_pipeline, "etl")

# Create analytics pipeline
analytics_pipeline = Pipeline()
AutoRegister.register_by_tag(analytics_pipeline, "analytics")
```

### Dependency Chains

```python
@step(name="fetch")
def fetch_data(ctx):
    return {"data": [...]}

@step(name="validate", depends_on=["fetch"])
def validate(ctx):
    return {"valid": True}

@step(name="transform", depends_on=["validate"])
def transform(ctx):
    return {"transformed": [...]}

@step(name="load", depends_on=["transform"])
def load(ctx):
    return {"loaded": True}
```

### Error Handling

```python
@step(name="risky", retry_count=3, timeout=10)
def risky_operation(context):
    # Will retry up to 3 times
    # Will timeout after 10 seconds
    return {}
```

## Best Practices

- ✅ Use descriptive step names
- ✅ Add descriptions for documentation
- ✅ Use tags for organization
- ✅ Declare all dependencies
- ✅ Set reasonable timeouts
- ❌ Don't create circular dependencies
- ❌ Don't modify global state
- ❌ Don't use side effects

## Troubleshooting

**Q: Decorator not working?**
- A: Make sure to import from `wpipe.decorators`
- Check for typos in step name

**Q: Steps not auto-registering?**
- A: Call `AutoRegister.register_all(pipeline)`
- Check that steps are actually decorated

**Q: Dependencies not working?**
- A: Verify dependency names match exactly
- Check for circular dependencies

## API Reference

### @step() Decorator

```python
@step(
    name: Optional[str] = None,
    timeout: Optional[float] = None,
    depends_on: Optional[List[str]] = None,
    retry_count: int = 0,
    parallel: bool = False,
    description: str = "",
    tags: Optional[List[str]] = None,
)
```

### StepRegistry

```python
registry = StepRegistry()
registry.register(decorated_step)
registry.register_func(func, name, **metadata)
registry.get(name) -> DecoratedStep
registry.get_all() -> Dict[str, DecoratedStep]
registry.clear()
```

### AutoRegister

```python
AutoRegister.register_all(pipeline, registry=None)
AutoRegister.register_by_tag(pipeline, tag, registry=None)
```

### Functions

```python
get_step_registry() -> StepRegistry
clear_registry() -> None
```

## See Also

- [Decorator Examples](../../examples/18_decorators/)
- [Phase 2 Features](../../PHASE_2_FEATURES.md)
