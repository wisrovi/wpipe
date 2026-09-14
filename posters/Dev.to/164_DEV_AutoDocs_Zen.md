# Auto-Documenting Architecture: Say Goodbye to Stale Diagrams

Documentation is the first casualty of shipping. We write beautiful Mermaid diagrams, push them to the README, then refactor everything in a sprint and never touch the docs again. Three months later, the diagram is a museum piece and the README is a friendly lie.

What if documentation regenerated itself from the code?

## The Documentation Debt Epidemic

Every project accumulates documentation debt: diagrams that don't match reality, wiki pages that contradict the source, onboarding docs that describe systems that no longer exist. The root cause is structural — manual docs and living code are on different cadences. Code changes constantly; nobody updates docs with the same rhythm.

The typical "fix" is more process: doc gates in CI, mandatory updates, documentation sprints. It never holds because it fights human behavior instead of eliminating the task.

## The Only Documentation That Works: Generated Docs

The alternative is to make documentation an **output of the pipeline itself**. When the diagram, the metadata, and the execution history are derived from code and runtime data, "out of date" stops being a thing.

wpipe embraces generation:

- **Mermaid graphs from code**: the DAG of your pipeline is generated from `set_steps()`. No hand-drawn nodes.
- **Step metadata**: `name`, `version`, `retry_count`, and the registered function are introspectable.
- **Runtime tracing**: every run is written to a tracker SQL database, so the "what really happened" is always available.

```python
from wpipe import Pipeline, step

@step(name="enrich", version="v1.4", retry_count=2)
def enrich(data):
    return {"enriched": data["raw"].upper()}

pipe = Pipeline(pipeline_name="autodocs", tracking_db="docs.db")
pipe.set_steps([enrich])

# The Mermaid flow is generated from the pipeline definition.
pipe.run({"raw": "hello"})
```

## What Stops Being a Problem

| Problem | Manual docs | wpipe generated |
| :--- | :--- | :--- |
| Stale diagrams | Guaranteed | Impossible (generated) |
| Unknown version of a step | "Ask Juan" | In the code/tracked |
| What ran in production | Logs buried | Tracker SQL query |
| Onboarding drift | Slow | Docs always match code |

## Conclusion

Documentation doesn't have to be a second job. When your orchestrator treats docs as a first-class generated artifact, your README finally reflects reality — on the day you write it and every day after.

> The best documentation is the one that can't go stale, because it doesn't exist until the code exists.

#AutoDocs #Mermaid #wpipe #Python #DeveloperExperience