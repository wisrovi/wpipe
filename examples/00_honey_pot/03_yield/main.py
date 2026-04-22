import random
import time
import cv2

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

test_Wsqlite()


SIZE_CAPTURE = 300


def generator_capture():
    image = cv2.imread("images.jpeg")
    for i in range(SIZE_CAPTURE):
        image_tmp = image.copy()

        # write in image the number of "i"
        cv2.putText(
            image_tmp, str(i), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )

        yield (i, image_tmp)


@step(name="start_capture", version="v1.0")
@to_obj
def start_capture(context: object):
    return {
        "capture": generator_capture(),
        "video_size": SIZE_CAPTURE,
        "process_complete": int(False),
        "A_predictions_all": [],
        "B_predictions_all": [],
        "C_predictions_all": [],
    }


@step(name="create_batch", version="v1.0")
class Create_batch:
    def __init__(self, size=2):
        self.size = size

    @to_obj
    def __call__(self, context: object):
        batch = []

        process_complete = False
        i = -1

        while len(batch) < self.size:
            try:
                i, image = next(context.capture)
                batch.append((i, image))
            except StopIteration:
                break

        if i >= context.video_size - 1:
            process_complete = True

        return {"batch": batch, "process_complete": int(process_complete)}


@step(name="notificar_telegram_error", version="v1.0")
def notificar_telegram_error(context, error):
    """
    Simula el envío de una notificación detallada a Telegram.
    Recibe el contexto y los detalles técnicos del error.
    """
    print("\n" + "!" * 60)
    print("🚨 ALERTA DE SISTEMA: ERROR DETECTADO")
    print("!" * 60)
    print(f"📍 ESTADO FALLIDO: {error['step_name']}")
    print(f"📄 ARCHIVO: {error['file_path']}")
    print(f"🔢 LÍNEA: {error['line_number']}")
    print(f"⚠️ MENSAJE: {error['error_message']}")
    print("-" * 60)
    # print("🔍 INFO DE LA BODEGA (CONTEXTO):")
    # print(
    #     f"   Modelo: {context.get('modelo')} | Gasolina: {context.get('nivel_gasolina')}"
    # )
    # print("-" * 60)
    # Aquí podrías usar requests.post para enviar el mensaje real
    return context


def random_mask():
    return [
        # tupla de dos valores de 0 a 255, de valor aleatorio
        (random.randint(0, 255), random.randint(0, 255))
        for _ in range(random.randint(30, 80))
    ]


TEMPLATE = {
    "class": "0",
    "class_name": "demo",
    "confidence": 0.2,
    "mask": random_mask(),
}

CLASS_NAMES_A = [f"class_A_{i}" for i in range(30)]
CLASS_NAMES_B = [f"class_B_{i}" for i in range(30)]
CLASS_NAMES_C = [f"class_C_{i}" for i in range(30)]


@step(name="simulated_inference", version="v1.0")
class Simulated_inference:
    def __init__(self, ref_class_names, sub_name):
        self.ref_class_names = ref_class_names
        self.sub_name = sub_name

    @to_obj
    def __call__(self, context: object):
        batch_ids = [id_ for id_, _ in context.batch]
        batch_images = [image for _, image in context.batch]

        # simulate if there are or there aren't predictions
        SELECTION = 50

        predictions = []

        for batch_id, batch_image in zip(batch_ids, batch_images):
            # simulated wait of predictions
            time.sleep(0.001)

            random_value = random.randint(0, 100)
            there_predictions = True if random_value > SELECTION else False

            if not there_predictions:
                predictions.append((batch_id, None))
                continue

            template_tmp = TEMPLATE.copy()
            template_tmp["class_name"] = random.choice(self.ref_class_names)
            template_tmp["confidence"] = random.random()
            template_tmp["mask"] = random_mask()

            predictions.append((batch_id, template_tmp))

        return {f"{self.sub_name}_predictions": predictions}


@step(name="draw_ia", version="v1.0")
@to_obj
def draw_ia(context: object):
    batch_ids = [id_ for id_, _ in context.batch]
    batch_images = [image for _, image in context.batch]

    a_predictions = context.A_predictions
    b_predictions = context.B_predictions
    c_predictions = context.C_predictions

    print(
        f"DEBUG draw_ia: batch={len(batch_ids)}, A={len(a_predictions)}, B={len(b_predictions)}, C={len(c_predictions)}"
    )

    a_preds_filtered = [(id_, p) for id_, p in a_predictions if id_ in batch_ids]
    b_preds_filtered = [(id_, p) for id_, p in b_predictions if id_ in batch_ids]
    c_preds_filtered = [(id_, p) for id_, p in c_predictions if id_ in batch_ids]

    new_batch_images = []

    for batch_id, batch_image in zip(batch_ids, batch_images):
        a_match = next(
            ((id_, p) for id_, p in a_preds_filtered if id_ == batch_id),
            (batch_id, None),
        )
        b_match = next(
            ((id_, p) for id_, p in b_preds_filtered if id_ == batch_id),
            (batch_id, None),
        )
        c_match = next(
            ((id_, p) for id_, p in c_preds_filtered if id_ == batch_id),
            (batch_id, None),
        )

        a_id, a_pred = a_match
        b_id, b_pred = b_match
        c_id, c_pred = c_match

        if a_id != batch_id or b_id != batch_id or c_id != batch_id:
            raise Exception("Error: desncronizacion")

        if a_pred:
            cv2.putText(
                batch_image,
                str(a_pred["class_name"]),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
        if b_pred:
            cv2.putText(
                batch_image,
                str(b_pred["class_name"]),
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
        if c_pred:
            cv2.putText(
                batch_image,
                str(c_pred["class_name"]),
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )

        new_batch_images.append((batch_id, batch_image))

    return {"batch": new_batch_images}


@step(name="save_images", version="v1.0")
@to_obj
def save_images(context: object):
    batch_ids = [id_ for id_, _ in context.batch]
    batch_images = [image for _, image in context.batch]

    path_to_save = "output/images"
    for batch_id, batch_image in zip(batch_ids, batch_images):
        cv2.imwrite(f"{path_to_save}/{batch_id}.jpg", batch_image)
    return {"saved": True}


db_path = "output/wpipe_dashboard.db"
pipe = Pipeline(
    pipeline_name="viaje_tmp",
    verbose=False,
    tracking_db=db_path,
)
pipe.add_error_capture([notificar_telegram_error])

pipe.set_steps(
    [
        start_capture,
        For(
            validation_expression="process_complete == 0",
            steps=[
                Create_batch(2),
                Parallel(
                    steps=[
                        Simulated_inference(CLASS_NAMES_A, "A"),
                        Simulated_inference(CLASS_NAMES_B, "B"),
                        Simulated_inference(CLASS_NAMES_C, "C"),
                    ],
                    max_workers=3,
                    # use_processes=False  # Cambiado a False para evitar errores de pickling con objetos complejos
                ),
                draw_ia,
            ],
        ),
        save_images,
    ],
)
pipe.run({})
