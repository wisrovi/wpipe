"""
Tests for nested pipeline functionality.

Note: These tests have known issues with the current Pipeline implementation.
The nested pipelines don't work correctly due to a bug in Pipeline.run().
Tests are marked as skipped until the bug is fixed.
"""

from wpipe.pipe import Pipeline


class TestNestedPipelines:
    """Test nested pipeline execution."""

    def test_nested_single_pipeline(self):
        """Test nesting a single pipeline as a step."""
        sub_pipeline = Pipeline()
        sub_pipeline.set_steps(
            [
                (lambda d: {"step1": True}, "SubStep1", "v1.0"),
                (lambda d: {"from_sub": True}, "SubStep2", "v1.0"),
            ]
        )

        main_pipeline = Pipeline()
        main_pipeline.set_steps(
            [
                (lambda d: {"main_before": True}, "MainBefore", "v1.0"),
                (sub_pipeline.run, "NestedPipeline", "v1.0"),
                (lambda d: {"main_after": True}, "MainAfter", "v1.0"),
            ]
        )

        result = main_pipeline.run({})
        assert "from_sub" in result
        assert "main_before" in result
        assert "main_after" in result

    def test_nested_multiple_pipelines(self):
        """Test nesting multiple pipelines."""
        pipeline1 = Pipeline()
        pipeline1.set_steps(
            [
                (lambda d: {"step1a": True}, "Step1A", "v1.0"),
                (lambda d: {"step1_done": True}, "Step1B", "v1.0"),
            ]
        )

        pipeline2 = Pipeline()
        pipeline2.set_steps(
            [
                (lambda d: {"step2a": True}, "Step2A", "v1.0"),
                (lambda d: {"step2_done": True}, "Step2B", "v1.0"),
            ]
        )

        main_pipeline = Pipeline()
        main_pipeline.set_steps(
            [
                (pipeline1.run, "Nested1", "v1.0"),
                (pipeline2.run, "Nested2", "v1.0"),
                (lambda d: {"final": True}, "Final", "v1.0"),
            ]
        )

        result = main_pipeline.run({})
        assert "step1_done" in result
        assert "step2_done" in result
        assert "final" in result

    def test_nested_pipeline_with_data_flow(self):
        """Test data flows correctly through nested pipelines."""
        sub_pipeline = Pipeline()
        sub_pipeline.set_steps(
            [
                (lambda d: {"intermediate": d.get("x", 0) * 2}, "Process1", "v1.0"),
                (lambda d: {"processed": d.get("intermediate", 0)}, "Process2", "v1.0"),
            ]
        )

        main_pipeline = Pipeline()
        main_pipeline.set_steps(
            [
                (lambda d: {"init": True}, "Init", "v1.0"),
                (sub_pipeline.run, "ProcessData", "v1.0"),
                (lambda d: {"final": d.get("processed", 0) + 10}, "Finalize", "v1.0"),
            ]
        )

        result = main_pipeline.run({"x": 5})
        assert result["processed"] == 10
        assert result["final"] == 20

    def test_nested_pipeline_with_functions(self):
        """Test mixing nested pipelines with regular functions."""
        sub_pipeline = Pipeline()
        sub_pipeline.set_steps(
            [
                (lambda d: {"nested_step1": True}, "NestedStep1", "v1.0"),
                (lambda d: {"nested_result": True}, "NestedStep2", "v1.0"),
            ]
        )

        main_pipeline = Pipeline()
        main_pipeline.set_steps(
            [
                (lambda d: {"before_nested": True}, "Before", "v1.0"),
                (sub_pipeline.run, "NestedPipeline", "v1.0"),
                (lambda d: {"after_nested": True}, "After", "v1.0"),
            ]
        )

        result = main_pipeline.run({})
        assert "before_nested" in result
        assert "nested_result" in result
        assert "after_nested" in result
