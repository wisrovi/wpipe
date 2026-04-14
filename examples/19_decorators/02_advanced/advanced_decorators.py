"""
Advanced decorator features example.

Demonstrates advanced @step decorator features including timeouts,
retry counts, and complex dependencies.
"""

from wpipe import Pipeline
from wpipe.decorators import AutoRegister, get_step_registry, step


@step(
    name="fetch_config",
    timeout=5,
    description="Load configuration from source",
    tags=["config", "required"],
)
def load_config(context):
    """Load configuration."""
    print("[Config] Loading...")
    return {"config": {"env": "production", "timeout": 30}}


@step(
    name="validate_config",
    depends_on=["fetch_config"],
    timeout=5,
    description="Validate configuration values",
    tags=["config", "validation"],
)
def validate_config(context):
    """Validate loaded configuration."""
    print("[Validation] Checking config...")
    config = context.get("config", {})
    valid = bool(config.get("env") and config.get("timeout"))
    return {"config_valid": valid, "validated_config": config}


@step(
    name="initialize_services",
    depends_on=["validate_config"],
    timeout=10,
    description="Initialize services based on config",
    tags=["services", "initialization"],
)
def initialize_services(context):
    """Initialize services."""
    print("[Services] Initializing...")
    if not context.get("config_valid"):
        raise ValueError("Invalid configuration")
    return {"services_initialized": True, "service_count": 3}


@step(
    name="run_health_check",
    depends_on=["initialize_services"],
    timeout=5,
    description="Check service health",
    tags=["health", "monitoring"],
)
def health_check(context):
    """Check service health."""
    print("[Health] Checking services...")
    return {"health_status": "healthy", "services_ok": context.get("service_count", 0)}


@step(
    name="report_status",
    depends_on=["run_health_check"],
    description="Generate final status report",
    tags=["reporting"],
)
def report_status(context):
    """Generate status report."""
    print("[Report] Generating...")
    return {
        "status": "complete",
        "health": context.get("health_status"),
        "services": context.get("services_ok", 0),
    }


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ADVANCED DECORATORS EXAMPLE")
    print("=" * 60)

    # Create pipeline
    pipeline = Pipeline()

    # Get registry and auto-register all decorated steps
    registry = get_step_registry()
    AutoRegister.register_all(pipeline, registry)

    print("\n📋 Registered steps:")
    for name, step_info in registry.get_all().items():
        metadata = step_info.get_metadata()
        print(f"  - {name}: {metadata.description} (timeout: {metadata.timeout}s)")

    # Run pipeline
    print("\n🔄 Running pipeline...")
    result = pipeline.run({})

    print("\n✓ Results:")
    print(f"  Status: {result.get('status')}")
    print(f"  Health: {result.get('health')}")
    print(f"  Services: {result.get('services')}")
    print("=" * 60 + "\n")
