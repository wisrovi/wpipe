"""
10 Microservice - Graceful Shutdown

Shows implementing graceful shutdown.
"""

from wpipe import Pipeline


def process_step(data):
    return {"processed": True}


class GracefulService:
    def __init__(self):
        self.running = True
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([(process_step, "Process", "v1.0")])

    def handle(self, data):
        if not self.running:
            return {"error": "Service stopped"}
        return self.pipeline.run(data)

    def shutdown(self):
        self.running = False
        print("Service shutting down gracefully")


def main():
    service = GracefulService()

    result1 = service.handle({"id": 1})
    print(f"Before shutdown: {result1}")

    service.shutdown()
    result2 = service.handle({"id": 2})
    print(f"After shutdown: {result2}")


if __name__ == "__main__":
    main()
