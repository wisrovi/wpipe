"""
DEMO LEVEL 35: Radar de Objetos Múltiples (Complex Pydantic)
------------------------------------------------------------
Añade: Estructuras de IA anidadas y listas de objetos.
Acumula: Visión ADAS (L10) y Pydantic (L16).

DIAGRAMA:
(Radar_IA) -> { 'lista': [ {'tipo': 'Coche', 'id': 1}, ... ] }
      |
      v
(Procesar_Radar) -> Valida cada objeto de la lista individualmente.
"""

from typing import List

from pydantic import BaseModel, Field

from wpipe import Pipeline, step, to_obj


class ObjetoDetectado(BaseModel):
    tipo: str
    confianza: float = Field(..., ge=0, le=1)


class RadarMap(BaseModel):
    detecciones: List[ObjetoDetectado]


@step(name="radar_yolo_pro")
def radar_yolo(d):
    return {
        "detecciones": [
            {"tipo": "Peatón", "confianza": 0.98},
            {"tipo": "Bicicleta", "confianza": 0.85},
            {"tipo": "Coche", "confianza": 0.92},
        ]
    }


@step(name="analisis_entorno")
@to_obj(RadarMap)
def analisis_entorno(ctx: RadarMap):
    print(f"👁️  Radar: Identificados {len(ctx.detecciones)} elementos en trayectoria.")
    for obj in ctx.detecciones:
        print(f"   - {obj.tipo} (Confianza: {obj.confianza*100:.0f}%)")
    return {"via_libre": False}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Advanced_Radar_L35", verbose=True)
    pipe.set_steps([radar_yolo, analisis_entorno])
    pipe.run({})
