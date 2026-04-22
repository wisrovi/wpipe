"""
DEMO LEVEL 129: API Error Handling
----------------------------------
Añade: Manejo de errores de API.
Continúa: L128.

DIAGRAMA:
try/except en llamadas API
"""

from wpipe.api_client import APIClient


if __name__ == "__main__":
    print(">>> API error handling...")

    client = APIClient(base_url="https://nonexistent.example.com")

    try:
        print("⚠️ Intentando conexión...")
        result = client.send_get("/test")
    except Exception as e:
        print(f"❌ Error capturado: {type(e).__name__}")

    print("✅ Sistema tolerante a errores")
