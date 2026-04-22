#!/usr/bin/env python3

import time
from wpipe import Pipeline, step

@step(name="slow_step", version="v1.0")
def slow_step(data):
    time.sleep(0.1)  # Simulate some work
    return data

def test_simple_pipeline():
    print("Testing simple pipeline with show_progress=True...")
    pipeline = Pipeline(
        pipeline_name="test_pipeline",
        verbose=False,
        show_progress=True,
    )
    
    pipeline.set_steps([
        slow_step,
        slow_step,
        slow_step,
    ])
    
    result = pipeline.run({})
    print("Pipeline completed")
    return result

if __name__ == "__main__":
    test_simple_pipeline()