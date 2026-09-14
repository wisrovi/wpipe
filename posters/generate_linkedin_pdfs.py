#!/usr/bin/env python3
"""Generate one modern companion PDF per LinkedIn day folder (visual-first, A6).

Strategy: LinkedIn readers skim. Each PDF is a compact card-deck on A6 —
one clean, airy idea per page, bigger type, minimal redundant graphics:

    1. Cover   — gradient, one-sentence pitch, key stat
    2. Pains   — the real problems (three cards)
    3. Wins    — what wpipe gives you (three icon cards)
    4. Diagram — the architecture, large
    5. Compare — the table (only when the post has one)
    6. Code    — the tiny learning curve
    7. Action  — soft CTA + footer

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
    ("📦", "Code-first", "Pipelines are Python — versionable, testable."),
    ("🧭", "Resume, don't restart", "Every step checkpoints to the WAL."),
    ("🪶", "Featherweight", "<50 MB. No broker, no daemon."),
]

METRICS = [("+117k", "downloads"), ("<50 MB", "RAM, total"), ("SQLite", "WAL state")]

TECH_CODE = {
    "n8n": "from wpipe import Pipeline, step\n\n@step(name=\"ingest\", retry_count=3)\ndef ingest(data):\n    return {\"rows\": data[\"payload\"]}\n\npipe = Pipeline(pipeline_name=\"from_n8n\")\npipe.set_steps([ingest])",
    "Zapier": "from wpipe import Pipeline, step\n\n@step(name=\"sync\", retry_count=3, retry_delay=5)\ndef sync(data):\n    return {\"done\": push_crm(data[\"lead\"])}\n\npipe = Pipeline(pipeline_name=\"zap2wpipe\")",
    "Make": "from wpipe import Pipeline, step, Parallel\n\n@step(name=\"a\", retry_count=3)\ndef a(d):\n    return {\"a\": d[\"x\"]}\n\n@step(name=\"b\", retry_count=3)\ndef b(d):\n    return {\"b\": d[\"y\"]}",
    "Airflow": "from wpipe import Pipeline, step\n\n@step(name=\"job\", retry_count=3, retry_delay=2)\ndef job(data):\n    return {\"ok\": run(data[\"job\"])}\n\npipe = Pipeline(pipeline_name=\"airflow_like\")",
    "Prefect": "from wpipe import Pipeline, step\n\n@step(name=\"resume_me\", checkpoint=True)\ndef resume_me(data):\n    return {\"state\": hydrate(data[\"cursor\"])}",
    "Luigi": "from wpipe import Pipeline, step\n\n@step(name=\"build\", retry_count=2, retry_delay=5)\ndef build(data):\n    return {\"out\": compile_targets(data[\"src\"])}",
    "Dagster": "from wpipe import Pipeline, step\n\n@step(name=\"core\", version=\"v2.1\")\ndef core(data):\n    return {\"v\": process(data[\"row\"])}",
    "Celery": "from wpipe import Pipeline, step\n\n@step(name=\"job\", retry_count=3, retry_delay=1)\ndef job(data):\n    return {\"result\": worker(data[\"task\"])}",
    "Cron": "from wpipe import Pipeline, step\n\n@step(name=\"job\", retry_count=3, retry_delay=10)\ndef job(data):\n    return {\"done\": run(data[\"command\"])}\n\npipe = Pipeline(pipeline_name=\"cron_pro\")",
}

DEFAULT_CODE = ("from wpipe import Pipeline, step\n\n"
                "@step(name=\"my_step\", retry_count=3, retry_delay=2, checkpoint=True)\n"
                "def my_step(data):\n    return {\"result\": process(data[\"input\"])}\n\n"
                "pipe = Pipeline(pipeline_name=\"my_pipeline\")\npipe.set_steps([my_step])")

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


def short_text(s, n=42):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


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
            if rows and len(rows[0]) <= 4:
                return rows
    return None


def highlight_code(code):
    out = esc(code)
    out = re.sub(r'(&quot;.*?&quot;)', r'<span class="str">\1</span>', out)
    kw_pairs = ["from wpipe import", "@step(", "Parallel(", "Pipeline(", "def ",
                "run(", "set_steps(", "retry_count", "retry_delay", "checkpoint",
                "tracking_db", "version="]
    for token in kw_pairs:
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
    if len(headline) > 90:
        headline = headline[:87].rstrip() + "…"

    pains = PAINS.get(tech, PAINS["wpipe"])
    tagline = TAGLINES.get(tech, TAGLINES["wpipe"])
    code = TECH_CODE.get(tech, DEFAULT_CODE)
    table = extract_table(txt)
    imgs = fetch_images(folder, tech, f"{day}_{tech}")

    pain_cards = "".join(f'<div class="pcard">{esc(p)}</div>' for p in pains[:3])
    win_cards = "".join(f'<div class="wcard"><span class="ico">{w[0]}</span>'
                        f"<div><b>{w[1]}</b><p>{w[2]}</p></div></div>" for w in WINS[:3])
    metric_html = "".join(f'<div class="stat"><b>{m[0]}</b><span>{m[1]}</span></div>' for m in METRICS)

    table_html = ""
    if table:
        head = table[0]
        body = table[1:][:4]
        thead = "<tr>" + "".join(f"<th>{esc(c)}</th>" for c in head) + "</tr>"
        body_html = "".join(
            "<tr>" + "".join(f"<td>{esc(short_text(c, 42))}</td>" for c in r) + "</tr>"
            for r in body)
        table_html = f'<table><thead>{thead}</thead><tbody>{body_html}</tbody></table>'

    dia_pages = ""
    if imgs:
        for p in imgs[:10]:
            dia_pages += f"""<div class="sheet"><div class="inner cardpage">
  <div class="titlebar"><span class="logo"><i>w</i>pipe</span><span class="daychip">DAY {day_num}</span></div>
  <div class="eyebrow">The architecture</div>
  <h2>One pipeline, fully instrumented</h2>
  <div class="figblock"><div class="figwrap"><div class="fig"><img src="file://{p}"/></div></div>
  <p class="cap">State, retries and audit — inside a single run.</p></div>
  </div></div>"""
    code_html = highlight_code(code)
    d = pal

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<style>
@page {{ size: 105mm 148mm; margin: 0; }}
* {{ box-sizing: border-box; }}
body, html {{ margin: 0; padding: 0; font-family: -apple-system, 'Segoe UI', Roboto,
  'Helvetica Neue', Arial, sans-serif; color: {d['ink']}; }}
.sheet {{ width: 105mm; min-height: 145mm; page-break-after: always;
  position: relative; background: {d['bg']}; }}
.sheet.last {{ page-break-after: auto; }}
.cover {{ height: 148mm; overflow: hidden; }}
.inner {{ padding: 15mm 13mm 0; }}
.cardpage {{ padding-bottom: 7mm; }}
.pains, .wins {{ display: flex; flex-direction: column; gap: 2.5mm; margin-top: 1mm; }}
table, .codecard, .cta, .titlebar, .cap, .foot, .pcard, .wcard {{ break-inside: avoid; }}
.eyebrow {{ display: inline-block; font-size: 9.5pt; letter-spacing: .22em; font-weight: 700;
  text-transform: uppercase; color: {d['m']}; margin-bottom: 3mm; }}
h1 {{ font-size: 30pt; line-height: 1.06; margin: 0 0 6mm; letter-spacing: -.01em; }}
h2 {{ font-size: 19.5pt; line-height: 1.12; margin: 0 0 4mm; letter-spacing: -.01em;
  color: {d['ink']}; }}
p.body {{ font-size: 13.5pt; line-height: 1.6; color: {d['soft']}; margin: 0 0 5mm; }}
.titlebar {{ display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 4mm; }}
.logo {{ font-weight: 800; font-size: 14pt; color: {d['ink']}; letter-spacing: -.02em; }}
.logo i {{ color: {d['m']}; font-style: normal; }}
.daychip {{ font-size: 8.5pt; font-weight: 800; letter-spacing: .12em; color: {d['m']};
  border: 1.5px solid {d['c']}; border-radius: 999px; padding: 1.8mm 4.5mm; }}

.cover {{ background: linear-gradient(135deg, {d['d']} 0%, {d['l']} 58%, {d['m']} 130%);
  color: #fff; }}
.cover .inner {{ height: 148mm; position: relative; z-index: 2; display: flex;
  flex-direction: column; }}
.blob {{ position: absolute; border-radius: 50%; background: rgba(255,255,255,.07); }}
.blob.b1 {{ width: 52mm; height: 52mm; top: -14mm; right: -18mm; }}
.blob.b2 {{ width: 34mm; height: 34mm; bottom: 24mm; left: -12mm; }}
.cover .logo {{ color: #fff; }}
.cover .spacer {{ flex: 1; }}
.cover .kicker {{ font-size: 9.5pt; letter-spacing: .28em; text-transform: uppercase;
  opacity: .8; font-weight: 700; margin-bottom: 5mm; }}
.cover h1 {{ font-size: 27pt; line-height: 1.05; margin: 0 0 7mm; }}
.cover .pitch {{ font-size: 14pt; line-height: 1.4; opacity: .94; font-weight: 500;
  margin: 0 0 7mm; }}
.stats {{ display: flex; gap: 3mm; }}
.stat {{ flex: 1; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.28);
  border-radius: 4mm; padding: 3.5mm 4mm; }}
.stat b {{ display: block; font-size: 15pt; line-height: 1; letter-spacing: -.02em; }}
.stat span {{ font-size: 7.5pt; opacity: .85; }}

.pcard {{ background: #fff; border: 1.5px solid {d['c']}; border-radius: 4mm;
  padding: 5mm 6mm; font-size: 13.5pt; font-weight: 700; color: {d['ink']}; }}

.wcard {{ display: flex; align-items: center; gap: 4mm; background: #fff;
  border: 1.5px solid {d['c']}; border-radius: 4mm; padding: 4.5mm 5.5mm; }}
.wcard .ico {{ font-size: 16pt; }}
.wcard b {{ font-size: 12.5pt; display: block; }}
.wcard p {{ font-size: 9.5pt; color: {d['soft']}; line-height: 1.4; margin: 0.5mm 0 0; }}

.figwrap {{ margin: 2mm 0 0; }}
.figblock {{ break-inside: avoid; }}
.fig {{ height: 68mm; display: flex; align-items: center; justify-content: center;
  background: #fff; border: 1.5px solid {d['c']}; border-radius: 4mm; padding: 2mm; }}
.fig img {{ max-width: 100%; max-height: 100%; }}
.cap {{ font-size: 8.5pt; color: {d['soft']}; text-align: center; margin-top: 2.5mm;
  line-height: 1.4; }}

table {{ width: 100%; border-collapse: collapse; margin-top: 1mm; background: #fff;
  border-radius: 4mm; overflow: hidden; }}
th {{ background: {d['d']}; color: #fff; text-align: left; padding: 3mm 3.5mm;
  font-size: 8.5pt; }}
td {{ border-bottom: 1px solid #e8efec; padding: 2.5mm 3.5mm; font-size: 8pt;
  color: {d['ink']}; line-height: 1.35; }}
tr:nth-child(even) td {{ background: {d['bg']}; }}

.codecard {{ background: #0d1b26; border-radius: 4mm; padding: 6mm 7mm; margin-top: 1mm; }}
.codecard pre {{ margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
  font-size: 9.5pt; line-height: 1.55; color: #cfe6da; white-space: pre-wrap; }}
.codecard .kw {{ color: #7fd7c0; font-weight: 700; }}
.codecard .str {{ color: #f0c674; }}
.codecard .stamp {{ display: inline-block; margin-top: 3.5mm; font-size: 7.5pt;
  letter-spacing: .15em; text-transform: uppercase; color: #6b8f80; }}

.cta {{ background: linear-gradient(120deg, {d['d']}, {d['l']}); color: #fff;
  border-radius: 6mm; padding: 8mm 9mm; margin-top: 9mm; }}
.cta b {{ font-size: 17pt; display: block; line-height: 1.15; }}
.cta p {{ font-size: 12pt; opacity: .92; margin: 3.5mm 0 0; line-height: 1.5; }}
.pill {{ display: inline-block; margin-top: 5mm; background: rgba(255,255,255,.16);
  border: 1px solid rgba(255,255,255,.4); border-radius: 999px; padding: 2.5mm 7mm;
  font-family: Consolas, monospace; font-size: 11.5pt; font-weight: 700; }}
.foot {{ display: flex; justify-content: space-between; align-items: center; margin-top: 9mm;
  padding-top: 4mm; border-top: 1px solid {d['c']}; font-size: 9pt; color: {d['soft']}; }}
.foot .logo {{ font-size: 11pt; }}
</style></head><body>

<!-- 1 · COVER -->
<div class="sheet cover"><div class="blob b1"></div><div class="blob b2"></div>
  <div class="inner">
    <div class="titlebar">
      <div class="logo"><i>w</i>pipe</div>
      <div class="chip" style="font-size:9pt;font-weight:800;letter-spacing:.18em;opacity:.9">DAY {day_num}</div>
    </div>
    <div class="spacer"></div>
    <div class="kicker">{esc(tech.upper())} pipelines, engineered</div>
    <h1>{esc(tech.title())}: {esc(tagline)}</h1>
    <p class="pitch">{esc(headline)}</p>
    <div class="stats">{metric_html}</div>
  </div>
</div>

<!-- 2 · PAINS -->
<div class="sheet"><div class="inner cardpage">
  <div class="titlebar"><span class="logo"><i>w</i>pipe</span><span class="daychip">DAY {day_num}</span></div>
  <div class="eyebrow">The context</div>
  <h2>Where it hurts today</h2>
  <div class="pains">{pain_cards}</div>
</div></div>

<!-- 3 · WINS -->
<div class="sheet"><div class="inner cardpage">
  <div class="titlebar"><span class="logo"><i>w</i>pipe</span><span class="daychip">DAY {day_num}</span></div>
  <div class="eyebrow">The shift</div>
  <h2>What you gain</h2>
  <div class="wins">{win_cards}</div>
</div></div>

{dia_pages}
{('<div class="sheet"><div class="inner cardpage">'
  '<div class="titlebar"><span class="logo"><i>w</i>pipe</span><span class="daychip">DAY ' + day_num + '</span></div>'
  '<div class="eyebrow">Side by side</div><h2>wpipe vs. the status quo</h2>'
  + table_html + '</div></div>') if table_html else ''}

<!-- CODE -->
<div class="sheet"><div class="inner cardpage">
  <div class="titlebar"><span class="logo"><i>w</i>pipe</span><span class="daychip">DAY {day_num}</span></div>
  <div class="eyebrow">See it in action</div>
  <h2>Six lines. That’s it.</h2>
  <div class="codecard"><pre>{code_html}</pre>
    <span class="stamp">checkpoints · retries · timeout · parallel · tracker</span></div>
</div></div>

<!-- ACTION -->
<div class="sheet last"><div class="inner cardpage">
  <div class="cta">
    <b>Try wpipe in your next pipeline ↙</b>
    <p>Install the library, wrap your step — checkpoints and docs appear by themselves.</p>
    <span class="pill">pip install wpipe</span>
  </div>
  <div class="foot"><span class="logo"><i>w</i>pipe</span>
    <span>Python-native orchestration</span></div>
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