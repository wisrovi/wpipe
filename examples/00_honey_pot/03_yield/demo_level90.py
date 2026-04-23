"""
DEMO LEVEL 90: ResourceMonitor + TaskTimer
-----------------------------------------
Adds: Combinar ResourceMonitor con TaskTimer.
Continues: L89.

DIAGRAM:
with ResourceMonitor + with TaskTimer
"""

import time

from wpipe import Pipeline, step, ResourceMonitor, TaskTimer

@step(name="proceso")
def proceso(data: dict) -> None:

    """Proceso step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔄 Procesando...")
    time.sleep(0.1)
    print("✅ Completado")
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Monitoreo completo...")

    with ResourceMonitor("Viaje_L90") as monitor:
        with TaskTimer("viaje_l90", timeout_seconds=5) as timer:
            pipe = Pipeline(pipeline_name="viaje_l90", verbose=True)
            pipe.set_steps([proceso])
            pipe.run({})

    summary = monitor.get_summary()
    print(f"\n📊 Recursos:")
    print(f"  RAM: {summary['peak_ram_mb']:.1f} MB")
    print(f"  Tiempo: {timer.elapsed_seconds:.3f}s")
    print(f"  Excedido: {timer.exceeded_timeout()}")
