🔄 ONE PIPELINE, TWO WORLDS: SYNC AND ASYNC

Many libraries force you to choose: build a sync orchestrator or an async one, and migrating between them means rewriting everything.

With wpipe that decision doesn't exist: you have Pipeline and PipelineAsync with 100% of the same features. What you learn in one, you apply in the other.

⚡ A REAL EXAMPLE, IN UNDER 20 LINES

Define fetch and process as async steps, compose them into a PipelineAsync, and await the run. I/O-bound work (network, API, files) never blocks the event loop.

🎯 WHY IT MATTERS IN 2026

1. Same mental model: checkpoints, retries, alerts, and tracker work identically in both.
2. I/O bound: network, API, and file tasks run without blocking the event loop.
3. Zero rewrites: switch Pipeline for PipelineAsync and your flow keeps its structure.

Sync/async parity isn't a luxury, it's the difference between an orchestrator that accompanies you and a tool that forces you to bend.

👇 Does your team already use asyncio in production? How do you orchestrate those flows today?

#Python #Async #SoftwareEngineering #wpipe #Backend #DataPipelines
