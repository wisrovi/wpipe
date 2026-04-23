"""
wpipe Dashboard - Enterprise-grade pipeline visualization

This module provides a FastAPI-based dashboard for visualizing pipeline executions.
The dashboard is modularized into:
- main.py: FastAPI app and API endpoints
- static/styles.css: All styles
- static/dashboard.js: All JavaScript logic
- templates/: HTML template views
"""

import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from webbrowser import open as open_url

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

from wpipe.tracking import PipelineTracker

# Get the dashboard directory path
DASHBOARD_DIR = Path(__file__).parent
TEMPLATES_DIR = DASHBOARD_DIR / "templates"

# Initialize Jinja2 environment
jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


def start_dashboard(
    db_path: str = "wpipe_dashboard.db",
    config_dir: Optional[str] = None,
    host: str = "127.0.0.1",
    port: int = 8035,
    open_browser: bool = False,
) -> None:
    """
    Start the wpipe dashboard server.

    Args:
        db_path: Path to the SQLite database.
        config_dir: Directory containing pipeline configurations.
        host: Host address to bind the server.
        port: Port to run the dashboard on.
        open_browser: Whether to automatically open the browser.
    """
    app = create_app(db_path, config_dir)

    if open_browser:

        def open_browser_delay() -> None:
            time.sleep(2.0)
            open_url(f"http://{host}:{port}")

        thread = threading.Thread(target=open_browser_delay, daemon=True)
        thread.start()

    uvicorn.run(app, host=host, port=port)


def create_app(
    db_path: str = "wpipe_dashboard.db",
    config_dir: Optional[str] = None,
) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Args:
        db_path: Path to the SQLite database.
        config_dir: Directory containing pipeline configurations.

    Returns:
        The configured FastAPI application instance.
    """
    app = FastAPI(title="wpipe Dashboard")

    # Mount static files
    static_dir = DASHBOARD_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    async def root() -> HTMLResponse:
        """Root endpoint that serves the dashboard HTML."""
        return HTMLResponse(get_dashboard_html())

    @app.get("/api/stats")
    async def get_stats() -> Dict[str, Any]:
        """Get pipeline execution statistics."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_stats()

    @app.get("/api/pipelines")
    async def get_pipelines(status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of pipelines, optionally filtered by status."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_pipelines(status=status)

    @app.get("/api/data/{table}")
    async def get_table_data(
        table: str,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get paginated data from a specific tracking table."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_table_data(
            table=table,
            page=page,
            page_size=page_size,
            search=search,
            status=status,
        )

    @app.get("/api/pipelines/{pipeline_id}")
    async def get_pipeline(pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific pipeline execution."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_pipeline(pipeline_id)

    @app.get("/api/pipelines/by-name/{pipeline_name}")
    async def get_pipeline_executions(
        pipeline_name: str, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get all executions of a pipeline by name."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_pipeline_executions(pipeline_name, limit=limit, offset=offset)

    @app.get("/api/pipelines/{pipeline_id}/graph")
    async def get_pipeline_graph(pipeline_id: str) -> Dict[str, Any]:
        """Get the execution graph for a pipeline."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_pipeline_graph(pipeline_id)

    @app.get("/api/pipelines/{pipeline_id}/yaml")
    async def get_pipeline_yaml(pipeline_id: str) -> Union[str, Dict[str, str]]:
        """Get the YAML configuration for a pipeline execution."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        pipeline = tracker.get_pipeline(pipeline_id)
        if pipeline and pipeline.get("config_yaml"):
            yaml_path = Path(pipeline["config_yaml"])
            if not yaml_path.exists() and config_dir:
                yaml_path = Path(config_dir) / f"{pipeline_id}.yaml"
            if not yaml_path.exists() and config_dir:
                yaml_path = Path(config_dir).resolve() / f"{pipeline_id}.yaml"
            if yaml_path.exists():
                return yaml_path.read_text(encoding="utf-8")
        return {"error": "YAML not found"}

    @app.get("/api/trends")
    async def get_trends(
        days: int = 7, pipeline_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get execution trends over time."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_trend_data(days=days, pipeline_name=pipeline_name)

    @app.get("/api/alerts")
    async def get_alerts(
        limit: int = 50, severity: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get recently fired alerts."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_fired_alerts(limit=limit, severity=severity)

    @app.get("/api/alerts/config")
    async def get_alert_config() -> List[Dict[str, Any]]:
        """Get alert threshold configurations."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_alert_thresholds()

    @app.get("/api/events")
    async def get_events(
        pipeline_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get pipeline events."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_events(pipeline_id=pipeline_id, limit=limit)

    @app.get("/api/slow-steps")
    async def get_slow_steps(limit: int = 10) -> List[Dict[str, Any]]:
        """Get the slowest pipeline steps."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_top_slow_steps(limit=limit)

    @app.get("/api/analysis/states")
    async def get_states_analysis() -> List[Dict[str, Any]]:
        """Get analysis of pipeline states."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_states_analysis()

    @app.get("/api/analysis/pipelines")
    async def get_pipelines_analysis() -> List[Dict[str, Any]]:
        """Get analysis of pipeline performance."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.get_pipelines_analysis()

    @app.post("/api/alerts/{alert_id}/acknowledge")
    async def acknowledge_alert(alert_id: int) -> Dict[str, Any]:
        """Acknowledge a fired alert."""
        tracker = PipelineTracker(db_path=db_path, config_dir=config_dir)
        return tracker.acknowledge_alert(alert_id)

    @app.get("/api/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy", "db": db_path}

    return app


def get_dashboard_html() -> str:
    """
    Generate the complete dashboard HTML using Jinja2 templates.

    Returns:
        The rendered HTML string.
    """
    try:
        template = jinja_env.get_template("base.html")
        return template.render()
    except (FileNotFoundError, RuntimeError) as e:
        # Fallback to simple inline HTML if templates fail
        return f"""<!DOCTYPE html>
<html>
<head><title>Error loading templates: {e}</title></head>
<body><h1>Dashboard Error</h1><p>{e}</p></body>
</html>"""
