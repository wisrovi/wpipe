# Industrial Pipelines on a Raspberry Pi: The Green-IT Way

## The Edge Computing Revolution

Industry 4.0 moved compute toward the data: sensors on the factory floor, gateways in cabinets, controllers at the machine. Edge devices process locally, send only summaries upstream, and keep working when the uplink blinks. The constraint that shapes all of this hardware is brutally simple: **there is very little memory and power to spare**.

Traditional orchestration — Airflow, its JVM neighbors, distributed schedulers — assumes a rack. It doesn't fit a rail-mounted ARM board.

## wpipe: The Edge-Native Orchestrator

wpipe was engineered for exactly these budgets:

- **<50MB RAM** steady state, leaving gigabytes-free or gigabytes-absent hardware to the workload.
- **Zero external services** — SQLite WAL file, no broker, no DB server.
- **Python-native** — ARM builds of CPython are first-class.

```python
from wpipe import Pipeline, step

@step(name="read_sensor", retry_count=3, retry_delay=10)
def read_sensor(data):
    return {"temp": read_modbus(data["addr"])}

@step(name="decide", retry_count=2)
def decide(data):
    return {"alert": data["temp"] > 85, **data}

@step(name="sync_cloud")
def sync_cloud(data):
    if data["alert"]:
        push_alert(data)
    return {"synced": True}

pipe = Pipeline(pipeline_name="factory_gateway", tracking_db="gateway.db")
pipe.set_steps([read_sensor, decide, sync_cloud])
pipe.run({"addr": 0x10})
```

A production deployment triggers this from cron on the device: same schedule reliability as a daemon, with zero always-on footprint beyond the pipeline itself.

## Battle Card: IoT Edition

| Feature | wpipe | Apache Airflow |
| :--- | :---: | :---: |
| Architecture | Lite (Python) | Heavy (JVM/Python/DB) |
| RAM | <50MB | 2GB+ |
| Energy | Ultra-low | High |
| External services | None | Scheduler + DB |
| Crash recovery | SQLite WAL | Infra-dependent |

```mermaid
graph LR
    Sensor[Sensor Data] --> wpipe[wpipe Agent]
    wpipe --> WAL[(SQLite WAL)]
    WAL --> Cloud[Cloud Sync]
```

## ARM Optimization Notes

- Checkpoints live on local flash: WAL writes are small, sequential, and power-loss safe.
- Because there's no broker, a network outage never blocks local processing.
- The pipeline consumes energy only while running — idle cost approaches zero.

## Conclusion

Green-IT isn't a certification sticker; it's the engineering choice to do more with less. wpipe turns a $50 single-board computer into a resilient, stateful orchestrator with industrial-grade behavior — proving that edge processing and sustainability are the same design.

#IoT #RaspberryPi #GreenIT #wpipe #Edge #Industry40