from wpipe import Pipeline, ResourceMonitor, TaskTimer
from wpipe.exception.api_error import ProcessError

db_path = 'output/tracking.db'  # Path to tracking database for to save metrics, events, alerts and execution history (with error capture)
config_dir = 'configs',  # Optional directory for pipeline configuration files (e.g., YAML or JSON)

pipeline = Pipeline(
    pipeline_name='professional_pipeline',
    pipeline_version='1.0.0',

    tracking_db=db_path,  # for to forencically capture errors, track events, alerts and execution history
    config_dir=config_dir,

    verbose=False, # Toggle detailed logging for debugging and monitoring

    # Retry configuration
    max_retries=3,
    retry_delay=0.5,
    retry_on_exceptions=(RuntimeError,),
    # Monitoring
    collect_system_metrics=True,  # Automatically collect CPU, RAM, and execution time metrics

    show_progress=True,  # Display a progress bar during pipeline execution
)

pipeline.set_steps([
    step_1
])

if __name__ == "__main__":
    try:
        with ResourceMonitor('<project_name>_pipeline_ResourceMonitor') as monitor:
            with TaskTimer('<project_name>_pipeline_TaskTimer', timeout_seconds=900) as timer:
                result = pipeline.run(initial_data)
                
                if timer.exceeded_timeout():
                   # print('⚠ Work exceeded timeout!')
                    pass
                else:
                    # print('✓ Work completed within timeout')
                    pass
                
        summary = monitor.get_summary()
        print(f'  - Peak RAM: {summary['peak_ram_mb']} MB')
        print(f'  - Avg CPU: {summary['avg_cpu_percent']}%')
        print(f'✓ Total time monitored: {timer.elapsed_seconds:.2f}s')
    except ProcessError as e:
        print(f"Error occurred: {e}")