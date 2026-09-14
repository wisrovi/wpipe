# IoT, Green, and Light: Orchestrating Field Devices Without a Datacenter

The IoT promise is compelling: sensors everywhere, decisions at the edge, no round-trip to a cloud for every event. The reality hits when you try to deploy the software — most orchestrators assume a beefy server in a rack, not a 1GB single-board computer in a dusty cabinet.

## The Field Problem

Field devices share brutal constraints:

- **Tiny memory**: 256MB-1GB, shared with the OS and the actual work.
- **Unstable power**: outages, brownouts, reboots.
- **No admin**: nobody is SSH-ing in to restart a process at 3 AM.

Green-IT on the edge isn't aspirational — it's survival. Software must use as little as possible because the hardware gives so little.

## wpipe on the Edge

wpipe was designed to run where heavyweight orchestrators cannot:

- **<50MB RAM**: leaves room for your application, your OS, and your sensors.
- **SQLite WAL persistence**: survives power loss without a database server.
- **Local-first**: no broker, no central coordinator, no internet required.

```python
from wpipe import Pipeline, step

@step(name="read_sensor", retry_count=3, retry_delay=10)
def read_sensor(data):
    value = read("sensor://temperature")   # may fail under brownout
    return {"temperature": value}

@step(name="decide", retry_count=2)
def decide(data):
    alert = data["temperature"] > 85
    return {"alert": alert, **data}

pipe = Pipeline(pipeline_name="edge_gateway", tracking_db="edge.db")
pipe.set_steps([read_sensor, decide])
pipe.run({})
```

The checkpointing is the silent hero here: an edge device that reboots mid-run resumes from the last committed step instead of losing sensor telemetry collected over hours.

## Comparison

| Dimension | Heavy orchestrator | wpipe on edge |
| :--- | :--- | :--- |
| RAM footprint | 500MB - 2GB+ | <50MB |
| External deps | Broker + DB + scheduler | SQLite only |
| Crash recovery | Infra-dependent | Checkpoint resume |
| Runs on Raspberry Pi | Usually no | Yes |

## Conclusion

Green-IT and the edge have the same requirement: do more with less. By taming the memory footprint and making state persistence local, wpipe turns a constrained field device into a resilient orchestrator — one that protects both your data and the power bill.

> The most sustainable pipeline is the one that runs on the hardware you already have.

#IoT #GreenIT #EdgeComputing #wpipe #Sustainability #Python