"""
09 Microservice - Dynamic Configuration

Shows loading configuration dynamically.
"""

from wpipe import Pipeline

def get_config_value(data):
    return {"config_loaded": True}

class ConfigurableService:
    def __init__(self, config):
        self.config = config
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([(get_config_value, "Load Config", "v1.0")])
    
    def handle(self, data):
        return self.pipeline.run(data)

def main():
    config = {"timeout": 30, "max_retries": 3}
    service = ConfigurableService(config)
    
    result = service.handle({})
    print(f"Service configured with: {service.config}")

if __name__ == "__main__":
    main()
