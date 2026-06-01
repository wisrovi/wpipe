from wpipe import step, to_obj, PipelineContext

class MyContext(PipelineContext):
    field: str

@step(name="StepClass10", version="v1.0")
class StepClass10:
    def __init__(self, config_param="value"):
        self.config_param = config_param

    @to_obj(MyContext)
    def __call__(self, ctx: MyContext):
        # Access typed data with ctx.field
        return {}