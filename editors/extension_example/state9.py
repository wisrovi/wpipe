from wpipe import step, to_obj, PipelineContext
from wpipe.timeout import timeout_sync
from typing import Any

class MyContext(PipelineContext):
    field: str

@step(
    name="drive",
    version="v1.0",
    timeout=10,
    description="Description of the step",
    tags=["tag1", "tag2"],
    retry_count=3,
    retry_delay=0.01,
)
class AdvancedStep:
    def __init__(self, config="value"):
        self.config = config

    @timeout_sync(seconds=2)
    def __call__(self, context: Any) -> Any:
        # Professional logic here
        return context