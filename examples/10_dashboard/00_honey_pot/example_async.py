import asyncio
import random

from wpipe import Condition, PipelineAsync


async def async_load_config(data: dict):
    """Async version of loading config"""
    await asyncio.sleep(0.05)
    print("[async_load_config] Loading configuration...")
    return {
        "inference": {"conf": 0.5},
        "model_results": [
            {"conf": 0.95, "name": "person", "class_id": 0},
            {"conf": 0.75, "name": "person", "class_id": 0},
            {"conf": 0.45, "name": "unknown", "class_id": -1},
        ]
    }


async def async_inference(data: dict):
    """Async version of model inference"""
    await asyncio.sleep(0.1)
    print("[async_inference] Running inference...")
    model_results = data.get("model_results", [])
    return {"model_results": model_results}


async def async_choice_random_result(data: dict):
    """Async version of random result selection"""
    await asyncio.sleep(0.05)
    model_results: list = data["model_results"]
    model_results.append([])
    chosen = random.choice(model_results)
    score = int(chosen.get("conf", 0) * 100)
    print(f"[async_choice_random_result] Selected score: {score}")
    return {"score": score}


class AsyncAuthorizedPersonReporter:
    NAME = "async_authorized_person_reporter"
    VERSION = "1.0.0"

    async def __call__(self, data: dict):
        score = data.get("score", 0)
        await asyncio.sleep(0.05)
        print(f"✓ ASYNC: Posting to Slack - Authorized person detected (Score: {score})")
        return {"authorized_person": True, "action": "post_to_slack"}


class AsyncUnauthorizedPersonReporter:
    NAME = "async_unauthorized_person_reporter"
    VERSION = "1.0.0"

    async def __call__(self, data: dict):
        score = data.get("score", 0)
        await asyncio.sleep(0.05)
        print(f"✗ ASYNC: Sending alert email - Unauthorized person (Score: {score})")
        return {"authorized_person": False, "action": "send_email"}


async def main():
    db_path = "wpipe_dashboard.db"
    config_dir = "configs"

    inferencer = PipelineAsync(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="async_honey_pot_inference",
        verbose=False,
    )

    inferencer.set_steps(
        [
            (async_load_config, "async_load_config", "v1.0"),
            (async_inference, "async_inference", "v1.0"),
            (async_choice_random_result, "async_choice_random_result", "v1.0"),
        ]
    )

    reporter = PipelineAsync(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="async_honey_pot_reporter",
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
                AsyncAuthorizedPersonReporter(),
                AsyncAuthorizedPersonReporter.NAME,
                AsyncAuthorizedPersonReporter.VERSION,
            ),
        ],
        branch_false=[
            (
                AsyncUnauthorizedPersonReporter(),
                AsyncUnauthorizedPersonReporter.NAME,
                AsyncUnauthorizedPersonReporter.VERSION,
            ),
        ],
    )

    reporter.set_steps(
        [
            (inferencer.run, "Async Inference Pipeline", "v1.0"),
            (conditional_reporter),
        ]
    )

    print("=" * 60)
    print("Starting Async Pipeline Example")
    print("=" * 60)
    
    for i in range(2):
        print(f"\n--- Iteration {i+1} ---")
        results = await reporter.run({})
        print(f"Results: score={results.get('score')}, action={results.get('action')}")

    print("\n" + "=" * 60)
    print("Async Pipeline Example Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

