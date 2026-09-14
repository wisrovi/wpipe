# 📊 Your pipeline, measured and visualized in real time

One thing is for your pipeline to "run." Another is to **watch it run**: which step is executing, how long each stage takes, which events it fired, where it last failed.

With **wpipe** observability isn't a plugin you buy separately — it's part of the engine. Every run is recorded in a SQL tracker, and you can visualize it with one line.

### 🖥️ A local dashboard in 2 lines

```python
from wpipe import start_dashboard

start_dashboard(db_path="tracking.db", port=5000)
# → http://localhost:5000
```

### 🧭 What you see from the dashboard

- **Timeline**: the real execution sequence of your steps.
- **Analytics**: average duration, success rate, top slow steps.
- **Alerts**: thresholds that fired (and when).
- **Events**: pre/post hooks and triggered events.
- **States / Pipelines**: the persistent state of each run.
- **Pipeline graph**: the DAG view generated from your code.

### ✅ Why this matters

1. **Visual debugging**: the problem stops being a "black box."
2. **Bottlenecks**: spot the slow step immediately.
3. **Audit**: history by default, no extra setup.
4. **Zero infra**: a local SQLite dashboard, not a monitoring cluster.

Observability shouldn't be a side project. It should come **out of the box**.

👇 **Do you dream of knowing what's happening in your pipeline? Which dashboard do you use today?**

#Python #DevOps #Observability #wpipe #DataEngineering