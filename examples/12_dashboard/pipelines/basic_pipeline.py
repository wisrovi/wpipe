"""Basic pipeline"""

from states import calculate_stats, fetch_data, process_records

from wpipe import Pipeline


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
