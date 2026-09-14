# The State Layer as the Bedrock of Pipeline Stability

## What Holds a Pipeline Together?

Ask a team what makes their pipeline stable and the answers vary: "good culture," "solid tests," "a senior who knows things." The unglamorous truth is narrower: **stability lives in the state layer**. If the system reliably knows where it is and what it has done, everything else becomes engineering. If it doesn't, everything else becomes firefighting.

## State: The Unpaid Scaffolding

Most applications of a pipeline's state are invisible until they break:

- Resumption after a crash (position).
- Exactly-once-ish semantics (what was committed).
- Auditing (what ran and when).
- Retry bookkeeping (attempt counts).

The fewer and more durable the sources of that state, the more stable the pipeline. wpipe consolidates state into one local store with ACID properties via SQLite WAL — durable, atomic, queryable.

```python
from wpipe import Pipeline, step

@step(name="pull", retry_count=2)
def pull(data):
    return {"value": fetch(data["key"])}

pipe = Pipeline(pipeline_name="bedrock", tracking_db="state.db")
pipe.set_steps([pull])

# Each step commit is atomic; the tracker records every run.
# State = one durable file = one answer to every stability question.
pipe.run({"key": "abc"})
```

## Why a Single Atomic Store Wins

- **One source of truth**: no chance for checkpoints and audit to disagree.
- **Atomic commits**: the state is either fully updated or not at all.
- **Crash-durable**: WAL survives power loss, delivering what "stable" means.
- **Queryable**: recovery logic can ask "what's the last committed step?" and get an answer.

## Battle Card

| Aspect | Implicit scattered state | Single atomic store (wpipe) |
| :--- | :---: | :---: |
| Source of truth | Ambiguous | Definite |
| Crash story | Depends on who is awake | Durable WAL |
| Recovery logic | Reverse-engineered | Query the state |
| Audit | Elusive | Tracker SQL |

## Conclusion

Calling any pipeline stable while its state is fragile is like calling a building sound when its foundation is wet cardboard. Making state explicit, atomic, and durable is the foundational move — every resilience feature builds on it.

#StateManagement #Stability #wpipe #SQLite #Python