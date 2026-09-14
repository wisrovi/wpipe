# Security at the Edge: Running Detection Workflows Where Data Lives

Security tooling has a deployment problem. The best threat detection in the world is useless if the data can't reach it — and in edge environments, that data lives on constrained devices far from the SOC.

## The Edge Constraint

Edge devices (Raspberry Pis, industrial gateways, K8s nodes on-prem) share one hard limit: they cannot run the heavy stack that enterprise security platforms require. Agents that need 2GB of RAM, a broker, and a central database simply don't fit.

Security orchestration therefore has two choices today:

1. Ship raw data to a central SOAR and process it there (latency, bandwidth, privacy problems).
2. Run lightweight processing locally and escalate only anomalies.

Option 2 is where wpipe lives.

## Orchestrate Detection as a Pipeline

A detection workflow is a data pipeline: **ingest → enrich → correlate → decide → respond**. Nothing about it requires a heavy framework. It requires reliability.

- **<50MB RAM** footprint fits the edge devices that need it.
- **SQLite WAL checkpoints** mean an interrupted detection run resumes from the last event processed — no lost IOCs during a power dip.
- **Pure Python steps** are auditable in a security review, versionable in git, and testable in CI.

```python
from wpipe import Pipeline, step

@step(name="ingest_events", retry_count=3)
def ingest_events(data):
    return {"events": data["raw_events"]}

@step(name="correlate_ioc", retry_count=2, retry_delay=1)
def correlate_ioc(data):
    hits = [e for e in data["events"] if e["score"] > 7]
    return {"suspicious": hits}

pipe = Pipeline(pipeline_name="edge_soar", tracking_db="edge_soc.db")
pipe.set_steps([ingest_events, correlate_ioc])
pipe.run({"raw_events": [...]})
```

## Clear Benefits for SecOps

| Concern | Heavy SOAR | wpipe edge |
| :--- | :--- | :--- |
| RAM | 500MB - 2GB+ | <50MB |
| Code transparency | Opaque playbooks | Auditable Python |
| Failure recovery | Depends on infra | Checkpoint resume |
| Run on premise | Often impossible | Native |

## Conclusion

Security shouldn't be locked behind heavyweight platforms. By making orchestration light, transparent, and crash-safe, wpipe brings detection workflows directly to the devices that generate the signals — reducing data egress, latency, and the attack surface of moving raw data around.

> Edge security wins when the pipeline fits the device.

#Cybersecurity #SOAR #EdgeComputing #wpipe #Python #SecOps