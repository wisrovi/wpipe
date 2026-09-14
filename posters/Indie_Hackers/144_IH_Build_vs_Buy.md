# Build vs Buy: The Orchestrator Decision That Determines Your Burn Rate

Every founder hits the orchestration fork: build your own pipeline infrastructure, or buy the platform that promises to do it for you. Both roads have eaten startups alive. The nuance — which nobody sells you — is that there's a third option: **choose infrastructure you can afford to be wrong about**.

## The Buy Path: Rapid, Then Expensive

Selling the "buy" case is easy: SaaS orchestration, zero ops, pretty UI, and a demo that makes your batch job feel production-grade. The bills arrive quietly:

- **Per-execution pricing** scales painfully as your data grows.
- **Lock-in gifts**: your flows live in their database, expressed in their DSL.
- **Exit is a migration**, and migrations of workflows are god-awful.

For a bootstrapper, the platform's mounting usage charges show up exactly when the business starts working — cannibalizing margin at the worst possible moment.

## The Build Path: Control, Then Distraction

Building your own "lightweight orchestrator" is a rite of passage that can swallow a quarter. You didn't want a distributed scheduler; you wanted to run a sync every hour. Now you're debugging backpressure on a Friday night.

The build path is only rational if orchestration *is* your product.

## The Third Option: A Library

wpipe sits in the gap: **a library you build with, not a platform you rent.** It gives the resilience features founders rarely get to build set-ups — checkpoints, retries, timeouts, observability — at an OSS price and a <50MB footprint.

```python
from wpipe import Pipeline, step

@step(name="sync", retry_count=3, retry_delay=5)
def sync(data):
    return {"status": push_to_crm(data["rows"])}

pipe = Pipeline(pipeline_name="lightops", tracking_db="ops.db")
pipe.set_steps([sync])
pipe.run({"rows": [...]})
```

## Battle Card

| Dimension | Buy (SaaS) | Build (custom) | wpipe library |
| :--- | :---: | :---: | :---: |
| Upfront cost | Free tier | Dev months | Free (OSS) |
| Scale cost | Per execution | Per engineer | ~Zero |
| Lock-in | High | None | None (Python) |
| Time-to-value | Fast | Slow | Fast |
| Ops burden | Vendor (locked) | Full | Minimal |

## Conclusion

The build-vs-buy question usually ignores the middle path: infrastructure as a *library you pay nothing for* and that keeps scaling costs at zero. For bootstrappers, that's not just a compromise — it's the option that protects runway in both directions.

#BuildVsBuy #Bootstrapping #IndieHackers #wpipe #Python