# pip install requests
import requests
import json


class APIClient:
    def __init__(self, base_url: str = None, token: str = None):
        """
        Inicializa el cliente API con la URL base y el token de autorización.
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def send_post(self, endpoint: str, data: dict):
        """
        Envía una solicitud POST a un endpoint específico.
        """

        if not self.base_url:
            raise Exception("No 'base_url' defined.")

        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()  # Lanza una excepción si el código de estado indica un error
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud POST a {url}: {e}")
            return None

    def send_get(self, endpoint: str):
        """
        Envía una solicitud GET a un endpoint específico.
        """

        if not self.base_url:
            raise Exception("No 'base_url' defined.")

        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud GET a {url}: {e}")
            return None

    # Métodos específicos para cada endpoint

    def register_worker(self, data: dict):
        return self.send_post("/matricula", data)

    def healthcheck_worker(self, data: dict):
        return self.send_post("/healthchecker", data)

    def register_process(self, data: dict):
        return self.send_post("/newprocess", data)

    def end_process(self, data: dict):
        return self.send_post("/endprocess", data)

    def update_task(self, data: dict):
        return self.send_post("/actualizar_task", data)

    def get_dashboard_workers(self):
        return self.send_get("/dashboard_workers")


# Ejemplo de uso
if __name__ == "__main__":
    # Configura la URL base y el token de autorización
    client = APIClient(base_url="http://192.168.1.60:8418", token="mysecrettoken")

    # Ejemplo de cómo registrar un trabajador
    data = {
        # Llena con los datos necesarios para la solicitud
    }

    # Llama al método para obtener el dashboard de trabajadores
    workers_info = client.get_dashboard_workers()
    print(workers_info)


# pip install requests
