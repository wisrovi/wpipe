"""
DTO models for pipeline tracking, performance, and monitoring in SQLite.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PipelineModel(BaseModel):
    """
    Data Transfer Object for the pipelines table.

    Attributes:
        id (str): Primary Key of the pipeline (ID/Registration).
        name (str): Name of the pipeline.
        worker_id (Optional[str]): ID of the worker executing the pipeline.
        worker_name (Optional[str]): Name of the worker.
        status (str): Current status of the pipeline (e.g., 'running', 'completed').
        started_at (Optional[str]): ISO timestamp of when the pipeline started.
        completed_at (Optional[str]): ISO timestamp of when the pipeline completed.
        total_duration_ms (Optional[float]): Total execution duration in milliseconds.
        input_data (Optional[str]): Input data stored as a JSON string.
        output_data (Optional[str]): Output data stored as a JSON string.
        error_message (Optional[str]): Error message if the pipeline failed.
        error_step (Optional[str]): Name of the step where the error occurred.
        parent_pipeline_id (Optional[str]): ID of the parent pipeline if nested.
        yaml_path (Optional[str]): Path to the YAML configuration file.
    """

    id: str = Field(..., description="Primary Key (ID/Registration)")
    name: str
    worker_id: Optional[str] = None
    worker_name: Optional[str] = None
    status: str = "running"
    started_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
    completed_at: Optional[str] = None
    total_duration_ms: Optional[float] = None
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    error_message: Optional[str] = None
    error_step: Optional[str] = None
    parent_pipeline_id: Optional[str] = None
    yaml_path: Optional[str] = None


class StepModel(BaseModel):
    """
    Data Transfer Object for the steps table.

    Attributes:
        id (Optional[int]): Primary Key of the step.
        pipeline_id (str): ID of the pipeline this step belongs to.
        step_order (int): Execution order of the step.
        step_name (str): Name of the step.
        step_version (Optional[str]): Version of the step implementation.
        step_type (str): Type of step (e.g., 'task').
        status (str): Current status of the step.
        parent_step_id (Optional[int]): ID of the parent step if nested.
        parallel_group (Optional[str]): Identifier for parallel execution groups.
        started_at (Optional[str]): ISO timestamp of when the step started.
        completed_at (Optional[str]): ISO timestamp of when the step completed.
        duration_ms (Optional[float]): Step execution duration in milliseconds.
        input_data (Optional[str]): Input data stored as a JSON string.
        output_data (Optional[str]): Output data stored as a JSON string.
        error_message (Optional[str]): Error message if the step failed.
        error_traceback (Optional[str]): Full traceback if the step failed.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    pipeline_id: str
    step_order: int
    step_name: str
    step_version: Optional[str] = None
    step_type: str = "task"
    status: str = "running"
    parent_step_id: Optional[int] = None
    parallel_group: Optional[str] = None
    started_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
    completed_at: Optional[str] = None
    duration_ms: Optional[float] = None
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None


class StepHistoryModel(BaseModel):
    """
    Data Transfer Object for the step_history table.

    Attributes:
        id (Optional[int]): Primary Key of the history entry.
        pipeline_id (str): ID of the pipeline.
        step_name (str): Name of the step.
        duration_ms (float): Execution duration in milliseconds.
        status (str): Status of the step execution.
        recorded_at (Optional[str]): ISO timestamp of the record.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    pipeline_id: str
    step_name: str
    duration_ms: float
    status: str
    recorded_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class PerformanceStatsModel(BaseModel):
    """
    Data Transfer Object for the performance_stats table.

    Attributes:
        id (Optional[int]): Primary Key of the statistics entry.
        entity_type (str): Type of entity ('pipeline' or 'step').
        entity_name (str): Name of the entity.
        period_start (str): Start of the aggregation period.
        period_end (str): End of the aggregation period.
        execution_count (int): Total number of executions.
        success_count (int): Number of successful executions.
        error_count (int): Number of failed executions.
        avg_duration_ms (float): Average duration in milliseconds.
        min_duration_ms (float): Minimum duration in milliseconds.
        max_duration_ms (float): Maximum duration in milliseconds.
        p50_duration_ms (float): 50th percentile (median) duration.
        p95_duration_ms (float): 95th percentile duration.
        p99_duration_ms (float): 99th percentile duration.
        created_at (Optional[str]): ISO timestamp of the record creation.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    entity_type: str
    entity_name: str
    period_start: str
    period_end: str
    execution_count: int
    success_count: int
    error_count: int
    avg_duration_ms: float
    min_duration_ms: float
    max_duration_ms: float
    p50_duration_ms: float
    p95_duration_ms: float
    p99_duration_ms: float
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class AlertConfigModel(BaseModel):
    """
    Data Transfer Object for the alerts_config table.

    Attributes:
        id (Optional[int]): Primary Key of the alert configuration.
        name (str): Name of the alert.
        metric (str): Metric to monitor.
        condition (str): Condition to check (e.g., '>', '<').
        value (float): Threshold value for the condition.
        severity (str): Severity level of the alert.
        message (Optional[str]): Alert message template.
        enabled (int): Whether the alert is enabled (1) or disabled (0).
    """

    id: Optional[int] = Field(None, description="Primary Key")
    name: str
    metric: str
    condition: str
    value: float
    severity: str = "warning"
    message: Optional[str] = None
    enabled: int = 1


class AlertFiredModel(BaseModel):
    """
    Data Transfer Object for the alerts_fired table.

    Attributes:
        id (Optional[int]): Primary Key of the fired alert.
        alert_config_id (int): ID of the triggering alert configuration.
        pipeline_id (str): ID of the pipeline that triggered the alert.
        step_id (Optional[int]): ID of the step that triggered the alert.
        metric (str): Monitored metric name.
        metric_value (float): Actual value that triggered the alert.
        threshold_value (float): Threshold value that was crossed.
        severity (str): Severity of the alert.
        message (Optional[str]): Final alert message.
        fired_at (Optional[str]): ISO timestamp of when the alert fired.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    alert_config_id: int
    pipeline_id: str
    step_id: Optional[int] = None
    metric: str
    metric_value: float
    threshold_value: float
    severity: str
    message: Optional[str] = None
    fired_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


class EventModel(BaseModel):
    """
    Data Transfer Object for the events table.

    Attributes:
        id (Optional[int]): Primary Key of the event.
        pipeline_id (str): ID of the associated pipeline.
        step_id (Optional[int]): ID of the associated step.
        event_type (str): Type of event.
        event_name (str): Name of the event.
        message (Optional[str]): Detailed event message.
        data (Optional[str]): Additional event data as a JSON string.
        tags (Optional[str]): Event tags stored as a string.
        created_at (Optional[str]): ISO timestamp of event creation.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    pipeline_id: str
    step_id: Optional[int] = None
    event_type: str
    event_name: str
    message: Optional[str] = None
    data: Optional[str] = None
    tags: Optional[str] = None
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class PipelineRelationModel(BaseModel):
    """
    Data Transfer Object for the pipeline_relations table.

    Attributes:
        id (Optional[int]): Primary Key of the relation.
        parent_pipeline_id (str): ID of the parent pipeline.
        child_pipeline_id (str): ID of the child pipeline.
        relation_type (str): Type of relation (e.g., 'triggered').
        metadata (Optional[str]): Additional metadata as a JSON string.
        created_at (Optional[str]): ISO timestamp of relation creation.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    parent_pipeline_id: str
    child_pipeline_id: str
    relation_type: str = "triggered"
    metadata: Optional[str] = None
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class SystemMetricsModel(BaseModel):
    """
    Data Transfer Object for the system_metrics table.

    Attributes:
        id (Optional[int]): Primary Key of the metrics entry.
        pipeline_id (str): ID of the pipeline being monitored.
        cpu_percent (Optional[float]): CPU usage percentage.
        memory_percent (Optional[float]): Memory usage percentage.
        memory_used_mb (Optional[float]): Used memory in MB.
        memory_available_mb (Optional[float]): Available memory in MB.
        disk_io_read_mb (Optional[float]): Disk read IO in MB.
        disk_io_write_mb (Optional[float]): Disk write IO in MB.
        recorded_at (Optional[str]): ISO timestamp of the measurement.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    pipeline_id: str
    cpu_percent: Optional[float] = None
    memory_percent: Optional[float] = None
    memory_used_mb: Optional[float] = None
    memory_available_mb: Optional[float] = None
    disk_io_read_mb: Optional[float] = None
    disk_io_write_mb: Optional[float] = None
    recorded_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class ResourceMetricsModel(BaseModel):
    """
    Data Transfer Object for the resource_metrics table.

    Attributes:
        id (Optional[int]): Primary Key of the resource metrics entry.
        task_name (str): Name of the task being monitored.
        start_ram_mb (Optional[float]): Initial RAM usage in MB.
        peak_ram_mb (Optional[float]): Peak RAM usage in MB.
        end_ram_mb (Optional[float]): Final RAM usage in MB.
        avg_cpu_percent (Optional[float]): Average CPU usage percentage.
        elapsed_seconds (Optional[float]): Total elapsed time in seconds.
        created_at (Optional[str]): ISO timestamp of record creation.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    task_name: str
    start_ram_mb: Optional[float] = None
    peak_ram_mb: Optional[float] = None
    end_ram_mb: Optional[float] = None
    avg_cpu_percent: Optional[float] = None
    elapsed_seconds: Optional[float] = None
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class CheckpointModel(BaseModel):
    """
    Data Transfer Object for the checkpoints table.

    Attributes:
        id (Optional[int]): Primary Key of the checkpoint.
        pipeline_id (str): ID of the associated pipeline.
        step_order (int): Execution order of the step.
        step_name (str): Name of the step.
        status (str): Status of the checkpoint.
        data (Optional[str]): Checkpoint data stored as a JSON string.
        created_at (Optional[str]): ISO timestamp of checkpoint creation.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    pipeline_id: str
    step_order: int
    step_name: str
    status: str
    data: Optional[str] = None
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class ComparisonModel(BaseModel):
    """
    Data Transfer Object for the comparisons table.

    Attributes:
        id (Optional[int]): Primary Key of the comparison entry.
        comparison_uuid (str): Unique identifier for the comparison.
        pipeline_a_id (str): ID of the first pipeline.
        pipeline_b_id (str): ID of the second pipeline.
        comparison_data (Optional[str]): Detailed comparison results as JSON.
        duration_diff_ms (Optional[float]): Difference in duration in milliseconds.
        status_diff (Optional[str]): Summary of status differences.
        created_at (Optional[str]): ISO timestamp of comparison creation.
    """

    id: Optional[int] = Field(None, description="Primary Key")
    comparison_uuid: str
    pipeline_a_id: str
    pipeline_b_id: str
    comparison_data: Optional[str] = None
    duration_diff_ms: Optional[float] = None
    status_diff: Optional[str] = None
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
