# 🕒 From orphan script to supervised service

In my previous post I talked about why Cron alone is a risk for critical tasks. Now the practical part: **how do you migrate?**

The trick is that you don't need to rewrite your business logic. You just need to wrap it.

### 🔄 The upgrade in 3 steps

**Before (legacy Cron):**
```bash
0 3 * * * /usr/bin/python3 /opt/jobs/sync.py >> /var/log/sync.log
```

**After (wpipe):**
```python
from wpipe import Pipeline, step

@step(name="sync", retry_count=3, retry_delay=5)
def sync(data):
    # Your same script as always, unchanged
    return {"status": "ok"}

pipe = Pipeline(pipeline_name="sync", tracking_db="sync.db")
pipe.set_steps([sync])
pipe.run({})
# Your cron still fires it... but it's no longer alone.
```

### 🎩 What you gain without touching the logic

| Capability | Cron | Cron + wpipe |
| :--- | :--- | :--- |
| Retries | ❌ None | ✅ Scheduled |
| Checkpoints | ❌ Restarts from zero | ✅ Resumes the step |
| Logs | Plain text | ✅ Searchable SQL Tracker |
| Alerts | Nothing | ✅ Configurable thresholds |
| Dashboard | No | ✅ Realtime on :5000 |

### 💡 The conclusion

You don't have to abandon your cron right away. **Keep the trigger you already know** and start gaining retries, checkpoints, and observability today. Your cron's v2 starts with an `@step`.

👇 **Does your current cron survive a 3 AM failure, or does it just "pray" for dawn?**

#Python #DevOps #Cron #wpipe #Reliability #Automation