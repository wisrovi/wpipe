"""
02 Retry - Success After Retries

Shows a function that succeeds after a few failed attempts.
"""

from wpipe import Pipeline


class FlakyStep:
    def __init__(self, fail_count=2):
        self.attempts = 0
        self.fail_count = fail_count

    def __call__(self, data):
        self.attempts += 1
        if self.attempts <= self.fail_count:
            raise ConnectionError(f"Attempt {self.attempts} failed")
        return {"success": True, "attempts": self.attempts}


def main():
    pipeline = Pipeline(max_retries=3, retry_delay=0.1, verbose=True)

    pipeline.set_steps(
        [
            (FlakyStep(fail_count=2), "Flaky Step", "v1.0"),
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
