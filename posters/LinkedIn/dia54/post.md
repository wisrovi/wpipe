# 🚨 Alerts that warn you before your users notice

Reactive monitoring works like this: the user calls, you run, you check logs and (hopefully) find the cause. **Proactive** monitoring is different: the system warns you when a metric crosses a threshold.

With **wpipe** you can define alerts with a simple API, no monitoring stack required.

### ⚠️ A duration alert in 4 lines

```python
from wpipe import Pipeline, Metric, Severity

pipe = Pipeline(pipeline_name="watched")

pipe.tracker.add_alert_threshold(
    metric=Metric.PIPELINE_DURATION,
    expression=">5000",              # ms
    severity=Severity.WARNING,
    steps=[lambda d: print("⚠ Slow pipeline!")],
)
```

### 🔎 What you can watch

- **Pipeline duration**: a process that took 2s now takes 10s.
- **Error rate** and failures of specific steps.
- **Custom metrics** you define per step.

### ✅ The real value

1. **Early detection**: you learn on the 3rd slow run, not the 50th.
2. **Automated response**: `steps` runs an action when it fires.
3. **Contextual severity**: warnings vs. criticals, without noise.

A watched pipeline doesn't eliminate problems; it eliminates **surprises**.

👇 **Do you notice a pipeline degrading from a customer call or from the dashboard on time?**

#Python #SRE #DevOps #wpipe #Monitoring