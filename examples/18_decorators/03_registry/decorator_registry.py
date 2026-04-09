"""
Step registry and tag-based registration example.

Demonstrates managing decorated steps using the registry,
filtering by tags, and conditional registration.
"""

from wpipe import Pipeline
from wpipe.decorators import step, AutoRegister, get_step_registry, clear_registry


# Production-critical steps
@step(name="auth", tags=["auth", "critical", "prod"])
def authenticate(context):
    """Authenticate user."""
    print("[Auth] Authenticating...")
    return {"authenticated": True, "user_id": 123}


@step(name="validate_permissions", depends_on=["auth"], tags=["auth", "critical", "prod"])
def validate_permissions(context):
    """Validate user permissions."""
    print("[Auth] Validating permissions...")
    return {"authorized": True, "permissions": ["read", "write"]}


# Data processing steps
@step(name="fetch_data", tags=["data", "io"])
def fetch_data(context):
    """Fetch data from source."""
    print("[Data] Fetching...")
    return {"data": [1, 2, 3, 4, 5]}


@step(name="process_data", depends_on=["fetch_data"], tags=["data", "processing"])
def process_data(context):
    """Process the data."""
    print("[Data] Processing...")
    return {"processed": [x * 2 for x in context.get("data", [])]}


# Analytics steps
@step(name="calculate_stats", tags=["analytics", "optional"])
def calculate_stats(context):
    """Calculate statistics."""
    print("[Analytics] Computing stats...")
    data = context.get("processed", [])
    return {"total": sum(data), "count": len(data), "avg": sum(data) / len(data) if data else 0}


@step(name="store_results", depends_on=["calculate_stats"], tags=["analytics", "optional"])
def store_results(context):
    """Store results."""
    print("[Analytics] Storing...")
    return {"stored": True, "timestamp": "2024-04-01"}


def run_full_pipeline():
    """Run the complete pipeline with all steps."""
    print("\n" + "=" * 60)
    print("FULL PIPELINE (All Registered Steps)")
    print("=" * 60)
    
    pipeline = Pipeline()
    registry = get_step_registry()
    AutoRegister.register_all(pipeline, registry)
    
    print(f"✓ Registered {len(registry.get_all())} steps")
    result = pipeline.run({})
    print(f"✓ Final result keys: {list(result.keys())}")
    return result


def run_critical_pipeline():
    """Run pipeline with only critical steps."""
    print("\n" + "=" * 60)
    print("CRITICAL-ONLY PIPELINE (Production)")
    print("=" * 60)
    
    # Clear and re-register only critical steps
    clear_registry()
    
    # Re-decorate only critical functions
    critical_auth = step(name="auth", tags=["auth", "critical"])(authenticate)
    critical_validate = step(name="validate", depends_on=["auth"], tags=["auth", "critical"])(validate_permissions)
    
    pipeline = Pipeline()
    registry = get_step_registry()
    
    # Register only critical steps
    for step_name, decorated in registry.get_all().items():
        if "critical" in decorated.get_metadata().tags:
            AutoRegister.register_by_tag(pipeline, "critical", registry)
            break
    
    print(f"✓ Registered critical steps only")
    result = pipeline.run({})
    print(f"✓ Result: {result}")
    return result


def run_data_pipeline():
    """Run pipeline with only data processing steps."""
    print("\n" + "=" * 60)
    print("DATA PROCESSING PIPELINE")
    print("=" * 60)
    
    pipeline = Pipeline()
    registry = get_step_registry()
    
    # Register only data-related steps
    AutoRegister.register_by_tag(pipeline, "data", registry)
    
    print(f"✓ Registered data processing steps")
    result = pipeline.run({})
    print(f"✓ Result keys: {list(result.keys())}")
    return result


if __name__ == "__main__":
    # Show all available steps in registry
    registry = get_step_registry()
    print("\n📋 Available Steps in Registry:")
    for name, step_info in registry.get_all().items():
        metadata = step_info.get_metadata()
        print(f"  - {name}: tags={metadata.tags}, depends_on={metadata.depends_on}")
    
    # Run different pipeline configurations
    run_full_pipeline()
    # run_critical_pipeline()  # Uncomment to test critical-only pipeline
    # run_data_pipeline()  # Uncomment to test data-only pipeline
    
    print("\n" + "=" * 60)
