"""
DEMO LEVEL 80: Lambda Complejo
-------------------------------
Añade: Lambda con lógica completa.
Continúa: L79.

DIAGRAMA:
(lambda d: if x > 0 else y)
"""

from wpipe import Pipeline


def verificar_sistema(data):
    print("🔍 Verificando sistema...")
    return {"fuel": 50, "temp": 90, "ok": True}


def evaluar_estado(data):
    fuel = data.get("fuel", 0)
    temp = data.get("temp", 0)

    if fuel < 20:
        print("⛽ ALERTA: Combustible bajo!")
    elif temp > 85:
        print("🌡️ ALERTA: Sobrecalentamiento!")
    else:
        print("✅ Sistema OK")
    return {"estado": "ok"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L80_LambdaComplex", verbose=True)
    pipe.set_steps(
        [
            verificar_sistema,
            evaluar_estado,
        ]
    )
    print("\n>>> Lambda con lógica condicional...\n")
    pipe.run({"fuel": 50, "temp": 90})
