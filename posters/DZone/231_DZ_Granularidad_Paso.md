# Step Granularity: The Design Lever Most Pipelines Get Wrong

## A Step Is a Decision, Not a Unit of Work

Engineers instinctively make steps as big as they can get away with: "load_all", "group_by_ten_dims", "full_etl". It feels efficient, but oversized steps defeat every orchestrator feature that depends on granularity:

- **Checkpoints** can only resume at step boundaries.
- **Retries** re-run the whole step.
- **Parallelism** can only split between steps.
- **Observability** only records per-step metrics.

If your step is a 40-minute mega-task, "retry the step" means "redo 40 minutes", and "resume at the checkpoint" means little. Granularity is the hidden lever behind all of it.

## Right Sizing Steps

A well-sized step is a **single responsibility** that can be re-run cheaply and independently:

- Small enough to undo with a retry (`retry_count` makes sense).
- Large enough to matter (don't fragment into function calls).
- Stateless between runs (its output must be safely reproducible).

```python
from wpipe import Pipeline, step

# Oversized:
@step(name="full_etl", retry_count=3)
def full_etl(data):
    rows = extract(data["source"]); clean(rows); load(rows)
    return {"done": True}

# Right-sized:
@step(name="extract", retry_count=3)
def extract(data):
    return {"rows": pull(data["source"])}

@step(name="clean", retry_count=2)
def clean(data):
    return {"rows": sanitize(data["rows"])}

@step(name="load", retry_count=3, retry_delay=1)
def load(data):
    return {"loaded": write(data["rows"])}
```

## The Benefits at the Right Granularity

| Concern | Coarse step | Fine step |
| :--- | :---: | :--- |
| Resume point | ~Whole job | Near-failure point |
| Retry blast radius | Huge | Small |
| Parallelism options | Closed | Open (`Parallel`) |
| Debug precision | Poor (one blob) | Precise |
| Doc fidelity | Vague | Granular |

## Conclusion

Granularity is a design decision, made invisible by convenience. Steps that carry one responsibility and can be re-run cheaply turn checkpoints, retries, and observability from slogans into actual engineering properties.

#DesignPatterns #Orchestration #wpipe #Python #DataEngineering