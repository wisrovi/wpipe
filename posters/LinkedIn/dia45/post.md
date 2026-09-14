# 🔁 Transient errors shouldn't take down your pipeline

An API responding slowly, a 2-second network timeout, a saturated DB connection... and your nightly job dies. Then you come in the morning to an empty log and "reprocess by hand."

Transient failures are a fact of life in production. What's NOT normal is **your architecture not tolerating them**.

### 🛠️ wpipe: retries that aren't a "while True"

With `wpipe` you define the retry strategy with two parameters and the library handles the rest:

```python
from wpipe import step, Pipeline

@step(name="api_connection", retry_count=3, retry_delay=1)
def api_connection(data):
    # Your API call or fragile operation here
    return {"connected": True}

pipe = Pipeline(pipeline_name="retry")
pipe.set_steps([api_connection])
pipe.run({"available": False})  # Retries 3 times before failing
```

### 🔄 Why it matters

| Without retries | With wpipe |
| :--- | :--- |
| Fails and restarts everything from zero | Retries with controlled pause |
| Error at 3 AM, discovered at 9 AM | Error logged with its context |
| Fear of touching the script | You can iterate without risk |

And when the problem IS serious, the failure goes to the **checkpoint**: the pipeline saves its exact state and can resume without re-running the costly steps that already succeeded.

It's not about avoiding errors (impossible). It's about making **your system absorb them** and move forward.

👇 **How many times have you had to reprocess data because of a temporary error?**

#Python #SoftwareEngineering #Backend #Reliability #wpipe #DataPipelines