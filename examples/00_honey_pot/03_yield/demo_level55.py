import os
import random
import time
import cv2
from wpipe import (
    For,
    Parallel,
    Pipeline,
    step,
    to_obj,
)

# Configuración idéntica al main original
SIZE_CAPTURE = 50
CLASS_NAMES = [f"Class_{i}" for i in range(10)]

def generator_capture():
    image = cv2.imread("images.jpeg")
    if image is None: # Fallback por si no encuentra la imagen
        import numpy as np
        image = np.zeros((300, 300, 3), dtype=np.uint8)
    for i in range(SIZE_CAPTURE):
        image_tmp = image.copy()
        cv2.putText(image_tmp, str(i), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        yield (i, image_tmp)

@step(name="start_capture")
@to_obj
def start_capture(context):
    return {"cap": generator_capture(), "video_size": SIZE_CAPTURE}

@step(name="create_batch")
@to_obj
def create_batch(context):
    try:
        frame_id, frame = next(context.cap)
        return {"batch": [(frame_id, frame)]}
    except StopIteration:
        return {"error": "Fin del generador"}

@step(name="heavy_inference")
class HeavyInference:
    def __init__(self, sub_name):
        self.sub_name = sub_name

    @to_obj
    def __call__(self, context):
        # Simulamos carga de CPU real
        start = time.time()
        while time.time() - start < 0.05:
            _ = 100 * 100
        
        return {f"{self.sub_name}_pred": "Detected"}

if __name__ == "__main__":
    os.makedirs("output/multiprocess", exist_ok=True)
    
    pipe = Pipeline(pipeline_name="viaje_multiproceso", verbose=True)
    
    pipe.set_steps([
        start_capture,
        For(
            iterations=SIZE_CAPTURE,
            steps=[
                create_batch,
                Parallel(
                    steps=[
                        HeavyInference("A"),
                        HeavyInference("B"),
                        HeavyInference("C"),
                    ],
                    max_workers=3,
                    use_processes=True # <--- ACTIVACIÓN DE MULTIPROCESO
                ),
            ]
        )
    ])
    
    print("Startsndo Pipeline con Multiprocesamiento (CPU Intensive)...")
    pipe.run({})
