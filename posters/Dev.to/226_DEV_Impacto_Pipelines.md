# The Impact of a Single Pipeline: Small Decisions, Big Footprints

Every pipeline you deploy makes a decision that compounds: how much infrastructure it asks for, how long it stays alive, how much energy it consumes while idle. Individually, ten megabytes here and a daemon there seem like nothing. Multiplied across an organization's fleet for a year, they become a measurable footprint.

## Where the Impact Hides

- **Idle processes**: schedulers and brokers that stay resident while no job runs.
- **Over-provisioning**: instances sized for the platform's baseline, not the workload.
- **Cold-start fleets**: runtimes that must be kept warm for responsiveness.
- **Amplified retries**: every retry chain repeats the same expensive scaffold.

The paradox: the more "reliable" the platform tries to be, the more machinery it keeps burning fuel between jobs.

## The Lightweight Alternative, Quantified

wpipe inverts the equation — ephemeral work, minimal idle:

- **No idle daemon**: the pipeline runs when triggered, then goes quiet. Idle energy ≈ 0.
- **<50MB RAM**: instances are sized for the actual task, not the platform.
- **Local SQLite state**: no database server to provision, patch, or keep warm.
- **In-process workers**: parallelism when needed, no extra fleet standing by.

```python
from wpipe import Pipeline, step

@step(name="job", retry_count=2, retry_delay=1)
def job(data):
    return {"ok": data["id"]}

pipe = Pipeline(pipeline_name="impact", tracking_db="impact.db")
pipe.set_steps([job])

# Triggered externally (cron/CI) close to the work. No fleet behind it.
pipe.run({"id": 1})
```

## Battle Card

| Dimension | Heavy platform | wpipe |
| :--- | :---: | :---: |
| Idle energy | Constant (daemons) | ~Zero |
| RAM baseline | 500MB - 2GB+ | <50MB |
| Infra provisioned | Scheduler+Broker+DB | None |
| Units of compute paid | Fleet + workload | Workload only |
| Per-retry overhead | Re-bootstrap platform | Single step retry |

## The Multiply Effect

Ten pipelines × a platform fleet each = a datacenter. Ten pipelines × lightweight libraries shared across one host = savings in procurement, energy, and a much smaller carbon line item. Small decisions, huge compounding.

## Conclusion

Engineering teams increasingly report the biggest lever in their carbon budget isn't algorithms — it's architecture: what we keep running, and what we refuse to keep running. A pipeline that uses only what its job needs is the sustainable default.

> The largest footprint in software is the infrastructure that exists between jobs.

#GreenIT #Sustainability #wpipe #Python #CarbonFootprint