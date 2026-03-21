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


def check_database(data):
    """Check database connectivity."""
    return {"db_status": "healthy", "db_latency_ms": 15}


def check_cache(data):
    """Check cache service status."""
    return {"cache_status": "healthy", "cache_hits": 100}


def check_api(data):
    """Check external API availability."""
    return {"api_status": "healthy", "api_version": "v2"}


def aggregate_health(data):
    """Aggregate all health checks."""
    statuses = {
        "database": data.get("db_status"),
        "cache": data.get("cache_status"),
        "api": data.get("api_status"),
    }
    all_healthy = all(s == "healthy" for s in statuses.values())
    return {
        "overall_status": "healthy" if all_healthy else "unhealthy",
        "services": statuses,
    }


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "health_token"}

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
