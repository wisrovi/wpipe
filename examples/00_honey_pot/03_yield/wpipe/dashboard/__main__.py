"""
Allow running the dashboard as a module: python -m wpipe.dashboard
"""

import argparse

from .main import start_dashboard


def main():
    parser = argparse.ArgumentParser(description="wpipe Dashboard")
    parser.add_argument("--db", default="pipeline.db", help="Path to SQLite database")
    parser.add_argument(
        "--config-dir", default=None, help="Path to YAML configs directory"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8035, help="Port to bind to")
    parser.add_argument(
        "--open", action="store_true", help="Open browser automatically"
    )

    args = parser.parse_args()
    start_dashboard(
        db_path=args.db,
        config_dir=args.config_dir,
        host=args.host,
        port=args.port,
        open_browser=args.open,
    )


if __name__ == "__main__":
    main()
