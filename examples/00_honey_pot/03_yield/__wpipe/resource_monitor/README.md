# Resource Monitoring

Track system resource usage (RAM, CPU) during pipeline task execution.

## Features

- **RAM tracking**: Monitor RAM usage (start, peak, end)
- **CPU monitoring**: Track CPU percentage during execution
- **Context manager**: Simple `with` statement usage
- **Metrics persistence**: Optional SQLite storage
- **Registry**: Track multiple tasks and aggregate metrics

## Quick Start

```python
from wpipe import ResourceMonitor

# Monitor a task
with ResourceMonitor("my_task", db_path="metrics.db") as monitor:
    do_work()

# Get summary
summary = monitor.get_summary()
print(f"Peak RAM: {summary['peak_ram_mb']} MB")
print(f"Elapsed: {summary['elapsed_seconds']}s")

# Use registry for multiple tasks
from wpipe import ResourceMonitorRegistry

registry = ResourceMonitorRegistry()

with ResourceMonitor("task1") as m1:
    task1()
registry.add("task1", m1)

with ResourceMonitor("task2") as m2:
    task2()
registry.add("task2", m2)

# Get aggregate stats
total_summary = registry.get_summary()
peak_ram = registry.get_peak_ram()
print(f"Total peak RAM: {peak_ram} MB")
```

## API

### ResourceMonitor

#### `__init__(task_name: str, db_path: Optional[str] = None)`
Initialize resource monitor.

#### `start()`
Start monitoring.

#### `stop()`
Stop monitoring and save metrics.

#### `get_summary() -> Dict`
Get monitoring summary including RAM, CPU, and timing.

#### Properties

- `elapsed_seconds`: Total execution time
- `ram_increase_mb`: RAM increase during execution
- `peak_ram_mb`: Peak RAM usage
- `avg_cpu_percent`: Average CPU usage

### ResourceMonitorRegistry

#### `add(task_name: str, monitor: ResourceMonitor)`
Add a monitor to the registry.

#### `get_summary() -> Dict`
Get summary of all monitored tasks.

#### `get_peak_ram() -> float`
Get peak RAM across all tasks.

#### `get_total_cpu_time() -> float`
Get total CPU time across all tasks.

## Stored Metrics

When `db_path` is provided, metrics are stored in SQLite:

```
resource_metrics table:
- task_name: str
- start_ram_mb: float
- peak_ram_mb: float
- end_ram_mb: float
- avg_cpu_percent: float
- elapsed_seconds: float
- created_at: timestamp
```

## Use Cases

- **Performance profiling**: Identify bottlenecks
- **Resource budgeting**: Track resource consumption
- **Capacity planning**: Forecast infrastructure needs
- **Alerting**: Detect anomalies in resource usage
- **Cost optimization**: Monitor cloud resource utilization
