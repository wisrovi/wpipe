# 🔄 One pipeline, two worlds: sync and async

Many libraries force you to choose: build a sync orchestrator or an async one, and migrating between them means rewriting everything.

With **wpipe** that decision doesn't exist: you have `Pipeline` and `PipelineAsync` with **100% of the same features**. What you learn in one, you apply in the other.

### ⚡ A real example, in under 20 lines

```python
import asyncio
from wpipe import PipelineAsync, step

@step(name="fetch")
async def fetch(data):
    await asyncio.sleep(0.5)   # I/O, non-blocking
    return {"data": "ready"}

@step(name="process")
async def process(data):
    return {"result": data["data"]}

async def main():
    pipe = PipelineAsync(pipeline_name="async_demo")
    pipe.set_steps([fetch, process])
    result = await pipe.run({"seed": 1})
    return result

asyncio.run(main())
```

### 🎯 Why it matters in 2026

1. **Same mental model**: checkpoints, retries, alerts, and tracker work identically in both.
2. **I/O bound**: network, API, and file tasks run without blocking the event loop.
3. **Zero rewrites**: switch `Pipeline` for `PipelineAsync` and your flow keeps its structure.

Sync/async parity isn't a luxury — it's the difference between an orchestrator that accompanies you and a tool that forces you to bend.

👇 **Does your team already use asyncio in production? How do you orchestrate those flows today?**

#Python #Async #SoftwareEngineering #wpipe #Backend #DataPipelines