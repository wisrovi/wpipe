#!/usr/bin/env python3
"""Generate one modern companion PDF per LinkedIn day folder.

Each PDF complements the LinkedIn post in posters/LinkedIn/diaNN/:
        companion.pdf         the rendered professional dossier
        diagrama*.png         the post's architecture images (embedded)

Usage:
    python3 posters/generate_linkedin_pdfs.py
"""
import os
import re
import sys
import glob
import shutil
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.dirname(os.path.abspath(__file__))
LINKEDIN = os.path.join(BASE, "LinkedIn")
TMP = os.path.join(os.path.dirname(BASE), "..", "..", "tmp", "wpipe_pdfs")
# Prefer the repo's own tmp-less location: /tmp is not in the repo.
TMP = "/tmp/opencode/wpipe_pdfs"
CHROME = "google-chrome"
MMDC = ["npx", "-y", "@mermaid-js/mermaid-cli"]
PUPPETEER_CONFIG = os.path.join("/tmp/opencode", "puppeteer-config.json")

PLATFORMS = ["n8n", "Zapier", "Make", "Airflow", "Prefect", "Luigi", "Dagster", "Celery", "Cron"]

TECH_CODE = {
    "n8n": """from wpipe import Pipeline, step

@step(name="ingest", retry_count=3)
def ingest(data):
    return {"payload": data["rows"]}

pipe = Pipeline(pipeline_name="from_n8n")
pipe.set_steps([ingest])

# Canonical JSON -> typed, versionable Python steps.""",
    "Zapier": """from wpipe import Pipeline, step

@step(name="sync", retry_count=3, retry_delay=5)
def sync(data):
    return {"status": push_to_crm(data["lead"])}

pipe = Pipeline(pipeline_name="zap_to_wpipe", tracking_db="sync.db")
pipe.set_steps([sync])""",
    "Make": """from wpipe import Pipeline, step
from wpipe import Parallel

@step(name="branch_a")
def branch_a(data): return {"a": data["x"]}

@step(name="branch_b")
def branch_b(data): return {"b": data["y"]}

pipe = Pipeline(pipeline_name="make_to_wpipe")
pipe.set_steps([Parallel(steps=[branch_a, branch_b])])""",
    "Airflow": """from wpipe import Pipeline, step

@step(name="task", retry_count=3, retry_delay=2)
def task(data):
    return {"ok": run(data["job"])}

pipe = Pipeline(pipeline_name="airflow_like", tracking_db="jobs.db")
pipe.set_steps([task])

# No scheduler daemon, no heavy metadata DB.""",
    "Prefect": """from wpipe import Pipeline, step

@step(name="resumable", checkpoint=True)
def resumable(data):
    return {"state": hydrate(data["cursor"])}

pipe = Pipeline(pipeline_name="resilient", tracking_db="state.db")
pipe.set_steps([resumable])""",
    "Luigi": """from wpipe import Pipeline, step

@step(name="build", retry_count=2, retry_delay=5)
def build(data):
    target = compile_targets(data["source"])
    return {"artifacts": target}

pipe = Pipeline(pipeline_name="luigi_like")
pipe.set_steps([build])""",
    "Dagster": """from wpipe import Pipeline, step

@step(name="step", version="v2.1")
def step(data):
    return {"value": process(data["row"])}

pipe = Pipeline(pipeline_name="dagster_like")
pipe.set_steps([step])

# Step-first resilience without the server.""",
    "Celery": """from wpipe import Pipeline, step

@step(name="job", retry_count=3, retry_delay=1)
def job(data):
    return {"result": worker(data["task"])}

pipe = Pipeline(pipeline_name="brokerless")
pipe.set_steps([job])

# Async-safe, but no Redis/RabbitMQ required.""",
    "Cron": """from wpipe import Pipeline, step

@step(name="job", retry_count=3, retry_delay=10)
def job(data):
    return {"done": run(data["command"])}

pipe = Pipeline(pipeline_name="cron_pro", tracking_db="cron.db")
pipe.set_steps([job])

# Keep the schedule; gain checkpoints + audit.""",
}

DEFAULT_CODE = """from wpipe import Pipeline, step

@step(name="my_step", retry_count=3, retry_delay=2, checkpoint=True)
def my_step(data):
    return {"result": process(data["input"])}

pipe = Pipeline(pipeline_name="my_pipeline", tracking_db="pipeline.db")
pipe.set_steps([my_step])
pipe.run({"input": [...]})

# Python-native orchestration: checkpoints, retries, self-documenting."""

TECH_MERMAID = {
    "n8n": "flowchart LR\n    A[No-Code Canvas] -->|export JSON| B[wpipe import]\n    B --> C[Code-First Steps]\n    C --> D[SQLite Checkpoints]\n    C --> E[SQL Tracker]\n    D --> F[Git-flow CI/CD]\n    E --> F",
    "Zapier": "flowchart LR\n    A[Zap Step] -->|API trigger| B[wpipe sync]\n    B --> C[Retry/Timeout]\n    C --> D[Checkpoint]\n    C --> E[Audit Tracker]\n    D --> F[Verified Delivery]\n    E --> F",
    "Make": "flowchart LR\n    A[Scenario] --> B[Parallel branches]\n    B --> C[Context merge]\n    C --> D[Atomic checkpoint]\n    D --> E[Forensic trace]",
    "Airflow": "flowchart LR\n    A[Scheduled DAG] -->|trigger| B[wpipe steps]\n    B --> C[WAL state]\n    C --> D[Resume on fail]\n    B --> E[Local dashboard]\n    D --> F[Output]",
    "Prefect": "flowchart LR\n    A[Long-running flow] --> B[State hydration]\n    B --> C[Checkpoint each step]\n    C --> D[Crash?]\n    D -->|yes| B\n    D -->|no| E[Completed]",
    "Luigi": "flowchart LR\n    A[Targets] --> B[Dependency graph]\n    B --> C[wpipe steps]\n    C --> D[SQLite WAL]\n    D --> E[Verified output]",
    "Dagster": "flowchart LR\n    A[Assets in code] --> B[Type-checked steps]\n    B --> C[Parallel where useful]\n    C --> D[Tracker per run]\n    D --> E[Auditable]",
    "Celery": "flowchart LR\n    A[Task] --> B[Broker-less queue]\n    B --> C[Worker in-process]\n    C --> D[Retry policy]\n    D --> E[Result + checkpoint]",
    "Cron": "flowchart LR\n    A[Legacy cron] -->|same schedule| B[wpipe step]\n    B --> C[ACID checkpoint]\n    C --> D[Partial failure?]\n    D -->|resume| B\n    D -->|done| E[Audit trail]",
}

DEFAULT_MERMAID = "flowchart LR\n    A[Input] --> B[Step: validate]\n    B --> C[Step: process]\n    C --> D[Checkpoint: WAL]\n    C --> E[Tracker SQL]\n    D --> F[Resume on failure]\n    E --> G[Self-documenting flow]"

BENEFITS = [
    ("Code-first", "Pipelines are Python: versionable, testable, reviewable in Git."),
    ("Checkpoints", "State persisted to SQLite WAL at every step; resume, don't restart."),
    ("Independently lean", "<50MB RAM. No broker, no daemon, no metadata server."),
]

FC_ICONS = [
    ("+117k downloads", "A community of efficiency-first developers."),
    ("<50MB RAM", "Fits containers, VMs, and Raspberry Pi-class hardware."),
    ("SQLite WAL", "Industrial durability without a database to administer."),
]


def detect_tech(text):
    for t in PLATFORMS:
        if re.search(rf"#\s*{re.escape(t)}|{re.escape(t)}", text, re.I):
            return t
    return None


def extract_post(path):
    txt = open(path, encoding="utf-8").read()
    title = ""
    m = re.search(r"^#\s*(.+)$", txt, re.M)
    if m:
        title = re.sub(r"^[^\w]+\s*", "", m.group(1).strip())
    headline = ""
    h = re.search(r"\*\*Headline:\s*(.+?)\*\*", txt, re.S)
    if h:
        headline = h.group(1).strip()
    paras = []
    for line in txt.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#") or s.startswith("```") or s.startswith("📊"):
            continue
        if s.startswith("|"):
            continue
        if re.search(r"Headline|Suggested Text|Image:|Post Draft|Hashtags|#\w+$|Feel free|you are welcome", s, re.I):
            continue
        if s in {"---", "👇", "🔄"} or s.startswith("👇"):
            continue
        clean = re.sub(r"[#>*]", "", s)
        clean = re.sub(r"\*\*", "", clean)
        clean = re.sub(r"^[-+•]?\s*", "", clean).strip()
        if len(clean) > 25 and not clean.startswith("http"):
            paras.append(clean)
    bullets = []
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith("🔹") or (s.startswith("- ") and "|" not in s):
            clean = re.sub(r"\*\*", "", s.lstrip("🔹- ")).strip()
            if clean and len(clean) < 140:
                bullets.append(clean)
    table = extract_table(txt)
    tags = re.findall(r"#([A-Za-z0-9]+)", txt)
    return {
        "title": title,
        "headline": headline or title,
        "paras": paras[:5],
        "bullets": bullets[:5],
        "table": table,
        "tags": tags,
        "tech": detect_tech(txt),
    }


def extract_table(txt):
    lines = txt.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            rows = []
            for j in range(i, len(lines)):
                row = lines[j].strip()
                if not row.startswith("|"):
                    break
                if re.match(r"^\s*\|[\s:\-|]+\|\s*$", row):
                    continue
                cells = [re.sub(r"\*\*", "", c).strip() for c in row.strip("|").split("|")]
                rows.append(cells)
            if rows:
                return rows
    return None


def html_table(rows):
    if not rows:
        return ""
    thead = "<tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>"
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f"<table><thead>{thead}</thead><tbody>{body}</tbody></table>"


def build_html(day, folder):
    post = extract_post(os.path.join(folder, "post.md"))
    tech = post["tech"] or "wpipe"
    code = TECH_CODE.get(tech, DEFAULT_CODE)
    table = post["table"] or [
        ["Aspect", f"Legacy / {tech}", "wpipe"],
        ["Definition", "Config/DSL or canvas", "Python code"],
        ["State", "Scattered / none", "SQLite WAL checkpoints"],
        ["Observability", "Partial", "Tracker SQL + dashboard"],
        ["Footprint", "Heavy", "<50MB RAM"],
    ]
    intro = " ".join(post["paras"][:2]) if post["paras"] else (
        f"Orchestration is where software gets real: schedules, retries, state, "
        f"observability. wpipe brings {tech}-grade automation to your stack with "
        f"the simplicity of a Python library."
    )
    bullets = post["bullets"] or BENEFITS[:3] and [b for _, b in BENEFITS[:3]]

    imgs = sorted(glob.glob(os.path.join(folder, "diagrama*.png")))
    if not imgs or not os.path.exists(imgs[0]):
        rendered = render_mermaid(tech, post["headline"])
        if rendered:
            imgs = [rendered]
    img_html = ""
    if imgs:
        items = "".join(
            f'<div class="fig"><img src="file://{os.path.abspath(p)}" alt="diagram"/></div>'
            for p in imgs[:6]
        )
        img_html = (
            "<section><h2>Under the hood</h2><p>The flow behind the post, as wpipe renders "
            "it from code.</p>"
            f'<div class="figrow">{items}</div></section>'
        )

    cards = "".join(
        f'<div class="card"><b>{a}</b><span>{b}</span></div>' for a, b in FC_ICONS
    )
    bcards = "".join(
        f'<div class="card"><b>{a}</b><span>{b}</span></div>' for a, b in BENEFITS
    )
    day_num = re.match(r"dia(\d+)", day).group(1)

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 14mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
       color: #14202b; margin: 0; line-height: 1.55; font-size: 10.5pt; }}
.wrap {{ max-width: 178mm; margin: 0 auto; }}
.band {{ background: linear-gradient(135deg, #0b3d2e 0%, #116149 55%, #0e8a5f 100%);
        color: #fff; border-radius: 14px; padding: 22px 26px; }}
.band .k {{ letter-spacing: .18em; text-transform: uppercase; font-size: 8pt; opacity: .85; }}
.band h1 {{ margin: 4px 0 2px; font-size: 21pt; line-height: 1.2; }}
.band p {{ margin: 4px 0 0; opacity: .95; font-size: 11pt; }}
h2 {{ font-size: 13pt; margin: 22px 0 8px; color: #0b3d2e;
     border-bottom: 2px solid #dfe9e4; padding-bottom: 4px; }}
.lead {{ font-size: 11pt; color: #33414d; }}
ul {{ margin: 8px 0; padding-left: 18px; }}
li {{ margin: 4px 0; }}
code, pre {{ font-family: 'SFMono-Regular', 'JetBrains Mono', Consolas, monospace; }}
pre {{ background: #0d1b26; color: #d7e6de; border-radius: 10px; padding: 14px 16px;
      font-size: 9pt; overflow-wrap: break-word; white-space: pre-wrap; }}
pre .c {{ color: #7fa; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 9.5pt; }}
th {{ background: #116149; color: #fff; text-align: left; padding: 7px 9px; }}
td {{ border-bottom: 1px solid #e3e9e6; padding: 6px 9px; vertical-align: top; }}
tr:nth-child(even) td {{ background: #f4f8f6; }}
.figrow {{ display: flex; flex-wrap: wrap; gap: 14px; }}
.fig {{ flex: 1 1 45%; min-width: 220px; text-align:center; }}
.fig img {{ max-width: 100%; border: 1px solid #e2e8e5; border-radius: 8px; }}
.grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0; }}
.card {{ background: #f0f6f3; border: 1px solid #d8e6de; border-radius: 10px; padding: 12px 14px; }}
.card b {{ color: #0b3d2e; display: block; font-size: 10pt; }}
.card span {{ font-size: 9pt; color: #41515c; }}
.next {{ background: #f6f8f7; border: 1px dashed #aac9ba; border-radius: 12px; padding: 14px 18px; }}
a {{ color: #0e8a5f; }}
.foot {{ margin-top: 18px; padding-top: 8px; border-top: 1px solid #dfe9e4;
        font-size: 8.5pt; color: #7a8991; }}
</style></head>
<body><div class="wrap">
  <div class="band">
    <div class="k">wpipe · Orchestration, engineered · Day {day_num}</div>
    <h1>{esc(tech)} at the center of your pipelines</h1>
    <p>{esc(post["headline"])}</p>
  </div>

  <h2>The context</h2>
  <p class="lead">{esc(intro)}</p>

  <h2>Why engineers shift to wpipe</h2>
  <ul>{''.join(f'<li>{esc(b)}</li>' for b in bullets)}</ul>

  <div class="grid">{bcards}</div>

  <h2>What it looks like</h2>
  <pre>{esc(code)}</pre>

  <h2>At a glance</h2>
  {html_table(table)}

  {img_html}

  <div class="grid">{cards}</div>

  <h2>Next step</h2>
  <div class="next">wpipe is a Python library — try it in your next pipeline:
  <pre>pip install wpipe</pre>
  Steps stay functions you already understand. Docs, diagrams, and dashboards follow.
  Explore <b>{tech}</b> workflows at <a>wpipe.readthedocs.io</a>.</div>

  <div class="foot">wpipe · Python-native orchestration with SQLite WAL checkpoints, retries,
     timeouts, parallelism, and self-documenting flows. <b>+117k</b> downloads.</div>
</div></body></html>"""
    return html


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def render_mermaid(tech, headline):
    spec = TECH_MERMAID.get(tech, DEFAULT_MERMAID)
    src = os.path.join(TMP, f"flow_{tech}.mmd")
    out = os.path.join(TMP, f"flow_{tech}.png")
    os.makedirs(TMP, exist_ok=True)
    with open(src, "w") as f:
        f.write(spec)
    if os.path.exists(out):
        return out
    cfg = ["-p", PUPPETEER_CONFIG, "-b", "white", "-s", "2"]
    cmd = MMDC + [
        "-i", src, "-o", out, "-p", PUPPETEER_CONFIG, "-b", "white", "-s", "2",
    ]
    env = dict(os.environ, PUPPETEER_SKIP_DOWNLOAD="1")
    try:
        subprocess.run(cmd, capture_output=True, env=env, timeout=120)
    except Exception:
        return None
    return out if os.path.exists(out) else None


def render_pdf(html, out_pdf):
    html_path = os.path.join(TMP, "page.html")
    os.makedirs(TMP, exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf}",
        f"file://{html_path}",
    ]
    subprocess.run(cmd, capture_output=True, timeout=120)
    return os.path.exists(out_pdf) and os.path.getsize(out_pdf) > 0


def main():
    folders = sorted(glob.glob(os.path.join(LINKEDIN, "dia*")))
    os.makedirs(TMP, exist_ok=True)
    ok = []
    fail = []
    for folder in folders:
        day = os.path.basename(folder)
        out = os.path.join(folder, "companion.pdf")
        try:
            html = build_html(day, folder)
            r = render_pdf(html, out)
            (ok if r else fail).append(day)
            print(f"[{'OK' if r else 'FAIL'}] {day}")
        except Exception as e:
            fail.append(day)
            print(f"[ERROR] {day}: {e}")
    print(f"\nDone: {len(ok)} PDFs generated, {len(fail)} failed.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())