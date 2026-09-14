# Orchestration Without a Cluster: Your Pipeline, Your Machine

"A distributed system is a system you can't understand." For years, the industry has equated orchestrating jobs with standing up a distributed platform: clusters, schedulers, brokers, workers. But most pipelines aren't distributed problems — they're sequential or locally-parallel problems wrapped in distributed machinery.

## The Cluster Reflex

It goes like this: we need to run jobs on a schedule, so we reach for the cluster. The cost appears later: cluster administration, network config, autoscaling rules, and a monitoring stack for the monitoring stack. Meanwhile the jobs themselves — a transform here, an API sync there — could run quite happily on a single machine.

wpipe challenges the reflex: orchestration should be **as big as your problem**, and for most problems that's one process plus a local SQLite file.

- **Same process**: your steps run in your Python process (or worker processes you control).
- **Same machine state**: checkpoints and history live in a local `.db`.
- **Escape hatch**: when you DO need more, `Parallel(steps=[...], use_processes=True)` spreads work across your cores — still no cluster.

```python
from wpipe import Pipeline, step

@step(name="transform", retry_count=3)
def transform(data):
    return {"value": data["raw"].upper()}

pipe = Pipeline(pipeline_name="no_cluster", tracking_db="local.db")
pipe.set_steps([transform])
pipe.run({"raw": "sample"})
```

## Battle Card

| Dimension | Cluster platform | wpipe on one machine |
| :--- | :--- | :--- |
| Moving parts | Many (nodes, brokers) | One library |
| Startup time | Minutes | Instant |
| Failure point | Federation issues | Your code |
| Parallelism | Pods/replicas | In-process workers |
| Energy | Many machines | One machine |

## When a Cluster Actually Earns Its Keep

Honest engineering: some workloads ARE distributed (huge fan-outs, long-running fleets, multi-region). wpipe won't pretend otherwise. But it lets you start small: build, test, and run the pipeline standing up locally; only if your actual metrics demand it, lift the same step definitions onto real infrastructure. The code — `@step` functions — doesn't change.

## Conclusion

Most pipelines live their whole lives on one machine. Treating them as cluster problems turns a weekend tool into a platform project. wpipe lets orchestration be just another library — and that's more power, not less.

> Don't upgrade your pipeline to a platform until the pipeline demonstrates it needs one.

#Orchestration #DistributedSystems #wpipe #Python #Architecture