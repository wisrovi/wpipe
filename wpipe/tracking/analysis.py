"""
Statistical analysis and trend calculation for the dashboard.
"""

import math
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class AnalysisManager:
    """Handles statistical aggregations and trend calculations."""

    def __init__(
        self,
        db_pipelines: Any,
        db_steps: Any,
        db_step_history: Any,
        db_alerts_fired: Any,
    ):
        """
        Initialize the AnalysisManager with database accessors.

        Args:
            db_pipelines: Database accessor for pipeline history.
            db_steps: Database accessor for step history.
            db_step_history: Database accessor for detailed step history.
            db_alerts_fired: Database accessor for fired alerts.
        """
        self.db_pipelines = db_pipelines
        self.db_steps = db_steps
        self.db_step_history = db_step_history
        self.db_alerts_fired = db_alerts_fired

    def get_stats(self) -> Dict[str, Any]:
        """
        Get overall statistics for dashboard summary cards.

        Returns:
            Dictionary with aggregated statistics.
        """
        try:
            all_p = self.db_pipelines.get_all()
        except (AttributeError, RuntimeError, ValueError):
            all_p = []

        total = len(all_p)
        completed = len([p for p in all_p if p.status == "completed"])
        errors = len([p for p in all_p if p.status == "error"])
        running = len([p for p in all_p if p.status == "running"])

        durations = [
            p.total_duration_ms
            for p in all_p
            if p.status == "completed" and p.total_duration_ms
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0

        try:
            all_steps = self.db_steps.get_all()
        except (AttributeError, RuntimeError, ValueError):
            all_steps = []

        total_steps = len(all_steps)
        completed_steps = len([s for s in all_steps if s.status == "completed"])

        try:
            fired = self.db_alerts_fired.get_all()
        except (AttributeError, RuntimeError, ValueError):
            fired = []
        unack = len([a for a in fired if getattr(a, "acknowledged", 0) == 0])

        return {
            "total_pipelines": total,
            "completed": completed,
            "errors": errors,
            "running": running,
            "success_rate": round((completed / total * 100), 1) if total > 0 else 0,
            "avg_duration_ms": round(avg_duration, 2),
            "total_steps": total_steps,
            "step_success_rate": (
                round((completed_steps / total_steps * 100), 1)
                if total_steps > 0
                else 0
            ),
            "unacknowledged_alerts": unack,
        }

    def get_trend_data(
        self, days: int = 7, pipeline_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get aggregated daily data for trend charts.

        Args:
            days: Number of days to look back.
            pipeline_name: Optional filter by pipeline name.

        Returns:
            A list of daily aggregated data dictionaries.
        """
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        try:
            all_p = self.db_pipelines.get_all()
        except (AttributeError, RuntimeError, ValueError):
            return []

        filtered = [p for p in all_p if p.started_at and p.started_at >= cutoff]
        if pipeline_name:
            filtered = [p for p in filtered if p.name == pipeline_name]

        daily: Dict[str, Dict[str, Any]] = {}
        for p in filtered:
            date = p.started_at.split("T")[0]
            if date not in daily:
                daily[date] = {
                    "date": date,
                    "count": 0,
                    "success": 0,
                    "errors": 0,
                    "durations": [],
                }
            daily[date]["count"] += 1
            if p.status == "completed":
                daily[date]["success"] += 1
                if p.total_duration_ms:
                    daily[date]["durations"].append(p.total_duration_ms)
            elif p.status == "error":
                daily[date]["errors"] += 1

        result = []
        for date in sorted(daily.keys()):
            day = daily[date]
            day["avg_duration"] = (
                sum(day["durations"]) / len(day["durations"]) if day["durations"] else 0
            )
            del day["durations"]
            result.append(day)
        return result

    def get_top_slow_steps(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Identify slowest steps across all executions.

        Args:
            limit: Maximum number of steps to return.

        Returns:
            A list of step statistics dictionaries.
        """
        try:
            all_history = self.db_step_history.get_all()
        except (AttributeError, RuntimeError, ValueError):
            return []

        stats: Dict[str, Dict[str, Any]] = {}
        for h in all_history:
            if h.status != "completed":
                continue
            if h.step_name not in stats:
                stats[h.step_name] = {
                    "step_name": h.step_name,
                    "count": 0,
                    "total_ms": 0,
                    "max_ms": 0,
                }
            stats[h.step_name]["count"] += 1
            stats[h.step_name]["total_ms"] += h.duration_ms
            stats[h.step_name]["max_ms"] = max(
                stats[h.step_name]["max_ms"], h.duration_ms
            )

        slow_steps = []
        for s in stats.values():
            s["avg_duration_ms"] = s["total_ms"] / s["count"]
            slow_steps.append(s)
        slow_steps.sort(key=lambda x: x["avg_duration_ms"], reverse=True)
        return slow_steps[:limit]

    def get_states_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis of all states/steps.

        Returns:
            Dictionary with states analysis.
        """
        try:
            all_steps = self.db_steps.get_all()
        except (AttributeError, RuntimeError, ValueError):
            all_steps = []

        if not all_steps:
            return {
                "total_states": 0,
                "total_executions": 0,
                "total_errors": 0,
                "most_used": [],
                "slowest": [],
                "most_errors": [],
            }

        stats: Dict[str, Dict[str, Any]] = {}
        for s in all_steps:
            name = s.step_name
            if name not in stats:
                stats[name] = {
                    "state_name": name,
                    "execution_count": 0,
                    "total_ms": 0,
                    "error_count": 0,
                }
            stats[name]["execution_count"] += 1
            if s.status == "error":
                stats[name]["error_count"] += 1
            if s.duration_ms:
                stats[name]["total_ms"] += s.duration_ms

        most_used = sorted(
            stats.values(), key=lambda x: x["execution_count"], reverse=True
        )[:20]
        for item in most_used:
            item["avg_duration_ms"] = item["total_ms"] / item["execution_count"]

        slowest = sorted(
            [s for s in stats.values() if s["execution_count"] > s["error_count"]],
            key=lambda x: (x["total_ms"] / (x["execution_count"] - x["error_count"])),
            reverse=True,
        )[:15]
        for item in slowest:
            item["avg_duration_ms"] = item["total_ms"] / (
                item["execution_count"] - item["error_count"]
            )

        most_errors = sorted(
            [s for s in stats.values() if s["error_count"] > 0],
            key=lambda x: x["error_count"] / x["execution_count"],
            reverse=True,
        )[:15]
        for item in most_errors:
            item["error_rate"] = item["error_count"] / item["execution_count"]

        return {
            "total_states": len(stats),
            "total_executions": len(all_steps),
            "total_errors": len([s for s in all_steps if s.status == "error"]),
            "most_used": most_used,
            "slowest": slowest,
            "most_errors": most_errors,
        }

    def get_pipelines_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis of all pipelines.

        Returns:
            Dictionary with pipelines analysis.
        """
        try:
            all_p = self.db_pipelines.get_all()
        except (AttributeError, RuntimeError, ValueError):
            all_p = []

        if not all_p:
            return {
                "total_pipelines": 0,
                "total_runs": 0,
                "avg_duration_ms": 0,
                "total_errors": 0,
                "slowest": [],
                "most_errors": [],
                "recent": [],
            }

        stats: Dict[str, Dict[str, Any]] = {}
        for p in all_p:
            if p.name not in stats:
                stats[p.name] = {
                    "name": p.name,
                    "execution_count": 0,
                    "total_ms": 0,
                    "error_count": 0,
                }
            stats[p.name]["execution_count"] += 1
            if p.status == "error":
                stats[p.name]["error_count"] += 1
            if p.total_duration_ms:
                stats[p.name]["total_ms"] += p.total_duration_ms

        slowest = sorted(
            [s for s in stats.values() if s["execution_count"] > s["error_count"]],
            key=lambda x: (x["total_ms"] / (x["execution_count"] - x["error_count"])),
            reverse=True,
        )[:10]
        for item in slowest:
            item["avg_duration_ms"] = item["total_ms"] / (
                item["execution_count"] - item["error_count"]
            )

        most_errors = sorted(
            [s for s in stats.values() if s["error_count"] > 0],
            key=lambda x: x["error_count"] / x["execution_count"],
            reverse=True,
        )[:10]
        for item in most_errors:
            item["error_rate"] = item["error_count"] / item["execution_count"]

        all_p.sort(key=lambda x: x.started_at or "", reverse=True)
        recent = []
        for p in all_p[:10]:
            try:
                recent.append(p.model_dump())
            except (AttributeError, TypeError):
                continue

        durations = [
            p.total_duration_ms
            for p in all_p
            if p.status == "completed" and p.total_duration_ms
        ]
        avg_dur = sum(durations) / len(durations) if durations else 0

        return {
            "total_pipelines": len(set(p.name for p in all_p)),
            "total_runs": len(all_p),
            "avg_duration_ms": avg_dur,
            "total_errors": len([p for p in all_p if p.status == "error"]),
            "slowest": slowest,
            "most_errors": most_errors,
            "recent": recent,
        }

    def _percentile(self, data: List[float], percentile: int) -> float:
        """
        Calculate the percentile of a list of values.

        Args:
            data: List of values.
            percentile: Percentile to calculate (0-100).

        Returns:
            The calculated percentile value.
        """
        if not data:
            return 0.0
        data_sorted = sorted(data)
        index = (len(data_sorted) - 1) * percentile / 100
        lower = math.floor(index)
        upper = math.ceil(index)
        if lower == upper:
            return data_sorted[int(index)]
        return data_sorted[int(lower)] * (upper - index) + data_sorted[int(upper)] * (
            index - lower
        )
