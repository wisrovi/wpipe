"""
DEMO LEVEL 87: ResourceMonitor con Proceso Pesado
---------------------------------------------
Adds: Monitoreo con proceso que consume recursos.
Continues: L86.

DIAGRAM:
with ResourceMonitor() --> proceso pesado
"""

import time

from wpipe import Pipeline, ResourceMonitor, step

@step(name="proceso_pesado")
def proceso_pesado(data: dict) -> None:

    """Proceso pesado step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔄 Procesando...")
    time.sleep(0.2)
    print("✅ Completado")
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Proceso monitorizado...")

    with ResourceMonitor("Viaje_L87") as monitor:
        pipe = Pipeline(pipeline_name="viaje_l87_heavyprocess", verbose=True)
        pipe.set_steps([proceso_pesado])
        pipe.run({})

    summary = monitor.get_summary()
    print(f"\n📊 Estado final:")
    print(f"  RAM: {summary['peak_ram_mb']:.1f} MB")
    print(f"  CPU: {summary['avg_cpu_percent']:.1f}%")
