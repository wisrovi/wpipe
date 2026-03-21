from prefect import flow, task


@task(name="Print Hello")
def print_hello(name):
    msg = f"Hello {name}!"
    print(msg)
    return msg


@task(name="welcome")
def welcome(data):
    print(f"Bienvenido {data}")


@flow(name="Hello Flow")
def hello_world(name="world"):
    message = print_hello(name)
    welcome(message)


if __name__ == "__main__":
    hello_world("Marvin")

    # sudo apt install graphviz
    hello_world.visualize()
