import random

from states.image_inference import ImageInference
from states.reporter import AuthorizedPersonReporter, UnauthorizedPersonReporter
from states.yaml_read import LoadConfig

from wpipe import Condition, Pipeline


def choice_random_result(data: dict):
    model_results: list = data["model_results"]

    # model_results.append([])

    chosen = random.choice(model_results)
    score = int(chosen.get("conf") * 100)

    return {"score": score}


def main():
    db_path = "wpipe_dashboard.db"
    config_dir = "configs"

    inferencer = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="honey_pot_inference",
        pipeline_version="1.0.0",
        verbose=False,
    )

    inferencer.set_states(
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
        config_dir=config_dir,
        pipeline_name="honey_pot_reporter",
        pipeline_version="1.0.0",
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

    conditional_reporter = Condition(
        expression="score > 80",
        branch_true=[
            (
                AuthorizedPersonReporter(),
                AuthorizedPersonReporter.NAME,
                AuthorizedPersonReporter.VERSION,
            ),
        ],
        branch_false=[
            (
                UnauthorizedPersonReporter(),
                UnauthorizedPersonReporter.NAME,
                UnauthorizedPersonReporter.VERSION,
            ),
        ],
    )

    reporter.add_pipeline(inferencer, "Inference", "v1.0")
    reporter.add_condition(conditional_reporter)

    for _ in range(4):
        results = reporter.run({})

        print(results)


if __name__ == "__main__":
    main()
