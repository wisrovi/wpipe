"""
Phase 2 Performance Benchmarking Suite.

Comprehensive benchmarks for parallel execution, composition, and decorators.
Measures speedup, memory usage, and execution timing across different scenarios.
"""

import time

from wpipe import Pipeline
from wpipe.composition import NestedPipelineStep
from wpipe.decorators import AutoRegister, clear_registry, get_step_registry, step
from wpipe.parallel import ExecutionMode, ParallelExecutor


def benchmark_io_parallelism():
    """Benchmark I/O-bound parallel execution."""
    print("\n📊 I/O PARALLELISM BENCHMARK")
    print("-" * 50)

    def io_task(context):
        time.sleep(0.5)
        return {}

    # Sequential
    executor_seq = ParallelExecutor(max_workers=1)
    for i in range(4):
        executor_seq.add_step(f"task_{i}", io_task, mode=ExecutionMode.SEQUENTIAL)

    start = time.time()
    executor_seq.execute({})
    seq_time = time.time() - start
    print(f"Sequential (4x 0.5s): {seq_time:.2f}s")

    # Parallel
    executor_par = ParallelExecutor(max_workers=4)
    for i in range(4):
        executor_par.add_step(f"task_{i}", io_task, mode=ExecutionMode.IO_BOUND)

    start = time.time()
    executor_par.execute({})
    par_time = time.time() - start
    print(f"Parallel (4x 0.5s):   {par_time:.2f}s")
    print(f"✓ Speedup: {seq_time/par_time:.1f}x")


def benchmark_composition():
    """Benchmark composition overhead."""
    print("\n📊 COMPOSITION OVERHEAD BENCHMARK")
    print("-" * 50)

    # Direct
    p_direct = Pipeline()
    p_direct.add_state("step_1", lambda c: {"x": 1})
    p_direct.add_state("step_2", lambda c: {"x": c.get("x", 0) + 1})

    start = time.time()
    for _ in range(100):
        p_direct.run({})
    direct_time = time.time() - start
    print(f"Direct pipeline (100 runs): {direct_time:.3f}s")

    # Nested
    sub = Pipeline()
    sub.add_state("sub_step", lambda c: {"x": c.get("x", 0) + 1})

    main = Pipeline()
    main.add_state("step_1", lambda c: {"x": 1})
    nested = NestedPipelineStep("nested", sub)
    main.add_state("nested", lambda c: nested.run(c))

    start = time.time()
    for _ in range(100):
        main.run({})
    nested_time = time.time() - start
    print(f"Nested composition (100 runs): {nested_time:.3f}s")
    print(f"✓ Overhead: {((nested_time/direct_time - 1) * 100):.1f}%")


def benchmark_decorators():
    """Benchmark decorator registration."""
    print("\n📊 DECORATOR PERFORMANCE BENCHMARK")
    print("-" * 50)

    clear_registry()

    # Create decorated steps
    for i in range(10):

        @step(name=f"step_{i}", tags=["bench"])
        def step_fn(context, _i=i):
            return {"result": _i * 2}

    p = Pipeline()
    registry = get_step_registry()
    AutoRegister.register_all(p, registry)

    start = time.time()
    for _ in range(100):
        p.run({})
    deco_time = time.time() - start
    print(f"10-step decorated pipeline (100 runs): {deco_time:.3f}s")
    print(f"✓ Per-step overhead: {(deco_time/100/10)*1000:.2f}ms")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("PHASE 2 PERFORMANCE BENCHMARKS")
    print("=" * 50)

    benchmark_io_parallelism()
    benchmark_composition()
    benchmark_decorators()

    print("\n" + "=" * 50)
    print("✓ All benchmarks complete")
    print("=" * 50 + "\n")
