"""
DEMO LEVEL 127: Múltiples APIs
------------------------------
Adds: Conectar a múltiples APIs.
Continues: L126.

DIAGRAM:
APIClient + API1 + API2
"""

from wpipe.api_client import APIClient

if __name__ == "__main__":
    print(">>> Múltiples APIs...")

    api1 = APIClient(base_url="https://api.weather.com")
    api2 = APIClient(base_url="https://api.traffic.com")

    print(f"✅ API 1: {api1.base_url}")
    print(f"✅ API 2: {api2.base_url}")
