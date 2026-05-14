import random

from states.image_inference import ImageInference
from states.reporter import AuthorizedPersonReporter, UnauthorizedPersonReporter
from states.yaml_read import LoadConfig

from wpipe import Condition, Pipeline


def choice_random_result(data: dict):
    model_results: list = data["model_results"]

    # model_results.append([])

    chosen = random.choice(model_results)
    score = 0
    if isinstance(chosen, dict):
        score = int(chosen.get("conf", 0) * 100)

    return {"score": score}


def main():
    db_path = "wpipe_dashboard.db"
    config_dir = "configs"

    inferencer = Pipeline(
        tracking_db=db_path,
        pipeline_name="honey_pot_inference",
        verbose=False,
    )

    inferencer.set_steps(
        [
            (LoadConfig("src/example.yaml"), LoadConfig.NAME, LoadConfig.VERSION),
            (
                ImageInference("src/head_detector.pt"),
                ImageInference.NAME,
                ImageInference.VERSION,
            ),
            (choice_random_result, "choice_random_result", "v1.0"),
        ]
    )

    reporter = Pipeline(
        tracking_db=db_path,
        pipeline_name="honey_pot_reporter",
        verbose=False,
        max_retries=3,
        retry_delay=0.5,
        retry_on_exceptions=(RuntimeError,),
    )

    reporter.add_event(
        event_type="notification",
        event_name="authorized_person",
        message="Results sent to external APIs",
    )

    # En wpipe v2+, se añaden los pipelines anidados directamente como pasos
    reporter.set_steps(
        [
            inferencer,
        ]
    )

    try:
        results = reporter.run({})
    except Exception as e:
        print(f"Error detectado: {e}")
        results = {"error": str(e)}

    print(f"\nFinal Result: {results}")


if __name__ == "__main__":
    main()
