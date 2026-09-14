# Executable Specifications: The Pipeline as Its Own Requirements

## The Requirements Handoff

Requirements travel poorly. The business describes a flow; the architect draws it; the developer implements something adjacent; a year later nobody can prove the final pipeline matches the original spec. Traceability — the word auditors love and engineers dread — fails because the spec and the implementation are different artifacts.

## Close the Gap: Specs That Run

If the specification is written in executable form, the round trip disappears. A pipeline definition — `set_steps`, `@step` metadata, data contracts — is simultaneously:

- a **requirements document** (what should happen, in what order),
- an **implementation** (it runs), and
- a **test artifact** (it can be validated and asserted against).

```python
from wpipe import Pipeline, step

@step(name="must_extract", retry_count=2)
def must_extract(data):
    return {"rows": data["source"]["items"]}

@step(name="must_dedupe", retry_count=2)
def must_dedupe(data):
    return {"unique_ids": {r["id"] for r in data["rows"]}}

pipe = Pipeline(pipeline_name="spec")
pipe.set_steps([must_extract, must_dedupe], config_path="requirements.yml")

# Each step's contract, retries, and ordering ARE the executable spec.
pipe.run({"source": {"items": []}})
```

## What Executable Specs Enable

- **Automatic traceability**: every requirement is a step that ran; the tracker proves it.
- **Audit-ready**: "does the dedupe step exist and run?" — answered by a query.
- **Impossible drift**: the spec and the behavior can't diverge, they're the same code.

## Battle Card

| Concern | Paper spec | Executable spec (wpipe) |
| :--- | :--- | :--- |
| Lives in | DOC/PDF | Git |
| Matches reality | Usually not | Always (same artifact) |
| Testable | No | Yes |
| Audit evidence | Signatures | Tracker SQL |
| Update cost | New round | Commit |

## Conclusion

The strongest requirements are the ones that cannot fail to be implemented — because implementing them *is* writing them. Executable specifications turn the pipeline into a self-verifying contract between intent and reality.

#RequirementsEngineering #Traceability #wpipe #Python #DataEngineering