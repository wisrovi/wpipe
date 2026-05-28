from state1 import StepClass
from state2 import function_name
from state4 import StepClass2
from state3 import StepClass3
from state5 import function_name5
from state6 import function_name6
from state7 import slow_step
from state8 import AdvancedStep8
from state_pipe import pipe_2
from state9 import AdvancedStep
from error_capture import error_capture

from wpipe import Pipeline, Condition, For, Parallel
from wpipe.exception.api_error import ProcessError

from wpipe.pipe.components.logic_blocks import Background
import os

pipeline = Pipeline(
    pipeline_name="my_pipeline",
    tracking_db="output/tracking.db",
    verbose=True,
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
                StepClass2(),
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
                AdvancedStep(),
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

pipeline.add_error_capture([error_capture])


if __name__ == "__main__":
    try:
        result = pipeline.run({})
    except ProcessError as e:
        print(f"Error occurred: {e}")
