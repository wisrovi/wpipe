"""
07 Microservice - Request Validation

Shows validating incoming requests.
"""

from wpipe import Pipeline

def validate_request(data):
    if "required_field" not in data:
        raise ValueError("Missing required_field")
    return {"validated": True}

def process(data):
    return {"processed": True}

class ValidatingService:
    def __init__(self):
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([
            (validate_request, "Validate", "v1.0"),
            (process, "Process", "v1.0"),
        ])
    
    def handle(self, data):
        return self.pipeline.run(data)

def main():
    service = ValidatingService()
    
    result = service.handle({"required_field": "present"})
    print(f"Valid request result: {result}")

if __name__ == "__main__":
    main()
