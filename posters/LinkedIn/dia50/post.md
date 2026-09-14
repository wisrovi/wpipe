# 🧩 Pipelines of pipelines: infinite composition

Most orchestration problems aren't solved with one giant pipeline. They're solved with **small, reusable pipelines** that compose together.

With **wpipe**, a pipeline can be just another step inside another pipeline. It's classic composition, applied to data orchestration.

### 🏗️ A simple example

```python
from wpipe import Pipeline, step

# --- Child pipeline (reusable logic) ---
sub = Pipeline(pipeline_name="child")
sub.set_steps([step_a, step_b])     # clean and testable

# --- Parent pipeline (high-level orchestration) ---
parent = Pipeline(pipeline_name="parent")
parent.set_steps([
    initial_step,
    sub,           # The child pipeline is just another step!
    final_step
])
```

### ✅ Why this changes your architecture

1. **Reuse**: the sub-pipeline lives in a module and is used across 10 flows.
2. **Testing**: each sub-pipeline is tested in isolation.
3. **Clarity**: the parent flow describes the business; the children, the implementation.
4. **Resilience**: checkpoints and tracking are preserved at both levels.

### 🚫 What you avoid

- Unreadable 500-line pipelines.
- Duplicated logic running in 3 different scripts.
- Teams afraid to touch the main flow.

Composition is the pattern that never fails: **small pieces, well tested, orchestrated at any scale**.

👇 **Are your pipelines 500-step monoliths or reusable pieces?**

#Python #SoftwareArchitecture #DataEngineering #wpipe #Backend