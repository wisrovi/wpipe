"""
DEMO LEVEL 86: ResourceMonitor
-------------------------------
Adds: Monitoreo de recursos del sistema.
Continues: Export de L85.

DIAGRAM:
with ResourceMonitor("nombre") --> measure RAM/CPU
"""

import time

from wpipe import Pipeline, ResourceMonitor, step

@step(name="proceso")
def proceso(data: dict) -> None:

    """Proceso step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.05)
    print("⚡ Proceso completado")
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Monitor de recursos...")

    with ResourceMonitor("Viaje_L86") as monitor:
        pipe = Pipeline(pipeline_name="viaje_l86_resource", verbose=True)
        pipe.set_steps([proceso])
        pipe.run({})

    summary = monitor.get_summary()
    print(f"\n📊 Resource Summary:")
    print(f"  Peak RAM: {summary['peak_ram_mb']:.1f} MB")
    print(f"  Avg CPU: {summary['avg_cpu_percent']:.1f}%")
