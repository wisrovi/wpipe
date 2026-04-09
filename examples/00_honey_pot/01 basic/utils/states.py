from functools import wraps


def state(name, version="v1.0"):
    """
    Decorador con parámetros que transforma una función en una clase estructurada.
    """
    def decorator(func):
        # Creamos la clase dinámicamente
        class StateWrapper:
            NAME = name
            VERSION = version

            def __init__(self, original_func):
                self.original_func = original_func
                # Copiamos metadatos de la función (nombre, docstring, etc.)
                wraps(original_func)(self)

            def __call__(self, *args, **kwargs):
                # Ejecuta la lógica de la función (incluyendo otros decoradores como @to_obj)
                return self.original_func(*args, **kwargs)

            def __repr__(self):
                return f"<State: {self.NAME} {self.VERSION}>"

        # Retornamos una instancia de la clase que envuelve la función
        return StateWrapper(func)
    
    return decorator
