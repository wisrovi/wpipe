from wpipe import Pipeline, step, Condition, Parallel, For
import logging

logger = logging.getLogger(__name__)

# Mock steps
@step(name="check_requirements")
def check_requirements(data):
    return data

@step(name="clean_folder")
def clean_folder(data):
    return data

@step(name="reset_part_model")
def reset_part_model(data):
    return data

@step(name="reset_damage_search")
def reset_damage_search(data):
    return data

@step(name="open_video_capture")
def open_video_capture(data):
    return data

@step(name="create_batch_frames")
def create_batch_frames(data):
    data["process_completed"] = 0
    return data

@step(name="filter_by_car")
def filter_by_car(data):
    return data

# Mock classes for steps that are classes
@step(name="DamageDetector")
class DamageDetector:
    def __init__(self):
        pass
    def __call__(self, data):
        return data

@step(name="PartSegmentator")
class PartSegmentator:
    def __init__(self):
        pass
    def __call__(self, data):
        return data

@step(name="get_angle")
def get_angle(data):
    return data

@step(name="DamageSegmentator")
class DamageSegmentator:
    def __init__(self):
        pass
    def __call__(self, data):
        return data

@step(name="DamageClasification")
class DamageClasification:
    def __init__(self):
        pass
    def __call__(self, data):
        return data

@step(name="DamageSecondClasification")
class DamageSecondClasification:
    def __init__(self):
        pass
    def __call__(self, data):
        return data

@step(name="add_watermark")
def add_watermark(data):
    return data

@step(name="save_video_report")
def save_video_report(data):
    return data

@step(name="damage_tracker")
def damage_tracker(data):
    logger.info("[main] damage_tracker...")
    return data

@step(name="parts_tracker")
def parts_tracker(data):
    logger.info("[main] parts_tracker...")
    return data

# Build the pipeline
pipeline = Pipeline(pipeline_name="test_pipeline")
pipeline.set_steps([
    check_requirements,
    clean_folder,
    reset_part_model,
    reset_damage_search,
    open_video_capture,
    For(
        validation_expression="process_completed == 0",
        steps=[
            create_batch_frames,
            Condition(
                expression="active_background_extractor == 1",
                branch_true=[filter_by_car],
                branch_false=[],
            ),
            Parallel(
                steps=[
                    DamageDetector(),  # Solo detector de daños (sin segmentación ni clasificación)
                    PartSegmentator(),  # Se ejecuta en hilo B
                    get_angle,  # Se ejecuta en hilo C
                ],
                max_workers=2,
                # use_processes=False  # Cambiado a False para evitar errores de pickling con objetos complejos
            ),
            Parallel(
                steps=[
                    DamageSegmentator(),  # Se ejecuta en hilo A
                    DamageClasification(),  # Se ejecuta en hilo B
                    DamageSecondClasification(),  # Se ejecuta en hilo C
                ],
                max_workers=3,
                # use_processes=False  # Cambiado a False para evitar errores de pickling con objetos complejos
            ),
            add_watermark,
            save_video_report,
        ],
    ),
    Condition(
        expression="tracker_external == 1",
        branch_true=[
            (
                lambda context: logger.info("[main] damage_tracker..."),
                "damage_tracker",
                "v1.0",
            ),
            (
                lambda context: logger.info("[main] parts_tracker..."),
                "parts_tracker",
                "v1.0",
            ),
        ],
        branch_false=[],
    ),
])

# Run the pipeline
try:
    result = pipeline.run({})
    print("Pipeline executed successfully")
    print("Result:", result)
except Exception as e:
    print("Pipeline execution failed with error:", e)
    import traceback
    traceback.print_exc()
