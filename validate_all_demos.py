import os
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

def run_demo(filename):
    path = os.path.join("examples/00_honey_pot/03_yield/", filename)
    try:
        # Run with a 10s timeout to prevent hanging
        res = subprocess.run(["python3", filename], cwd="examples/00_honey_pot/03_yield/", capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            return filename, True, ""
        else:
            return filename, False, res.stderr
    except subprocess.TimeoutExpired:
        return filename, False, "TIMEOUT (15s)"
    except Exception as e:
        return filename, False, str(e)

def main():
    demos = sorted([f for f in os.listdir("examples/00_honey_pot/03_yield/") if f.startswith("demo_level") and f.endswith(".py")],
                   key=lambda x: int(re.search(r'(\d+)', x).group(1)))
    
    print(f"Testing {len(demos)} demos...")
    
    # We use sequential execution here to avoid database locks since many write to the same output files
    results = []
    for demo in demos:
        print(f"Running {demo}...", end="\r")
        results.append(run_demo(demo))
    
    failed = [r for r in results if not r[1]]
    
    print("\n\n" + "="*50)
    print(f"VALIDATION SUMMARY")
    print(f"Total:  {len(results)}")
    print(f"Passed: {len(results) - len(failed)}")
    print(f"Failed: {len(failed)}")
    print("="*50)
    
    if failed:
        print("\nFAILED DEMOS:")
        for name, _, err in failed:
            print(f"- {name}: {err.strip().splitlines()[-1] if err.strip() else 'Unknown error'}")
        exit(1)
    else:
        print("\n✅ All demos passed successfully!")

if __name__ == "__main__":
    main()
