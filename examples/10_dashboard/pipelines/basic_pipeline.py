"""Basic pipeline"""

from wpipe import Pipeline
from states import fetch_data, process_records, calculate_stats


def basic_pipeline(name: str = "basic_pipeline"):
    """Create basic pipeline with fetch, process, stats."""
    return (
        Pipeline(name=name)
        .add_step(fetch_data)
        .add_step(process_records)
        .add_step(calculate_stats)
    )


def run_basic_pipeline(db_path: str, config_dir: str):
    """Run the basic pipeline."""
    pipeline = basic_pipeline()
    return pipeline.run(tracking_db=db_path, config_dir=config_dir)
