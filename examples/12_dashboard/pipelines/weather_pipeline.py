"""Weather pipeline with conditions"""

from states import cooling_on, fan_high, heating_on, log_action, read_temp

from wpipe import Pipeline


def weather_pipeline(name: str = "weather_pipeline", temp_threshold: int = 25):
    """Create weather-controlled pipeline with condition."""
    return (
        Pipeline(name=name)
        .add_step(read_temp)
        .add_condition(
            condition_fn=lambda data: data.get("temperature", 0) >= temp_threshold,
            true_branch=Pipeline(name=f"{name}_cooling")
            .add_step(cooling_on)
            .add_step(fan_high)
            .add_step(log_action),
            false_branch=Pipeline(name=f"{name}_heating")
            .add_step(heating_on)
            .add_step(log_action),
        )
    )


def run_weather_pipeline(db_path: str, config_dir: str, temp: int = None):
    """Run weather pipeline."""
    # Set temperature if provided
    if temp:
        p = weather_pipeline(temp_threshold=temp)
    else:
        p = weather_pipeline()
    return p.run(tracking_db=db_path, config_dir=config_dir)
