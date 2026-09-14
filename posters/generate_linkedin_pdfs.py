#!/usr/bin/env python3
"""Generate one modern companion PDF per LinkedIn day folder (visual-first).

Strategy: LinkedIn readers skim. Each PDF is a 5-page visual dossier —
one idea per page, big type, diagrams as the hero, minimal text:

    1. Cover     — bold gradient, one-sentence pitch, key stat
    2. The shift — pain -> wpipe (two visual cards)
    3. Diagram   — the architecture, large and centered
    4. Wins      — icon benefit cards (+ compact table when the post has one)
    5. Action    — tiny code, our biggest numbers, soft CTA

Usage:
    python3 posters/generate_linkedin_pdfs.py
"""
import os
import re
import sys
import glob
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
LINKEDIN = os.path.join(BASE, "LinkedIn")
TMP = "/tmp/opencode/wpipe_pdfs"
CHROME = "google-chrome"
MMDC = ["npx", "-y", "@mermaid-js/mermaid-cli"]
PUPPETEER_CONFIG = os.path.join("/tmp/opencode", "puppeteer-config.json")

PLATFORMS = ["n8n", "Zapier", "Make", "Airflow", "Prefect", "Luigi", "Dagster", "Celery", "Cron"]

TAGLINES = {
    "n8n": "No-code today, code you can ship tomorrow.",
    "Zapier": "Automations that finally hold state.",
    "Make": "Visual flows, real engineering rigor.",
    "Airflow": "DAG power, none of the daemon.",
    "Prefect": "Long-running flows that never lose their place.",
    "Luigi": "Dependencies without the legacy lock-in.",
    "Dagster": "Step-first resilience, minus the server.",
    "Celery": "Async jobs without the broker tax.",
    "Cron": "Upgrade cron from script to system.",
    "wpipe": "Pipelines that resume, not restart.",
}

PAINS = {
    "n8n": ["READMEs stay empty", "JSON exports un-diffable", "Debugging is a black box"],
    "Zapier": ["Zaps break silently", "No real retry policy", "Data held hostage by a SaaS"],
    "Make": ["More canvas JS, less logic", "Parallelism done by hand", "Observability is luck"],
    "Airflow": ["A metadata DB to babysit", "DAGs drift from reality", "CI for DAGs is painful"],
    "Prefect": ["Long runs lose state", "Workers + server + fleet", "Observability gets costly"],
    "Luigi": ["Last-mile brittleness", "No granular resume", "Sprawl in one repo"],
    "Dagster": ["A service to run one flow", "Type-checked but heavy", "Slow onboarding curve"],
    "Celery": ["A broker to install and tune", "Fire-and-forget tasks", "Hard to replay a job"],
    "Cron": ["Failures are silent", "No history, no audit", "One typo kills the job"],
    "wpipe": ["State lost on crash", "Retries hand-rolled", "Zero audit trail"],
}

WINS = [
    ("📦", "Code-first", "Pipelines are Python — versionable, testable, reviewable."),
    ("🧭", "Resume, don't restart", "Every step checkpoints to SQLite WAL."),
    ("🪶", "Featherweight", "<50 MB RAM. No broker, no daemon."),
]

METRICS = [("+117k", "downloads"), ("<50 MB", "RAM, total"), ("SQLite", "WAL state")]

TECH_CODE = {
    "n8n": "from wpipe import Pipeline, step\n\n@step(name=\"ingest\", retry_count=3)\ndef ingest(data):\n    return {\"rows\": data[\"payload\"]}\n\npipe = Pipeline(pipeline_name=\"from_n8n\")\npipe.set_steps([ingest])\npipe.run(task_ctx)",
    "Zapier": "from wpipe import Pipeline, step\n\n@step(name=\"sync\", retry_count=3, retry_delay=5)\ndef sync(data):\n    return {\"done\": push_crm(data[\"lead\"])}\n\npipe = Pipeline(pipeline_name=\"zap2wpipe\", tracking_db=\"sync.db\")\npipe.set_steps([sync])",
    "Make": "from wpipe import Pipeline, step, Parallel\n\n@step(name=\"a\", retry_count=3)\ndef a(d): return {\"a\": d[\"x\"]}\n\n@step(name=\"b\", retry_count=3)\ndef b(d): return {\"b\": d[\"y\"]}\n\npipe.set_steps([Parallel(steps=[a, b])])",
    "Airflow": "from wpipe import Pipeline, step\n\n@step(name=\"job\", retry_count=3, retry_delay=2)\ndef job(data):\n    return {\"ok\": run(data[\"job\"])}\n\npipe = Pipeline(pipeline_name=\"airflow_like\")",
    "Prefect": "from wpipe import Pipeline, step\n\n@step(name=\"resume_me\", checkpoint=True)\ndef resume_me(data):\n    return {\"state\": hydrate(data[\"cursor\"])}\n\npipe = Pipeline(pipeline_name=\"resilient\")",
    "Luigi": "from wpipe import Pipeline, step\n\n@step(name=\"build\", retry_count=2, retry_delay=5)\ndef build(data):\n    return {\"out\": compile_targets(data[\"src\"])}\n\npipe = Pipeline(pipeline_name=\"luigi_like\")",
    "Dagster": "from wpipe import Pipeline, step\n\n@step(name=\"core\", version=\"v2.1\")\ndef core(data):\n    return {\"v\": process(data[\"row\"])}\n\npipe = Pipeline(pipeline_name=\"dagster_like\")",
    "Celery": "from wpipe import Pipeline, step\n\n@step(name=\"job\", retry_count=3, retry_delay=1)\ndef job(data):\n    return {\"result\": worker(data[\"task\"])}\n\npipe = Pipeline(pipeline_name=\"brokerless\")",
    "Cron": "from wpipe import Pipeline, step\n\n@step(name=\"job\", retry_count=3, retry_delay=10)\ndef job(data):\n    return {\"done\": run(data[\"command\"])}\n\npipe = Pipeline(pipeline_name=\"cron_pro\", tracking_db=\"cron.db\")",
}

DEFAULT_CODE = ("from wpipe import Pipeline, step\n\n"
                "@step(name=\"my_step\", retry_count=3, retry_delay=2, checkpoint=True)\n"
                "def my_step(data):\n    return {\"result\": process(data[\"input\"])}\n\n"
                "pipe = Pipeline(pipeline_name=\"my_pipeline\", tracking_db=\"p.db\")\n"
                "pipe.set_steps([my_step])\npipe.run({\"input\": [...]})")

TECH_MERMAID = {
    "n8n": "flowchart LR\n    A[No-Code Canvas] -->|export JSON| B[wpipe import]\n    B --> C[Code-First Steps]\n    C --> D[SQLite Checkpoints]\n    C --> E[SQL Tracker]\n    D --> F[Git-flow CI/CD]\n    E --> F",
    "Zapier": "flowchart LR\n    A[Zap] -->|API trigger| B[wpipe sync]\n    B --> C[Retry/Timeout]\n    C --> D[Checkpoint]\n    C --> E[Audit Tracker]\n    D --> F[Verified Delivery]\n    E --> F",
    "Make": "flowchart LR\n    A[Scenario] --> B[Parallel branches]\n    B --> C[Context merge]\n    C --> D[Atomic checkpoint]\n    D --> E[Forensic trace]",
    "Airflow": "flowchart LR\n    A[Scheduled DAG] -->|trigger| B[wpipe steps]\n    B --> C[WAL state]\n    C --> D[Resume on fail]\n    B --> E[Local dashboard]\n    D --> F[Output]",
    "Prefect": "flowchart LR\n    A[Long-running flow] --> B[State hydration]\n    B --> C[Checkpoint each step]\n    C --> D[Crash?]\n    D -->|yes| B\n    D -->|no| E[Completed]",
    "Luigi": "flowchart LR\n    A[Targets] --> B[Dependency graph]\n    B --> C[wpipe steps]\n    C --> D[SQLite WAL]\n    D --> E[Verified output]",
    "Dagster": "flowchart LR\n    A[Assets in code] --> B[Type-checked steps]\n    B --> C[Parallel where useful]\n    C --> D[Tracker per run]\n    D --> E[Auditable]",
    "Celery": "flowchart LR\n    A[Task] --> B[Broker-less queue]\n    B --> C[Worker in-process]\n    C --> D[Retry policy]\n    D --> E[Result + checkpoint]",
    "Cron": "flowchart LR\n    A[Legacy cron] -->|same schedule| B[wpipe step]\n    B --> C[ACID checkpoint]\n    C --> D[Partial failure?]\n    D -->|resume| B\n    D -->|done| E[Audit trail]",
}

DEFAULT_MERMAID = ("flowchart LR\n    A[Input] --> B[Validate]\n    B --> C[Process]\n    C --> D[Checkpoint WAL]\n"
                   "C --> E[Tracker SQL]\n    D --> F[Resume on failure]\n    E --> G[Auto-doc]")

PALETTES = [
    {"d": "#0b3d2e", "m": "#0e8a5f", "l": "#116149", "bg": "#f0f7f3", "c": "#dcefe5",
     "ink": "#12372c", "soft": "#5d746a"},
    {"d": "#0d2c4a", "m": "#1565c0", "l": "#1a73e8", "bg": "#eef4fb", "c": "#dce8f7",
     "ink": "#12304e", "soft": "#5a6f87"},
    {"d": "#123b3a", "m": "#0e9aa7", "l": "#12939f", "bg": "#eefafa", "c": "#d8eef0",
     "ink": "#10393a", "soft": "#57706f"},
    {"d": "#2a2350", "m": "#5e35b1", "l": "#7c4dff", "bg": "#f4f1fb", "c": "#e6def7",
     "ink": "#2b2350", "soft": "#6d6492"},
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def detect_tech(text):
    for t in PLATFORMS:
        if re.search(rf"#\s*{re.escape(t)}|{re.escape(t)}", text, re.I):
            return t
    return None


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


def highlight_code(code):
    out = esc(code)
    out = re.sub(r'(&quot;.*?&quot;)', r'<span class="str">\1</span>', out)
    kw_pairs = [
        ("from wpipe import", "from wpipe import"),
        ("@step(", "@step("),
        ("Parallel(", "Parallel("),
        ("Pipeline(", "Pipeline("),
        ("def ", "def "),
        ("run(", "run("),
        ("set_steps(", "set_steps("),
        ("retry_count", "retry_count"),
        ("retry_delay", "retry_delay"),
        ("checkpoint", "checkpoint"),
        ("tracking_db", "tracking_db"),
        ("version=", "version="),
    ]
    for token, _ in kw_pairs:
        out = out.replace(esc(token), f'<b class="kw">{esc(token)}</b>')
    return out


def render_mermaid(tech, fname):
    spec = TECH_MERMAID.get(tech, DEFAULT_MERMAID)
    src = os.path.join(TMP, f"flow_{fname}.mmd")
    out = os.path.join(TMP, f"flow_{fname}.png")
    os.makedirs(TMP, exist_ok=True)
    if os.path.exists(out):
        return out
    with open(src, "w") as f:
        f.write(spec)
    env = dict(os.environ, PUPPETEER_SKIP_DOWNLOAD="1")
    try:
        subprocess.run(MMDC + ["-i", src, "-o", out, "-p", PUPPETEER_CONFIG,
                               "-b", "white", "-s", "3"], capture_output=True, env=env, timeout=120)
    except Exception:
        return None
    return out if os.path.exists(out) else None


def render_pdf(html, out_pdf):
    html_path = os.path.join(TMP, "page.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}",
                    f"file://{html_path}"], capture_output=True, timeout=120)
    return os.path.exists(out_pdf) and os.path.getsize(out_pdf) > 0


def fetch_images(folder, tech, fname):
    imgs = sorted(glob.glob(os.path.join(folder, "diagrama*.png")))
    if imgs:
        return [os.path.abspath(p) for p in imgs]
    m = render_mermaid(tech, fname)
    return [m] if m else []


def build_html(day, folder):
    txt = open(os.path.join(folder, "post.md"), encoding="utf-8").read()
    tech = detect_tech(txt) or "wpipe"
    pal = PALETTES[int(re.match(r"dia(\d+)", day).group(1)) % len(PALETTES)]
    day_num = re.match(r"dia(\d+)", day).group(1)

    m = re.search(r"\*\*Headline:\s*(.+?)\*\*", txt, re.S)
    headline = (m.group(1).strip() if m else "") or "Orchestration that scales with you."
    if len(headline) > 110:
        headline = headline[:107].rstrip() + "…"

    pains = PAINS.get(tech, PAINS["wpipe"])
    tagline = TAGLINES.get(tech, TAGLINES["wpipe"])
    code = TECH_CODE.get(tech, DEFAULT_CODE)
    table = extract_table(txt)
    imgs = fetch_images(folder, tech, f"{day}_{tech}")

    # ---- visuals built from CSS -------------------------------------
    steps = ["Input", "Validate", "Retry ×3", "Checkpoint WAL", "Tracker SQL", "Output"]
    anatomy = "".join(
        f'<span class="dot">{t}</span>' + ('<i>→</i>' if i < len(steps) - 1 else '')
        for i, t in enumerate(steps))
    pain_cards = "".join(f'<div class="pcard">{esc(p)}</div>' for p in pains)
    win_cards = "".join(f'<div class="wcard"><span class="ico">{w[0]}</span>'
                        f"<div><b>{w[1]}</b><p>{w[2]}</p></div></div>" for w in WINS)
    metric_html = "".join(f'<div class="stat"><b>{m[0]}</b><span>{m[1]}</span></div>' for m in METRICS)
    table_html = ""
    if table:
        thead = "<tr>" + "".join(f"<th>{esc(c)}</th>" for c in table[0]) + "</tr>"
        body = "".join(
            "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>"
            for r in table[1:][:6])
        table_html = f'<table><thead>{thead}</thead><tbody>{body}</tbody></table>'

    img_html = ""
    if imgs:
        show = imgs[:10]
        style = "one" if len(show) == 1 else "many"
        gal = "".join(f'<div class="gi"><img src="file://{p}"/><span>flow</span></div>' for p in show)
        img_html = (f'<div class="gal {style}">{gal}</div>')

    resume_bar = "".join(
        '<span class="f" style="background:%s"></span>' % (pal["m"] if i < 3 else "#dfe7e4")
        for i in range(7))
    code_html = highlight_code(code)
    d = pal

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body, html {{ margin: 0; padding: 0; font-family: -apple-system, 'Segoe UI', Roboto,
  'Helvetica Neue', Arial, sans-serif; color: {d['ink']}; }}
.sheet {{ width: 210mm; min-height: 297mm; page-break-after: always;
  position: relative; background: {d['bg']}; }}
.sheet.last {{ page-break-after: auto; }}
.cover {{ height: 297mm; overflow: hidden; }}.pains, .wins, .resume, .gi, .codecard, .cta, table {{ break-inside: avoid; }}
.inner {{ padding: 20mm 20mm 0; }}
.eyebrow {{ display:inline-block; font-size: 10pt; letter-spacing: .22em; font-weight: 700;
  text-transform: uppercase; color: {d['m']}; margin-bottom: 6mm; }}
h1 {{ font-size: 30pt; line-height: 1.08; margin: 0 0 6mm; letter-spacing: -.01em; }}
h2 {{ font-size: 19pt; margin: 0 0 7mm; letter-spacing: -.01em; color: {d['ink']}; }}
p.body {{ font-size: 12.5pt; line-height: 1.65; color: {d['soft']}; margin: 0; }}
.titlebar {{ display:flex; align-items:center; justify-content:space-between; margin-bottom: 8mm; }}
.logo {{ font-weight: 800; font-size: 15pt; color: {d['ink']}; letter-spacing: -.02em; }}
.logo i {{ color: {d['m']}; font-style: normal; }}
.daychip {{ font-size: 10pt; font-weight: 800; letter-spacing: .12em; color: {d['m']};
  border: 2px solid {d['c']}; border-radius: 999px; padding: 2.5mm 7mm; }}

.cover {{ background: linear-gradient(135deg, {d['d']} 0%, {d['l']} 58%, {d['m']} 130%);
  color: #fff; }}
.cover .inner {{ height: 297mm; position: relative; z-index: 2; display: flex;
  flex-direction: column; }}
.blob {{ position:absolute; border-radius: 50%; background: rgba(255,255,255,.07); }}
.blob.b1 {{ width: 90mm; height: 90mm; top: -20mm; right: -25mm; }}
.blob.b2 {{ width: 60mm; height: 60mm; bottom: 30mm; left: -18mm; }}
.cover .logo {{ color:#fff; }}
.cover .chip {{ font-size: 10pt; font-weight: 800; letter-spacing: .18em; opacity: .9; }}
.cover .spacer {{ flex: 1; }}
.cover .pitch {{ font-size: 15pt; line-height: 1.45; opacity: .92; font-weight: 500;
  max-width: 150mm; margin: 0 0 10mm; }}
.cover .kicker {{ font-size: 11pt; letter-spacing: .3em; text-transform: uppercase;
  opacity: .75; font-weight: 700; margin-bottom: 6mm; }}
.cover h1 {{ font-size: 34pt; line-height: 1.05; margin: 0 0 8mm; }}
.stats {{ display:flex; gap: 6mm; margin-top: 4mm; }}
.stat {{ flex: 1; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25);
  border-radius: 6mm; padding: 6mm 7mm; }}
.stat b {{ display:block; font-size: 24pt; letter-spacing: -.02em; line-height: 1; }}
.stat span {{ font-size: 9.5pt; opacity: .85; }}

.pains {{ display:grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; margin: 10mm 0 0; }}
.pcard {{ background: #fff; border: 1.5px solid {d['c']}; border-radius: 6mm; padding: 8mm;
  font-size: 13pt; font-weight: 700; color: {d['ink']}; text-align: center; }}
.arrowdown {{ text-align: center; font-size: 20pt; color: {d['m']}; margin: 7mm 0 2mm; }}
.fixnote {{ text-align:center; font-size: 13pt; font-weight: 800; color:{d['m']}; }}
.wins {{ display:grid; grid-template-columns: repeat(3,1fr); gap: 6mm; margin-top: 6mm; }}
.wcard {{ background:#fff; border:1.5px solid {d['c']}; border-radius:6mm; padding: 7mm 6mm; }}
.wcard .ico {{ font-size: 24pt; }}
.wcard b {{ font-size: 13.5pt; display:block; margin: 3mm 0 1.5mm; }}
.wcard p {{ font-size: 10.5pt; color: {d['soft']}; line-height: 1.5; margin: 0; }}
.resume {{ margin-top: 8mm; background:#fff; border:1.5px solid {d['c']}; border-radius:6mm;
  padding: 6mm 8mm; }}
.resume b {{ font-size: 11.5pt; display:block; margin-bottom: 3mm; }}
.resume .bar {{ display:flex; gap: 2mm; }}
.resume .f {{ height: 7mm; border-radius: 999px; flex: 1; }}
.resume .cap {{ font-size: 9.5pt; color: {d['soft']}; margin-top: 2.5mm; display:block; }}

.gal {{ display:grid; gap: 6mm; margin-top: 4mm; text-align:center; }}
.gal.one {{ grid-template-columns: 1fr; }}
.gal.many {{ grid-template-columns: repeat(2, 1fr); }}
.gi {{ background:#fff; border:1.5px solid {d['c']}; border-radius:6mm; padding: 6mm; }}
.gi img {{ max-width: 100%; max-height: 150mm; }}
.gi.one img {{ max-height: 160mm; }}
.gi span {{ font-size: 9pt; color:{d['soft']}; display:block; margin-top:2mm; }}

.anatomy {{ display:flex; align-items:center; justify-content:center; gap: 3mm;
  flex-wrap: wrap; margin-top: 9mm; }}
.dot {{ background:{d['c']}; color:{d['ink']}; font-size: 10.5pt; font-weight: 700;
  border-radius: 999px; padding: 3.5mm 7mm; }}
.anatomy i {{ color:{d['m']}; font-style: normal; font-weight:800; }}

table {{ width: 100%; border-collapse: collapse; margin-top: 2mm; background:#fff;
  border-radius: 6mm; overflow: hidden; }}
th {{ background: {d['d']}; color: #fff; text-align: left; padding: 5mm 6mm;
  font-size: 11pt; }}
td {{ border-bottom: 1px solid #e8efec; padding: 4.5mm 6mm; font-size: 10.5pt;
  color: {d['ink']}; }}
tr:nth-child(even) td {{ background: {d['bg']}; }}
.tablecaption {{ font-size: 9.5pt; color:{d['soft']}; margin-top: 3mm; }}

.codecard {{ background: #0d1b26; border-radius: 6mm; padding: 8mm 9mm; margin-top: 2mm; }}
.codecard pre {{ margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
  font-size: 11pt; line-height: 1.6; color: #cfe6da; white-space: pre-wrap; }}
.codecard .kw {{ color: #7fd7c0; font-weight: 700; }}
.codecard .str {{ color: #f0c674; }}
.codecard .stamp {{ display:inline-block; margin-top: 4mm; font-size: 9pt; letter-spacing:.15em;
  text-transform: uppercase; color:#6b8f80; }}

.cta {{ background: linear-gradient(120deg, {d['d']}, {d['l']}); color:#fff;
  border-radius: 8mm; padding: 10mm 12mm; margin-top: 10mm; }}
.cta b {{ font-size: 16pt; display: block; }}
.cta p {{ font-size: 11.5pt; opacity: .92; margin: 3mm 0 0; line-height: 1.5; }}
.pill {{ display:inline-block; margin-top: 5mm; background: rgba(255,255,255,.16);
  border: 1px solid rgba(255,255,255,.4); border-radius: 999px; padding: 3mm 8mm;
  font-family: Consolas, monospace; font-size: 12pt; font-weight: 700; }}
.foot {{ display:flex; justify-content:space-between; align-items:center; margin-top: 10mm;
  padding-top: 5mm; border-top: 1px solid {d['c']}; font-size: 9.5pt; color:{d['soft']}; }}
.foot .logo {{ font-size: 12pt; }}
</style></head><body>

<!-- 1 · COVER -->
<div class="sheet cover"><div class="blob b1"></div><div class="blob b2"></div>
  <div class="inner">
    <div class="titlebar">
      <div class="logo"><i>w</i>pipe</div>
      <div class="chip">DAY {day_num} · LINKEDIN COMPANION</div>
    </div>
    <div class="spacer"></div>
    <div class="kicker">{esc(tech).upper()} pipelines, engineered</div>
    <h1>{esc(tech.title())}: {esc(tagline)}</h1>
    <p class="pitch">{esc(headline)}</p>
    <div class="stats">{metric_html}</div>
  </div>
</div>

<!-- 2 · THE SHIFT -->
<div class="sheet"><div class="inner">
  <div class="titlebar"><span class="eyebrow">The shift</span></div>
  <h2>Where it hurts today</h2>
  <p class="body">Three things quietly cost teams time and trust every single week.</p>
  <div class="pains">{pain_cards}</div>
  <div class="arrowdown">↓</div>
  <div class="fixnote">wpipe turns these into code you control.</div>
  <h2 style="margin-top:9mm">What you gain</h2>
  <div class="wins">{win_cards}</div>
  <div class="resume">
    <b>Crash at step 7? Resume from step 4.</b>
    <div class="bar">{resume_bar}</div>
    <span class="cap">Every step persists its state to SQLite WAL — a rerun cost you never pay again.</span>
  </div>
</div></div>

<!-- 3 · THE DIAGRAM -->
<div class="sheet"><div class="inner">
  <div class="titlebar"><span class="eyebrow">The architecture</span></div>
  <h2>One pipeline, fully instrumented</h2>
  <p class="body">State, retries, parallelism and audit — all inside the same run.</p>
  {img_html}
  <div class="anatomy">{anatomy}</div>
</div></div>

<!-- 4 · THE WINS -->
<div class="sheet"><div class="inner">
  <div class="titlebar"><span class="eyebrow">Side by side</span></div>
  <h2>wpipe vs. the status quo</h2>
  {table_html if table_html else '<div class="wins">' + win_cards + '</div>'}
  <div class="tablecaption">Based on what the engineering community hits daily.</div>
  <div class="cta">
    <b>Answers four questions in one run&nbsp;↘</b>
    <p>Did it run, how far, what failed, and can it resume? Yes, yes, exactly, and automatically.</p>
    <span class="pill">python my_pipeline.py</span>
  </div>
</div></div>

<!-- 5 · ACTION -->
<div class="sheet last"><div class="inner">
  <div class="titlebar"><span class="eyebrow">See it in action</span></div>
  <h2>Six lines. That’s the learning curve.</h2>
  <div class="codecard"><pre>{code_html}</pre>
    <span class="stamp">checkpoints · retries · timeout · parallel · tracker</span></div>
  <div class="wins" style="margin-top:9mm">{win_cards}</div>
  <div class="cta">
    <b>Try wpipe in your next pipeline</b>
    <p>Install the library, wrap your step, and watch checkpoints and docs appear by themselves.</p>
    <span class="pill">pip install wpipe</span>
  </div>
  <div class="foot"><span class="logo"><i>w</i>pipe</span>
    <span>Python-native orchestration · wpipe</span></div>
</div></div>

</body></html>"""
    return html


def main():
    folders = sorted(glob.glob(os.path.join(LINKEDIN, "dia*")))
    os.makedirs(TMP, exist_ok=True)
    ok, fail = [], []
    for folder in folders:
        day = os.path.basename(folder)
        out = os.path.join(folder, "companion.pdf")
        try:
            okp = render_pdf(build_html(day, folder), out)
            (ok if okp else fail).append(day)
            print(f"[{'OK' if okp else 'FAIL'}] {day}")
        except Exception as e:
            fail.append(day)
            print(f"[ERROR] {day}: {e}")
    print(f"\nDone: {len(ok)} generated, {len(fail)} failed.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())