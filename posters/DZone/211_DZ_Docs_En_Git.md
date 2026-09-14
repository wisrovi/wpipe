# Docs in Git: Versioning Your Architecture Like You Version Code

## The Untracked Architecture

Your pipeline's architecture has a serious version-control problem: it lives in files that are rarely committed, or in tools that aren't Git at all. Diagrams in wikis, docs in corporate portals, flow descriptions in slide decks — none of it gets reviewed, diffed, or reverted. Git, meanwhile, holds your code to a far higher standard.

## Why Docs Should Be Code

When documentation becomes a first-class commit, every engineering muscle applies:

- **Pull requests** review architecture changes alongside the code that caused them.
- **`git diff`** shows exactly what moved in the flow.
- **`git blame`** answers "who drew this?" and "why?"
- **Reverts** undo architecture changes cleanly.

## wpipe Keeps Docs In-Sync With the Repo

Because wpipe generates diagrams from code, the documentation lives *with* the code and updates with the same commit. The pipeline definition, its Mermaid DAG, and its execution metadata are all reviewable in one diff — no external tool, no sync job.

```python
from wpipe import Pipeline, step

@step(name="ingest", version="v2.0", retry_count=2)
def ingest(data):
    return {"rows": data["raw"]}

@step(name="serve", version="v1.3")
def serve(data):
    return {"ok": True}

pipe = Pipeline(pipeline_name="versioned_docs", tracking_db="docs_repo.db")
pipe.set_steps([ingest, serve])
# The Mermaid for this pipeline is a byproduct of set_steps(), committed in Git.
```

## Battle Card

| Concern | Docs outside Git | Docs in Git (wpipe) |
| :--- | :---: | :---: |
| Change history | None | Full history |
| Review | None | PR-based |
| Correlation with code | Manual | Same commit |
| Recovery | Loss-prone | Revert-able |

## Conclusion

Architecture that doesn't live in Git eventually floats away from the system it describes. Keeping pipeline docs in the repository — and generated from code — makes "what's our architecture?" answerable forever, with the same rigor as the code itself.

#Git #Documentation #wpipe #Architecture #DevOps