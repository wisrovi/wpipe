"""
DEMO LEVEL 5: Bodega Inicial Dinámica
-------------------------------------
Añade: Inyección de datos al iniciar el pipeline (run).
Acumula: Paso 1 al 4 (motor, frenos, validar, GPS).

DIAGRAMA:
[Bodega con 'clima': 'Soleado'] <--- Inyectado en run()
      |
      v
(Pasos 1-4) --> [motor, frenos, destino, etc.]
      |
      v
(ajustar_climatizador) -> ¡Usa el dato inyectado al inicio!
"""

from wpipe import Pipeline, step, to_obj


# Heredados simplificados:
def encender_motor(data):
    return {"motor": "ON"}


@step(name="configurar_gps")
class ConfigurarGPS:
    def __init__(self, d):
        self.d = d

    def __call__(self, data):
        return {"destino": self.d}


# NUEVO EN L5: Uso de datos inyectados externamente
@step(name="ajustar_clima")
@to_obj
def ajustar_clima(ctx):
    # 'clima' vendrá del diccionario inicial del run()
    print(f"🌡️ Clima exterior: {ctx.clima}. Ajustando aire...")
    return {"clima_interior": 22}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L5", verbose=True)
    pipe.set_steps([encender_motor, ConfigurarGPS("Madrid"), ajustar_clima])

    # PASAMOS DATOS INICIALES AQUÍ:
    pipe.run({"clima": "Soleado"})
