"""
DEMO LEVEL 124: send_post
-----------------------------
Adds: Método POST.
Continues: L123.

DIAGRAM:
client.send_post(endpoint, data)
"""

from wpipe.api_client import APIClient

if __name__ == "__main__":
    print(">>> send_post...")

    client = APIClient(base_url="https://jsonplaceholder.typicode.com")

    print("✅ POST request preparado")
    print(f"📡 Endpoint: /posts")
