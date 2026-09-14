# Contract-First Pipelines: Agree on the Data Before You Write a Step

## The Integration Ambiguity

Every pipeline failure second-guessed with "maybe the schema changed" is a pipeline that lacked a contract. When step A produces a dict and step B silently assumes a shape, drift causes subtle breakage: wrong types, missing keys, silent `None`s propagating through three transforms before surfacing.

Contract-first flips the order: **define the data contract explicitly, then let the orchestrator enforce it.**

## What a Contract Gives You

- **Explicit interfaces**: each step declares the fields it expects and produces.
- **Fail-fast validation**: a shape mismatch stops the run at the step that causes it — not three steps later.
- **Self-documenting schemas**: the contracts *are* the pipeline's interface documentation.
- **Safety under evolution**: versioned contracts make breaking changes visible.

## Contracts in wpipe

wpipe's typed context (`PipelineContext`) treats the data passed between steps as a structured, inspectable object — the natural place for contract enforcement to live.

```python
from wpipe import Pipeline, step

@step(name="ingest", retry_count=2)
def ingest(data):
    # Contract: produces {"account_id": str, "amount": float}
    return {"account_id": data["id"], "amount": float(data["amount"])}

@step(name="charge", retry_count=3, retry_delay=1)
def charge(data):
    # Contract: consumes {"account_id": str, "amount": float}
    assert isinstance(data["account_id"], str)
    assert data["amount"] > 0
    return {"charged": True}

pipe = Pipeline(pipeline_name="payments")
pipe.set_steps([ingest, charge])
```

The asserts are cheap and portable; the orchestrator's validation adds a machine-checked layer on top.

## Battle Card

| Dimension | Implicit data | Contract-first (wpipe) |
| :--- | :---: | :---: |
| Interface definition | In developer heads | In code/context |
| Failure detection | Step N+3 | Step that breaks it |
| Schema evolution | Silent | Versioned & visible |
| Documentation | None | Contracts in code |

## Conclusion

Contracts are how data pipelines survive organizational growth. Declaring them ahead of time — and enforcing them in a typed pipeline context — converts "I thought it worked" into "it fails loudly and explains itself."

#ContractFirst #DataContracts #wpipe #Python #DataEngineering