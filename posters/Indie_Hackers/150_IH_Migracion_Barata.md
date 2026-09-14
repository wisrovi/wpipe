# The Cheap Migration: Modernizing Legacy Data Jobs Without a Big-Bang Project

The scariest phrase in operations is "we need to modernize the pipeline." It conjures a quarter-long project, a rewrite committee, and a migration window nobody wants to own. But modernization doesn't have to be a rewrite — it can be a **bridge**, and bridges are built incrementally.

## Why Full Rewrites Stall

Legacy flows (cron scripts, fragile in-house tools) keep running for years because they *work*. The risks of touching them are concentrated — a failure means an outage that's your name on the ticket. So the rewrite never starts, and the technical debt keeps accruing.

The migration that ships is the one that doesn't threaten the status quo: add a stateful layer **around** existing logic, not a replacement of it.

## wpipe as the Migration Bridge

wpipe wraps existing functions with decorators — your business logic stays untouched while gaining checkpoints, retries, and audit:

```python
from wpipe import Pipeline, step

# Before: your existing function, untouched
def legacy_process(row):
    result = do_the_thing(row)   # unchanged business logic
    return result

# After: same logic, now stateful
@step(name="legacy_process", retry_count=3, retry_delay=5, checkpoint=True)
def legacy_step(data):
    return {**data, "result": legacy_process(data["row"])}

pipe = Pipeline(pipeline_name="bridge", tracking_db="bridge.db")
pipe.set_steps([legacy_step])
pipe.run({"row": next_row})
```

The first pipeline run is the first checkpointed run. No big-bang, no parallel system to babysit — value lands in an afternoon.

## Battle Card

| Step | Big-bang rewrite | Bridge migration (wpipe) |
| :--- | :---: | :---: |
| Start | After planning project | Today, in code |
| Risk | High (all-or-nothing) | Low (incremental) |
| Investment | Months | Afternoon |
| Rollback | Painful | Git revert |
| Business logic change | Risk of drift | None (reused) |

## Conclusion

Migrating legacy jobs is a business decision, not just a technical one. The cheap path — wrap, checkpoint, resume — delivers durability and observability with near-zero disruption, which is why bridge migrations actually get finished.

#Migration #Legacy #IndieHackers #wpipe #Python #Reliability