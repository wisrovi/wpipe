"""
Basic type hinting example.

Demonstrates basic type validation in pipelines.
"""

from typing import TypedDict, Dict, Any
from wpipe import PipelineContext, TypeValidator, TimeoutError
import time

class UserContext(PipelineContext):
    """Typed context for user processing pipeline."""
    user_id: int
    username: str
    email: str
    processed: bool

def validate_user_data(data: Dict[str, Any]) -> UserContext:
    """Validate user data against schema."""
    schema = {
        "user_id": int,
        "username": str,
        "email": str,
        "processed": bool,
    }
    
    try:
        validated = TypeValidator.validate_dict(data, schema)
        return validated
    except (TypeError, KeyError) as e:
        print(f"✗ Validation failed: {e}")
        raise

def process_step_1(context: UserContext) -> Dict[str, Any]:
    """First processing step."""
    print(f"Processing user {context['username']} ({context['user_id']})...")
    return {"processed": True, "step": 1}

def process_step_2(context: Dict[str, Any]) -> Dict[str, Any]:
    """Second processing step."""
    print(f"Further processing...")
    return {"step": 2, "completed": True}

if __name__ == "__main__":
    print("=== Basic Type Hinting Example ===\n")
    
    # Valid data
    print("--- Example 1: Valid Data ---")
    valid_data = {
        "user_id": 123,
        "username": "john_doe",
        "email": "john@example.com",
        "processed": False,
    }
    
    try:
        context = validate_user_data(valid_data)
        print(f"✓ Validation passed for user: {context['username']}")
        
        result_1 = process_step_1(context)
        context.update(result_1)
        print(f"✓ Step 1 completed")
        
        result_2 = process_step_2(context)
        context.update(result_2)
        print(f"✓ Step 2 completed\n")
    except (TypeError, KeyError) as e:
        print(f"✗ Processing failed: {e}\n")
    
    # Invalid data - wrong type
    print("--- Example 2: Invalid Data (Wrong Type) ---")
    invalid_data_1 = {
        "user_id": "not_an_int",  # Wrong!
        "username": "jane_doe",
        "email": "jane@example.com",
        "processed": False,
    }
    
    try:
        context = validate_user_data(invalid_data_1)
    except (TypeError, KeyError) as e:
        print(f"✗ Validation caught error: {e}\n")
    
    # Invalid data - missing field
    print("--- Example 3: Invalid Data (Missing Field) ---")
    invalid_data_2 = {
        "user_id": 456,
        "username": "bob_smith",
        # Missing 'email' and 'processed'
    }
    
    try:
        context = validate_user_data(invalid_data_2)
    except (TypeError, KeyError) as e:
        print(f"✗ Validation caught error: {e}\n")
    
    # Using TypeValidator directly
    print("--- Example 4: Direct Type Validation ---")
    
    # Validate simple types
    try:
        validated_int = TypeValidator.validate(123, int)
        print(f"✓ Validated int: {validated_int}")
        
        validated_str = TypeValidator.validate("hello", str)
        print(f"✓ Validated str: {validated_str}")
        
        validated_list = TypeValidator.validate([1, 2, 3], list)
        print(f"✓ Validated list: {validated_list}")
    except TypeError as e:
        print(f"✗ Type validation failed: {e}")
    
    # Try wrong type
    print("\n--- Example 5: Type Mismatch ---")
    try:
        invalid = TypeValidator.validate("not_a_number", int)
    except TypeError as e:
        print(f"✓ Caught type mismatch: {e}")
