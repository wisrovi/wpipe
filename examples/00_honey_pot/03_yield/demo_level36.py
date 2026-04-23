"""
DEMO LEVEL 36: Vehicle Logbook (YAML)
-------------------------------------
Adds: Persistence of the context data in YAML files.
Accumulates: All trip history.

DIAGRAM:
(Trip Finished) -> [Context] -> (write_yaml) -> [logbook.yaml]
      |
(New Trip) <---- (read_yaml) <----- [logbook.yaml]
"""

import os
from typing import Any, Dict
from wpipe import Pipeline, step
from wpipe.util import escribir_yaml, leer_yaml

@step(name="generate_logbook")
def generate_logbook(data: Any) -> Dict[str, str]:
    """Generates a trip logbook and saves it to a YAML file.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Path to the generated logbook.
    """
    # Save final trip data for the next session
    final_data = {
        "odometer": 450.5,
        "fuel_remaining": 15,
        "last_position": "Valencia",
        "errors_detected": 0,
    }
    path = "output/trip_logbook.yaml"
    os.makedirs("output", exist_ok=True)
    escribir_yaml(path, final_data)
    print(f"📄 Logbook saved at {path}. Data ready for next start.")
    return {"logbook_path": path}

@step(name="read_previous_logbook")
def read_previous_logbook(data: Dict[str, Any]) -> Dict[str, Any]:
    """Reads a previously saved logbook.

    Args:
        data: Input context containing logbook path.

    Returns:
        Dict[str, Any]: History data from the logbook.
    """
    # Simulate tomorrow's start by reading today's data
    history = leer_yaml(data["logbook_path"])
    print(
        f"📥 Logbook recovered: The car was in {history['last_position']} with {history['fuel_remaining']}% fuel."
    )
    return {"history": history}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="logbook_system_l36", verbose=True)
    pipe.set_steps([generate_logbook, read_previous_logbook])
    pipe.run({})
