from wpipe_steps.database.redis.hash import RedisHashReadSync
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

from wpipe import Pipeline, Condition, For, Parallel
from wpipe.exception.api_error import ProcessError

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
            iterations=10,
            validation_expression="status != 'error'",
            steps=[
                function_name5,
                Parallel(
                    steps=[
                        function_name5,
                        function_name6,
                    ],
                    max_workers=1,
                ),
                AdvancedStep9(),
                For(
                    iterations=10,
                    validation_expression="status != 'error'",
                    steps=[AdvancedStep8(), function_name5],
                ),
            ],
        ),
        Parallel(
            steps=[
                function_name5,
                pipe_2,
            ],
            max_workers=2,
        ),
        Background(slow_step),
    ]
)

pipeline.add_state(StepClass10())
pipeline.add_state(function_name11)


pipeline.add_state(RedisHashReadSync(host="localhost", port=6379))

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
        result = pipeline.run(initial_data)
    except ProcessError as e:
        print(f"Error occurred: {e}")
