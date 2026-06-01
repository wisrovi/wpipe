from typing import Dict, Any
from wpipe import to_obj, step

@step(name="error_capture", version="v1.0", tags=["error_capture"])
@to_obj
def error_capture(context: Any, error: Dict[str, Any]) -> Any:
    """Captures and logs errors occurring within the pipeline."""
    print("\n" + "!" * 60)
    print("🚨 SYSTEM ALERT: ERROR DETECTED")
    print("!" * 60)
    print(f"📍 FAILED STEP: {error['step_name']}")
    print(f"📄 FILE: {error['file_path']}")
    print(f"🔢 LINE: {error['line_number']}")
    print(f"⚠️ MESSAGE: {error['error_message']}")
    print("-" * 60)
    return context

