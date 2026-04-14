"""
Unified API reporting and metrics logic for synchronous and asynchronous pipelines.
"""

import json
import traceback
from typing import Any, Optional, Dict
from wpipe.api_client import APIClient
from .constants import Codes


class ReportingMixin:
    """Provides methods for reporting status to external APIs."""

    def _api_task_update(
        self,
        api_client: Optional[APIClient],
        task_info: Dict[str, Any],
        verbose: bool = False
    ) -> None:
        """Report task status to API."""
        if not api_client:
            return
        try:
            api_client.update_task(task_info)
        except Exception as e:
            if verbose:
                print(f"[API ERROR] Task update failed: {e}")

    def _api_process_update(
        self,
        api_client: Optional[APIClient],
        process_info: Dict[str, Any],
        verbose: bool = False
    ) -> None:
        """Report process status to API."""
        if not api_client:
            return
        try:
            api_client.update_process(process_info)
        except Exception as e:
            if verbose:
                print(f"[API ERROR] Process update failed: {e}")

    def _format_error_traceback(self, exception: Exception) -> list:
        """Format exception traceback as a list of lines."""
        return traceback.format_exception(
            type(exception), exception, exception.__traceback__
        )
