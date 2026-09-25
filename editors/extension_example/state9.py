from typing import Any

from pydantic import BaseModel

from wpipe import step, to_obj
from wpipe.timeout import timeout_sync


class MyContext(BaseModel):
    field: str


@step(
    name="AdvancedStep9",
    version="v1.0",
    timeout=10,
    description="Description of the step",
    tags=["tag1", "tag2"],
    retry_count=3,
    retry_delay=0.01,
)
class AdvancedStep9:
    def __init__(self, config="value"):
        self.config = config

    @timeout_sync(seconds=2)
    @to_obj(MyContext)
    def __call__(self, context: Any) -> Any:
        # Professional logic here
        return context
