from types import SimpleNamespace
from functools import wraps


def dict_to_sns(data):
    if isinstance(data, dict):
        # Convertimos cada valor interno primero y luego el diccionario actual
        return SimpleNamespace(**{k: dict_to_sns(v) for k, v in data.items()})
    elif isinstance(data, list):
        # Si hay una lista, procesamos cada elemento por si contiene más dicts
        return [dict_to_sns(i) for i in data]
    else:
        # Si es un valor simple (str, int, bool), se queda igual
        return data


def to_obj(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Convertimos los argumentos posicionales que sean diccionarios
        new_args = [dict_to_sns(arg) for arg in args]
        # Convertimos los argumentos nombrados que sean diccionarios
        new_kwargs = {k: dict_to_sns(v) for k, v in kwargs.items()}

        return func(*new_args, **new_kwargs)

    return wrapper


if __name__ == "__main__":

    @to_obj
    def demo(args_dict):
        print("complete",args_dict)
        print("name:", args_dict.name)
        print("age:", args_dict.age)
        print("hobbies:", args_dict.hobbies)
        print("first hobby:", args_dict.hobbies[0])
        print("street:", args_dict.address.street)
        print("city:", args_dict.address.city)

    demo(
        {
            "name": "Alice",
            "age": 30,
            "hobbies": ["reading", "hiking"],
            "address": {"street": "123 Main St", "city": "Anytown"},
        }
    )
