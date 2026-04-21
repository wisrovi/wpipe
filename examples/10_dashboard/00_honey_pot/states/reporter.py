class AuthorizedPersonReporter:
    NAME = "authorized_person_reporter"
    VERSION = "1.0.0"

    def __init__(self):
        pass

    def __call__(self, data: dict):
        score = data.get("score", 0)

        print(f"!!! POSTEANDO EN SLACK: Score {score} aceptable !!!")

        return {"authorized_person": True}


class UnauthorizedPersonReporter:
    NAME = "unauthorized_person_reporter"
    VERSION = "1.0.0"

    def __init__(self):
        pass

    def __call__(self, data):
        score = data.get("score", 0)

        print(f"!!! ENVIANDO CORREO DE ALERTA: Score bajo {score} !!!")

        return {"authorized_person": False}
