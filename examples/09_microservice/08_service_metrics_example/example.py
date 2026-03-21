"""
08 Microservice - Metrics Collection

Shows collecting service metrics.
"""

from wpipe import Pipeline
import time

def process_step(data):
    return {"processed": True}

class MetricsService:
    def __init__(self):
        self.total_requests = 0
        self.total_time = 0
        
    def handle(self, data):
        start = time.time()
        
        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(process_step, "Process", "v1.0")])
        result = pipeline.run(data)
        
        elapsed = time.time() - start
        self.total_requests += 1
        self.total_time += elapsed
        
        return result
    
    def get_metrics(self):
        return {
            "requests": self.total_requests,
            "avg_time": self.total_time / max(self.total_requests, 1)
        }

def main():
    service = MetricsService()
    
    for _ in range(3):
        service.handle({})
    
    print(f"Metrics: {service.get_metrics()}")

if __name__ == "__main__":
    main()
