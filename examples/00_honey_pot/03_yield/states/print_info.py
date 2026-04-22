from wpipe import to_obj, Pipeline
from wpipe.decorators import step, AutoRegister, get_step_registry


@step(name="print_info", version="v1.0")
class Print_info:
    def __init__(self, info: str, loop_iteration_key: str = None):
        self.info = info
        self.loop_iteration_key = loop_iteration_key
        self.NAME = "print_info"
        self.VERSION = "v1.0"

    @to_obj
    def __call__(self, data):
        if self.loop_iteration_key:
            iteration = getattr(data, self.loop_iteration_key, "N/A")
            print(f"{self.info} (Iteración: {iteration})")
        else:
            print(f"{self.info}")
        return {}


@step(name="print_info_2", version="v1.0")
class Print_info_2:
    def __init__(self, info: str, loop_iteration_key: str = None):
        self.info = info
        self.loop_iteration_key = loop_iteration_key
        self.NAME = "print_info_2"
        self.VERSION = "v1.0"

    @to_obj
    def __call__(self, data):
        if self.loop_iteration_key:
            iteration = getattr(data, self.loop_iteration_key, "N/A")
            print(f"{self.info} (Iteración: {iteration})")
        else:
            print(f"{self.info}")
        return {}


registry = get_step_registry()

nested = Pipeline(
    pipeline_name="viaje_tmp",
    verbose=False,
    tracking_db="output/wpipe_dashboard.db",
    show_progress=False,
)

AutoRegister.register_all(nested, registry)
