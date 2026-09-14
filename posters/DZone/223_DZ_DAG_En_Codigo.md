# The DAG in Code: Why Your Flow Should Be Source, Not Screenshots

## The Diagram You Can Execute

A directed acyclic graph is the mental model behind every pipeline. Yet in most tools it lives as a picture — nodes and arrows in a UI — while the real logic hides in a system of unruly callbacks. The picture and the logic never quite agree, and the DAG becomes less a description of the system and more a rumor about it.

## The Alternative: The DAG Is the Code

When the DAG *is* Python, the graph and the execution are one artifact:

```python
from wpipe import Pipeline, step

@step(name="download", retry_count=3)
def download(data):
    return {"file": get(data["url"])}

@step(name="validate", retry_count=2)
def validate(data):
    return {"ok": check(data["file"])}

@step(name="publish", retry_count=3, retry_delay=2)
def publish(data):
    return {"status": push(data["file"])}

pipe = Pipeline(pipeline_name="dag_in_code")
pipe.set_steps([download, validate, publish])
pipe.run({"url": "https://example.com/asset"})
```

`set_steps([download, validate, publish])` is both:

- **the graph**, from which the Mermaid DAG auto-generates, and
- **the executor**, which runs it with checkpoints, retries, and tracking.

## Why Code-Borne DAGs Are Better

- **Diffable**: renaming or reordering steps is a readable diff.
- **Enforceable**: graph structure is lintable/testable in CI.
- **Composable**: sub-DAGs (nested pipelines) build from the same primitives.
- **Unforgeable**: the DAG can't drift from the code, because it is the code.

## Battle Card

| Aspect | UI-drawn DAG | DAG in code (wpipe) |
| :--- | :---: | :---: |
| Execution source | Hidden handlers | The graph itself |
| Diff/history | None | Git-native |
| Auto-docs | Manual export | Generated |
| Testing the flow | Not possible | pytest on steps |
| Trust over time | Wanes | Constant |

## Conclusion

The strongest guarantee a pipeline can have is that its graph and its implementation are the same object. With the DAG living in code, the diagram you look at is literally the program you run.

#DAG #Orchestration #wpipe #Python #Architecture