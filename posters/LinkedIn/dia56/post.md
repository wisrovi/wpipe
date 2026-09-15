# 🎓 Orchestration Without 3 Certifications

When someone wants to start with orchestration, the "traditional" path is: read a thousand docs, spin up an environment, understand a panel, dream of Airflow... and get frustrated. The barrier isn't the concept — it's the tool.

With **wpipe** onboarding is part of the library: a **Learning Tour with 140 levels** that takes you from the very basics to the most advanced flows.

### 🚶 First steps

```python
from wpipe import Pipeline, step

@step(name="greet")
def greet(name):
    return {"message": f"Hello, {name}!"}

pipe = Pipeline(pipeline_name="myFirst")
pipe.set_steps([greet])

pipe.run({"name": "World"})
# -> {'message': 'Hello, World!'}
```

Then you keep scaling: conditions, loops, parallelism, checkpoints, async, dashboard.

### ✅ Why it matters

1. **Short curve**: from "hello world" to industrial pipeline in one session.
2. **One mental model**: instead of learning 5 different tools.
3. **Real retention**: you advance at your pace, level by level, no jumps.

Orchestration should be taught the way you learn to program: **by practicing, not by reading a 900-page manual**.

👇 **How long did it take you to build your first "serious" pipeline? And what was your first excuse not to?**

#Python #Learning #SoftwareEngineering #wpipe #DataEngineering