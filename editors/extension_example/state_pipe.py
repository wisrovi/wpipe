from wpipe import Pipeline
import os
from wpipe.tracking import Metric, Severity

from wpipe import step


@step(name="step_a", version="v1.0")
def step_a(data):
    # Your logic here
    return data


@step(name="step_b", version="v1.0")
def step_b(data):
    # Your logic here
    return data


pipe_2 = Pipeline(
    pipeline_name="my_pipeline_2",
    tracking_db="output/tracking_pipe2.db",
    verbose=False,
    show_progress=False,
)

pipe_2.add_event(
    event_type="notification",
    event_name="authorized_person",
    message="Results sent to external APIs",
)

pipe_2.tracker.add_alert_threshold(
    metric=Metric.STEP_DURATION,
    expression=">100",
    severity=Severity.WARNING,
)

pipe_2.set_steps([step_a, step_b])
