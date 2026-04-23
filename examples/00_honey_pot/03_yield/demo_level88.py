"""
DEMO LEVEL 88: ResourceMonitor en Bucle
-------------------------------------
Adds: Monitoreo en múltiples ejecuciones.
Continues: L87.

DIAGRAM:
for i in range(3): ResourceMonitor()
"""

import time

from wpipe import Pipeline, ResourceMonitor, step


@step(name="task")
def task(data: dict) -> None:
    """Task step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.02)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Múltiples ejecuciones...")

    with ResourceMonitor("Viaje_L88") as monitor:
        for i in range(3):
            pipe = Pipeline(pipeline_name=f"Viaje_L88_{i}", verbose=False)
            pipe.set_steps([task])
            pipe.run({})
            print(f"  ✅ iteración {i}")

    summary = monitor.get_summary()
    print(f"\n📊 Total 3 ejecuciones:")
    print(f"  Peak RAM: {summary['peak_ram_mb']:.1f} MB")
    print(f"  Avg CPU: {summary['avg_cpu_percent']:.1f}%")
