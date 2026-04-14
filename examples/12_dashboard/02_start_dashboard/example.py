"""
Dashboard - Start Dashboard

This example shows different ways to start the wpipe Dashboard.

The dashboard provides a modern web interface to:
- View pipeline execution history
- See statistics and charts
- Visualize pipeline flow
- Inspect individual execution details
"""

import sys


def example_cli():
    """Start dashboard using CLI command."""
    print("=" * 60)
    print("Example 1: Using CLI command")
    print("=" * 60)
    print("Run in terminal:")
    print("  cd ..")
    print(
        "  python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )
    print()


def example_module():
    """Start dashboard using Python module."""
    print("=" * 60)
    print("Example 2: Using Python module")
    print("=" * 60)
    print("Run in terminal:")
    print("  cd ..")
    print(
        "  python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )
    print()


def example_python():
    """Start dashboard using Python code."""
    print("=" * 60)
    print("Example 3: Using Python code")
    print("=" * 60)
    print(
        """
# Option A: Using start_dashboard function
from wpipe import start_dashboard

start_dashboard(
    db_path="pipeline_data.db",
    host="127.0.0.1",
    port=8000,
    open_browser=True
)

# Option B: Using the module directly
import uvicorn
from wpipe.dashboard.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
    )


def example_config():
    """Dashboard configuration options."""
    print("=" * 60)
    print("Dashboard Configuration Options")
    print("=" * 60)
    print(
        """
--host HOST         Host to bind (default: 127.0.0.1)
--port PORT         Port to bind (default: 8000)
--db DB_PATH        SQLite database path (default: register.db)
--open              Automatically open browser
--reload            Enable auto-reload for development
"""
    )


def main():
    """Show all ways to start the dashboard."""
    print("\n" + "=" * 60)
    print("WPIPE DASHBOARD - START OPTIONS")
    print("=" * 60 + "\n")

    try:
        import fastapi
        import uvicorn

        print("✓ Dashboard dependencies installed\n")
    except ImportError:
        print("✗ Dashboard dependencies not installed")
        print("\nInstall with: pip install -e '.[dashboard]'\n")
        sys.exit(1)

    example_cli()
    example_module()
    example_python()
    example_config()

    print("=" * 60)
    print("API Endpoints Available")
    print("=" * 60)
    print(
        """
GET /               - Dashboard HTML
GET /api/health     - Health check
GET /api/records    - List records (supports ?limit, ?offset, ?search)
GET /api/records/1  - Get specific record
GET /api/stats      - Get statistics
GET /api/config     - Get current configuration
POST /api/config    - Update configuration
"""
    )


if __name__ == "__main__":
    main()
