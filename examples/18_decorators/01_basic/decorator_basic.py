"""
Step decorators example.

Demonstrates using @wpipe.step() decorator to define steps inline.
"""

from wpipe import Pipeline
from wpipe.decorators import step, AutoRegister, get_step_registry
import time


@step(timeout=10, description="Fetch user data from API")
def fetch_users(context):
    """Fetch users from API."""
    print("    [FETCH] Fetching users...")
    time.sleep(0.5)
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"},
        ]
    }


@step(
    depends_on=["fetch_users"],
    timeout=10,
    description="Validate user data"
)
def validate_users(context):
    """Validate users."""
    print("    [VALIDATE] Validating users...")
    users = context["users"]
    
    valid_users = [u for u in users if "id" in u and "name" in u]
    invalid = len(users) - len(valid_users)
    
    return {
        "valid_users": valid_users,
        "invalid_count": invalid,
        "validation_passed": invalid == 0,
    }


@step(
    depends_on=["validate_users"],
    description="Transform user data"
)
def transform_users(context):
    """Transform users."""
    print("    [TRANSFORM] Transforming users...")
    users = context["valid_users"]
    
    transformed = [
        {
            "id": u["id"],
            "username": u["name"].lower(),
            "email": f"{u['name'].lower()}@example.com",
        }
        for u in users
    ]
    
    return {"transformed_users": transformed}


@step(
    depends_on=["transform_users"],
    description="Save users to database"
)
def save_users(context):
    """Save users."""
    print("    [SAVE] Saving users...")
    users = context["transformed_users"]
    
    return {
        "saved_count": len(users),
        "save_status": "completed",
    }


if __name__ == "__main__":
    print("=== Step Decorators Example ===\n")
    
    # Get decorated steps from registry
    print("→ Getting decorated steps from registry...")
    registry = get_step_registry()
    
    print(f"  Found {len(registry.get_all())} decorated steps:")
    for name, decorated in registry.get_all().items():
        metadata = decorated.get_metadata()
        print(f"    - {name}: {metadata.description}")
    
    # Create pipeline
    print("\n→ Creating pipeline with auto-registration...")
    pipeline = Pipeline()
    
    # Auto-register all decorated steps
    AutoRegister.register_all(pipeline, registry)
    
    print(f"  Registered {len(pipeline.steps)} steps to pipeline")
    
    # Execute pipeline
    print("\n→ Executing pipeline...\n")
    start = time.time()
    result = pipeline.run({})
    elapsed = time.time() - start
    
    print(f"\n✓ Pipeline completed in {elapsed:.2f}s!")
    print(f"\nResults:")
    print(f"  Saved users: {result.get('saved_count')}")
    print(f"  Save status: {result.get('save_status')}")
    print(f"  Validation: {result.get('validation_passed')}")
    
    # Show decorated step registry
    print(f"\n✓ Registered {len(registry.get_all())} steps")
