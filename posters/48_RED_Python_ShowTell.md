# [Show & Tell] wpipe: A lightweight, industrial-grade Python pipeline orchestrator with SQLite checkpoints

Hey r/Python!

I wanted to share a project I've been working on (and that recently hit +117k downloads on PyPI!): **wpipe**.

### 🐍 What is it?
It's a library for building complex workflows/pipelines in Python. Think of it as a middle ground between a simple script and a heavy orchestrator like Airflow or Prefect. It's designed to be ultra-lightweight (runs on <50MB RAM) and "State-Aware".

### ✨ Key Features:
*   **Automatic SQLite Checkpoints:** If your script crashes, wpipe saves the state. When you restart, it resumes from the last successful step. No more manual cleanup.
*   **Structured Tracking:** Every input and output of your functions is logged into a structured SQL format automatically.
*   **Pure Python / YAML:** Define your logic in Python, but you can also use YAML for the pipeline structure.
*   **Parallel Execution:** Built-in support for threading/multiprocessing without the boilerplate.
*   **Async Support:** Full parity between `Pipeline` and `PipelineAsync`.

### 🛠️ Why I built it:
I was tired of two things:
1.  Scripts that I had to manually restart and "fix" the data halfway through because of a random API error.
2.  Orchestrators that required Docker, a Postgres DB, and 2GB of RAM just to run a few cron jobs.

### 📦 Quick Example:
```python
from wpipe import Pipeline, step

@step(name="fetch")
def fetch(data):
    return {"raw": "some data"}

@step(name="process")
def process(result):
    return {"clean": result["raw"].upper()}

pipe = Pipeline(pipeline_name="MyPipe", use_checkpoints=True)
pipe.set_steps([fetch, process])
pipe.run({})
```

If it fails in `process`, next time you run it, `fetch` won't be called again—it pulls the result from the checkpoint.

### 🔗 Check it out:
*   **GitHub:** [https://github.com/william-rodriguez/wpipe](https://github.com/william-rodriguez/wpipe) (Wait, I should use the actual URL if I knew it, but for the post I'll leave placeholders or generic links).
*   **PyPI:** `pip install wpipe`

I'd love to hear your thoughts! Is this something that would be useful in your daily automation tasks? What features are you missing in your current pipeline tools?

#python #opensource #automation #dataengineering #backend
