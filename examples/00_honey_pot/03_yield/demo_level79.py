"""
DEMO LEVEL 79: Lambda Procesando Datos
------------------------------------
Adds: Lambda que transforma datos.
Continues: L78.

DIAGRAM:
(lambda d: modificar(d))
"""

from wpipe import Pipeline

def inicializar(data):
    print(f"📥 Input: fuel={data.get('fuel')}")
    return {"fuel": 100, "km": 0}

def actualizar(data):
    fuel = data.get("fuel", 100)
    km = data.get("km", 0)
    consumption = km * 0.05
    fuel_restante = fuel - consumption
    print(f"⛽ fuel: {fuel} -> {fuel_restante}km (consumption: {consumption:.1f}L)")
    return {"fuel": fuel_restante}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l79_lambdaprocess", verbose=True)
    pipe.set_steps(
        [
            inicializar,
            (lambda d: {"km": d.get("km", 0) + 50}, "add_km", "v1.0"),
            actualizar,
        ]
    )
    print("\n>>> Lambda procesando datos...\n")
    pipe.run({})
