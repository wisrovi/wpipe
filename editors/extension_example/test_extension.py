from wpipe_steps.database.redis.hash.read_hash_sync import RedisHashReadSync
from state1 import StepClass
from state2 import function_name
from state4 import StepClass4
from state3 import StepClass3
from state5 import function_name5
from state6 import function_name6
from state7 import slow_step
from state8 import AdvancedStep8
from state_pipe import pipe_2
from state9 import AdvancedStep9
from error_capture import error_capture
from state10 import StepClass10
from state11 import function_name11
from states import State12, State13

from wpipe import Pipeline, Condition, For, Parallel, ResourceMonitor, TaskTimer
from wpipe.exception.api_error import ProcessError
from wpipe.sqlite import Wsqlite

from wpipe.pipe.components.logic_blocks import Background
import os

pipeline = Pipeline(
    pipeline_name="my_pipeline",
    tracking_db="output/tracking.db",
    verbose=False,
    collect_system_metrics=True,
)

pipeline.set_steps(
    [
        StepClass(),
        function_name,
        Condition(
            expression="valor > 100",
            branch_true=[
                function_name,
                StepClass4(),
            ],
            branch_false=[
                StepClass3(),
            ],
        ),
        For(
            validation_expression="status != 'error'",
            steps=[
                Parallel(
                    steps=[
                        function_name5,
                        function_name6,
                    ],
                    max_workers=1,
                ),
                AdvancedStep9(),
            ],
        ),
        For(
            iterations=10,
            steps=[
                AdvancedStep8(),
                State13(config="custom_config"),
            ],
        ),
        Parallel(
            steps=[
                State12(config="custom_value"),
                pipe_2,
            ],
            max_workers=2,
        ),
        Background(slow_step),
        RedisHashReadSync(host="localhost", port=6379),
        function_name11,
    ]
)

pipeline.add_state(StepClass10())


pipeline.add_error_capture([error_capture])


if __name__ == "__main__":
    try:
        # Provide data for logic branches and the Redis step
        initial_data = {
            "valor": 150,
            "hash_name": "test_hash",
            "key": "test_key",
            "field": "test_field",  # For StepClass10
        }

        with ResourceMonitor("test_pipeline_ResourceMonitor") as monitor:
            with TaskTimer("test_pipeline_TaskTimer", timeout_seconds=900) as timer:
                with Wsqlite(db_name="output/test_Wsqlite.db") as db:
                    db.input = initial_data
                    print(f"Input set, record UUID: {db.record_uuid}")
                    result = pipeline.run(initial_data)

                    db.output = result
                    print(f"Output set, record UUID: {db.record_uuid}")
                    print(f"Total records: {db.count_records()}")

                    db.details = {
                        "monitoring_summary": monitor.get_summary(),
                        "task_time_seconds": timer.elapsed_seconds,
                    }

                    db.error = {
                        "there_were_errors": monitor.get_summary().get(
                            "total_errors", 0
                        )
                        > 0,
                    }

                    if timer.exceeded_timeout():
                        # print("⚠ Work exceeded timeout!")
                        pass
                    else:
                        # print("✓ Work completed within timeout")
                        pass

        summary = monitor.get_summary()
        print(f"  - Peak RAM: {summary['peak_ram_mb']} MB")
        print(f"  - Avg CPU: {summary['avg_cpu_percent']}%")
        print(f"✓ Total time monitored: {timer.elapsed_seconds:.2f}s")

    except ProcessError as e:
        print(f"Error occurred: {e}")
