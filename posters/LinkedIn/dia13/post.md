# 💎 WPipe vs. Dagster: Is "Asset-Based" Always Best?

Dagster has done great work with its asset-based approach, but at what cost? For many projects, the infrastructure needed to run Dagster is simply too heavy. 🏋️‍♂️

**WPipe** offers a "Code-First" alternative that prioritizes lightness and resilience without the need for complex IO Managers.

### ⚔️ Battle Card: WPipe vs. Dagster

| Feature | WPipe | Dagster |
| :--- | :---: | :--- |
| **RAM Usage** | **< 50MB** | > 500MB |
| **Setup** | Instant | Moderate |
| **Resilience** | SQLite WAL | DB / IO Managers |
| **Edge Ready** | ✅ Yes | ❌ Difficult |

### 🛠️ Simplicity with `@state`

Instead of defining complex asset graphs, in WPipe you focus on your pipeline's state:

```python
from wpipe import state, to_obj

@state(name="DataAnalysis", version="v1.0")
@to_obj
def analyze(data: dict):
    # Process your data with full confidence
    return {"score": sum(data.values()) / len(data)}
```

### 📊 Direct Visual Documentation

📊 Image to upload with this post: diagrama.png

With **+117k downloads**, WPipe proves you can have professional orchestration with a fraction of the resources.

Do you prefer the complexity of assets or the simplicity of state? 👇

#Dagster #WPipe #DataEngineering #Python #Efficiency #Microservices