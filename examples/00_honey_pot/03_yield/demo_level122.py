"""
DEMO LEVEL 122: APIClient con URL
------------------------------
Adds: APIClient con base_url.
Continues: L121.

DIAGRAM:
APIClient(base_url="https://api.example.com")
"""

from wpipe.api_client import APIClient

if __name__ == "__main__":
    print(">>> APIClient con URL...")

    client = APIClient(base_url="https://api.openweathermap.org")
    print(f"✅ Cliente: {client.base_url}")
