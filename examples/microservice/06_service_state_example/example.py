"""
06 Microservice - Service State Management

Shows managing service state across requests.
"""

from wpipe import Pipeline
from wpipe.log import new_logger

def process_step(data):
    return {"processed": True}

class StatefulService:
    def __init__(self):
        self.request_count = 0
        self.logger = new_logger("stateful_service")
        
    def process(self, data):
        self.request_count += 1
        self.logger.info(f"Request #{self.request_count}")
        
        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(process_step, "Process", "v1.0")])
        
        return pipeline.run(data)

def main():
    service = StatefulService()
    
    result1 = service.process({"id": 1})
    result2 = service.process({"id": 2})
    
    print(f"Total requests: {service.request_count}")

if __name__ == "__main__":
    main()
