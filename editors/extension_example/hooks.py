import time


# 1. Define a Pre-Hook: Runs BEFORE each step
def audit_pre_hook(context, step_info):
    """
    Log start time and inject common metadata.
    """
    print(
        f"\n[AUDIT] 🚀 Starting step: {step_info['name']} (Type: {step_info['step_type']})"
    )

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

    print(
        f"[AUDIT] {result_str} | Step: {step_info['name']} | Duration: {duration:.4f}s"
    )

    context["audit_log"].append(f"End {step_info['name']} with {status}")
