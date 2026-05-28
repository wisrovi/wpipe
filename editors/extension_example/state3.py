from wpipe import step, to_obj, PipelineContext

class MyContext(PipelineContext):
    field: str

@step(name="step_3", version="v1.0")
class StepClass3:
    def __init__(self, config_param="value"):
        self.config_param = config_param
        self.NAME = "step_name"
        self.VERSION = "v1.0"

    @to_obj(MyContext)
    def __call__(self, ctx: MyContext):
        # Access typed data with ctx.field
        return {}