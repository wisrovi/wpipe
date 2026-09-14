# Sustainable Code: Measuring Good Software Beyond Speed

We optimize for latency and throughput until the metrics look good, and we call that "performance." But sustained performance — the ability to keep delivering value at a constant energy and maintenance cost — is a different metric entirely.

## Sustainable Code = Code That Lasts

Sustainable software has three properties:

1. **Efficient**: uses only the resources it needs (CPU, RAM, energy).
2. **Maintainable**: the next engineer can change it without fear.
3. **Resilient**: failures are contained, not catastrophic.

Conveniently, these are also the properties of code that's pleasant to work with.

## What Unsustainable Code Looks Like

- A "job" that spins up a 2GB cluster for a 500-row transform.
- A pipeline wrapped in 200 lines of YAML that orchestrates 10 lines of logic.
- A mega-script where steps can't be resumed, re-run, or tested in isolation.

Each of these burns budget — compute, energy, or engineering attention — without adding capability.

## wpipe: Efficiency That's Boring On Purpose

wpipe keeps sustainability structural:

- **Steps are functions**: pure, testable, composable. Maintenance-friendly by design.
- **State is local**: SQLite WAL instead of a fleet of services.
- **Resilience is default**: checkpoints, retries, timeouts — capabilities, not configuration tasks.
- **Footprint is small**: <50MB RAM, so resources serve the workload, not the orchestrator.

```python
from wpipe import Pipeline, step

@step(name="transform", retry_count=2, retry_delay=1)
def transform(data):
    return {"result": data["input"] * 2}

@step(name="report")
def report(data):
    log(data)   # tracker records it automatically too
    return {"done": True}

pipe = Pipeline(pipeline_name="sust")
pipe.set_steps([transform, report])
pipe.run({"input": 21})
```

## Battle Card

| Property | Unsustainable | wpipe |
| :--- | :--- | :--- |
| Resource use | Over-provisioned | <50MB, minimal |
| Change cost | High (platform ceremonies) | Python diff |
| Failure handling | Ad-hoc | Checkpoint + retry |
| Long-term cost | Grows with grief | Stays flat |
| Energy footprint | High | Low |

## Conclusion

Sustainability is a code quality. A pipeline that's cheap to run, cheap to maintain, and cheap to repair is one your future self and the planet will both thank you for.

> Sustainable code is measured in total cost of ownership, not requests per second.

#SustainableCode #CleanCode #wpipe #GreenIT #Python