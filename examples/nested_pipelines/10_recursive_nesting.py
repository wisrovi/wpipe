"""
10 Nested Pipelines - Recursive Nesting

Shows recursive pipeline structure.
"""

from wpipe import Pipeline


def process(data):
    return {"processed": True}


def main():
    p1 = Pipeline(verbose=False)
    p1.set_steps([(process, "P1", "v1.0")])

    p2 = Pipeline(verbose=False)
    p2.set_steps([(p1.run, "P1 nested", "v1.0")])

    p3 = Pipeline(verbose=True)
    p3.set_steps([(p2.run, "P2 nested", "v1.0")])

    result = p3.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
