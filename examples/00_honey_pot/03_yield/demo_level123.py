"""
DEMO LEVEL 123: send_get
----------------------
Adds: Método GET.
Continues: L122.

DIAGRAM:
client.send_get(endpoint)
"""

from wpipe.api_client import APIClient

if __name__ == "__main__":
    print(">>> send_get...")

    client = APIClient(base_url="https://jsonplaceholder.typicode.com")

    print("✅ GET request preparado")
    print(f"📡 URL: {client.base_url}/posts/1")
