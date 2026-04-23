"""
DEMO LEVEL 30: Satellite Route (External YAML)
-----------------------------------------------
Adds: Loading trip configuration from a YAML file.
Accumulates: Modularization (L19).

DIAGRAM:
[satellite.yaml] -> (read_yaml) -> [Configuration] -> Pipeline.run()
"""

import os
from typing import Any, Dict

from wpipe import Pipeline, step
from wpipe.util import escribir_yaml, leer_yaml

@step(name="show_destination")
def show_destination(data: Dict[str, Any]) -> Dict[str, str]:
    """Show destination step based on external configuration.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Estimated arrival.
    """
    config = data.get("external_config", {})
    print(
        f"📡 Satellite: Received route to {config.get('destination')} via {config.get('route')}"
    )
    return {"estimated_arrival": "14:00"}

if __name__ == "__main__":
    # We create a configuration file simulating the mobile app
    os.makedirs("pipeline_configs", exist_ok=True)
    mock_config = {"destination": "Lisbon", "route": "Toll", "stops": 2}
    config_path = "pipeline_configs/satellite.yaml"
    escribir_yaml(config_path, mock_config)

    # NEW IN L30: We load data before starting
    satellite_data = leer_yaml(config_path)

    pipe = Pipeline(pipeline_name="connected_car_l30", verbose=True)
    pipe.set_steps([show_destination])

    print(">>> Synchronizing with mobile...")
    pipe.run({"external_config": satellite_data})
