import yaml


def leer_yaml(archivo, verbose: bool = False):
    try:
        with open(archivo, "r") as file:
            contenido = yaml.safe_load(file)
            return contenido
    except FileNotFoundError:
        if verbose:
            print(f"El archivo {archivo} no se encontró.")
    except yaml.YAMLError as e:
        if verbose:
            print(f"Error al leer el archivo YAML: {e}")
    return {}


def escribir_yaml(archivo, datos, verbose: bool = False):
    try:
        with open(archivo, "w") as file:
            yaml.dump(datos, file, default_flow_style=False, allow_unicode=True)
            if verbose:
                print(f"Archivo YAML creado exitosamente en {archivo}")
    except IOError as e:
        if verbose:
            print(f"Error al escribir el archivo YAML: {e}")
