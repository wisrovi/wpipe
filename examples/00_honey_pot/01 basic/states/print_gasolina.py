from wpipe import to_obj, timeout_sync


@timeout_sync(seconds=2)
@to_obj
def print_gasolina(data):
    print(
        f"    Nivel gasolina: {data.nivel_gasolina}",
        "- Nivel aceite:",
        data.nivel_aceite,
    )
    return {}
