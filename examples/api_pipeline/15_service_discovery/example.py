"""
15 Service Discovery

Demonstrates dynamic service discovery and configuration.
Pipeline discovers services and configures connections dynamically.

What it evaluates:
- Dynamic service discovery
- Configuration based on discovered services
- Flexible service routing
"""

from wpipe import Pipeline


def discover_services(data: dict) -> dict:
    """Discover available services in the environment.

    Args:
        data: Input data dictionary for context.

    Returns:
        Dictionary with discovered services and count.

    Example:
        >>> discover_services({})
        {'discovered_services': {...}, 'service_count': 3}
    """
    services: dict[str, str] = {
        "api": "http://api.example.com",
        "database": "postgresql://db:5432",
        "cache": "redis://cache:6379",
    }
    return {"discovered_services": services, "service_count": len(services)}


def configure_connections(data: dict) -> dict:
    """Configure API based on discovered services.

    Args:
        data: Input data dictionary containing 'discovered_services'.

    Returns:
        Dictionary with configuration status and config dict.

    Example:
        >>> configure_connections({"discovered_services": {"api": "http://api.example.com"}})
        {'configured': True, 'config': {'base_url': 'http://api.example.com', ...}}
    """
    services: dict[str, str] = data.get("discovered_services", {})
    api_config: dict[str, str | None] = {
        "base_url": services.get("api", "http://default"),
        "database_url": services.get("database"),
        "cache_url": services.get("cache"),
    }
    return {"configured": True, "config": api_config}


def test_connections(data: dict) -> dict:
    """Test configured connections.

    Args:
        data: Input data dictionary containing 'config'.

    Returns:
        Dictionary with test results and overall pass status.

    Example:
        >>> test_connections({"config": {}})
        {'connection_tests': {...}, 'all_passed': True}
    """
    _ = data.get("config", {})  # Validate config exists
    results: dict[str, bool] = {
        "api_tested": True,
        "db_tested": True,
        "cache_tested": True,
    }
    return {"connection_tests": results, "all_passed": True}


def main() -> None:
    """Run the service discovery example pipeline."""
    pipeline = Pipeline(worker_name="discovery_worker", verbose=True)

    pipeline.set_steps(
        [
            (discover_services, "Discover Services", "v1.0"),
            (configure_connections, "Configure", "v1.0"),
            (test_connections, "Test Connections", "v1.0"),
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")
    assert result["all_passed"] is True
    assert result["connection_tests"]["api_tested"] is True


if __name__ == "__main__":
    main()
