import os
import csv
from datetime import datetime
from wpipe import Pipeline, step, Parallel, PipelineContext

# Define a custom context for our marketing pipeline
class MarketingContext(PipelineContext):
    def __init__(self, row):
        super().__init__()
        self.file_name = row['Archivo']
        self.platform = row['Plataforma']
        self.target_date = row['Fecha Sugerida']
        self.status = "Pending"
        self.content = ""

@step(name="Validate_Content", version="v1.0", retry_count=2)
def validate_content(context: MarketingContext):
    """Checks if the poster file exists and is high quality."""
    file_path = os.path.join("posters", context.file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Poster {context.file_name} not found.")
    
    with open(file_path, 'r') as f:
        content = f.read()
        if "WPipe implements a robust execution model" in content and content.count("WPipe implements") > 3:
            raise ValueError(f"File {context.file_name} contains repetitive garbage text.")
        context.content = content
    
    print(f"[VALIDATED] {context.file_name} for {context.platform}")
    return context

@step(name="Format_for_Platform", version="v1.0")
def format_content(context: MarketingContext):
    """Adapts content (titles, hashtags) based on the target platform."""
    # Placeholder for actual formatting logic (e.g., stripping markdown for LinkedIn)
    context.status = "Ready"
    return context

@step(name="Simulate_Publication", version="v1.0")
def publish_simulation(context: MarketingContext):
    """Simulates the API call to LinkedIn/Medium/etc."""
    today = datetime.now().strftime("%Y-%m-%d")
    if context.target_date <= today:
        print(f"🚀 [PUBLISHING NOW] {context.file_name} to {context.platform}")
        context.status = "Published"
    else:
        print(f"🕒 [SCHEDULED] {context.file_name} is set for {context.target_date}")
        context.status = "Scheduled"
    return context

def main():
    print("--- wpipe Marketing Orchestration Engine ---")
    
    # Initialize the Pipeline
    marketing_pipe = Pipeline(
        pipeline_name="wpipe_Massive_Marketing",
        verbose=False,
        tracking_db="posters/marketing_tracking.db"
    )

    # Define steps: Validation -> Formatting -> Simulated Publish
    marketing_pipe.set_steps([
        validate_content,
        format_content,
        publish_simulation
    ])

    # Read the publication map
    with open('posters/publication_map.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # We use a list to store contexts for parallel execution
        tasks = [MarketingContext(row) for row in reader if row['Archivo'].endswith('.md')]

    print(f"Loaded {len(tasks)} publication tasks.")

    # Run in parallel to demonstrate wpipe performance
    # In a real scenario, you'd run this daily via Cron (ironically) or wpipe itself
    for task_ctx in tasks[:10]: # Demoing with the first 10 for safety
        marketing_pipe.run(task_ctx.__dict__)

    print("\n--- Orchestration Complete. Check posters/marketing_tracking.db for full logs. ---")

if __name__ == "__main__":
    main()
