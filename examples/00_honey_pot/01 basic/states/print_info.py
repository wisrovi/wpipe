from wpipe import to_obj
from wpipe.decorators import step


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
