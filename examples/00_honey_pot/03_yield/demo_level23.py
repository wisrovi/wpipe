"""
DEMO LEVEL 23: Compartimentación (Data Filtering)
--------------------------------------------------
Añade: Paso de sub-bodegas para proteger datos sensibles.
Acumula: Modularización (L19).

DIAGRAMA:
[Bodega Global: motor_id, posicion, imagen, velocidad]
      |
      v
(IA_Publicidad) <- ¡Solo recibe 'posicion'! (Privacidad)
"""

from wpipe import Pipeline, step


@step(name="telemetria_completa")
def telemetria_completa(d):
    return {"id_motor": "X-100", "posicion": "Gran Via", "velocidad": 50}


# NUEVO EN L23: Un paso que solo ve lo que le filtramos
@step(name="sugerir_restaurantes")
def sugerir_restaurantes(data):
    # Verificamos que no podamos ver el 'id_motor'
    id_visible = "id_motor" in data
    print(
        f"📍 Sugerencia en {data.get('posicion')}: ¿Ves el ID del motor? {id_visible}"
    )
    return {"sugerencia": "VIPS a 200m"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L23_Privacy", verbose=True)

    pipe.set_steps(
        [
            telemetria_completa,
            # Filtramos la bodega usando una función lambda intermedia
            (lambda d: {"posicion": d["posicion"]}, "FiltroPrivacidad", "v1"),
            sugerir_restaurantes,
        ]
    )

    pipe.run({})
