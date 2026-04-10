"""
SQLite database module for storing pipeline execution records.
"""

from wsqlite import WSQLite as Wsqlite

from .Sqlite import SQLite

__all__ = ["SQLite", "Wsqlite"]
