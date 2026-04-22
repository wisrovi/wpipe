"""
DEMO LEVEL 130: API Completo (Demo Final)
-----------------------------------
Añade: Demo final integrando todo.
Continúa: L129.

DIAGRAMA:
Demo completo de API con pipeline
"""

from wpipe import Pipeline, step, Metric
from wpipe.api_client import APIClient


@step(name="iniciar")
def iniciar(data):
    print("🔑 Iniciando sistema API...")
    return {"iniciado": True}


@step(name="procesar")
def procesar(data):
    print("⚡ Procesando datos...")
    Metric.record("api_calls", 1)
    return {"procesado": True}


if __name__ == "__main__":
    print("=" * 50)
    print("🎉 DEMO FINAL - API Integration")
    print("=" * 50)

    pipe = Pipeline(pipeline_name="Viaje_L130", verbose=True)
    pipe.set_steps([iniciar, procesar])
    pipe.run({})

    print("\n✅ Demo completado con éxito!")
    print(f"📊 Metric: api_calls = 1")
