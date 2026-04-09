"""Minimal PipelineAsync for Phase 1."""
import asyncio
from .pipe import Pipeline

class PipelineAsync(Pipeline):
    """Async wrapper for Pipeline."""
    async def run(self, *args, **kwargs):
        """Run async pipeline."""
        return await asyncio.get_event_loop().run_in_executor(None, super().run, *args)
