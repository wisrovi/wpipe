"""
DEMO LEVEL 43: Async con Retry (Usando Pipeline)
--------------------------------------
Añade: Retry en pipeline async.
Continúa: L42.

DIAGRAMA:
(conectar_coche) -[fallo]-> retry --> [conectado]
"""

import asyncio
import random

from wpipe import PipelineAsync


async def conectar_coche(data):
    if random.random() < 0.4:
        raise ConnectionError("Bluetooth no disponible")
    print("📱 [ASYNC] Coche conectado")
    return {"conectado": True}


async def sincronizar_datos(data):
    print("🔄 [ASYNC] Datos sincronizados")
    return {"sync": "ok"}


if __name__ == "__main__":

    async def main():
        pipe = PipelineAsync(
            pipeline_name="Viaje_L43_AsyncRetry",
            verbose=True,
            max_retries=3,
            retry_delay=0.1,
        )
        pipe.set_steps([conectar_coche, sincronizar_datos])
        print("\n>>> Probando retry async...\n")
        try:
            await pipe.run({})
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
