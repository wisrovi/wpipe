"""
Pipeline composition with context filtering example.

Demonstrates using composition to create modular pipelines with
smart context filtering and isolation between sub-pipelines.
"""

from wpipe import Pipeline
from wpipe.composition import CompositionHelper, NestedPipelineStep


def create_data_extraction_pipeline():
    """Create a sub-pipeline for data extraction."""
    pipeline = Pipeline()

    pipeline.add_state(
        "extract_raw",
        lambda c: {
            "raw_users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "raw_posts": [{"id": 101, "title": "Hello"}],
        },
    )

    return pipeline


def create_validation_pipeline():
    """Create a sub-pipeline for validation."""
    pipeline = Pipeline()

    pipeline.add_state(
        "validate_users",
        lambda c: {"valid_users": [u for u in c.get("raw_users", []) if u.get("name")]},
    )

    pipeline.add_state(
        "validate_posts",
        lambda c: {
            "valid_posts": [p for p in c.get("raw_posts", []) if p.get("title")]
        },
    )

    return pipeline


def create_main_pipeline():
    """Create main pipeline with composition."""
    main = Pipeline()

    # First sub-pipeline: extraction
    extract_sub = create_data_extraction_pipeline()
    main.add_state("extract_step", lambda c: extract_sub.run(c))

    # Context filter: only pass raw data to validation
    def filter_for_validation(context):
        return CompositionHelper.extract_context_subset(
            context, ["raw_users", "raw_posts"]
        )

    # Second sub-pipeline: validation with filtering
    validate_sub = create_validation_pipeline()
    nested_validate = NestedPipelineStep(
        "validate_step", validate_sub, context_filter=filter_for_validation
    )

    main.add_state("validate", lambda c: nested_validate.run(c))

    # Final aggregation
    main.add_state(
        "finalize",
        lambda c: {
            "status": "complete",
            "users_count": len(c.get("valid_users", [])),
            "posts_count": len(c.get("valid_posts", [])),
        },
    )

    return main


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("COMPOSITION WITH FILTERING EXAMPLE")
    print("=" * 60)

    pipeline = create_main_pipeline()
    result = pipeline.run({})

    print("\n✓ Results:")
    print(f"  Status: {result.get('status')}")
    print(f"  Valid users: {result.get('users_count')}")
    print(f"  Valid posts: {result.get('posts_count')}")
    print("=" * 60 + "\n")
