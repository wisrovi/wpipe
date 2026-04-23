"""
DEMO LEVEL 121: APIClient Básico
-------------------------------
Adds: Cliente para APIs externas.
Continues: ParallelExecutor de L120.

DIAGRAM:
APIClient.get(url)
"""

from wpipe.api_client import APIClient

if __name__ == "__main__":
    print(">>> APIClient básico...")

    client = APIClient()

    print(f"✅ Cliente creado")
    print(f"📡 Base URL: {client.base_url}")
