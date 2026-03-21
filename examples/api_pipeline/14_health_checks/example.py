"""
14 Health Checks

Demonstrates implementing health check functionality.
Pipeline can be used to verify service dependencies are healthy.

What it evaluates:
- Health check step in pipeline
- Service dependency verification
- Status reporting for monitoring
"""

from wpipe import Pipeline


def check_database(data: dict) -> dict:
    """Check database connectivity.

    Args:
        data: Input data dictionary for context.

    Returns:
        Dictionary with database status and latency.

    Example:
        >>> check_database({})
        {'db_status': 'healthy', 'db_latency_ms': 15}
    """
    return {"db_status": "healthy", "db_latency_ms": 15}


def check_cache(data: dict) -> dict:
    """Check cache service status.

    Args:
        data: Input data dictionary for context.

    Returns:
        Dictionary with cache status and hit count.

    Example:
        >>> check_cache({})
        {'cache_status': 'healthy', 'cache_hits': 100}
    """
    return {"cache_status": "healthy", "cache_hits": 100}


def check_api(data: dict) -> dict:
    """Check external API availability.

    Args:
        data: Input data dictionary for context.

    Returns:
        Dictionary with API status and version.

    Example:
        >>> check_api({})
        {'api_status': 'healthy', 'api_version': 'v2'}
    """
    return {"api_status": "healthy", "api_version": "v2"}


def aggregate_health(data: dict) -> dict:
    """Aggregate all health checks.

    Args:
        data: Input data dictionary with service status fields.

    Returns:
        Dictionary with overall status and individual service statuses.

    Example:
        >>> aggregate_health({"db_status": "healthy", "cache_status": "healthy", "api_status": "healthy"})
        {'overall_status': 'healthy', 'services': {...}}
    """
    statuses: dict[str, str | None] = {
        "database": data.get("db_status"),
        "cache": data.get("cache_status"),
        "api": data.get("api_status"),
    }
    all_healthy: bool = all(s == "healthy" for s in statuses.values())
    return {
        "overall_status": "healthy" if all_healthy else "unhealthy",
        "services": statuses,
    }


def main() -> None:
    """Run the health checks example pipeline."""
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "health_token",
    }

    pipeline = Pipeline(
        worker_name="health_check_worker", api_config=api_config, verbose=True
    )

    pipeline.set_steps(
        [
            (check_database, "Check DB", "v1.0"),
            (check_cache, "Check Cache", "v1.0"),
            (check_api, "Check API", "v1.0"),
            (aggregate_health, "Aggregate Health", "v1.0"),
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")
    assert result["overall_status"] == "healthy"


if __name__ == "__main__":
    main()
