# Pipeline Composition

Use pipelines as steps within other pipelines for modular, reusable designs.

## Features

- **PipelineAsStep**: Simple pipeline nesting
- **NestedPipelineStep**: Advanced composition with filtering
- **CompositionHelper**: Utilities for context management
- **Flexible merging**: Multiple strategies for result aggregation

## Quick Start

```python
from wpipe import Pipeline
from wpipe.composition import NestedPipelineStep

# Create sub-pipeline (ETL)
etl_pipeline = Pipeline()
etl_pipeline.add_state("extract", extract_data)
etl_pipeline.add_state("transform", transform_data)
etl_pipeline.add_state("load", load_data)

# Create main pipeline
main_pipeline = Pipeline()

# Add sub-pipeline as a step
etl_step = NestedPipelineStep("etl", etl_pipeline)
main_pipeline.add_state("etl", lambda ctx: etl_step.run(ctx))
main_pipeline.add_state("validate", validate_results)

# Execute
result = main_pipeline.run({})
```

## Context Management

### Merge Strategies

```python
# Child values override parent
merged = CompositionHelper.merge_contexts(parent, child, "child_wins")

# Parent values preserved
merged = CompositionHelper.merge_contexts(parent, child, "parent_wins")

# Lists are concatenated
merged = CompositionHelper.merge_contexts(parent, child, "merge_list")
```

### Context Filtering

```python
# Extract specific keys
subset = CompositionHelper.extract_context_subset(context, ["key1", "key3"])

# Validate compatibility
CompositionHelper.validate_context_compatibility(parent_schema, child_schema)
```

## Advanced Usage

### Context Transformation

```python
def filter_input(context):
    """Transform parent context for child."""
    return {"input_data": context.get("data")}

nested = NestedPipelineStep(
    "sub",
    sub_pipeline,
    context_filter=filter_input,
)
```

### Result Filtering

```python
def filter_output(result):
    """Filter child results."""
    return {k: v for k, v in result.items() if not k.startswith("_")}

nested = NestedPipelineStep(
    "sub",
    sub_pipeline,
    result_filter=filter_output,
)
```

## API

### PipelineAsStep

Simple wrapper to treat pipeline as step.

```python
step = PipelineAsStep("name", pipeline)
result = step.run(context)
```

### NestedPipelineStep

Advanced composition with filtering and timing.

```python
nested = NestedPipelineStep(
    name="sub_pipeline",
    pipeline=sub_pipeline,
    context_filter=None,        # Optional transform
    result_filter=None,         # Optional filter
    timeout=None,               # Optional timeout
)

result = nested.run(parent_context)
exec_time = nested.get_execution_time()
```

### CompositionHelper

Static utility methods for composition.

```python
# Merge contexts
merged = CompositionHelper.merge_contexts(parent, child, strategy)

# Extract subset
subset = CompositionHelper.extract_context_subset(context, keys)

# Validate types
CompositionHelper.validate_context_compatibility(schema1, schema2)
```

## Use Cases

- **ETL Workflows**: Separate extract, transform, load
- **Microservices**: Pipeline per domain
- **Modularity**: Reusable sub-pipelines
- **Testing**: Test sub-pipelines independently

## Best Practices

- ✅ Keep sub-pipelines focused and single-purpose
- ✅ Document expected input/output schemas
- ✅ Use context filtering for data hiding
- ✅ Consider timeout for sub-pipelines
- ❌ Don't nest too deeply (>3 levels)
- ❌ Don't share mutable objects in context

## Troubleshooting

**Q: Context conflicts?**
- A: Use explicit merge strategy
- Filter context at boundaries

**Q: Performance degradation?**
- A: Check for unnecessary context copying
- Profile sub-pipeline execution

## See Also

- [Composition Examples](../../examples/17_composition/)
- [Phase 2 Features](../../PHASE_2_FEATURES.md)
