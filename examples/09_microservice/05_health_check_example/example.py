"""
05 Microservice - Health Check Endpoint

Shows implementing a health check for microservice monitoring.
"""

from wpipe import Pipeline
from wpipe.log import new_logger


def process_step(data):
    return {"status": "ok", "processed": True}


class HealthCheckService:
    def __init__(self, name="health_service"):
        self.name = name
        self.logger = new_logger(process_name=name)
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([(process_step, "Process", "v1.0")])

    def health_check(self):
        return {
            "service": self.name,
            "status": "healthy",
            "pipeline_ready": True,
        }

    def process(self, data):
        return self.pipeline.run(data)


def main():
    service = HealthCheckService("test_service")

    print("Health check:", service.health_check())
    print("Process result:", service.process({"test": "data"}))


if __name__ == "__main__":
    main()
