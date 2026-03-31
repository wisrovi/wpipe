"""
Example demonstrating complete type hinting in WPipe pipelines.

Shows best practices for using type hints to catch errors at development time
and improve IDE autocomplete and documentation.
"""

from typing import TypedDict, Dict, List, Optional, Any
from wpipe import Pipeline


# Define typed data structures for each pipeline step
class LoadedData(TypedDict):
    """Data returned from load_users step."""
    users: List[Dict[str, str]]
    count: int


class ProcessedData(TypedDict):
    """Data returned from process_users step."""
    active_users: List[Dict[str, Any]]
    inactive_users: List[Dict[str, Any]]
    total_processed: int


class AnalyzedData(TypedDict):
    """Data returned from analyze_users step."""
    average_age: float
    total_active: int
    total_inactive: int
    most_common_country: str


# Step functions with full type hints
def load_users(data: Dict[str, Any]) -> LoadedData:
    """
    Load user data from source.
    
    Args:
        data: Pipeline data dictionary
        
    Returns:
        LoadedData with users list and count
    """
    print("[Load] Reading users from database...")
    
    users = [
        {"id": "1", "name": "Alice", "age": "28", "country": "US"},
        {"id": "2", "name": "Bob", "age": "35", "country": "UK"},
        {"id": "3", "name": "Charlie", "age": "42", "country": "US"},
    ]
    
    return {
        "users": users,
        "count": len(users),
    }


def process_users(data: LoadedData) -> ProcessedData:
    """
    Process and categorize users.
    
    Args:
        data: LoadedData with users and count
        
    Returns:
        ProcessedData with categorized users
    """
    print("[Process] Categorizing users...")
    
    users: List[Dict[str, str]] = data["users"]
    active = []
    inactive = []
    
    for user in users:
        age = int(user.get("age", 0))
        if age >= 30:
            active.append(user)
        else:
            inactive.append(user)
    
    return {
        "active_users": active,
        "inactive_users": inactive,
        "total_processed": len(users),
    }


def analyze_users(data: ProcessedData) -> AnalyzedData:
    """
    Analyze user statistics.
    
    Args:
        data: ProcessedData with categorized users
        
    Returns:
        AnalyzedData with statistics
    """
    print("[Analyze] Computing statistics...")
    
    active: List[Dict[str, Any]] = data["active_users"]
    inactive: List[Dict[str, Any]] = data["inactive_users"]
    
    all_users = active + inactive
    
    if not all_users:
        average_age = 0.0
        most_common = "Unknown"
    else:
        total_age = sum(int(u.get("age", 0)) for u in all_users)
        average_age = total_age / len(all_users)
        
        countries = [u.get("country", "") for u in all_users]
        most_common = max(set(countries), key=countries.count)
    
    return {
        "average_age": average_age,
        "total_active": len(active),
        "total_inactive": len(inactive),
        "most_common_country": most_common,
    }


def demo_type_hinting() -> None:
    """Demonstrate type-hinted pipeline."""
    print("\n" + "=" * 60)
    print("TYPE HINTING IN WPIPE PIPELINES")
    print("=" * 60 + "\n")
    print("✓ All functions have complete type hints")
    print("✓ IDE can validate data flow between steps")
    print("✓ Runtime errors like KeyError are caught early\n")
    
    pipeline: Pipeline = Pipeline(
        pipeline_name="typed_pipeline",
        verbose=True,
    )
    
    pipeline.set_steps([
        (load_users, "load_users", "v1.0"),
        (process_users, "process_users", "v1.0"),
        (analyze_users, "analyze_users", "v1.0"),
    ])
    
    # Run pipeline with type-safe data
    result = pipeline.run({})
    
    print("\n" + "=" * 60)
    print("PIPELINE RESULT")
    print("=" * 60)
    print(f"\nAverage age: {result.get('average_age', 0):.1f}")
    print(f"Active users: {result.get('total_active', 0)}")
    print(f"Inactive users: {result.get('total_inactive', 0)}")
    print(f"Most common country: {result.get('most_common_country', 'Unknown')}\n")


if __name__ == "__main__":
    demo_type_hinting()
