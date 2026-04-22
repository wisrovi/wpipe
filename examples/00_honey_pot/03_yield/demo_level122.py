"""
DEMO LEVEL 122: APIClient con URL
------------------------------
Añade: APIClient con base_url.
Continúa: L121.

DIAGRAMA:
APIClient(base_url="https://api.example.com")
"""

from wpipe.api_client import APIClient


if __name__ == "__main__":
    print(">>> APIClient con URL...")

    client = APIClient(base_url="https://api.openweathermap.org")
    print(f"✅ Cliente: {client.base_url}")
