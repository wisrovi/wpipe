from wpipe import timeout_sync, to_obj


@timeout_sync(seconds=2)
@to_obj
def print_gasolina(data):
    print(
        f"    Nivel gasolina: {data.nivel_gasolina}",
        "- Nivel aceite:",
        data.nivel_aceite,
    )
    return {}
