"""
DEMO LEVEL 121: APIClient Básico
-------------------------------
Añade: Cliente para APIs externas.
Continúa: ParallelExecutor de L120.

DIAGRAMA:
APIClient.get(url)
"""

from wpipe.api_client import APIClient


if __name__ == "__main__":
    print(">>> APIClient básico...")

    client = APIClient()

    print(f"✅ Cliente creado")
    print(f"📡 Base URL: {client.base_url}")
