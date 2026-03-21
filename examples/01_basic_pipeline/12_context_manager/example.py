"""
Basic Pipeline - Context Manager Steps

Pipeline steps that use context managers.
"""

from wpipe import Pipeline


class FileProcessor:
    def __enter__(self):
        self.data = []
        return self
    
    def __call__(self, data):
        self.data.append(data.get("value", 0))
        return {"processed": len(self.data)}
    
    def __exit__(self, *args):
        pass


def main():
    pipeline = Pipeline(verbose=True)
    
    processor = FileProcessor()
    
    pipeline.set_steps([
        (processor, "Process Files", "v1.0"),
    ])
    
    result = pipeline.run({"value": 100})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
