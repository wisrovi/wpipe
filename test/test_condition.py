import pytest
from wpipe import Pipeline, Condition


def test_condition_evaluate_true():
    condition = Condition(
        expression="x > 5",
        branch_true=[],
    )
    assert condition.evaluate({"x": 10}) is True


def test_condition_evaluate_false():
    condition = Condition(
        expression="x > 5",
        branch_true=[],
    )
    assert condition.evaluate({"x": 3}) is False


def test_condition_evaluate_string():
    condition = Condition(
        expression="data_type == 'A'",
        branch_true=[],
    )
    assert condition.evaluate({"data_type": "A"}) is True
    assert condition.evaluate({"data_type": "B"}) is False


def test_condition_get_branch_true():
    branch_steps = [("func1", "Step 1", "v1")]
    condition = Condition(
        expression="x > 5",
        branch_true=branch_steps,
        branch_false=[],
    )
    assert condition.get_branch({"x": 10}) == branch_steps


def test_condition_get_branch_false():
    branch_false_steps = [("func2", "Step 2", "v1")]
    condition = Condition(
        expression="x > 5",
        branch_true=[],
        branch_false=branch_false_steps,
    )
    assert condition.get_branch({"x": 3}) == branch_false_steps


def test_condition_get_branch_no_else():
    condition = Condition(
        expression="x > 5",
        branch_true=[("func1", "Step 1", "v1")],
    )
    assert condition.get_branch({"x": 3}) == []


def test_condition_invalid_expression():
    condition = Condition(
        expression="invalid syntax !!!",
        branch_true=[],
    )
    with pytest.raises(ValueError):
        condition.evaluate({"x": 5})


def test_pipeline_with_condition_true():
    def fetch(data):
        return {"data_type": "A", "value": 100}

    def process_a(data):
        return {"processed": data["value"] * 2}

    pipeline = Pipeline()
    condition = Condition(
        expression="data_type == 'A'",
        branch_true=[(process_a, "Process A", "v1.0")],
    )
    pipeline.set_steps(
        [
            (fetch, "Fetch", "v1.0"),
            condition,
        ]
    )

    result = pipeline.run({})
    assert result["processed"] == 200
    assert result["data_type"] == "A"


def test_pipeline_with_condition_false():
    def fetch(data):
        return {"data_type": "B", "value": 100}

    def process_b(data):
        return {"processed": data["value"] + 50}

    pipeline = Pipeline()
    condition = Condition(
        expression="data_type == 'A'",
        branch_true=[
            (process_a := lambda d: {"processed": d["value"] * 2}, "Process A", "v1.0")
        ],
        branch_false=[(process_b, "Process B", "v1.0")],
    )
    pipeline.set_steps(
        [
            (fetch, "Fetch", "v1.0"),
            condition,
        ]
    )

    result = pipeline.run({})
    assert result["processed"] == 150
