# 🧬 Data contracts: your pipeline validated where it hurts most

In data, the classic error is elegant: a field arrives as `str` where you expected `int`, or a `None` travels through 4 steps until it explodes at the end. In a contract-less script, you discover that in production.

With **wpipe** you define your pipeline's **data contract** and validation happens automatically — like a schema in a database, but at every step.

### 📦 A contract with PipelineContext

```python
from wpipe import Pipeline, step, PipelineContext

class User(PipelineContext):
    name: str
    age: int
    email: str

@step(name="validate_user")
def validate(user: User):
    if user.age < 18:
        return {"valid": False, "reason": "underage"}
    return {"valid": True}

pipe = Pipeline(pipeline_name="validation")
pipe.set_steps([validate])
pipe.run({"name": "Ana", "age": 25, "email": "ana@example.com"})
# -> {'valid': True}
```

### ✅ What it gives you

| Without contract | With PipelineContext |
| :--- | :--- |
| The error appears at the end | Validation happens at the edge |
| Types "work by accident" | Types verified against the schema |
| No shape documentation | The contract is self-documenting |

### 🧠 The philosophy

You don't validate out of distrust: you validate because **the data entering the pipeline defines how safely you can operate**. A strict but extensible contract turns data errors into process errors, not production incidents.

Correct data in = predictable pipeline out.

👇 **Do your pipelines validate input types, or trust that "whoever sends, sends well"?**

#Python #DataEngineering #TypeSafety #wpipe #SoftwareEngineering