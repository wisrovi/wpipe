# SaaS vs Self-Hosted Orchestration: The Infrastructure Math Founders Forget

Founders obsess over product-market fit and pay little attention to one of the most recurring line items in a growing company: **orchestration**. The choice between a hosted orchestration service and running your own has a deceptively simple spreadsheet — and hidden terms that compound.

## The Two Column Budgets

**SaaS orchestration columns:**
- Per-execution or per-seat pricing that scales with success.
- Instead of ops, you get vendor lock-in and a DSL.
- Uptime is theirs until the outage is yours (notice when the credits pause).

**Self-hosted heavyweight columns:**
- Compute for scheduler + metadata DB + broker + workers.
- An admin's attention budget, permanently allocated.
- Version upgrades, security patches, reconciliation.

Both get expensive — the SaaS grows with usage, the heavy self-host grows with toil.

## The Lightweight Self-Host: A Different Equation

wpipe is self-hosted, but on entirely different terms: **a library**. There's no stack to administer when the state layer is a SQLite file and the engine lives inside your process.

```python
from wpipe import Pipeline, step

@step(name="billing_job", retry_count=3, retry_delay=5)
def billing_job(data):
    return {"invoice": generate_invoice(data["customer"])}

pipe = Pipeline(pipeline_name="biller", tracking_db="biller.db")
pipe.set_steps([billing_job])

# Also async-ready and exportable:
# pipe = Pipeline(name, tracking_db, async_mode=True)
```

- No seat licenses, no per-execution fees — cost is flat.
- No broker to patch — one local file carries the state.
- Runs where you already run Python, on hardware you already pay for.

## Battle Card

| Line item | SaaS orchestration | Heavy self-host | wpipe (light self-host) |
| :--- | :---: | :---: | :---: |
| Scaling cost | Per execution | Per admin | ~Flat |
| Ops surface | Vendor-managed but lock-in | Full | Minimal |
| Footprint | N/A | 500MB - 2GB+ | <50MB |
| Lock-in | Flow DSL | Moderate | None (code) |
| Failure ownership | Blurred | Yours | Yours + checkpoints |

## Conclusion

The founder's math on orchestration comes down to compounding costs: what does this tool cost when we win? wpipe's flat, code-owned, self-hosted model means the line item stays flat while the business grows — the direction all infrastructure budgets should slope.

#SaaS #SelfHosted #IndieHackers #wpipe #Bootstrapping #Python