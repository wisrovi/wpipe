# Architecture Efficiency: The Metric We Should Optimize First

We measure throughput, latency, and uptime — the usual suspects. But underneath all of them sits a quieter metric: **architecture efficiency**, or how much machinery you operate per unit of valuable work. It's the ratio of scaffolding to product, and it predicts every other number on your dashboard.

## The Efficiency Ratio

Think of it as:

`work done / (machinery running × time alive)`

If you run a 500MB-2GB platform around the clock to execute ten minutes of transforms a day, your ratio is terrible — thousands of compute-hours consumed per hour of actual work. Optimizing the transform itself (micro-optimizations) barely moves the ratio. The architecture dominates.

## What Efficient Architecture Looks Like

- **Machinery that stops when the work stops** — no resident fleet waiting between jobs.
- **State that doesn't require provisioning** — a file, not a server.
- **Workers that scale with the work** — not a pool sized for peaks.
- **Everything paid for is in use**, at least mostly.

## wpipe: A High-Efficiency Ratio by Construction

- **Runs on demand**: triggered by cron/CI, alive only during the run.
- **Local state**: SQLite WAL; nothing to administer or keep warm.
- **Needs almost nothing to coexist**: <50MB RAM alongside the app.
- **Parallel when useful**: `Parallel(steps=[...])` uses your cores; nothing idles afterward.

```python
from wpipe import Pipeline, step

@step(name="first", retry_count=2)
def first(data):
    return {"a": data["n"] + 1}

@step(name="second")
def second(data):
    return {"b": data["a"] * 2}

pipe = Pipeline(pipeline_name="efficient")
pipe.set_steps([first, second])
pipe.run({"n": 1})
```

## Battle Card

| Resource | Low-efficiency | High-efficiency (wpipe) |
| :--- | :---: | :---: |
| Always-on processes | Scheduler+broker+DB | None |
| RAM per deploy | 500MB - 2GB+ | <50MB |
| Machines provisioned | Fleet for platform | Host already there |
| Idle hours | 24/7 | Only while running |
| Admin overhead | Patch/monitor platform | None |

## Conclusion

Before tuning a function by microseconds, tune the architecture by orders of magnitude. Cut the always-on machinery, shrink the state layer to a file, and let the work be ephemeral. Efficiency isn't the cleverest algorithm — it's the least machinery per unit of value.

> The most efficient system is the one that extinguishes itself when it's done.

#Architecture #Efficiency #wpipe #GreenIT #Python