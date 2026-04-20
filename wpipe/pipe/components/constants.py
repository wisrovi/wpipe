"""
Error codes and execution constants for WPipe.
"""

class Codes:
    """Standard task and process status codes."""
    TASK_RUNNING = 100
    TASK_COMPLETED = 200
    TASK_FAILED = 502
    TASK_WAITING = 300

    PROCESS_CREATED = 1
    PROCESS_RUNNING = 2
    PROCESS_FINISHED = 3
    PROCESS_FAILED = 4
