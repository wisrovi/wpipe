# Resource Monitoring Examples

Examples demonstrating system resource tracking during pipeline execution.

## Examples

### 01_basic
Basic resource monitoring for individual tasks.

**Run**: `python 01_basic/basic_monitoring.py`

**What it shows**:
- ResourceMonitor context manager
- Tracking RAM and CPU usage
- ResourceMonitorRegistry for aggregation

### 02_limits
Setting and enforcing resource limits.

**What it shows**:
- Resource limit detection
- Alerting on resource thresholds
- Limiting resource-intensive tasks

### 03_registry
Using ResourceMonitorRegistry for multiple tasks.

**What it shows**:
- Tracking multiple tasks
- Aggregate statistics
- Peak resource analysis

### 04_reporting
Generating resource reports.

**What it shows**:
- Exporting metrics to SQLite
- Generating reports
- Performance trending

## Key Concepts

- **Per-task monitoring**: ResourceMonitor for individual tasks
- **Aggregate tracking**: ResourceMonitorRegistry for multiple tasks
- **Metrics**: RAM (MB), CPU (%), elapsed time
- **Persistence**: Optional SQLite storage

## Common Patterns

```python
# Monitor single task
with ResourceMonitor("my_task", db_path="metrics.db") as monitor:
    do_work()

summary = monitor.get_summary()
print(f"Peak RAM: {summary['peak_ram_mb']} MB")

# Monitor multiple tasks
registry = ResourceMonitorRegistry()
for task_name in task_list:
    with ResourceMonitor(task_name, db_path="metrics.db") as m:
        run_task()
    registry.add(task_name, m)

peak_ram = registry.get_peak_ram()
```

## Stored Data

Metrics are stored in SQLite `resource_metrics` table:

```
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
- **Capacity planning**: Forecast infrastructure
- **Cost optimization**: Monitor cloud usage
- **Alerting**: Detect anomalies

## Notes

- Requires psutil library: `pip install psutil`
- CPU monitoring uses inter-sample intervals
- RAM tracking is in megabytes (MB)
- All timing is in seconds

## See Also

- [Resource Monitoring Documentation](../../wpipe/resource_monitor/README.md)
- [Phase 1 Features Guide](../../PHASE_1_FEATURES.md)
