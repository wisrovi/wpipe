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


def authenticate_user(data: dict) -> dict:
    """Simulate user authentication.

    Args:
        data: Input data dictionary containing 'token'.

    Returns:
        Dictionary with user info and token validity status.

    Example:
        >>> authenticate_user({"token": "valid_token"})
        {'user': 'authenticated_user', 'token_valid': True}
    """
    token: str = data.get("token", "")
    return {"user": "authenticated_user", "token_valid": len(token) > 0}


def fetch_protected_resource(data: dict) -> dict:
    """Fetch resource requiring authentication.

    Args:
        data: Input data dictionary for context.

    Returns:
        Dictionary with protected resource info.

    Example:
        >>> fetch_protected_resource({})
        {'resource': 'protected_data', 'access': 'granted'}
    """
    return {"resource": "protected_data", "access": "granted"}


def process_protected(data: dict) -> dict:
    """Process authenticated resource.

    Args:
        data: Input data dictionary containing 'resource'.

    Returns:
        Dictionary with processing status and resource.

    Example:
        >>> process_protected({"resource": "data"})
        {'processed': True, 'resource': 'data'}
    """
    return {"processed": True, "resource": data.get("resource")}


def main() -> None:
    """Run the authentication example pipeline."""
    api_config: dict[str, str | dict[str, str]] = {
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
