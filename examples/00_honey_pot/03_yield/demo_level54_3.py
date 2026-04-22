import os
import random
import time

import cv2
from genericpath import exists

from extras.wsqlite_test import test_Wsqlite
from wpipe import (
    Condition,
    For,
    Metric,
    Parallel,
    Pipeline,
    PipelineContext,
    PipelineExporter,
    ResourceMonitor,
    Severity,
    TaskTimer,
    auto_dict_input,
    object_to_dict,
    step,
    to_obj,
)


SIZE_CAPTURE = 150


def generator_capture():
    image = cv2.imread("images.jpeg")
    for i in range(SIZE_CAPTURE):
        image_tmp = image.copy()
        cv2.putText(
            image_tmp, str(i), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )
        yield (i, image_tmp)


@step(name="start_capture", version="v1.0")
@to_obj
def start_capture(context: object):
    cap = generator_capture()
    return {
        "cap": cap,
        "video_size": SIZE_CAPTURE,
        "process_complete": int(False),
    }


@step(name="create_batch", version="v1.0")
class Create_batch:
    def __init__(self, size=2):
        self.size = size

    @to_obj
    def __call__(self, context: object):
        print("Running Create_batch step...", flush=True)
        batch = []
        process_complete = False

        for _ in range(self.size):
            frame_id, frame = next(context.cap)

            batch.append((frame_id, frame))

            if frame_id >= context.video_size:
                process_complete = True

        return {"batch": batch, "process_complete": process_complete}


@step(name="notificar_telegram_error", version="v1.0")
def notificar_telegram_error(context, error):
    print("\n" + "!" * 60)
    print("🚨 ALERTA DE SISTEMA: ERROR DETECTADO")
    print("!" * 60)
    print(f"📍 ESTADO FALLIDO: {error['step_name']}")
    print(f"📄 ARCHIVO: {error['file_path']}")
    print(f"🔢 LÍNEA: {error['line_number']}")
    print(f"⚠️ MENSAJE: {error['error_message']}")
    print("-" * 60)
    return context


def random_mask():
    return [
        (random.randint(0, 255), random.randint(0, 255))
        for _ in range(random.randint(30, 80))
    ]


TEMPLATE = {
    "class": "0",
    "class_name": "demo",
    "confidence": 0.2,
    "mask": random_mask(),
}

CLASS_NAMES_A = [f"A_{i}" for i in range(30)]
CLASS_NAMES_B = [f"B_{i}" for i in range(30)]
CLASS_NAMES_C = [f"C_{i}" for i in range(30)]


@step(name="simulated_inference", version="v1.0")
class Simulated_yolo_inference:
    _counter = 0

    def __init__(self, ref_class_names, sub_name):
        self.ref_class_names = ref_class_names
        self.sub_name = sub_name
        self._instance_id = Simulated_yolo_inference._counter
        Simulated_yolo_inference._counter += 1

    @to_obj
    def __call__(self, context: object):
        batch_ids = [id_ for id_, _ in context.batch]
        batch_images = [image for _, image in context.batch]

        SELECTION = 50

        predictions = []

        for frame_id, frame in zip(batch_ids, batch_images):
            time.sleep(0.001)

            random_value = random.randint(0, 100)
            there_predictions = True if random_value > SELECTION else False

            if not there_predictions:
                predictions.append((frame_id, None))
                continue

            template_tmp = TEMPLATE.copy()
            template_tmp["class_name"] = random.choice(self.ref_class_names)
            template_tmp["confidence"] = round(random.random(), 2)
            template_tmp["mask"] = random_mask()

            predictions.append((frame_id, template_tmp))

        return {f"{self.sub_name}_predictions": predictions}


def put_text(frame, text, y=80):
    cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame


@step(name="draw_ia", version="v1.0")
@to_obj
def draw_ia(context: object):
    batch_ids = [id_ for id_, _ in context.batch]
    batch_images = [image for _, image in context.batch]

    a_predictions = context.A_predictions
    b_predictions = context.B_predictions
    c_predictions = context.C_predictions

    print(f"[DEBUG draw_ia] batch_ids: {batch_ids}", flush=True)
    print(f"[DEBUG draw_ia] batch has: {len(context.batch)} items", flush=True)

    new_batch_images = []

    for frame_id, frame, (A_id, A_predict), (B_id, B_predict), (C_id, C_predict) in zip(
        batch_ids, batch_images, a_predictions, b_predictions, c_predictions
    ):
        if frame_id != A_id != B_id != C_id:
            raise Exception("Error: desncronizacion")

        if A_predict is not None:
            A_text = (
                str(A_predict["class_name"]) + "-" + str(A_predict.get("confidence"))
            )
        else:
            A_text = "-o-"

        if B_predict is not None:
            B_text = (
                str(B_predict["class_name"]) + "-" + str(B_predict.get("confidence"))
            )
        else:
            B_text = "-o-"

        if C_predict is not None:
            C_text = (
                str(C_predict["class_name"]) + "-" + str(C_predict.get("confidence"))
            )
        else:
            C_text = "-o-"

        frame = put_text(frame, A_text, y=80)
        frame = put_text(frame, B_text, y=120)
        frame = put_text(frame, C_text, y=160)

        new_batch_images.append((frame_id, frame))

    return {"batch": new_batch_images}


@step(name="save_images", version="v1.0")
@to_obj
def save_images(context: object):
    import sys

    print("save_images called!", flush=True)
    batch_ids = [id_ for id_, _ in context.batch]
    batch_images = [image for _, image in context.batch]

    print(f"[save_images] Saving {len(batch_ids)} images", flush=True)

    path_to_save = "output/images"
    for frame_id, frame in zip(batch_ids, batch_images):
        cv2.imwrite(f"{path_to_save}/{frame_id}.jpg", frame)
    return {"saved": True}


os.makedirs("output/images", exist_ok=True)


db_path = "output/wpipe_dashboard.db"
pipe = Pipeline(
    pipeline_name="viaje_tmp",
    verbose=False,
    show_progress=False,
    tracking_db=db_path,
)
pipe.add_error_capture([notificar_telegram_error])

pipe.set_steps(
    [
        start_capture,
        For(
            iterations=150,
            steps=[
                Create_batch(2),
                Parallel(
                    steps=[
                        Simulated_yolo_inference(CLASS_NAMES_A, "A"),
                        Simulated_yolo_inference(CLASS_NAMES_B, "B"),
                        Simulated_yolo_inference(CLASS_NAMES_C, "C"),
                    ],
                    max_workers=3,
                    use_processes=False,
                ),
                draw_ia,
                save_images,
            ],
        ),
    ],
)
pipe.run({})
