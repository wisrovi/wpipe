from wpipe import step

@step(name="step_7", version="v1.0")
def slow_step(data):
    # Your logic here
    return data