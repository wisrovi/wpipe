from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PipelineModel(BaseModel):
    """DTO for the pipelines table."""

    id: str = Field(..., description="Primary Key (Matrícula)")
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
    """DTO for the steps table."""

    id: Optional[int] = Field(None, description="Primary Key")
    pipeline_id: str
    step_order: int
    step_name: str
    step_version: Optional[str] = None
    step_type: str = "task"
    status: str = "running"
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
    """DTO for the step_history table."""

    id: Optional[int] = Field(None, description="Primary Key")
    pipeline_id: str
    step_name: str
    duration_ms: float
    status: str
    recorded_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class PerformanceStatsModel(BaseModel):
    """DTO for the performance_stats table."""

    id: Optional[int] = Field(None, description="Primary Key")
    entity_type: str  # 'pipeline' or 'step'
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
    """DTO for the alerts_config table."""

    id: Optional[int] = Field(None, description="Primary Key")
    name: str
    metric: str
    condition: str
    value: float
    severity: str = "warning"
    message: Optional[str] = None
    enabled: int = 1


class AlertFiredModel(BaseModel):
    """DTO for the alerts_fired table."""

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
    """DTO for the events table."""

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
    """DTO for the pipeline_relations table."""

    id: Optional[int] = Field(None, description="Primary Key")
    parent_pipeline_id: str
    child_pipeline_id: str
    relation_type: str = "triggered"
    metadata: Optional[str] = None
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat()
    )


class SystemMetricsModel(BaseModel):
    """DTO for the system_metrics table."""

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


class ComparisonModel(BaseModel):
    """DTO for the comparisons table."""

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
