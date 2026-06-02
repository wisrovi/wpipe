"""
wpipe CLI - Command Line Interface for wpipe library.

This module provides the main entry point for the 'wpipe' command.
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

from wpipe import __version__


def main():
    """Main entry point for the wpipe CLI."""
    parser = argparse.ArgumentParser(
        description="wpipe CLI - Industrial-grade pipeline orchestration tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"wpipe {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: dashboard
    dashboard_parser = subparsers.add_parser(
        "dashboard", help="Start the wpipe visualization dashboard"
    )
    dashboard_parser.add_argument(
        "--port", type=int, default=8035, help="Port to run the dashboard on"
    )
    dashboard_parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host address to bind the server"
    )
    dashboard_parser.add_argument(
        "--db", type=str, default="wpipe_dashboard.db", help="Path to the SQLite database"
    )
    dashboard_parser.add_argument(
        "--config-dir", type=str, help="Directory containing pipeline configurations"
    )
    dashboard_parser.add_argument(
        "--open", action="store_true", help="Automatically open the browser"
    )

    # Command: run
    run_parser = subparsers.add_parser("run", help="Execute a pipeline script")
    run_parser.add_argument(
        "file", type=str, help="Path to the Python file containing the pipeline"
    )

    args = parser.parse_args()

    if args.command == "dashboard":
        from wpipe import start_dashboard

        print(f"🚀 Starting wpipe Dashboard on http://{args.host}:{args.port}")
        start_dashboard(
            db_path=args.db,
            config_dir=args.config_dir,
            host=args.host,
            port=args.port,
            open_browser=args.open,
        )

    elif args.command == "run":
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ Error: File '{args.file}' not found.")
            sys.exit(1)

        print(f"⚙️ Running pipeline script: {file_path.absolute()}")
        
        # Add current directory to sys.path to allow local imports in the script
        sys.path.insert(0, str(file_path.parent.absolute()))
        
        try:
            # Load and execute the python file
            spec = importlib.util.spec_from_file_location("__main__", str(file_path))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            else:
                print(f"❌ Error: Could not load module from '{args.file}'")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Execution Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
