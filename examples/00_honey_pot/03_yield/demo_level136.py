"""
DEMO LEVEL 136: Background en PipelineAsync
--------------------------------------------
Adds: Background task en pipeline asíncrono.
Continues: L135.

DIAGRAM:
PipelineAsync → Background(async_task) → next
"""

import asyncio
import time

from wpipe import PipelineAsync
from wpipe.pipe.components.logic_blocks import Background


async def process_task(data):
    """Tarea de procesamiento."""
    print("⚡ Procesando...")
    await asyncio.sleep(0.05)
    return {"processed": True}


async def background_async(data):
    """Tarea async en background."""
    print("🔄 [BG-ASYNC] Iniciando tarea async...")
    await asyncio.sleep(0.2)
    print("🔄 [BG-ASYNC] ¡Completado!")


async def after_background(data):
    """Después de background."""
    print("✅ Pipeline async continúa sin esperar!")
    return data


async def main():
    print(">>> DEMO 136: Background en PipelineAsync")
    print("=" * 50)

    start = time.time()

    pipe = PipelineAsync(pipeline_name="demo_136", verbose=False)
    pipe.set_steps([
        process_task,
        Background(background_async),
        after_background,
    ])

    result = await pipe.run({})

    elapsed = time.time() - start
    print(f"\n⏱️ Tiempo: {elapsed*1000:.0f}ms")


if __name__ == "__main__":
    asyncio.run(main())