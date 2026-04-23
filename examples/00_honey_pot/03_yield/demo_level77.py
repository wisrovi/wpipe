"""
DEMO LEVEL 77: Lambda con Retorno
-------------------------------
Adds: Lambda que retorna datos.
Continues: L76.

DIAGRAM:
(lambda d: {"key": value})
"""

from wpipe import Pipeline

def process(data):
    print(f"📊 Velocidad: {data.get('speed')} km/h")
    return {"procesado": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l77_lambdareturn", verbose=True)
    pipe.set_steps(
        [
            (lambda d: {"speed": 120}, "set_speed", "v1.0"),
            (lambda d: {"temperatura": 25}, "set_temp", "v1.0"),
            process,
        ]
    )
    print("\n>>> Lambda con retorno de datos...\n")
    pipe.run({})
