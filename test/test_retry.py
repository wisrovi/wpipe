import pytest
from wpipe import Pipeline


def test_pipeline_retry_success_first_try():
    def step1(data):
        return {"result": data["x"] * 2}

    pipeline = Pipeline(max_retries=3, retry_delay=0.1)
    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
        ]
    )

    result = pipeline.run({"x": 5})
    assert result["result"] == 10


def test_pipeline_retry_success_after_failures():
    attempt_counter = {"count": 0}

    def unreliable_step(data):
        attempt_counter["count"] += 1
        if attempt_counter["count"] < 3:
            raise ConnectionError(f"Attempt {attempt_counter['count']} failed")
        return {"result": data["x"] * 2}

    pipeline = Pipeline(
        verbose=False,
        max_retries=3,
        retry_delay=0.05,
        retry_on_exceptions=(ConnectionError,),
    )
    pipeline.set_steps(
        [
            (unreliable_step, "Unreliable", "v1.0"),
        ]
    )

    result = pipeline.run({"x": 5})
    assert result["result"] == 10
    assert attempt_counter["count"] == 3


def test_pipeline_retry_exhausted():
    def always_fails(data):
        raise ConnectionError("Always fails")

    pipeline = Pipeline(
        verbose=False,
        max_retries=2,
        retry_delay=0.01,
        retry_on_exceptions=(ConnectionError,),
    )
    pipeline.set_steps(
        [
            (always_fails, "Always Fails", "v1.0"),
        ]
    )

    with pytest.raises(Exception):
        pipeline.run({"x": 5})


def test_pipeline_retry_filtered_exception():
    def fails_with_valueerror(data):
        raise ValueError("This should not be retried")

    pipeline = Pipeline(
        verbose=False,
        max_retries=3,
        retry_delay=0.01,
        retry_on_exceptions=(ConnectionError,),
    )
    pipeline.set_steps(
        [
            (fails_with_valueerror, "Fails with ValueError", "v1.0"),
        ]
    )

    with pytest.raises(Exception):
        pipeline.run({"x": 5})


def test_pipeline_retry_multiple_steps():
    attempt_counter = {"count": 0}

    def unreliable_step(data):
        attempt_counter["count"] += 1
        if attempt_counter["count"] < 2:
            raise ConnectionError(f"Attempt {attempt_counter['count']} failed")
        return {"result": data["x"] * 2}

    def step2(data):
        return {"final": data["result"] + 10}

    pipeline = Pipeline(
        verbose=False,
        max_retries=3,
        retry_delay=0.01,
        retry_on_exceptions=(ConnectionError,),
    )
    pipeline.set_steps(
        [
            (unreliable_step, "Unreliable", "v1.0"),
            (step2, "Step 2", "v1.0"),
        ]
    )

    result = pipeline.run({"x": 5})
    assert result["result"] == 10
    assert result["final"] == 20


def test_pipeline_no_retry_by_default():
    def step1(data):
        return {"result": data["x"] * 2}

    pipeline = Pipeline()
    assert pipeline.max_retries == 0
    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
        ]
    )

    result = pipeline.run({"x": 5})
    assert result["result"] == 10
