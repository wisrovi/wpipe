# 🧵 Real parallelism, without spinning up a cluster

Your pipeline has 3 steps that don't depend on each other. Today, in a sequential script, they run one after another wasting time. In production that means: more compute hours, more RAM used, more waiting.

### ⚡ wpipe gives you parallelism with a single class

```python
from wpipe import Pipeline, step, Parallel

@step(name="task_a")
def task_a(data):  return {"a": "done"}

@step(name="task_b")
def task_b(data):  return {"b": "done"}

@step(name="task_c")
def task_c(data):  return {"c": "done"}

pipe = Pipeline(pipeline_name="parallel")
pipe.set_steps([
    Parallel(steps=[task_a, task_b, task_c], max_workers=3)
])
```

All three steps run **at the same time**, and the result is consolidated. Just one line.

### 🔀 Threads or processes: you decide

| Scenario | Recommended |
| :--- | :--- |
| I/O tasks (network, DB, files) | Threads (`use_processes=False`) |
| Heavy CPU tasks (pandas, ML) | Processes, with GIL bypass |

The library handles *thread-safety* for you: it writes to SQLite in WAL mode without corrupting state, even with several steps running in parallel.

### 📉 The result

- Lower end-to-end latency in your flows.
- Less infrastructure: no external worker pool needed.
- Parallel orchestration that stays **deterministic** and traceable.

Parallelism isn't magic — it's good design. But that **one-line cost** helps a lot.

👇 **Do you have independent steps running serially today? How much time are you losing by not parallelizing?**

#Python #ParallelProgramming #Backend #wpipe #SoftwareEngineering