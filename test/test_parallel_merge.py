"""Regression tests for the Parallel block merge policies.

Covers the bug where updates to pre-existing variables inside a Parallel
block were discarded (or clobbered non-deterministically) when merging
worker results back into the global context.
"""

import pytest
from wpipe import Pipeline, PipelineAsync, step, Parallel


@step(name="inc_counter", version="v1.0")
def inc_counter(data: dict):
    data["counter"] = data.get("counter", 0) + 1
    return data


@step(name="make_extra", version="v1.0")
def make_extra(data: dict):
    data["extra"] = "from-step"
    return data


@step(name="bump_created", version="v1.0")
def bump_created(data: dict):
    data["created_on_fly"] = data.get("created_on_fly", 0) + 1
    return data


@step(name="who_a", version="v1.0")
def who_a(data: dict):
    data["who"] = "A"
    return data


@step(name="who_b", version="v1.0")
def who_b(data: dict):
    data["who"] = "B"
    return data


@step(name="who_c", version="v1.0")
def who_c(data: dict):
    data["who"] = "C"
    return data


def run_parallel(steps, data, merge_policy="accumulate", use_processes=False):
    p = Pipeline(pipeline_name="parallel_merge_test", show_progress=False)
    p.set_steps([Parallel(steps=steps, merge_policy=merge_policy, use_processes=use_processes)])
    return p.run(data)


def test_parallel_accumulate_updates_existing_key():
    res = run_parallel([inc_counter, inc_counter, inc_counter], {"counter": 0})
    assert res["counter"] == 3


def test_parallel_updates_existing_key_and_creates_new_one():
    res = run_parallel([inc_counter, make_extra], {"counter": 0})
    assert res["counter"] == 1
    assert res["extra"] == "from-step"


def test_parallel_accumulate_created_on_fly():
    res = run_parallel([bump_created, bump_created, bump_created], {})
    assert res["created_on_fly"] == 3


def test_parallel_last_wins_policy():
    res = run_parallel([who_a, who_b, who_c], {}, merge_policy="last_wins")
    assert res["who"] == "C"


def test_parallel_accumulate_last_write_for_strings():
    res = run_parallel([who_a, who_b, who_c], {}, merge_policy="accumulate")
    assert res["who"] == "C"


def test_parallel_custom_callable_policy():
    res = run_parallel([inc_counter, inc_counter, inc_counter], {"counter": 0},
                       merge_policy=lambda current, new: current + new)
    assert res["counter"] == 3


def test_parallel_accumulate_with_processes():
    res = run_parallel([inc_counter, inc_counter, inc_counter], {"counter": 0},
                       use_processes=True)
    assert res["counter"] == 3


@pytest.mark.asyncio
async def test_async_parallel_accumulate():
    p = PipelineAsync(pipeline_name="async_parallel_merge", show_progress=False)
    p.set_steps([Parallel(steps=[inc_counter, inc_counter, inc_counter])])
    res = await p.run({"counter": 0})
    assert res["counter"] == 3


@pytest.mark.asyncio
async def test_async_parallel_last_wins():
    p = PipelineAsync(pipeline_name="async_parallel_last_wins", show_progress=False)
    p.set_steps([Parallel(steps=[who_a, who_b, who_c], merge_policy="last_wins")])
    res = await p.run({})
    assert res["who"] == "C"
