"""ETL Pipeline"""

from wpipe import Pipeline
from states import (
    extract_data,
    transform_data,
    load_data,
    clean_data,
    parse_data,
    normalize_data,
    validate_data,
    insert_records,
    verify_load,
)


def etl_pipeline(name: str = "etl_pipeline"):
    """Create ETL pipeline."""
    return (
        Pipeline(name=name)
        .add_step(extract_data)
        .add_step(transform_data)
        .add_step(load_data)
    )


def etl_full_pipeline(name: str = "etl_full"):
    """Create full ETL pipeline with validation."""
    return (
        Pipeline(name=name)
        .add_step(extract_data)
        .add_step(clean_data)
        .add_step(parse_data)
        .add_step(normalize_data)
        .add_step(validate_data)
        .add_step(insert_records)
        .add_step(verify_load)
    )


def run_etl_pipeline(db_path: str, config_dir: str):
    """Run ETL pipeline."""
    pipeline = etl_pipeline()
    return pipeline.run(tracking_db=db_path, config_dir=config_dir)
