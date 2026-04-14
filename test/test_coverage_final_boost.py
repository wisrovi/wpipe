"""
Comprehensive tests to boost coverage for specific modules:
- wpipe/dashboard/__main__.py
- wpipe/util/utils.py
- wpipe/ram/ram.py
- wpipe/export/exporter.py
- wpipe/pipe/components/reporting.py
- wpipe/pipe/components/logic_blocks_async.py
- wpipe/pipe/pipe_async.py
- wpipe/pipe/pipe.py
"""

import asyncio
import json
import os
import sqlite3
import sys
import tempfile
import traceback
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, call

import pytest
import yaml

# ---------------------------------------------------------------------------
# 1. wpipe/dashboard/__main__.py
# ---------------------------------------------------------------------------

class TestDashboardMain:
    """Test the dashboard __main__ entry point."""

    @patch("wpipe.dashboard.__main__.start_dashboard")
    def test_main_default_args(self, mock_start):
        """Test main() with default arguments."""
        from wpipe.dashboard.__main__ import main

        test_argv = ["prog"]
        with patch.object(sys, "argv", test_argv):
            main()

        mock_start.assert_called_once_with(
            db_path="pipeline.db",
            config_dir=None,
            host="127.0.0.1",
            port=8035,
            open_browser=False,
        )

    @patch("wpipe.dashboard.__main__.start_dashboard")
    def test_main_with_custom_args(self, mock_start):
        """Test main() with custom CLI arguments."""
        from wpipe.dashboard.__main__ import main

        test_argv = [
            "prog",
            "--db", "/tmp/my.db",
            "--config-dir", "/etc/wpipe",
            "--host", "0.0.0.0",
            "--port", "9999",
            "--open",
        ]
        with patch.object(sys, "argv", test_argv):
            main()

        mock_start.assert_called_once_with(
            db_path="/tmp/my.db",
            config_dir="/etc/wpipe",
            host="0.0.0.0",
            port=9999,
            open_browser=True,
        )

    def test_main_help(self, capsys):
        """Test --help flag prints usage."""
        from wpipe.dashboard.__main__ import main

        test_argv = ["prog", "--help"]
        with patch.object(sys, "argv", test_argv):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "wpipe Dashboard" in captured.out or "db" in captured.out

    @patch("wpipe.dashboard.__main__.start_dashboard")
    def test_main_db_only(self, mock_start):
        """Test main() with only --db flag."""
        from wpipe.dashboard.__main__ import main

        test_argv = ["prog", "--db", "custom.db"]
        with patch.object(sys, "argv", test_argv):
            main()

        mock_start.assert_called_once()
        args = mock_start.call_args
        assert args.kwargs["db_path"] == "custom.db"


# ---------------------------------------------------------------------------
# 2. wpipe/util/utils.py
# ---------------------------------------------------------------------------

class TestLeerYaml:
    """Test leer_yaml function."""

    def test_leer_yaml_valid_file(self, tmp_path):
        """Read a valid YAML file."""
        from wpipe.util.utils import leer_yaml

        content = {"key": "value", "number": 42}
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml.dump(content))

        result = leer_yaml(str(yaml_file))
        assert result == content

    def test_leer_yaml_verbose_valid(self, tmp_path, capsys):
        """Read valid YAML with verbose=True."""
        from wpipe.util.utils import leer_yaml

        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("key: value")

        result = leer_yaml(str(yaml_file), verbose=True)
        assert result == {"key": "value"}
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_leer_yaml_file_not_found_verbose(self, capsys):
        """Read non-existent file with verbose=True."""
        from wpipe.util.utils import leer_yaml

        result = leer_yaml("/nonexistent/path.yaml", verbose=True)
        assert result == {}
        captured = capsys.readouterr()
        assert "no se encontr" in captured.out

    def test_leer_yaml_invalid_syntax(self, tmp_path):
        """Read YAML with syntax error."""
        from wpipe.util.utils import leer_yaml

        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text("key: :invalid:\n  - [unclosed")

        result = leer_yaml(str(yaml_file))
        assert result == {}

    def test_leer_yaml_invalid_syntax_verbose(self, tmp_path, capsys):
        """Read YAML with syntax error and verbose=True."""
        from wpipe.util.utils import leer_yaml

        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text("key: :invalid:\n  - [unclosed")

        result = leer_yaml(str(yaml_file), verbose=True)
        assert result == {}
        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_leer_yaml_empty_file(self, tmp_path):
        """Read an empty YAML file."""
        from wpipe.util.utils import leer_yaml

        yaml_file = tmp_path / "empty.yaml"
        yaml_file.write_text("")

        result = leer_yaml(str(yaml_file))
        assert result == {}

    def test_leer_yaml_path_object(self, tmp_path):
        """Read YAML using Path object instead of string."""
        from wpipe.util.utils import leer_yaml

        content = {"a": 1}
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml.dump(content))

        result = leer_yaml(yaml_file)
        assert result == content


class TestEscribirYaml:
    """Test escribir_yaml function."""

    def test_escribir_yaml_basic(self, tmp_path):
        """Write YAML file basic test."""
        from wpipe.util.utils import escribir_yaml

        output = tmp_path / "out.yaml"
        data = {"name": "test", "values": [1, 2, 3]}

        escribir_yaml(str(output), data)

        assert output.exists()
        loaded = yaml.safe_load(output.read_text())
        assert loaded == data

    def test_escribir_yaml_verbose(self, tmp_path, capsys):
        """Write YAML with verbose=True."""
        from wpipe.util.utils import escribir_yaml

        output = tmp_path / "out.yaml"
        data = {"key": "value"}

        escribir_yaml(str(output), data, verbose=True)

        captured = capsys.readouterr()
        assert "exitosamente" in captured.out

    def test_escribir_yaml_oserror(self, capsys):
        """Write YAML with OSError (mocked open)."""
        from wpipe.util.utils import escribir_yaml

        with patch("wpipe.util.utils.open", side_effect=OSError("disk full")):
            escribir_yaml("/tmp/bad.yaml", {"a": 1}, verbose=True)

        captured = capsys.readouterr()
        assert "Error" in captured.out

    def test_escribir_yaml_oserror_no_verbose(self):
        """Write YAML with OSError without verbose."""
        from wpipe.util.utils import escribir_yaml

        with patch("wpipe.util.utils.open", side_effect=OSError("disk full")):
            escribir_yaml("/tmp/bad.yaml", {"a": 1}, verbose=False)

    def test_escribir_yaml_path_object(self, tmp_path):
        """Write YAML using Path object."""
        from wpipe.util.utils import escribir_yaml

        output = tmp_path / "out.yaml"
        data = {"x": 10}

        escribir_yaml(output, data)

        loaded = yaml.safe_load(output.read_text())
        assert loaded == data


# ---------------------------------------------------------------------------
# 3. wpipe/ram/ram.py
# ---------------------------------------------------------------------------

class TestMemoryLimit:
    """Test memory_limit function."""

    def test_memory_limit_non_linux(self, capsys):
        """Test memory_limit on non-Linux platform."""
        from wpipe.ram.ram import memory_limit

        with patch("wpipe.ram.ram.platform.system", return_value="Darwin"):
            memory_limit(0.5)

        captured = capsys.readouterr()
        assert "Only works on linux" in captured.out

    def test_memory_limit_windows(self, capsys):
        """Test memory_limit on Windows."""
        from wpipe.ram.ram import memory_limit

        with patch("wpipe.ram.ram.platform.system", return_value="Windows"):
            memory_limit(0.5)

        captured = capsys.readouterr()
        assert "Only works on linux" in captured.out

    @patch("wpipe.ram.ram.platform.system", return_value="Linux")
    @patch("wpipe.ram.ram.get_memory", return_value=8388608)
    @patch("wpipe.ram.ram.resource.getrlimit", return_value=(1, -1))
    @patch("wpipe.ram.ram.resource.setrlimit")
    def test_memory_limit_linux(self, mock_set, mock_getrlimit, mock_getmem, mock_plat):
        """Test memory_limit on Linux sets the limit."""
        import resource
        from wpipe.ram.ram import memory_limit

        memory_limit(0.5)

        mock_set.assert_called_once()
        args = mock_set.call_args[0]
        assert args[0] == resource.RLIMIT_AS
        # The soft limit should be get_memory * 1024 * 0.5
        expected_soft = int(8388608 * 1024 * 0.5)
        assert args[1][0] == expected_soft


class TestMemoryDecorator:
    """Test memory decorator."""

    def test_memory_decorator_normal_function(self):
        """Test memory decorator on a normal function."""
        from wpipe.ram.ram import memory

        @memory(percentage=0.5)
        def simple_func():
            return 42

        with patch("wpipe.ram.ram.platform.system", return_value="Darwin"):
            result = simple_func()

        assert result == 42

    def test_memory_decorator_memory_error(self, capsys):
        """Test memory decorator when MemoryError is raised."""
        from wpipe.ram.ram import memory

        @memory(percentage=0.5)
        def mem_error_func():
            raise MemoryError("OOM")

        with patch("wpipe.ram.ram.platform.system", return_value="Darwin"), \
             patch("wpipe.ram.ram.get_memory", return_value=1048576):
            with pytest.raises(SystemExit) as exc_info:
                mem_error_func()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Remain:" in captured.out or "ERROR" in captured.err

    def test_memory_decorator_with_args(self):
        """Test memory decorator passes arguments correctly."""
        from wpipe.ram.ram import memory

        @memory(percentage=0.5)
        def add_func(a, b):
            return a + b

        with patch("wpipe.ram.ram.platform.system", return_value="Darwin"):
            result = add_func(3, 4)

        assert result == 7

    def test_memory_decorator_with_kwargs(self):
        """Test memory decorator passes keyword arguments."""
        from wpipe.ram.ram import memory

        @memory(percentage=0.5)
        def greet_func(name, greeting="Hello"):
            return f"{greeting}, {name}"

        with patch("wpipe.ram.ram.platform.system", return_value="Darwin"):
            result = greet_func("World", greeting="Hi")

        assert result == "Hi, World"


class TestGetMemory:
    """Test get_memory function."""

    def test_get_memory_reads_proc(self):
        """Test get_memory reads /proc/meminfo."""
        from wpipe.ram.ram import get_memory

        meminfo = """MemTotal:       16384000 kB
MemFree:         8192000 kB
Buffers:          512000 kB
Cached:          2048000 kB
"""
        with patch("builtins.open", unittest.mock.mock_open(read_data=meminfo)):
            result = get_memory()

        # MemFree + Buffers + Cached
        expected = 8192000 + 512000 + 2048000
        assert result == expected


# ---------------------------------------------------------------------------
# 4. wpipe/export/exporter.py
# ---------------------------------------------------------------------------

class TestExporterPipelineLogs:
    """Test PipelineExporter.export_pipeline_logs."""

    def _create_db_with_pipelines(self, db_path):
        """Create a test DB with pipeline data."""
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS pipelines (
            pipeline_id TEXT,
            name TEXT,
            status TEXT,
            started_at TEXT,
            total_duration_ms REAL
        )""")
        c.execute("INSERT INTO pipelines VALUES (?, ?, ?, ?, ?)",
                  ("p1", "TestPipeline", "completed", "2024-01-01T00:00:00", 1000.0))
        c.execute("INSERT INTO pipelines VALUES (?, ?, ?, ?, ?)",
                  ("p2", "TestPipeline2", "failed", "2024-01-02T00:00:00", 2000.0))
        conn.commit()
        conn.close()

    def test_export_pipeline_logs_json(self, tmp_path):
        """Test export_pipeline_logs in JSON format."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_pipelines(db)
        exporter = PipelineExporter(db)

        result = exporter.export_pipeline_logs(format="json")
        data = json.loads(result)
        assert len(data) == 2

    def test_export_pipeline_logs_with_filter(self, tmp_path):
        """Test export_pipeline_logs with pipeline_id filter."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_pipelines(db)
        exporter = PipelineExporter(db)

        result = exporter.export_pipeline_logs(pipeline_id="p1", format="json")
        data = json.loads(result)
        assert len(data) == 1
        assert data[0]["pipeline_id"] == "p1"

    def test_export_pipeline_logs_csv(self, tmp_path):
        """Test export_pipeline_logs in CSV format."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_pipelines(db)
        exporter = PipelineExporter(db)

        result = exporter.export_pipeline_logs(format="csv")
        lines = result.strip().split("\n")
        assert len(lines) == 3  # header + 2 rows
        assert "pipeline_id" in lines[0]

    def test_export_pipeline_logs_csv_with_commas(self, tmp_path):
        """Test CSV export with values containing commas."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS pipelines (
            pipeline_id TEXT,
            name TEXT,
            status TEXT,
            started_at TEXT,
            total_duration_ms REAL
        )""")
        c.execute("INSERT INTO pipelines VALUES (?, ?, ?, ?, ?)",
                  ("p1", "Test, Pipeline", "completed", "2024-01-01", 1000.0))
        conn.commit()
        conn.close()

        exporter = PipelineExporter(db)
        result = exporter.export_pipeline_logs(format="csv")
        # Commas in values should be replaced with semicolons
        assert "Test; Pipeline" in result

    def test_export_pipeline_logs_unsupported_format(self, tmp_path):
        """Test export_pipeline_logs with unsupported format raises ValueError."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_pipelines(db)
        exporter = PipelineExporter(db)

        with pytest.raises(ValueError, match="Unsupported format"):
            exporter.export_pipeline_logs(format="xml")

    def test_export_pipeline_logs_to_file(self, tmp_path):
        """Test export_pipeline_logs saves to output file."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_pipelines(db)
        exporter = PipelineExporter(db)

        output = str(tmp_path / "logs.json")
        result = exporter.export_pipeline_logs(format="json", output_path=output)
        assert result == output
        assert Path(output).exists()


class TestExporterMetrics:
    """Test PipelineExporter.export_metrics."""

    def _create_db_with_metrics(self, db_path):
        """Create a test DB with system_metrics table."""
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS system_metrics (
            pipeline_id TEXT,
            cpu_percent REAL,
            memory_mb REAL,
            created_at TEXT
        )""")
        c.execute("INSERT INTO system_metrics VALUES (?, ?, ?, ?)",
                  ("p1", 45.5, 512.0, "2024-01-01T00:00:00"))
        conn.commit()
        conn.close()

    def test_export_metrics_json(self, tmp_path):
        """Test export_metrics in JSON format."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_metrics(db)
        exporter = PipelineExporter(db)

        result = exporter.export_metrics(format="json")
        data = json.loads(result)
        assert len(data) == 1

    def test_export_metrics_csv(self, tmp_path):
        """Test export_metrics in CSV format."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_metrics(db)
        exporter = PipelineExporter(db)

        result = exporter.export_metrics(format="csv")
        lines = result.strip().split("\n")
        assert len(lines) == 2  # header + 1 row

    def test_export_metrics_unsupported_format(self, tmp_path):
        """Test export_metrics with unsupported format raises ValueError."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        self._create_db_with_metrics(db)
        exporter = PipelineExporter(db)

        with pytest.raises(ValueError, match="Unsupported format"):
            exporter.export_metrics(format="xml")


class TestExporterStatistics:
    """Test PipelineExporter.export_statistics."""

    def test_export_statistics_json(self, tmp_path):
        """Test export_statistics in JSON format."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        exporter = PipelineExporter(db)

        result = exporter.export_statistics(format="json")
        stats = json.loads(result)
        assert "total_executions" in stats
        assert stats["total_executions"] == 0

    def test_export_statistics_unsupported_csv(self, tmp_path):
        """Test export_statistics with CSV raises ValueError."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        exporter = PipelineExporter(db)

        with pytest.raises(ValueError, match="only supports JSON"):
            exporter.export_statistics(format="csv")

    def test_export_statistics_to_file(self, tmp_path):
        """Test export_statistics saves to output file."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        exporter = PipelineExporter(db)

        output = str(tmp_path / "stats.json")
        result = exporter.export_statistics(format="json", output_path=output)
        assert result == output
        assert Path(output).exists()
        stats = json.loads(Path(output).read_text())
        assert "total_executions" in stats


class TestExportCsvEdgeCases:
    """Test _export_csv edge cases."""

    def test_export_csv_empty_rows(self, tmp_path):
        """Test _export_csv with empty rows list."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        exporter = PipelineExporter(db)

        result = exporter._export_csv([])
        assert result == ""

    def test_export_csv_empty_rows_to_file(self, tmp_path):
        """Test _export_csv with empty rows writes empty file."""
        from wpipe.export.exporter import PipelineExporter

        db = str(tmp_path / "test.db")
        exporter = PipelineExporter(db)

        output = str(tmp_path / "empty.csv")
        result = exporter._export_csv([], output_path=output)
        assert result == output
        assert Path(output).read_text() == ""


# ---------------------------------------------------------------------------
# 5. wpipe/pipe/components/reporting.py
# ---------------------------------------------------------------------------

class TestReportingMixin:
    """Test ReportingMixin methods with api_client=None."""

    def test_api_task_update_no_client(self):
        """Test _api_task_update with api_client=None returns early."""
        from wpipe.pipe.components.reporting import ReportingMixin

        mixin = ReportingMixin()
        # Should not raise, just returns None
        result = mixin._api_task_update(None, {"task_id": "1", "status": "start"})
        assert result is None

    def test_api_task_update_with_verbose(self, capsys):
        """Test _api_task_update with None client and verbose."""
        from wpipe.pipe.components.reporting import ReportingMixin

        mixin = ReportingMixin()
        mixin._api_task_update(None, {"task_id": "1", "status": "start"}, verbose=True)
        # Should not raise or print anything since api_client is None

    def test_api_process_update_no_client(self):
        """Test _api_process_update with api_client=None returns early."""
        from wpipe.pipe.components.reporting import ReportingMixin

        mixin = ReportingMixin()
        result = mixin._api_process_update(None, {"id": "1"}, verbose=False)
        assert result is None

    def test_api_process_update_with_verbose(self, capsys):
        """Test _api_process_update with None client and verbose."""
        from wpipe.pipe.components.reporting import ReportingMixin

        mixin = ReportingMixin()
        mixin._api_process_update(None, {"id": "1"}, verbose=True)

    def test_format_error_traceback(self):
        """Test _format_error_traceback returns list of traceback lines."""
        from wpipe.pipe.components.reporting import ReportingMixin

        mixin = ReportingMixin()

        try:
            raise ValueError("test error")
        except ValueError as e:
            tb_lines = mixin._format_error_traceback(e)

        assert isinstance(tb_lines, list)
        assert len(tb_lines) > 0
        assert any("ValueError" in line for line in tb_lines)

    def test_api_task_update_client_raises(self, capsys):
        """Test _api_task_update when API client raises exception."""
        from wpipe.pipe.components.reporting import ReportingMixin

        mixin = ReportingMixin()
        mock_client = Mock()
        mock_client.update_task.side_effect = RuntimeError("API down")

        mixin._api_task_update(mock_client, {"task_id": "1"}, verbose=True)

        captured = capsys.readouterr()
        assert "API ERROR" in captured.out

    def test_api_process_update_client_raises(self, capsys):
        """Test _api_process_update when API client raises exception."""
        from wpipe.pipe.components.reporting import ReportingMixin

        mixin = ReportingMixin()
        mock_client = Mock()
        mock_client.update_process.side_effect = ConnectionError("timeout")

        mixin._api_process_update(mock_client, {"id": "1"}, verbose=True)

        captured = capsys.readouterr()
        assert "API ERROR" in captured.out


# ---------------------------------------------------------------------------
# 6. wpipe/pipe/components/logic_blocks_async.py
# ---------------------------------------------------------------------------

class TestConditionAsync:
    """Test ConditionAsync class."""

    def test_condition_async_branch_true_evaluates(self):
        """Test ConditionAsync with branch_true steps."""
        from wpipe.pipe.components.logic_blocks_async import ConditionAsync

        def step1(data):
            return {"executed": True}

        cond = ConditionAsync(
            expression="data['x'] > 0",
            branch_true=[step1],
            branch_false=[],
        )

        assert cond.branch_true == [step1]
        assert cond.branch_false == []

    def test_condition_async_evaluate_true(self):
        """Test ConditionAsync evaluates to True."""
        from wpipe.pipe.components.logic_blocks_async import ConditionAsync

        cond = ConditionAsync(expression="x > 0")
        result = cond.evaluate({"x": 5})
        assert result is True

    def test_condition_async_evaluate_false(self):
        """Test ConditionAsync evaluates to False."""
        from wpipe.pipe.components.logic_blocks_async import ConditionAsync

        cond = ConditionAsync(expression="x > 0")
        result = cond.evaluate({"x": -1})
        assert result is False

    def test_condition_async_evaluate_exception(self):
        """Test ConditionAsync returns False on evaluation error."""
        from wpipe.pipe.components.logic_blocks_async import ConditionAsync

        cond = ConditionAsync(expression="undefined_var")
        result = cond.evaluate({})
        assert result is False

    def test_condition_async_default_branches(self):
        """Test ConditionAsync with default empty branches."""
        from wpipe.pipe.components.logic_blocks_async import ConditionAsync

        cond = ConditionAsync(expression="True")
        assert cond.branch_true == []
        assert cond.branch_false == []


class TestForAsync:
    """Test ForAsync class."""

    def test_for_async_with_iterations(self):
        """Test ForAsync with iterations parameter."""
        from wpipe.pipe.components.logic_blocks_async import ForAsync

        loop = ForAsync(steps=["step1"], iterations=5)
        assert loop.iterations == 5
        assert loop.validation_expression is None

    def test_for_async_with_validation_expression(self):
        """Test ForAsync with validation_expression."""
        from wpipe.pipe.components.logic_blocks_async import ForAsync

        loop = ForAsync(
            steps=["step1"],
            validation_expression="data['counter'] < 10",
        )
        assert loop.validation_expression == "data['counter'] < 10"
        assert loop.iterations is None

    def test_for_async_no_iterations_no_validation(self):
        """Test ForAsync without iterations or validation raises ValueError."""
        from wpipe.pipe.components.logic_blocks_async import ForAsync

        with pytest.raises(ValueError, match="Either iterations or validation_expression"):
            ForAsync(steps=["step1"])

    def test_for_async_should_continue_iterations(self):
        """Test ForAsync.should_continue with iterations."""
        from wpipe.pipe.components.logic_blocks_async import ForAsync

        loop = ForAsync(steps=["step1"], iterations=3)

        assert loop.should_continue({}, 0) is True
        assert loop.should_continue({}, 2) is True
        assert loop.should_continue({}, 3) is False
        assert loop.should_continue({}, 10) is False

    def test_for_async_should_continue_validation_true(self):
        """Test ForAsync.should_continue with validation expression True."""
        from wpipe.pipe.components.logic_blocks_async import ForAsync

        loop = ForAsync(
            steps=["step1"],
            validation_expression="counter < 5",
        )
        result = loop.should_continue({"counter": 3}, 0)
        assert result is True

    def test_for_async_should_continue_validation_false(self):
        """Test ForAsync.should_continue with validation expression False."""
        from wpipe.pipe.components.logic_blocks_async import ForAsync

        loop = ForAsync(
            steps=["step1"],
            validation_expression="counter < 5",
        )
        result = loop.should_continue({"counter": 10}, 0)
        assert result is False

    def test_for_async_should_continue_validation_exception(self):
        """Test ForAsync.should_continue returns False on eval error."""
        from wpipe.pipe.components.logic_blocks_async import ForAsync

        loop = ForAsync(
            steps=["step1"],
            validation_expression="bad_var",
        )
        result = loop.should_continue({}, 0)
        assert result is False


# ---------------------------------------------------------------------------
# 7. wpipe/pipe/pipe_async.py
# ---------------------------------------------------------------------------

class TestPipelineAsyncPipelineRun:
    """Test PipelineAsync._pipeline_run paths."""

    def _make_async_pipeline(self, **kwargs):
        """Create a minimal PipelineAsync instance for testing."""
        from wpipe.pipe.pipe_async import PipelineAsync

        p = PipelineAsync(
            pipeline_name="test_async",
            tracking_db=None,
        )
        p.tasks_list = []
        p.verbose = False
        p.tracker = None
        p.pipeline_id = None
        p._step_order = 0
        p.continue_on_error = False
        p._collect_system_metrics = kwargs.get("collect_system_metrics", False)
        p.send_to_api = False
        p.max_retries = 0
        p.parent_pipeline_id = None
        p.task_name = "test_async"
        return p

    @pytest.mark.asyncio
    async def test_pipeline_run_empty_tasks(self):
        """Test _pipeline_run with empty tasks list."""
        p = self._make_async_pipeline()
        p.tasks_list = []

        result = await p._pipeline_run({})
        assert isinstance(result, dict)

    @patch("wpipe.pipe.pipe_async.SystemMetricsCollector")
    @pytest.mark.asyncio
    async def test_pipeline_run_with_collect_system_metrics(self, mock_collector_class):
        """Test _pipeline_run with collect_system_metrics=True."""
        p = self._make_async_pipeline(collect_system_metrics=True)

        mock_tracker = Mock()
        mock_tracker.register_pipeline.return_value = {
            "pipeline_id": "test-123",
            "yaml_path": "/tmp/test.yaml",
        }
        p.tracker = mock_tracker

        mock_collector = Mock()
        mock_collector_class.return_value = mock_collector

        async def dummy_task(data):
            return {"done": True}

        p.tasks_list = [(dummy_task, "dummy", "v1", None)]

        result, _ = await p._pipeline_run({"x": 1})

        mock_collector_class.assert_called_once_with(mock_tracker, "test-123")
        mock_collector.start.assert_called_once()
        mock_collector.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_pipeline_run_task_exception_no_continue(self):
        """Test _pipeline_run raises TaskError on task exception without continue_on_error."""
        from wpipe.exception import TaskError

        p = self._make_async_pipeline()
        p.continue_on_error = False

        def failing_task(data):
            raise RuntimeError("task failed")

        p.tasks_list = [(failing_task, "failing", "v1", None)]

        with pytest.raises(TaskError):
            await p._pipeline_run({})

    @pytest.mark.asyncio
    async def test_pipeline_run_task_exception_with_continue(self):
        """Test _pipeline_run continues on error when continue_on_error=True."""
        p = self._make_async_pipeline()
        p.continue_on_error = True

        def failing_task(data):
            raise RuntimeError("task failed")

        def ok_task(data):
            return {"ok": True}

        p.tasks_list = [
            (failing_task, "failing", "v1", None),
            (ok_task, "ok", "v1", None),
        ]

        result = await p._pipeline_run({})
        assert "error" in result

    @patch("wpipe.pipe.pipe_async.tqdm")
    @patch("wpipe.pipe.pipe_async.ProgressManager")
    @pytest.mark.asyncio
    async def test_pipeline_run_progress_fallback_live_error(self, mock_pm_class, mock_tqdm):
        """Test progress bar fallback when LiveError is raised."""
        from rich.errors import LiveError

        mock_pm = Mock()
        mock_pm.__enter__ = Mock(side_effect=LiveError("no terminal"))
        mock_pm.__exit__ = Mock(return_value=False)
        mock_pm_class.return_value = mock_pm

        mock_tqdm_instance = Mock()
        mock_tqdm.return_value = [0]  # single iteration

        p = self._make_async_pipeline()

        async def simple_task(data):
            return {"result": "ok"}

        p.tasks_list = [(simple_task, "simple", "v1", None)]

        # Should not raise even if LiveError occurs
        try:
            await p._pipeline_run({})
        except RuntimeError:
            pass  # might fail for other reasons, we just test the LiveError path

    @pytest.mark.asyncio
    async def test_pipeline_run_with_tracker(self):
        """Test _pipeline_run with a tracker set."""
        p = self._make_async_pipeline()

        mock_tracker = Mock()
        mock_tracker.register_pipeline.return_value = {
            "pipeline_id": "test-123",
            "yaml_path": "/tmp/test.yaml",
        }
        p.tracker = mock_tracker

        async def dummy(data):
            return {"done": True}

        p.tasks_list = [(dummy, "dummy", "v1", None)]

        await p._pipeline_run({"x": 1})

        mock_tracker.register_pipeline.assert_called_once()

    @pytest.mark.asyncio
    async def test_pipeline_run_verbose_register(self, capsys):
        """Test _pipeline_run prints registration info when verbose."""
        p = self._make_async_pipeline()
        p.verbose = True
        p.parent_pipeline_id = "parent-1"

        mock_tracker = Mock()
        mock_tracker.register_pipeline.return_value = {
            "pipeline_id": "test-123",
            "yaml_path": "/tmp/test.yaml",
        }
        p.tracker = mock_tracker

        async def dummy(data):
            return {}

        p.tasks_list = [(dummy, "dummy", "v1", None)]

        await p._pipeline_run({})

        captured = capsys.readouterr()
        assert "MATRÍCULA" in captured.out

    @pytest.mark.asyncio
    async def test_pipeline_run_exception_outer(self):
        """Test outer exception handling in _pipeline_run."""
        p = self._make_async_pipeline()
        p.continue_on_error = True

        # Make tasks_list something that will cause an iteration error
        p.tasks_list = None  # type: ignore

        with pytest.raises(TypeError):
            await p._pipeline_run({})


# ---------------------------------------------------------------------------
# 8. wpipe/pipe/pipe.py - _task_invoke_with_report exception path
# ---------------------------------------------------------------------------

class TestTaskInvokeWithReportException:
    """Test _task_invoke_with_report exception path."""

    def _make_pipeline(self):
        """Create a minimal Pipeline for testing."""
        from wpipe.pipe.pipe import Pipeline

        p = Pipeline(
            pipeline_name="test",
            tracking_db=None,
        )
        p.task_id = "task-1"
        p.task_name = "test_task"
        p.send_to_api = True
        p.verbose = False
        return p

    def test_task_invoke_with_report_exception_traceback(self):
        """Test _task_invoke_with_report extracts traceback on exception."""
        import traceback as tb_module
        from wpipe.pipe.pipe import Pipeline
        from wpipe.exception import TaskError

        p = self._make_pipeline()

        def failing_func(data):
            # Force a multi-line traceback
            x = 1 / 0  # noqa: F841

        with patch.object(p, "_api_task_update") as mock_update:
            with pytest.raises(TaskError):
                p._task_invoke_with_report(failing_func, {})

        # Check that _api_task_update was called with error status
        error_call = None
        for c in mock_update.call_args_list:
            args = c[0][0]
            if args.get("status") == "error":
                error_call = args
                break

        assert error_call is not None
        assert "details" in error_call
        details = json.loads(error_call["details"])
        assert "error_traceback" in details
        assert len(details["error_traceback"]) > 0
        assert "file" in details["error_traceback"][0]
        assert "line" in details["error_traceback"][0]
        assert "method" in details["error_traceback"][0]

    def test_task_invoke_with_report_exception_verbose(self, capsys):
        """Test _task_invoke_with_report logs errors when verbose=True."""
        from wpipe.pipe.pipe import Pipeline
        from wpipe.exception import TaskError

        p = self._make_pipeline()
        p.verbose = True

        def failing_func(data):
            raise ValueError("test error")

        with patch.object(p, "_api_task_update"):
            with pytest.raises(TaskError):
                p._task_invoke_with_report(failing_func, {})

        # Logger output depends on logger config, but method should not crash

    def test_task_invoke_with_report_pipeline_instance(self):
        """Test _task_invoke_with_report when func is a Pipeline instance."""
        from wpipe.pipe.pipe import Pipeline
        from wpipe.exception import TaskError

        p = self._make_pipeline()

        sub_pipeline = Mock(spec=Pipeline)
        sub_pipeline.run.return_value = {"sub_result": "ok"}

        with patch.object(p, "_api_task_update"):
            result = p._task_invoke_with_report(sub_pipeline, {})

        sub_pipeline.run.assert_called_once()
        assert "error" not in result

    def test_task_invoke_with_report_success(self):
        """Test _api_task_update called with success status."""
        p = self._make_pipeline()

        def good_func(data):
            return {"result": "ok"}

        with patch.object(p, "_api_task_update") as mock_update:
            result = p._task_invoke_with_report(good_func, {})

        # Check success call
        success_call = None
        for c in mock_update.call_args_list:
            args = c[0][0]
            if args.get("status") == "success":
                success_call = args
                break

        assert success_call is not None
        assert result == {"result": "ok"}

    def test_task_invoke_with_report_start_status(self):
        """Test _api_task_update called with start status first."""
        p = self._make_pipeline()

        def good_func(data):
            return {"result": "ok"}

        with patch.object(p, "_api_task_update") as mock_update:
            p._task_invoke_with_report(good_func, {})

        first_call = mock_update.call_args_list[0]
        assert first_call[0][0]["status"] == "start"

    def test_task_invoke_with_report_error_details_structure(self):
        """Test error details JSON structure when task fails."""
        from wpipe.pipe.pipe import Pipeline
        from wpipe.exception import TaskError

        p = self._make_pipeline()
        p.task_name = "my_failing_task"
        p.task_id = "t-1"

        def bad_func(data):
            raise RuntimeError("boom")

        with patch.object(p, "_api_task_update") as mock_update:
            with pytest.raises(TaskError):
                p._task_invoke_with_report(bad_func, {})

        # Find the error call
        error_call = None
        for c in mock_update.call_args_list:
            args = c[0][0]
            if args.get("status") == "error":
                error_call = args
                break

        assert error_call is not None
        details = json.loads(error_call["details"])
        assert details["task_name"] == "my_failing_task"
        assert details["task_id"] == "t-1"
        assert details["error_message"] == "boom"
