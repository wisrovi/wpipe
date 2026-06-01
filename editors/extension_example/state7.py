from wpipe import step

@step(name="slow_step", version="v1.0")
def slow_step(data):
    # Your logic here
    return data