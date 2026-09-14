# ⚙️ Declarative configuration, without leaving the Python ecosystem

In the "low-code" world you switch environments when you want to configure: a visual panel, a giant YAML, a proprietary database. All outside your code, all hard to version.

With **wpipe** configuration lives in the developer's world: you load your flow and your parameters without abandoning Python.

### 📋 YAML configuration + code

```python
from wpipe import Pipeline, step

@step(name="process")
def process(data):
    # Inferred from the config or context
    return {"result": data["input"] * data.get("factor", 1)}

pipe = Pipeline(pipeline_name="configurable")
pipe.set_steps([process], config_path="pipeline.yml")
```

Your `pipeline.yml` defines parameters, and your pipeline consumes them:

```yaml
pipeline_name: configurable
verbose: true
retry_count: 3
params:
  factor: 2
```

### 🎯 Why "code-first" config wins

| Aspect | Visual panel | Config in code (wpipe) |
| :--- | :--- | :--- |
| Versioning | ❌ No diffs | ✅ Native Git Flow |
| Review | Blind clicks | ✅ Pull Request |
| Portability | Provider-dependent | ✅ One YAML or Python file |
| Vendor exit | Traumatic | ✅ Trivial (pip install) |

### 💡 The key point

You're not choosing between "code" and "config." You're choosing where the **source of truth** lives: in your repository, reviewable, testable, portable.

The sovereignty of your automation starts by getting it into Git.

👇 **Do your pipelines live in a repository or in an on/off panel?**

#Python #DevOps #Backend #wpipe #SoftwareEngineering