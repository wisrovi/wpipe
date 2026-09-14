# 🔥 Fire & Forget: tasks that don't block your pipeline

Not every task in a flow needs to be awaited. Telemetry, notifications, an email send, or an internal sync can run **without blocking** the main result.

In most orchestrators, "launching something non-blocking" is a battle: queues, workers, brokers, supervisors. With **wpipe** it's a single class: `Background`.

### ⚡ Fire & Forget in action

```python
from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background

@step(name="main_task")
def main_task(data):
    print("Running main task...")
    return {"status": "done"}

@step(name="telemetry")
def telemetry(data):
    import time
    time.sleep(2)  # Costly task that must not delay you
    print("Telemetry sent")

pipe = Pipeline(pipeline_name="with_background")
pipe.set_steps([
    main_task,
    Background(telemetry),   # Does not block the pipeline
])
```

The pipeline **continues immediately**; the heavy task runs in a daemon thread. Result: the flow finishes on time and telemetry is still sent.

### 🎯 When to use it

- 📤 Send metrics or logs to an external service.
- 🔔 Notifications that must not delay business.
- 🧹 Cleanup and post-execution auxiliary tasks.
- Emails / webhooks where latency doesn't matter.

### 🧠 The golden rule

Every step in your pipeline should answer: does it **need** to block the next one? If the answer is "no," that step is a perfect candidate for `Background`.

Orchestrating isn't just chaining steps — it's **deciding what waits and what doesn't**.

👇 **Which of your tasks are you still waiting on "just in case" that could go in the background?**

#Python #Backend #SoftwareEngineering #wpipe #Automation