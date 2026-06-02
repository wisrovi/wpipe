"""
Example 25b: Asynchronous Global Hooks in WPipe.

WPipe supports both synchronous and asynchronous hooks for PipelineAsync.
"""

import asyncio
import time
from wpipe import PipelineAsync, step

# Async Pre-Hook
async def async_pre_hook(context, step_info):
    print(f"\n[ASYNC HOOK] ⏳ Preparing for: {step_info['name']}")
    await asyncio.sleep(0.05) # Simulate async I/O (e.g., checking a remote config)
    context["async_ready"] = True

# Async Post-Hook
async def async_post_hook(context, step_info, status):
    print(f"[ASYNC HOOK] 🏁 Cleaned up after: {step_info['name']}")
    await asyncio.sleep(0.05)

@step(name="fetch_api")
async def fetch(context):
    print(f"   Fetching data (Async Ready: {context.get('async_ready')})")
    await asyncio.sleep(0.1)
    return {"api_result": "Success"}

async def main():
    # Create Async Pipeline
    p = PipelineAsync(pipeline_name="Async Hooks Demo")
    
    # Register Async Hooks
    p.add_pre_hook(async_pre_hook)
    p.add_post_hook(async_post_hook)
    
    p.set_steps([fetch])
    
    print("--- Starting Async Pipeline ---")
    await p.run({})
    print("--- Async Pipeline Finished ---")

if __name__ == "__main__":
    asyncio.run(main())
