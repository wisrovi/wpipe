import asyncio
import random

from states.image_inference import ImageInference
from states.reporter import AuthorizedPersonReporter, UnauthorizedPersonReporter
from states.yaml_read import LoadConfig

from wpipe import Condition, Pipeline, PipelineAsync


def choice_random_result(data: dict):
    model_results: list = data["model_results"]

    model_results.append([])

    chosen = random.choice(model_results)
    score = int(chosen.get("conf") * 100)

    return {"score": score}


async def async_notification(data: dict):
    """Async notification step"""
    await asyncio.sleep(0.05)
    score = data.get("score", 0)
    print(f"[ASYNC] Sent notification for score: {score}")
    return {"notification_sent": True}


def main():
    db_path = "wpipe_dashboard.db"
    config_dir = "configs"

    # SYNC PIPELINE: Image inference
    inferencer = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
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

    # ASYNC PIPELINE: Reporting and notifications (calls sync inference)
    async def run_reporting():
        reporter = PipelineAsync(
            tracking_db=db_path,
            config_dir=config_dir,
            pipeline_name="honey_pot_reporter_async",
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

        reporter.set_steps(
            [
                (inferencer.run, "Sync Inference", "v1.0"),
                (conditional_reporter),
                (async_notification, "async_notification", "v1.0"),
            ]
        )

        # Run 4 iterations
        for i in range(4):
            print(f"\n--- Iteration {i+1} (Hybrid: Sync + Async) ---")
            results = await reporter.run({})
            print(f"Final result: score={results.get('score')}, notification_sent={results.get('notification_sent')}")

    # Execute hybrid pipeline
    print("=" * 70)
    print("HYBRID PIPELINE: Sync (Inference) → Async (Reporting + Notifications)")
    print("=" * 70)
    asyncio.run(run_reporting())


if __name__ == "__main__":
    main()
