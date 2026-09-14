# No More Outdated Diagrams: Documentation That Can't Decay

## The Stale Diagram Problem

Every project eventually carries the same cargo: diagrams so outdated that engineers quietly stop looking at them. New hires read them, waste a week, and learn to distrust all documentation. The repair cost is real — and perpetually deferred, because hand-updating docs is unglamorous work nobody schedules.

## Why Staleness Is Guaranteed

Diagrams describe a *moment*; code describes a *trajectory*. Any artifact decoupled from implementation drifts by definition. The only defenses people try — documentation sprints, wiki guards, "sign-off on diagram changes" — all require sustained human effort. None of them hold.

## The Alternative: Generated Artifacts

If a diagram is an output of the pipeline definition, staleness becomes impossible. There is nothing to forget to update, because the diagram regenerates from code.

- Change `set_steps()` → the DAG changes.
- Change a step's `retry_count` → the metadata changes.
- Nothing to draw → nothing to drift.

```python
from wpipe import Pipeline, step

@step(name="raw", retry_count=3)
def raw(data):
    return {"value": data["input"]}

@step(name="final")
def final(data):
    return {"result": data["value"] * 2}

pipe = Pipeline(pipeline_name="fresh")
pipe.set_steps([raw, final])
# Add/reorder steps: the diagram updates itself. No redraw step.
```

## Battle Card

| Artifact | Hand-maintained | Generated (wpipe) |
| :--- | :--- | :--- |
| Truce with reality | Brief | Permanent |
| Update effort | Manual task | None |
| Trust over time | Declines | Constant |
| Code-review impact | None | Visible diff |

## Conclusion

The most reliable diagram is the one with no author — because authors are eventually replaced by drift. Generated-from-code diagrams stay accurate for the life of the system, which is exactly what documentation is supposed to do.

#Architecture #AutoDocs #wpipe #Documentation #Git