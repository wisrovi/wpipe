"""
DEMO LEVEL 89: ResourceMonitor con Pipeline async
----------------------------------------------
Adds: Monitoreo con PipelineAsync.
Continues: L88.

DIAGRAM:
with ResourceMonitor + PipelineAsync
"""

import asyncio

from wpipe import PipelineAsync, ResourceMonitor

async def tarea_async(data):
    print("⚡ Tarea async ejecutándose...")
    await asyncio.sleep(0.05)
    print("✅ Tarea completada")

async def main():
    with ResourceMonitor("Viaje_L89") as monitor:
        pipe = PipelineAsync(pipeline_name="viaje_l89_async", verbose=True)
        pipe.set_steps([tarea_async])
        await pipe.run({})

    summary = monitor.get_summary()
    print(f"\n📊 Async Resource:")
    print(f"  RAM: {summary['peak_ram_mb']:.1f} MB")
    print(f"  CPU: {summary['avg_cpu_percent']:.1f}%")

if __name__ == "__main__":
    print(">>> Pipeline async con monitor...")
    asyncio.run(main())
