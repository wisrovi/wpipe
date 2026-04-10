"""
SQLite database module for storing pipeline execution records.
"""

from wsqlite import WSQLite as Wsqlite_original
from .sqlite_logs import LogGestor, LogGestorModel

# Alias LogGestor as Wsqlite for the requested import
Wsqlite = LogGestor

from .Sqlite import SQLite

__all__ = ["SQLite", "Wsqlite", "LogGestor", "LogGestorModel"]
