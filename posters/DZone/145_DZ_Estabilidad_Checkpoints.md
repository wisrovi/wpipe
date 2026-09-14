# Stability Through Checkpoints: The 'Save Game' Pattern for Data Workflows

## The Crash You Can't Afford

Data pipelines fail at the worst times: three hours into a six-hour run, in the middle of the night, right before the business opens. The damage isn't the failure — failures are inevitable. The damage is the **reprocessing**: starting over from step one and paying for the same compute, network calls, and time twice.

## The Save Game Analogy

Video games solved this decades ago with a checkpoint — serialize progress so a defeat returns you to the last platform you actually reached. Pipelines have the same shape: a long sequence of steps where losing position is wildly more expensive than a retry ever could be.

wpipe bakes this in with **SQLite WAL checkpoints**:

```python
from wpipe import Pipeline, step

@step(name="extract", retry_count=3, retry_delay=2)
def extract(data):
    return {"rows": pull(data["source"])}

@step(name="transform", checkpoint=True)
def transform(data):
    return {"clean": normalize(data["rows"])}

@step(name="load", retry_count=3)
def load(data):
    return {"loaded": write(data["clean"])}

pipe = Pipeline(pipeline_name="savegame", tracking_db="savegame.db")
pipe.set_steps([extract, transform, load])

# Fail at 'load'? Re-run resumes at 'load' with the checkpointed context.
pipe.run({"source": "legacy://x"})
```

## What a Checkpoint Actually Commits

- The step's **produced context** (its output).
- The pipeline's **position**.
- A **runtime record** in the tracker.

Because the checkpoint writes to SQLite's WAL, the commit is atomic and survives power loss — the exact durability semantics you'd expect from a "save game."

## Battle Card

| Scenario | No checkpoints | wpipe checkpoints |
| :--- | :---: | :---: |
| Fail at step 80/100 | Rerun 80 steps | Resume at 80 |
| Power loss mid-run | Start over | Resume committed state |
| Failed dependency call | Refetch everything | Only redo the failed step |
| DevOps toil | Manual restart ops | Automatic resume |

## Conclusion

Checkpoints are the difference between "it failed and it cost us" and "it failed and resumed." For production data workflows, that difference is the actual system availability — which is why stability starts with a durable save point.

#Checkpoints #Resilience #wpipe #Python #DataEngineering