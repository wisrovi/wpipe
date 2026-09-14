# Your Cloud in One File: SQLite as the Entire State Layer

Infrastructure-as-a-service taught us to think in services. Messaging? That's a service. State? That's a database. Scheduling? A scheduler cluster. Ironically, the most reliable state layer a pipeline could ask for is a single file on disk — and it's been sitting in the Python standard library the whole time.

## The Service Reflex

"Why would I trust a local file for pipeline state?" echoes through every architecture review. The reflex assumes that production-grade state requires a server: a deployment, a connection pool, backups. But look at what a pipeline actually needs from state:

1. Where did the last successful step stop?
2. What context did that step produce?
3. What are the execution metrics for this run?

That's a checkpoint row and an events table. It is not a horizontally-sharded database workload.

## SQLite WAL: Built for Exactly This

SQLite in Write-Ahead Logging (WAL) mode provides exactly the durability properties a pipeline needs:

- **Atomic commits**: a step's state is saved all-or-nothing.
- **Crash recovery**: committed state survives power loss and process kills.
- **Single-writer math**: your pipeline is the only writer — no concurrency fights.
- **Zero administration**: copy the file for a backup; delete it to reset.

```python
from wpipe import Pipeline, step

@step(name="etl", retry_count=3)
def etl(data):
    return {"processed": data["rows"]}

pipe = Pipeline(pipeline_name="file_state", tracking_db="pipeline.db")
pipe.set_steps([etl])
pipe.run({"rows": 10_000})
```

Everything wpipe needs for resilience — checkpoints, tracker, retry bookkeeping — lives in `pipeline.db`.

## Battle Card

| Aspect | Dedicated DB server | SQLite WAL file |
| :--- | :---: | :---: |
| Deploy | Server + config | Copy the file |
| Admins needed | Yes | No |
| RAM | Shared buffers (100MB+) | Part of <50MB |
| Crash scenario | Multi-tier recovery | Open file, resume |
| Backup | Tooling + scripting | `cp pipeline.db` |

## What You Give Up (Compared to a Server)

Honestly: multi-user concurrent writes at scale, and remote access. A single pipeline needs neither. When you genuinely outgrow that, the pipeline's state can move into shared infrastructure later — without rewriting the step logic that uses it.

## Conclusion

Calling the state layer "a database" pushed orchestrators into running databases. But the pragmatic, durable, green answer for a pipeline is one file. Your entire cloud — checkpointing, tracing, alerting answers — can live in ~KB of disk, answering instantly, forever.

> The cloud is someone else's computer. Your pipeline's state is a file on yours.

#SQLite #StateManagement #wpipe #Python #DataEngineering