"""
wpipe Dashboard - Enterprise-grade pipeline visualization

This module provides a FastAPI-based dashboard for visualizing pipeline executions.
The dashboard is modularized into:
- main.py: FastAPI app and API endpoints
- static/styles.css: All styles
- static/dashboard.js: All JavaScript logic
- templates/: HTML template views
"""

import json
from pathlib import Path
from typing import Optional

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
    db_path: str = "pipeline.db",
    config_dir: Optional[str] = None,
    host: str = "127.0.0.1",
    port: int = 8035,
    open_browser: bool = False,
):
    """Start the wpipe dashboard server."""
    import uvicorn
    from webbrowser import open as open_url

    app = create_app(db_path, config_dir)

    if open_browser:
        import threading

        def open_browser_delay():
            import time

            time.sleep(1.5)
            open_url(f"http://{host}:{port}")

        threading.Thread(target=open_browser_delay, daemon=True).start()

    uvicorn.run(app, host=host, port=port)


def create_app(
    db_path: str = "pipeline.db",
    config_dir: Optional[str] = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="wpipe Dashboard")

    # Mount static files
    static_dir = DASHBOARD_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    async def root():
        return HTMLResponse(get_dashboard_html(db_path, config_dir))

    @app.get("/api/stats")
    async def get_stats():
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_stats()

    @app.get("/api/pipelines")
    async def get_pipelines(status: Optional[str] = None):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipelines(status=status)

    @app.get("/api/data/{table}")
    async def get_table_data(
        table: str,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
    ):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_table_data(
            table=table,
            page=page,
            page_size=page_size,
            search=search,
            status=status,
        )

    @app.get("/api/pipelines/{pipeline_id}")
    async def get_pipeline(pipeline_id: str):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipeline(pipeline_id)

    @app.get("/api/pipelines/{pipeline_id}/graph")
    async def get_pipeline_graph(pipeline_id: str):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipeline_graph(pipeline_id)

    @app.get("/api/pipelines/{pipeline_id}/yaml")
    async def get_pipeline_yaml(pipeline_id: str):
        tracker = PipelineTracker(db_path, config_dir)
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
    async def get_trends(days: int = 7, pipeline_name: Optional[str] = None):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_trend_data(days=days, pipeline_name=pipeline_name)

    @app.get("/api/alerts")
    async def get_alerts(limit: int = 50, severity: Optional[str] = None):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_fired_alerts(limit=limit, severity=severity)

    @app.get("/api/alerts/config")
    async def get_alert_config():
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_alert_thresholds()

    @app.get("/api/events")
    async def get_events(pipeline_id: Optional[str] = None, limit: int = 50):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_events(pipeline_id=pipeline_id, limit=limit)

    @app.get("/api/slow-steps")
    async def get_slow_steps(limit: int = 10):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_top_slow_steps(limit=limit)

    @app.get("/api/analysis/states")
    async def get_states_analysis():
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_states_analysis()

    @app.get("/api/analysis/pipelines")
    async def get_pipelines_analysis():
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipelines_analysis()

    @app.post("/api/alerts/{alert_id}/acknowledge")
    async def acknowledge_alert(alert_id: int):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.acknowledge_alert(alert_id)

    @app.get("/api/health")
    async def health_check():
        return {"status": "healthy", "db": db_path}

    return app


def get_dashboard_html(db_path: str, config_dir: Optional[str] = None) -> str:
    """Generate the complete dashboard HTML using Jinja2 templates."""
    try:
        template = jinja_env.get_template("base.html")
        return template.render()
    except Exception as e:
        # Fallback to simple inline HTML if templates fail
        return f"""<!DOCTYPE html>
<html>
<head><title>Error loading templates: {e}</title></head>
<body><h1>Dashboard Error</h1><p>{e}</p></body>
</html>"""
