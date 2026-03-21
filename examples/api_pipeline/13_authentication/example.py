"""
13 Authentication

Demonstrates using authentication tokens in API requests.
Shows different auth schemes supported by the API client.

What it evaluates:
- Token-based authentication
- Custom authentication headers
- Secure API communication
"""

from wpipe import Pipeline


def authenticate_user(data):
    """Simulate user authentication."""
    token = data.get("token", "")
    return {"user": "authenticated_user", "token_valid": len(token) > 0}


def fetch_protected_resource(data):
    """Fetch resource requiring authentication."""
    return {"resource": "protected_data", "access": "granted"}


def process_protected(data):
    """Process authenticated resource."""
    return {"processed": True, "resource": data.get("resource")}


def main():
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "Bearer_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "headers": {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"},
    }

    pipeline = Pipeline(worker_name="auth_worker", api_config=api_config, verbose=True)

    pipeline.set_steps(
        [
            (authenticate_user, "Authenticate", "v1.0"),
            (fetch_protected_resource, "Fetch Resource", "v1.0"),
            (process_protected, "Process Resource", "v1.0"),
        ]
    )

    result = pipeline.run({"token": "Bearer_valid_token"})
    print(f"Result: {result}")
    assert result["processed"] is True


if __name__ == "__main__":
    main()
