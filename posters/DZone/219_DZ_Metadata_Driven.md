# Metadata-Driven Orchestration: When the Pipeline Knows Itself

## Orchestration Without Self-Knowledge

Most orchestration systems execute steps mechanically: call this function, then this one. They don't *know* what they are — no step names, no versions, no retry policies, no record of the graph they implement. That ignorance becomes cost: debugging requires reconstructing behavior from side effects.

## Metadata Makes the Difference

A metadata-driven pipeline treats its own definition as first-class data:

- **Step metadata** (`name`, `version`, `retry_count`) captured by the `@step` decorator.
- **Graph structure** known from `set_steps()`.
- **Runtime records** written to the tracker on every run.

With three sources of truth wired together, the orchestrator can document itself, debug itself, and adapt — reading its own instruction manual at runtime.

```python
from wpipe import Pipeline, step

@step(name="scrape", version="v1.4", retry_count=3, retry_delay=2)
def scrape(data):
    return {"page": fetch(data["url"])}

@step(name="rank", version="v2.0")
def rank(data):
    return {"score": score(data["page"])}

pipe = Pipeline(pipeline_name="selfaware", tracking_db="meta.db")
pipe.set_steps([scrape, rank])
pipe.run({"url": "https://example.com"})

# The tracker records name, version, duration, result for each step —
# the pipeline's complete self-description.
```

## What Self-Knowledge Buys You

- **Auto-generated docs**: the graph and metadata ARE the documentation.
- **Precise debugging**: every diagnosis starts from a schema of what ran.
- **Cross-step auditing**: version mismatches become visible instantly.
- **Greenfield abstraction**: `Parallel`, checkpoints, and dashboards work off the same metadata.

## Battle Card

| Capability | Blind executor | Metadata-driven (wpipe) |
| :--- | :---: | :---: |
| Knows step names | No | Yes |
| Knows versions | No | Yes |
| Knows graph shape | No | Yes |
| Records runtime | Scattered logs | Structured tracker |
| Self-documents | No | Yes |

## Conclusion

Pipelines that know themselves are easier to run, debug, and document. Making metadata a first-class citizen — rather than an afterthought — is what turns orchestration into engineering.

#Metadata #Orchestration #wpipe #Python #Observability