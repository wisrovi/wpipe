"""
Example 25: Using Global Hooks (Middlewares) in WPipe.

Hooks allow you to execute logic across ALL steps of your pipeline without
modifying the step functions themselves.

Use cases:
- Global logging/auditing
- Context enrichment (injecting data)
- Monitoring performance
- Resource cleanup
"""

import time
from wpipe import Pipeline, step

# 1. Define a Pre-Hook: Runs BEFORE each step
def audit_pre_hook(context, step_info):
    """
    Log start time and inject common metadata.
    """
    print(f"\n[AUDIT] 🚀 Starting step: {step_info['name']} (Type: {step_info['step_type']})")
    
    # We can inject data into the context that will be available to the step
    context["_global_start_ts"] = time.time()
    
    if "audit_log" not in context:
        context["audit_log"] = []
    
    context["audit_log"].append(f"Start {step_info['name']}")

# 2. Define a Post-Hook: Runs AFTER each step
def audit_post_hook(context, step_info, status):
    """
    Calculate duration and log completion status.
    """
    start_ts = context.get("_global_start_ts", time.time())
    duration = time.time() - start_ts
    
    # status will be "success" or an Exception object if it failed
    result_str = "✅ SUCCESS" if status == "success" else f"❌ FAILED: {status}"
    
    print(f"[AUDIT] {result_str} | Step: {step_info['name']} | Duration: {duration:.4f}s")
    
    context["audit_log"].append(f"End {step_info['name']} with {status}")

# 3. Define some normal steps
@step(name="extract_data")
def extract(context):
    print("   Extracting data...")
    time.sleep(0.1)
    return {"raw_data": [1, 2, 3]}

@step(name="transform_data")
def transform(context):
    print("   Transforming data...")
    data = context.get("raw_data", [])
    return {"processed_data": [x * 2 for x in data]}

def main():
    # Create the pipeline
    p = Pipeline(pipeline_name="Hooks Demo Pipeline")
    
    # REGISTER THE HOOKS
    p.add_pre_hook(audit_pre_hook)
    p.add_post_hook(audit_post_hook)
    
    # Set the execution flow
    p.set_steps([
        extract,
        transform
    ])
    
    print("--- Starting Pipeline Execution ---")
    result = p.run({})
    print("\n--- Pipeline Finished ---")
    
    print("\nFinal Audit Log stored in context:")
    for entry in result.get("audit_log", []):
        print(f"  - {entry}")

if __name__ == "__main__":
    main()
