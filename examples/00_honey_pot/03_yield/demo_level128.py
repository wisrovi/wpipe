"""
DEMO LEVEL 128: API con Headers
------------------------------
Adds: Headers personalizados.
Continues: L127.

DIAGRAM:
client.headers = {"Authorization": "Bearer ..."}
"""

from wpipe.api_client import APIClient

if __name__ == "__main__":
    print(">>> API con headers...")

    client = APIClient(base_url="https://api.example.com")
    client.headers = {
        "Authorization": "Bearer token123",
        "Content-Type": "application/json",
    }

    print("✅ Headers configurados:")
    for k, v in client.headers.items():
        print(f"  {k}: {v}")
