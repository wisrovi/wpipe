# ⏱️ A "stuck" pipeline is worse than a failing one

Do you know the silent villain? The task that never finishes: an API call stuck on the client library's default timeout, an `ssh` waiting for a password, a `pandas.read_csv` against an S3 that takes 40 minutes.

With Cron or loose scripts, that job stays there forever — consuming RAM, holding a slot, and leaving everyone wondering: did it finish? Did it crash?

### 🛡️ wpipe sets per-step time limits

```python
from wpipe import step, timeout_sync, Pipeline

@timeout_sync(seconds=5)
@step(name="slow_task")
def slow_task(data):
    import time
    time.sleep(10)  # Simulates a hung task
    return {"status": "ok"}

pipe = Pipeline(pipeline_name="timeout")
pipe.set_steps([slow_task])
# If it takes more than 5 seconds -> controlled TimeoutError
```

So a step that exceeds its time budget **fails explicitly** rather than hanging. And with wpipe's retries + checkpoints, that failure is just another event in your history, not a mystery.

### 📊 Your pipeline, your service contract

- Max time per step defined in code (versionable).
- No production surprises: you know how long each stage can take.
- Timeout failures are recorded in the SQL tracker with their context.

Setting limits isn't being strict — it's being **predictable**.

👇 **How much debugging time has a task that "never finished" cost you?**

#Python #Reliability #SoftwareEngineering #wpipe #Backend #Automation