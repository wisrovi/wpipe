"""
09 Microservice - Service Dependencies

Shows managing service dependencies.
"""

from wpipe import Pipeline


def process_step(data):
    return {"processed": True}


class DependentService:
    def __init__(self, dependency):
        self.dependency = dependency
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([(process_step, "Process", "v1.0")])

    def handle(self, data):
        if not self.dependency.is_ready():
            return {"error": "Dependency not ready"}
        return self.pipeline.run(data)


class MockDependency:
    def __init__(self):
        self.ready = True

    def is_ready(self):
        return self.ready


def main():
    dep = MockDependency()
    service = DependentService(dep)

    result = service.handle({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
