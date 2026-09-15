# 📄 Logs, Metrics, Audits: Export What Your Pipeline Did

A resilient pipeline is useless if you can't afterwards **prove** what happened: for an audit, a compliance report, or comparing performance evolution across runs.

With **wpipe** history is persisted by default. And when you need it, you export it in seconds.

### 📤 Export in 3 lines

```python
from wpipe import PipelineExporter

exporter = PipelineExporter("tracking.db")

# Complete execution logs
json_data = exporter.export_pipeline_logs(format="json")
csv_data  = exporter.export_pipeline_logs(format="csv")

# Consolidated statistics
stats = exporter.export_statistics(format="json")
```

### 🗂️ What you get

| Format | Use |
| :--- | :--- |
| **JSON** | Integrations, APIs, external systems |
| **CSV** | Spreadsheets, stakeholder reports |
| **Statistics** | Success rate, average duration, per-step |

### 🧠 Why "export" is strategic

1. **Real auditing**: not "I think it worked," but "here's the log."
2. **Performance analysis**: compare metrics across pipeline versions.
3. **Interoperability**: your run data travels wherever you need it.

Modern orchestration doesn't end when the pipeline finishes: it ends when **you can explain what it did**.

👇 **How hard would it be today to generate a report of what your automation ran last week?**

#Python #DataEngineering #DevOps #wpipe #Observability