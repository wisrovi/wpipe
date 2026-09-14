# No Cold Start: The Pipeline That's There When You Need It

Cold starts are the tax you pay for idle complexity. Serverless functions made the cold start famous — a dident request queues behind a container that had to wake up. But serverless isn't the only place cold starts hide. They live in any orchestrator that keeps a heavy runtime dormant and spins it up on demand.

## What Actually Causes Cold Starts

A "cold" pipeline is one that must bootstrap its entire runtime before running: load the scheduler, connect the broker, hydrate the metadata database, warm the worker pools. The more machinery lives between "trigger" and "first row processed", the longer the cold start.

Heavy platforms make that worse in the other direction: they keep machinery **permanently warm**, which eliminates the cold start but pays for an always-on fleet. You're choosing between "slow to wake" or "never sleeps".

## wpipe: Neither

wpipe's runtime is the Python process you already have:

- **No daemon to boot** — your pipeline runs inside your own process or a cron trigger.
- **No broker handshake** — there is no broker.
- **No metadata hydration** — state is a local SQLite file, opened in milliseconds.

```python
from wpipe import Pipeline, step

@step(name="task")
def task(data):
    return {"done": data["input"]}

pipe = Pipeline(pipeline_name="instant")
pipe.set_steps([task])

# Triggered by cron/CI; there is nothing to "warm up" for this call.
pipe.run({"input": 42})
```

The result is a pipeline that starts when triggered and stops when finished — no warm fleet while idle, no long boot when called. Just compute on demand.

## Battle Card

| Aspect | Serverless-heavy | Always-on fleet | wpipe |
| :--- | :---: | :---: | :---: |
| Cold start | Yes (per invocation) | None | None |
| Idle cost | Low | High (24/7) | ~Zero |
| Infra to boot | Runtime+context | — | Nothing |
| Footprint | Pay per call | 500MB-2GB resident | <50MB |

## Conclusion

A pipeline that leaps into action — instantly, without a warm fleet or a slow boot — is both cheaper and better behaved. That's the difference between a scheduling platform and a library that respects the moment it's called.

> The best runtime is the one you don't have to wake up, because it was already there.

#ColdStart #Serverless #wpipe #Python #GreenIT