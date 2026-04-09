"""
Parallel CPU-bound tasks example.

Demonstrates executing multiple CPU-bound tasks (like calculations) in parallel
using ProcessPoolExecutor to bypass Python's GIL.
"""

import time
import math
from wpipe.parallel import ParallelExecutor, ExecutionMode


def calculate_fibonacci(context):
    """CPU-bound: Calculate fibonacci series."""
    print("[Fibonacci] Starting calculation...")
    result = sum(1 for _ in range(35000000))
    print("[Fibonacci] ✓ Completed")
    return {"fib_result": result}


def calculate_primes(context):
    """CPU-bound: Count prime numbers."""
    print("[Primes] Starting calculation...")
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    count = sum(1 for n in range(2, 100000) if is_prime(n))
    print("[Primes] ✓ Completed")
    return {"prime_count": count}


def calculate_matrix(context):
    """CPU-bound: Matrix operations."""
    print("[Matrix] Starting calculation...")
    matrix = [[sum(i * j for i in range(100)) for j in range(100)] for _ in range(100)]
    print("[Matrix] ✓ Completed")
    return {"matrix_ops": len(matrix)}


def summarize_results(context):
    """Summarize all calculations."""
    print("[Summarize] Aggregating results...")
    return {
        "calculations_done": 3,
        "status": "complete",
        "fib": context.get("fib_result", 0),
        "primes": context.get("prime_count", 0),
    }


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PARALLEL CPU-BOUND TASKS EXAMPLE")
    print("=" * 60)
    
    executor = ParallelExecutor(max_workers=3)
    
    executor.add_step("calc_fib", calculate_fibonacci, mode=ExecutionMode.CPU_BOUND)
    executor.add_step("calc_primes", calculate_primes, mode=ExecutionMode.CPU_BOUND)
    executor.add_step("calc_matrix", calculate_matrix, mode=ExecutionMode.CPU_BOUND)
    executor.add_step("summarize", summarize_results, depends_on=["calc_fib", "calc_primes", "calc_matrix"])
    
    start = time.time()
    result = executor.execute({})
    elapsed = time.time() - start
    
    print("\n✓ Results:")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  Calculations completed: {result.get('calculations_done', 0)}")
    print("=" * 60 + "\n")
