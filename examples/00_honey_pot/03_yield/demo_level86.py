"""
DEMO LEVEL 86: ResourceMonitor
-------------------------------
Añade: Monitoreo de recursos del sistema.
Continúa: Export de L85.

DIAGRAMA:
with ResourceMonitor("nombre") --> medir RAM/CPU
"""

import time

from wpipe import Pipeline, ResourceMonitor, step


@step(name="proceso")
def proceso(data):
    time.sleep(0.05)
    print("⚡ Proceso completado")
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Monitor de recursos...")

    with ResourceMonitor("Viaje_L86") as monitor:
        pipe = Pipeline(pipeline_name="Viaje_L86_Resource", verbose=True)
        pipe.set_steps([proceso])
        pipe.run({})

    summary = monitor.get_summary()
    print(f"\n📊 Resource Summary:")
    print(f"  Peak RAM: {summary['peak_ram_mb']:.1f} MB")
    print(f"  Avg CPU: {summary['avg_cpu_percent']:.1f}%")
