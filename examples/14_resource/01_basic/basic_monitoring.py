"""
Basic resource monitoring example.

Demonstrates tracking RAM and CPU usage during task execution.
"""

import time

from wpipe import ResourceMonitor, ResourceMonitorRegistry


def cpu_intensive_task():
    """Task that uses CPU."""
    print("Running CPU-intensive task...")
    result = 0
    for i in range(10_000_000):
        result += i
    return result


def memory_intensive_task():
    """Task that uses memory."""
    print("Running memory-intensive task...")
    large_list = list(range(1_000_000))
    time.sleep(1)
    return len(large_list)


def io_task():
    """Simulate I/O task."""
    print("Running I/O task...")
    time.sleep(2)
    return "I/O complete"


if __name__ == "__main__":
    print("=== Basic Resource Monitoring Example ===\n")

    # Example 1: Monitor single task
    print("--- Example 1: Single Task Monitoring ---")
    with ResourceMonitor("cpu_task", db_path="resources.db") as monitor:
        result = cpu_intensive_task()

    summary = monitor.get_summary()
    print(f"✓ Task completed")
    print(f"  Elapsed: {summary['elapsed_seconds']}s")
    print(f"  Peak RAM: {summary['peak_ram_mb']:.2f} MB")
    print(f"  RAM increase: {summary['ram_increase_mb']:.2f} MB")
    print(f"  Avg CPU: {summary['avg_cpu_percent']:.2f}%\n")

    # Example 2: Monitor multiple tasks with registry
    print("--- Example 2: Multiple Tasks with Registry ---")
    registry = ResourceMonitorRegistry()

    # Task 1
    print("\nMonitoring CPU task...")
    with ResourceMonitor("cpu_intensive", db_path="resources.db") as m1:
        cpu_intensive_task()
    registry.add("cpu_intensive", m1)

    # Task 2
    print("\nMonitoring memory task...")
    with ResourceMonitor("memory_intensive", db_path="resources.db") as m2:
        memory_intensive_task()
    registry.add("memory_intensive", m2)

    # Task 3
    print("\nMonitoring I/O task...")
    with ResourceMonitor("io_task", db_path="resources.db") as m3:
        io_task()
    registry.add("io_task", m3)

    # Get aggregate stats
    print("\n--- Aggregate Statistics ---")
    peak_ram = registry.get_peak_ram()
    total_cpu_time = registry.get_total_cpu_time()

    print(f"Peak RAM across all tasks: {peak_ram:.2f} MB")
    print(f"Total CPU time: {total_cpu_time:.2f}%")

    # Get individual summaries
    print("\n--- Individual Task Summaries ---")
    all_summaries = registry.get_summary()
    for task_name, summary in all_summaries.items():
        print(f"\n{task_name}:")
        print(f"  Elapsed: {summary['elapsed_seconds']}s")
        print(f"  RAM: {summary['start_ram_mb']:.2f} → {summary['peak_ram_mb']:.2f} MB")
        print(f"  CPU avg: {summary['avg_cpu_percent']:.2f}%")

    print("\n✓ Metrics saved to resources.db")
