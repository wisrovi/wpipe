"""
wpipe Dashboard - Enterprise-grade pipeline visualization
"""

from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from wpipe.tracking import PipelineTracker


def create_app(
    db_path: str = "pipeline.db",
    config_dir: Optional[str] = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="wpipe Dashboard")

    @app.get("/")
    async def root():
        return HTMLResponse(get_dashboard_html(db_path, config_dir))

    @app.get("/api/stats")
    async def get_stats():
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_stats()

    @app.get("/api/pipelines")
    async def get_pipelines(status: Optional[str] = None):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipelines(status=status)

    @app.get("/api/pipelines/{pipeline_id}")
    async def get_pipeline(pipeline_id: str):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipeline(pipeline_id)

    @app.get("/api/pipelines/{pipeline_id}/graph")
    async def get_pipeline_graph(pipeline_id: str):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipeline_graph(pipeline_id)

    @app.get("/api/pipelines/{pipeline_id}/yaml")
    async def get_pipeline_yaml(pipeline_id: str):
        tracker = PipelineTracker(db_path, config_dir)
        pipeline = tracker.get_pipeline(pipeline_id)
        if pipeline and pipeline.get("config_yaml"):
            yaml_path = Path(pipeline["config_yaml"])
            if not yaml_path.exists() and config_dir:
                yaml_path = Path(config_dir) / f"{pipeline_id}.yaml"
            if not yaml_path.exists() and config_dir:
                yaml_path = Path(config_dir).resolve() / f"{pipeline_id}.yaml"
            if yaml_path.exists():
                return yaml_path.read_text(encoding="utf-8")
        return {"error": "YAML not found"}

    @app.get("/api/trends")
    async def get_trends(days: int = 7, pipeline_name: Optional[str] = None):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_trend_data(days=days, pipeline_name=pipeline_name)

    @app.get("/api/alerts")
    async def get_alerts(limit: int = 50, severity: Optional[str] = None):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_fired_alerts(limit=limit, severity=severity)

    @app.get("/api/alerts/config")
    async def get_alert_config():
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_alert_thresholds()

    @app.get("/api/events")
    async def get_events(pipeline_id: Optional[str] = None, limit: int = 50):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_events(pipeline_id=pipeline_id, limit=limit)

    @app.get("/api/slow-steps")
    async def get_slow_steps(limit: int = 10):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_top_slow_steps(limit=limit)

    @app.post("/api/alerts/{alert_id}/acknowledge")
    async def acknowledge_alert(alert_id: int):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.acknowledge_alert(alert_id)

    @app.get("/api/health")
    async def health_check():
        return {"status": "healthy", "db": db_path}

    return app


def get_dashboard_html(db_path: str, config_dir: Optional[str] = None) -> str:
    """Generate the complete dashboard HTML."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>wpipe Dashboard | Pipeline Intelligence</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <style>
        :root{{
            --bg-dark:#030712;--bg-primary:#0a0f1e;--bg-secondary:#111827;--bg-tertiary:#1f2937;--bg-elevated:#1a2234;
            --bg-card:rgba(17,24,39,0.95);--bg-glass:rgba(10,15,30,0.92);
            --text-primary:#f8fafc;--text-secondary:#cbd5e1;--text-muted:#64748b;--text-dim:#475569;
            --accent-primary:#6366f1;--accent-primary-hover:#818cf8;--accent-blue:#3b82f6;
            --accent-emerald:#10b981;--accent-amber:#f59e0b;--accent-rose:#f43f5e;--accent-cyan:#06b6d4;
            --accent-purple:#8b5cf6;--accent-pink:#ec4899;
            --gradient-primary:linear-gradient(135deg,#6366f1,#8b5cf6);--gradient-success:linear-gradient(135deg,#10b981,#34d399);
            --gradient-danger:linear-gradient(135deg,#f43f5e,#fb7185);--gradient-info:linear-gradient(135deg,#3b82f6,#60a5fa);
            --border-subtle:rgba(148,163,184,0.1);--border-default:rgba(148,163,184,0.15);--border-strong:rgba(148,163,184,0.25);
            --shadow-sm:0 1px 2px rgba(0,0,0,0.3);--shadow-md:0 4px 6px rgba(0,0,0,0.4);--shadow-lg:0 10px 25px rgba(0,0,0,0.5);
            --shadow-glow:0 0 40px rgba(99,102,241,0.15);--shadow-card:0 8px 32px rgba(0,0,0,0.4);
            --radius-sm:6px;--radius-md:10px;--radius-lg:14px;--radius-xl:20px;--radius-full:9999px;
            --font-sans:'Inter',system-ui,sans-serif;--font-mono:'JetBrains Mono',monospace;--font-display:'Space Grotesk',sans-serif;
            --transition-fast:0.15s ease;--transition-normal:0.25s ease;--transition-slow:0.4s cubic-bezier(0.4,0,0.2,1);
        }}
        
        *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
        
        html{{font-size:15px;scroll-behavior:smooth}}
        
        body{{
            font-family:var(--font-sans);background:var(--bg-dark);color:var(--text-primary);
            min-height:100vh;line-height:1.6;overflow-x:hidden
        }}
        
        body::before{{
            content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
            background: 
                radial-gradient(ellipse 80% 50% at 20% -10%,rgba(99,102,241,0.15) 0%,transparent 50%),
                radial-gradient(ellipse 60% 40% at 80% 110%,rgba(139,92,246,0.1) 0%,transparent 50%),
                radial-gradient(ellipse 40% 30% at 50% 50%,rgba(6,182,212,0.05) 0%,transparent 50%);
        }}
        
        /* ===== HEADER ===== */
        .header{{
            position:sticky;top:0;z-index:100;background:var(--bg-glass);
            backdrop-filter:blur(24px) saturate(180%);border-bottom:1px solid var(--border-subtle);
            box-shadow:0 4px 30px rgba(0,0,0,0.3)
        }}
        
        .header-inner{{
            max-width:1800px;margin:0 auto;padding:0.75rem 2rem;display:flex;
            align-items:center;justify-content:space-between;gap:1.5rem
        }}
        
        .brand{{display:flex;align-items:center;gap:1rem}}
        
        .brand-logo{{
            width:48px;height:48px;background:var(--gradient-primary);border-radius:var(--radius-lg);
            display:grid;place-items:center;font-size:1.5rem;box-shadow:0 4px 20px rgba(99,102,241,0.4);
            animation:pulse-glow 3s ease-in-out infinite
        }}
        
        @keyframes pulse-glow{{
            0%,100%{{box-shadow:0 4px 20px rgba(99,102,241,0.4)}}
            50%{{box-shadow:0 4px 30px rgba(99,102,241,0.6)}}
        }}
        
        .brand-text h1{{
            font-family:var(--font-display);font-size:1.5rem;font-weight:700;
            background:linear-gradient(135deg,#f8fafc,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent
        }}
        
        .brand-text span{{
            font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:3px;font-weight:500
        }}
        
        .header-search{{flex:1;max-width:400px;position:relative}}
        
        .header-search input{{
            width:100%;background:var(--bg-tertiary);border:1px solid var(--border-default);
            border-radius:var(--radius-full);padding:0.6rem 1rem 0.6rem 2.75rem;
            color:var(--text-primary);font-size:0.9rem;outline:none;transition:var(--transition-fast)
        }}
        
        .header-search input:focus{{border-color:var(--accent-primary);box-shadow:0 0 0 3px rgba(99,102,241,0.15)}}
        
        .header-search input::placeholder{{color:var(--text-muted)}}
        
        .header-search i{{position:absolute;left:1rem;top:50%;transform:translateY(-50%);color:var(--text-muted)}}
        
        .header-actions{{display:flex;align-items:center;gap:0.75rem}}
        
        .db-status{{
            display:flex;align-items:center;gap:0.5rem;background:var(--bg-tertiary);
            border:1px solid var(--border-default);border-radius:var(--radius-full);
            padding:0.4rem 0.9rem;font-size:0.8rem;color:var(--text-muted)
        }}
        
        .db-status .dot{{
            width:8px;height:8px;background:var(--accent-emerald);border-radius:50%;
            animation:pulse-dot 2s infinite
        }}
        
        @keyframes pulse-dot{{0%,100%{{opacity:1}}50%{{opacity:0.5}}}}
        
        .btn{{
            display:inline-flex;align-items:center;gap:0.5rem;padding:0.5rem 1rem;
            border-radius:var(--radius-full);font-size:0.85rem;font-weight:500;cursor:pointer;
            transition:var(--transition-fast);border:none;font-family:inherit
        }}
        
        .btn-primary{{
            background:var(--gradient-primary);color:white;
            box-shadow:0 2px 12px rgba(99,102,241,0.35)
        }}
        
        .btn-primary:hover{{transform:translateY(-1px);box-shadow:0 4px 20px rgba(99,102,241,0.5)}}
        
        .btn-ghost{{background:var(--bg-tertiary);color:var(--text-secondary);border:1px solid var(--border-default)}}
        
        .btn-ghost:hover{{background:var(--bg-elevated);color:var(--text-primary);border-color:var(--border-strong)}}
        
        .lang-select{{
            background:var(--bg-tertiary);color:var(--text-primary);border:1px solid var(--border-default);
            padding:0.4rem 0.75rem;border-radius:var(--radius-full);font-size:0.8rem;
            cursor:pointer;outline:none
        }}
        
        /* ===== MAIN LAYOUT ===== */
        .container{{
            position:relative;z-index:1;max-width:1800px;margin:0 auto;
            padding:1.5rem 2rem 3rem
        }}
        
        /* ===== STATS GRID ===== */
        .stats-grid{{
            display:grid;grid-template-columns:repeat(6,1fr);gap:1rem;margin-bottom:1.5rem
        }}
        
        @media(max-width:1400px){{.stats-grid{{grid-template-columns:repeat(3,1fr)}}}}
        @media(max-width:768px){{.stats-grid{{grid-template-columns:repeat(2,1fr)}}}}
        
        .stat-card{{
            background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-xl);
            padding:1.25rem;position:relative;overflow:hidden;
            transition:var(--transition-normal)
        }}
        
        .stat-card::before{{
            content:'';position:absolute;top:0;left:0;right:0;height:3px;
            background:var(--gradient-primary);opacity:0;transition:var(--transition-normal)
        }}
        
        .stat-card:hover{{transform:translateY(-2px);box-shadow:var(--shadow-card);border-color:var(--border-strong)}}
        
        .stat-card:hover::before{{opacity:1}}
        
        .stat-card.blue::before{{background:linear-gradient(90deg,#3b82f6,#60a5fa)}}
        .stat-card.green::before{{background:linear-gradient(90deg,#10b981,#34d399)}}
        .stat-card.purple::before{{background:linear-gradient(90deg,#8b5cf6,#a78bfa)}}
        .stat-card.cyan::before{{background:linear-gradient(90deg,#06b6d4,#22d3ee)}}
        .stat-card.amber::before{{background:linear-gradient(90deg,#f59e0b,#fbbf24)}}
        .stat-card.rose::before{{background:linear-gradient(90deg,#f43f5e,#fb7185)}}
        
        .stat-icon{{
            width:44px;height:44px;border-radius:var(--radius-lg);display:grid;
            place-items:center;margin-bottom:0.75rem;font-size:1.1rem
        }}
        
        .stat-icon.blue{{background:rgba(59,130,246,0.15);color:#60a5fa}}
        .stat-icon.green{{background:rgba(16,185,129,0.15);color:#34d399}}
        .stat-icon.purple{{background:rgba(139,92,246,0.15);color:#a78bfa}}
        .stat-icon.cyan{{background:rgba(6,182,212,0.15);color:#22d3ee}}
        .stat-icon.amber{{background:rgba(245,158,11,0.15);color:#fbbf24}}
        .stat-icon.rose{{background:rgba(244,63,94,0.15);color:#fb7185}}
        
        .stat-value{{
            font-family:var(--font-display);font-size:2rem;font-weight:700;margin-bottom:0.15rem;
            background:linear-gradient(135deg,#f8fafc,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent
        }}
        
        .stat-label{{font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;font-weight:500}}
        
        .stat-trend{{
            display:inline-flex;align-items:center;gap:0.25rem;font-size:0.75rem;margin-top:0.5rem;
            padding:0.2rem 0.5rem;border-radius:var(--radius-full)
        }}
        
        .stat-trend.up{{background:rgba(16,185,129,0.15);color:#34d399}}
        .stat-trend.down{{background:rgba(244,63,94,0.15);color:#fb7185}}
        
        /* ===== MAIN GRID ===== */
        .main-grid{{
            display:grid;grid-template-columns:1fr 380px;gap:1.5rem
        }}
        
        @media(max-width:1200px){{.main-grid{{grid-template-columns:1fr}}}}
        
        .left-panel{{min-width:0}}
        .right-panel{{min-width:0}}
        
        /* ===== TABS ===== */
        .tabs{{
            display:flex;gap:0.5rem;margin-bottom:1rem;background:var(--bg-tertiary);
            padding:0.35rem;border-radius:var(--radius-lg);width:fit-content
        }}
        
        .tab{{
            padding:0.6rem 1.25rem;border-radius:var(--radius-md);font-size:0.85rem;
            font-weight:500;cursor:pointer;color:var(--text-muted);background:none;border:none;
            transition:var(--transition-fast);display:flex;align-items:center;gap:0.5rem
        }}
        
        .tab:hover{{color:var(--text-primary);background:var(--bg-elevated)}}
        
        .tab.active{{
            background:var(--gradient-primary);color:white;
            box-shadow:0 2px 12px rgba(99,102,241,0.4)
        }}
        
        .tab .badge{{
            background:rgba(255,255,255,0.2);padding:0.1rem 0.5rem;border-radius:var(--radius-full);
            font-size:0.7rem;margin-left:0.25rem
        }}
        
        /* ===== CARDS ===== */
        .card{{
            background:var(--bg-card);border:1px solid var(--border-subtle);
            border-radius:var(--radius-xl);overflow:hidden
        }}
        
        .card-header{{
            padding:1rem 1.25rem;border-bottom:1px solid var(--border-subtle);
            display:flex;align-items:center;justify-content:space-between
        }}
        
        .card-title{{
            font-weight:600;font-size:0.95rem;display:flex;align-items:center;gap:0.5rem
        }}
        
        .card-title i{{color:var(--accent-primary)}}
        
        .card-body{{padding:1.25rem}}
        
        /* ===== GRAPH ===== */
        .graph-container{{
            background:linear-gradient(180deg,var(--bg-primary) 0%,var(--bg-secondary) 100%);
            border-radius:var(--radius-lg);min-height:380px;position:relative;
            border:1px solid var(--border-subtle);overflow:hidden
        }}
        
        .graph-svg{{width:100%;height:380px}}
        
        .graph-empty{{
            position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
            text-align:center;color:var(--text-muted)
        }}
        
        .graph-empty i{{font-size:4rem;opacity:0.2;margin-bottom:1rem;display:block}}
        
        .pipeline-info{{display:flex;align-items:center;gap:0.75rem}}
        
        .pipeline-id{{
            font-family:var(--font-mono);font-size:0.75rem;padding:0.25rem 0.6rem;
            background:rgba(6,182,212,0.15);color:#22d3ee;border-radius:var(--radius-full)
        }}
        
        /* ===== STEPS LIST ===== */
        .steps-section{{margin-top:1.25rem}}
        
        .steps-header{{
            font-size:0.9rem;font-weight:600;margin-bottom:0.75rem;
            display:flex;align-items:center;gap:0.5rem;color:var(--text-secondary)
        }}
        
        .steps-header i{{color:var(--accent-primary)}}
        
        .step-card{{
            background:var(--bg-secondary);border-radius:var(--radius-lg);margin-bottom:0.5rem;
            border:1px solid var(--border-subtle);overflow:hidden;transition:var(--transition-fast)
        }}
        
        .step-card:hover{{border-color:var(--border-strong)}}
        
        .step-card.expanded{{border-color:var(--accent-primary)}}
        
        .step-header{{
            padding:0.75rem 1rem;display:flex;align-items:center;gap:0.75rem;cursor:pointer
        }}
        
        .step-icon{{
            width:32px;height:32px;border-radius:var(--radius-md);display:grid;
            place-items:center;font-size:0.8rem
        }}
        
        .step-icon.completed{{background:rgba(16,185,129,0.2);color:#34d399}}
        .step-icon.error{{background:rgba(244,63,94,0.2);color:#fb7185}}
        .step-icon.running{{background:rgba(59,130,246,0.2);color:#60a5fa}}
        
        .step-info{{flex:1;min-width:0}}
        
        .step-name{{font-weight:500;font-size:0.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
        
        .step-meta{{display:flex;gap:0.75rem;font-size:0.75rem;color:var(--text-muted);margin-top:0.2rem}}
        
        .step-meta span{{display:flex;align-items:center;gap:0.25rem}}
        
        .step-chevron{{color:var(--text-muted);transition:transform 0.2s}}
        
        .step-card.expanded .step-chevron{{transform:rotate(180deg)}}
        
        .step-details{{display:none;padding:0 1rem 1rem;border-top:1px solid var(--border-subtle)}}
        
        .step-card.expanded .step-details{{display:block;animation:slideDown 0.2s ease}}
        
        @keyframes slideDown{{from{{opacity:0;transform:translateY(-10px)}}to{{opacity:1;transform:translateY(0)}}}}
        
        .data-panel{{
            margin-top:0.75rem;background:var(--bg-primary);border-radius:var(--radius-md);
            padding:0.75rem;border:1px solid var(--border-subtle)
        }}
        
        .data-panel-header{{
            font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;
            color:var(--text-muted);margin-bottom:0.5rem;font-weight:600
        }}
        
        .data-panel-header.input{{color:#60a5fa}}
        .data-panel-header.output{{color:#34d399}}
        
        .data-content{{
            font-family:var(--font-mono);font-size:0.75rem;color:var(--text-secondary);
            white-space:pre-wrap;word-break:break-all;max-height:200px;overflow-y:auto
        }}
        
        /* ===== ERROR BOX ===== */
        .error-box{{
            background:rgba(244,63,94,0.08);border:1px solid rgba(244,63,94,0.25);
            border-radius:var(--radius-lg);padding:1rem;margin-top:1rem
        }}
        
        .error-title{{
            display:flex;align-items:center;gap:0.5rem;color:#fb7185;font-weight:600;font-size:0.9rem;margin-bottom:0.5rem
        }}
        
        .error-content{{
            font-family:var(--font-mono);font-size:0.8rem;background:rgba(0,0,0,0.3);
            padding:0.75rem;border-radius:var(--radius-md);color:#fca5a5
        }}
        
        /* ===== YAML BOX ===== */
        .yaml-box{{
            background:var(--bg-primary);border:1px solid var(--border-subtle);
            border-radius:var(--radius-lg);padding:1rem;margin-top:1rem
        }}
        
        .yaml-title{{
            font-size:0.8rem;color:#22d3ee;font-weight:600;margin-bottom:0.5rem;
            display:flex;align-items:center;gap:0.5rem
        }}
        
        .yaml-content{{
            font-family:var(--font-mono);font-size:0.7rem;color:var(--text-secondary);
            white-space:pre-wrap;background:rgba(0,0,0,0.3);padding:0.75rem;
            border-radius:var(--radius-md);max-height:250px;overflow:auto
        }}
        
        /* ===== ALERTS ===== */
        .alert-item{{
            display:flex;align-items:flex-start;gap:0.75rem;padding:0.85rem;
            background:var(--bg-secondary);border-radius:var(--radius-lg);margin-bottom:0.5rem;
            border-left:3px solid
        }}
        
        .alert-item.critical{{border-left-color:var(--accent-rose)}}
        .alert-item.warning{{border-left-color:var(--accent-amber)}}
        .alert-item.info{{border-left-color:var(--accent-blue)}}
        
        .alert-icon{{width:32px;height:32px;border-radius:var(--radius-md);display:grid;place-items:center}}
        
        .alert-icon.critical{{background:rgba(244,63,94,0.15);color:#fb7185}}
        .alert-icon.warning{{background:rgba(245,158,11,0.15);color:#fbbf24}}
        
        .alert-content{{flex:1}}
        
        .alert-pipeline{{font-family:var(--font-mono);font-size:0.7rem;color:var(--text-muted)}}
        
        .alert-message{{font-size:0.85rem;color:var(--text-secondary);margin-top:0.25rem}}
        
        .alert-time{{font-size:0.7rem;color:var(--text-muted);margin-top:0.35rem}}
        
        /* ===== EVENTS TIMELINE ===== */
        .event-timeline{{position:relative;padding-left:1.5rem}}
        
        .event-timeline::before{{
            content:'';position:absolute;left:7px;top:0;bottom:0;width:2px;
            background:var(--border-default)
        }}
        
        .event-item{{position:relative;padding-bottom:1rem}}
        
        .event-item::before{{
            content:'';position:absolute;left:-1.35rem;top:0.25rem;width:10px;height:10px;
            background:var(--accent-purple);border-radius:50%;border:2px solid var(--bg-dark)
        }}
        
        .event-time{{font-size:0.7rem;color:var(--text-muted);margin-bottom:0.25rem}}
        
        .event-title{{font-size:0.85rem;font-weight:600}}
        
        .event-desc{{font-size:0.8rem;color:var(--text-muted);margin-top:0.15rem}}
        
        /* ===== PIPELINE LIST ===== */
        .pipeline-list{{
            display:flex;flex-direction:column;gap:0.5rem;max-height:calc(100vh - 280px);
            overflow-y:auto;padding-right:0.5rem
        }}
        
        .pipeline-list::-webkit-scrollbar{{width:4px}}
        .pipeline-list::-webkit-scrollbar-track{{background:transparent}}
        .pipeline-list::-webkit-scrollbar-thumb{{background:var(--bg-tertiary);border-radius:2px}}
        
        .pipeline-item{{
            background:var(--bg-secondary);border-radius:var(--radius-lg);padding:0.85rem 1rem;
            cursor:pointer;transition:var(--transition-fast);border:1px solid transparent
        }}
        
        .pipeline-item:hover{{background:var(--bg-elevated);border-color:var(--border-strong)}}
        
        .pipeline-item.active{{
            border-color:var(--accent-primary);background:rgba(99,102,241,0.08);
            box-shadow:0 0 0 1px var(--accent-primary),0 4px 20px rgba(99,102,241,0.2)
        }}
        
        .pipeline-top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:0.35rem}}
        
        .status-badge{{
            padding:0.2rem 0.6rem;border-radius:var(--radius-full);font-size:0.7rem;font-weight:600;
            text-transform:uppercase;letter-spacing:0.5px
        }}
        
        .status-badge.completed{{background:rgba(16,185,129,0.15);color:#34d399}}
        .status-badge.error{{background:rgba(244,63,94,0.15);color:#fb7185}}
        .status-badge.running{{background:rgba(59,130,246,0.15);color:#60a5fa}}
        .status-badge.pending{{background:rgba(245,158,11,0.15);color:#fbbf24}}
        
        .pipeline-name{{font-weight:600;font-size:0.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px}}
        
        .pipeline-meta{{display:flex;gap:0.85rem;font-size:0.7rem;color:var(--text-muted)}}
        
        .pipeline-meta span{{display:flex;align-items:center;gap:0.25rem}}
        
        .duration-tag{{color:var(--accent-purple);font-weight:500}}
        
        /* ===== FILTER CHIPS ===== */
        .filter-bar{{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:0.75rem}}
        
        .filter-chips{{display:flex;gap:0.4rem;flex-wrap:wrap}}
        
        .chip{{
            padding:0.35rem 0.85rem;border-radius:var(--radius-full);font-size:0.75rem;
            cursor:pointer;background:var(--bg-tertiary);color:var(--text-muted);
            border:1px solid transparent;transition:var(--transition-fast)
        }}
        
        .chip:hover{{border-color:var(--border-strong);color:var(--text-primary)}}
        
        .chip.active{{
            background:var(--accent-primary);color:white;
            box-shadow:0 2px 10px rgba(99,102,241,0.4)
        }}
        
        /* ===== LOADING ===== */
        .loading{{display:flex;align-items:center;justify-content:center;padding:2rem}}
        
        .spinner{{
            width:32px;height:32px;border:3px solid var(--border-default);
            border-top-color:var(--accent-primary);border-radius:50%;
            animation:spin 0.8s linear infinite
        }}
        
        @keyframes spin{{to{{transform:rotate(360deg)}}}}
        
        /* ===== EMPTY STATE ===== */
        .empty-state{{text-align:center;padding:3rem;color:var(--text-muted)}}
        
        .empty-state i{{font-size:3rem;opacity:0.2;margin-bottom:1rem;display:block}}
        
        /* ===== MODAL ===== */
        .modal-overlay{{
            display:none;position:fixed;inset:0;background:rgba(0,0,0,0.8);
            z-index:9998;align-items:center;justify-content:center;padding:1rem
        }}
        
        .modal-overlay.active{{display:flex}}
        
        .modal{{
            background:var(--bg-card);border:1px solid var(--border-subtle);
            border-radius:var(--radius-xl);max-width:750px;width:100%;max-height:90vh;
            overflow-y:auto;padding:2rem;box-shadow:0 25px 60px rgba(0,0,0,0.6)
        }}
        
        .modal-header{{
            display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem
        }}
        
        .modal-title{{
            font-family:var(--font-display);font-size:1.5rem;font-weight:700;
            background:linear-gradient(135deg,#f8fafc,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent
        }}
        
        .modal-close{{
            background:none;border:none;color:var(--text-muted);font-size:1.5rem;cursor:pointer
        }}
        
        /* ===== TOOLTIP ===== */
        #tooltip{{
            position:fixed;background:rgba(15,23,42,0.98);border:1px solid var(--border-strong);
            border-radius:10px;padding:12px 16px;color:#f8fafc;font-size:0.8rem;
            z-index:9999;pointer-events:none;box-shadow:0 10px 40px rgba(0,0,0,0.5);
            max-width:280px;white-space:pre-line;line-height:1.5;opacity:0;transition:opacity 0.15s
        }}
        
        #tooltip.visible{{opacity:1}}
        
        /* ===== CHART ===== */
        .chart-container{{position:relative;height:280px;margin-top:0.5rem}}
        
        /* ===== KEYBOARD HINTS ===== */
        kbd{{
            background:var(--bg-tertiary);border:1px solid var(--border-default);
            border-radius:4px;padding:0.1rem 0.4rem;font-size:0.7rem;
            font-family:var(--font-mono);color:var(--text-muted)
        }}
        
        /* ===== ANIMATIONS ===== */
        @keyframes fadeIn{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
        
        .animate-in{{animation:fadeIn 0.3s ease forwards}}
        
        .animate-delay-1{{animation-delay:0.1s;opacity:0}}
        .animate-delay-2{{animation-delay:0.2s;opacity:0}}
        .animate-delay-3{{animation-delay:0.3s;opacity:0}}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <div class="brand">
                <div class="brand-logo"><i class="fas fa-bolt"></i></div>
                <div class="brand-text">
                    <h1>wpipe</h1>
                    <span>Pipeline Intelligence</span>
                </div>
            </div>
            
            <div class="header-search">
                <i class="fas fa-search"></i>
                <input type="text" id="search-input" placeholder="Search pipelines... (Ctrl+K)" oninput="filterPipelinesBySearch(this.value)">
            </div>
            
            <div class="header-actions">
                <div class="db-status">
                    <span class="dot"></span>
                    <span id="db-status">Connected</span>
                </div>
                
                <select class="lang-select" id="lang-select" onchange="changeLanguage(this.value)">
                    <option value="en">🇺🇸 EN</option>
                    <option value="es">🇪🇸 ES</option>
                </select>
                
                <button class="btn btn-ghost" onclick="refreshData()" title="Refresh (R)">
                    <i class="fas fa-arrows-rotate"></i>
                </button>
                
                <button class="btn btn-primary" onclick="showTutorial()">
                    <i class="fas fa-rocket"></i> <span data-i18n="tutorial">Tutorial</span>
                </button>
            </div>
        </div>
    </header>

    <main class="container">
        <!-- Stats Row -->
        <div class="stats-grid">
            <div class="stat-card blue animate-in animate-delay-1">
                <div class="stat-icon blue"><i class="fas fa-diagram-project"></i></div>
                <div class="stat-value" id="s-total">-</div>
                <div class="stat-label" data-i18n="totalPipelines">Total Pipelines</div>
                <div class="stat-trend up" id="s-total-trend" style="display:none"></div>
            </div>
            <div class="stat-card green animate-in animate-delay-2">
                <div class="stat-icon green"><i class="fas fa-circle-check"></i></div>
                <div class="stat-value" id="s-success">-</div>
                <div class="stat-label" data-i18n="successRate">Success Rate</div>
            </div>
            <div class="stat-card purple animate-in animate-delay-3">
                <div class="stat-icon purple"><i class="fas fa-bolt"></i></div>
                <div class="stat-value" id="s-avg-time">-</div>
                <div class="stat-label" data-i18n="avgDuration">Avg Duration</div>
            </div>
            <div class="stat-card cyan">
                <div class="stat-icon cyan"><i class="fas fa-layer-group"></i></div>
                <div class="stat-value" id="s-steps">-</div>
                <div class="stat-label" data-i18n="totalSteps">Total Steps</div>
            </div>
            <div class="stat-card amber">
                <div class="stat-icon amber"><i class="fas fa-bell"></i></div>
                <div class="stat-value" id="s-alerts">-</div>
                <div class="stat-label" data-i18n="activeAlerts">Active Alerts</div>
            </div>
            <div class="stat-card rose">
                <div class="stat-icon rose"><i class="fas fa-circle-xmark"></i></div>
                <div class="stat-value" id="s-errors">-</div>
                <div class="stat-label" data-i18n="errors">Errors</div>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="main-grid">
            <!-- Left Panel -->
            <div class="left-panel">
                <!-- Tabs -->
                <div class="tabs">
                    <button class="tab active" data-tab="graph" onclick="switchTab('graph')">
                        <i class="fas fa-diagram-project"></i> <span data-i18n="graph">Graph</span>
                    </button>
                    <button class="tab" data-tab="timeline" onclick="switchTab('timeline')">
                        <i class="fas fa-chart-gantt"></i> <span data-i18n="timeline">Timeline</span>
                    </button>
                    <button class="tab" data-tab="analytics" onclick="switchTab('analytics')">
                        <i class="fas fa-chart-line"></i> <span data-i18n="analytics">Analytics</span>
                    </button>
                    <button class="tab" data-tab="alerts" onclick="switchTab('alerts')">
                        <i class="fas fa-bell"></i> <span data-i18n="alerts">Alerts</span>
                        <span class="badge" id="alert-badge" style="display:none"></span>
                    </button>
                    <button class="tab" data-tab="events" onclick="switchTab('events')">
                        <i class="fas fa-bookmark"></i> <span data-i18n="events">Events</span>
                    </button>
                </div>

                <!-- Tab Content: Graph -->
                <div id="tab-graph" class="tab-content">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title"><i class="fas fa-diagram-project"></i> <span data-i18n="executionGraph">Execution Graph</span></div>
                            <div class="pipeline-info" id="graph-pipeline-info"></div>
                        </div>
                        <div class="card-body">
                            <div class="graph-container">
                                <svg class="graph-svg" id="graph-svg">
                                    <defs>
                                        <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                            <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
                                        </marker>
                                        <linearGradient id="gSuccess" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stop-color="#10b981"/><stop offset="100%" stop-color="#059669"/>
                                        </linearGradient>
                                        <linearGradient id="gError" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stop-color="#ef4444"/><stop offset="100%" stop-color="#dc2626"/>
                                        </linearGradient>
                                        <linearGradient id="gRunning" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#2563eb"/>
                                        </linearGradient>
                                        <linearGradient id="gPending" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stop-color="#f59e0b"/><stop offset="100%" stop-color="#d97706"/>
                                        </linearGradient>
                                        <linearGradient id="gCondition" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#7c3aed"/>
                                        </linearGradient>
                                    </defs>
                                    <g id="graph-edges"></g>
                                    <g id="graph-nodes"></g>
                                </svg>
                                <div id="graph-empty" class="graph-empty">
                                    <i class="fas fa-diagram-project"></i>
                                    <p data-i18n="selectPipeline">Select a pipeline to visualize</p>
                                </div>
                            </div>

                            <div id="steps-section" class="steps-section" style="display:none">
                                <div class="steps-header"><i class="fas fa-list-check"></i> <span data-i18n="executionSteps">Execution Steps</span></div>
                                <div id="steps-list"></div>
                            </div>

                            <div id="error-panel" class="error-box" style="display:none">
                                <div class="error-title"><i class="fas fa-circle-exclamation"></i> <span id="error-step-name">Error</span></div>
                                <div id="error-content" class="error-content"></div>
                            </div>

                            <div id="yaml-panel" class="yaml-box" style="display:none">
                                <div class="yaml-title"><i class="fas fa-file-code"></i> <span data-i18n="yamlConfig">Configuration YAML</span></div>
                                <pre class="yaml-content" id="yaml-content"></pre>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab Content: Timeline -->
                <div id="tab-timeline" class="tab-content" style="display:none">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title"><i class="fas fa-chart-gantt"></i> <span data-i18n="executionTimeline">Execution Timeline</span></div>
                            <select id="timeline-filter" onchange="loadTimeline()" style="background:var(--bg-tertiary);color:var(--text-primary);border:1px solid var(--border-default);padding:0.35rem 0.75rem;border-radius:var(--radius-md);font-size:0.8rem;">
                                <option value="7">7 <span data-i18n="days">days</span></option>
                                <option value="14">14 <span data-i18n="days">days</span></option>
                                <option value="30">30 <span data-i18n="days">days</span></option>
                            </select>
                        </div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas id="timeline-chart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab Content: Analytics -->
                <div id="tab-analytics" class="tab-content" style="display:none">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title"><i class="fas fa-chart-pie"></i> <span data-i18n="analyticsOverview">Analytics Overview</span></div>
                        </div>
                        <div class="card-body">
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem">
                                <div>
                                    <h4 style="font-size:0.85rem;color:var(--text-muted);margin-bottom:0.75rem" data-i18n="statusDistribution">Status Distribution</h4>
                                    <div class="chart-container">
                                        <canvas id="pie-chart"></canvas>
                                    </div>
                                </div>
                                <div>
                                    <h4 style="font-size:0.85rem;color:var(--text-muted);margin-bottom:0.75rem" data-i18n="slowestSteps">Slowest Steps</h4>
                                    <div id="slow-steps-list"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab Content: Alerts -->
                <div id="tab-alerts" class="tab-content" style="display:none">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title"><i class="fas fa-bell"></i> <span data-i18n="pipelineAlerts">Pipeline Alerts</span></div>
                            <div class="filter-chips">
                                <span class="chip active" data-severity="" onclick="filterAlerts('')">All</span>
                                <span class="chip" data-severity="critical" onclick="filterAlerts('critical')">Critical</span>
                                <span class="chip" data-severity="warning" onclick="filterAlerts('warning')">Warning</span>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="alerts-list"></div>
                        </div>
                    </div>
                </div>

                <!-- Tab Content: Events -->
                <div id="tab-events" class="tab-content" style="display:none">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title"><i class="fas fa-bookmark"></i> <span data-i18n="pipelineEvents">Pipeline Events</span></div>
                        </div>
                        <div class="card-body">
                            <div class="event-timeline" id="events-list"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Panel: Pipeline List -->
            <div class="right-panel">
                <div class="filter-bar">
                    <div class="filter-chips">
                        <span class="chip active" data-status="" onclick="filterPipelines('')"><span data-i18n="all">All</span></span>
                        <span class="chip" data-status="completed" onclick="filterPipelines('completed')"><span data-i18n="completed">Completed</span></span>
                        <span class="chip" data-status="error" onclick="filterPipelines('error')"><span data-i18n="error">Error</span></span>
                        <span class="chip" data-status="running" onclick="filterPipelines('running')"><span data-i18n="running">Running</span></span>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-title"><i class="fas fa-list"></i> <span data-i18n="pipelines">Pipelines</span> <span id="pipeline-count" style="color:var(--text-muted);font-weight:normal;font-size:0.8rem"></span></div>
                    </div>
                    <div class="card-body" style="padding:0.75rem">
                        <div id="pipeline-list" class="pipeline-list">
                            <div class="loading"><div class="spinner"></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Tutorial Modal -->
    <div class="modal-overlay" id="tutorial-modal">
        <div class="modal" id="tutorial-content"></div>
    </div>

    <!-- Tooltip -->
    <div id="tooltip"></div>

    <script>
        // State
        let pipelines = [], selectedPipeline = null, currentFilter = '', searchQuery = '';
        let timelineChart = null, pieChart = null;
        
        // Translations
        const translations = {{
            en: {{
                tutorial: "Tutorial", refresh: "Refresh", all: "All", completed: "Completed",
                error: "Error", running: "Running", pending: "Pending", graph: "Graph",
                timeline: "Timeline", analytics: "Analytics", alerts: "Events", events: "Events",
                totalPipelines: "Total Pipelines", successRate: "Success Rate", avgDuration: "Avg Duration",
                activeAlerts: "Active Alerts", errors: "Errors", totalSteps: "Total Steps",
                selectPipeline: "Select a pipeline to visualize", executionGraph: "Execution Graph",
                executionSteps: "Execution Steps", yamlConfig: "Configuration YAML",
                pipelineAlerts: "Pipeline Alerts", pipelineEvents: "Pipeline Events",
                executionTimeline: "Execution Timeline", analyticsOverview: "Analytics Overview",
                statusDistribution: "Status Distribution", slowestSteps: "Slowest Steps",
                days: "days", noAlerts: "No alerts", noEvents: "No events", input: "INPUT", output: "OUTPUT",
                version: "Version", status: "Status", duration: "Duration", expression: "Expression",
                welcome: "Welcome to wpipe Dashboard",
                tutorialContent: `
                    <p style="color:var(--text-secondary);margin-bottom:1.5rem;font-size:0.95rem;line-height:1.7;">
                        This dashboard provides complete visibility into your pipeline executions with enterprise-grade features.
                    </p>
                    <div style="display:flex;flex-direction:column;gap:0.85rem">
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #3b82f6">
                            <strong style="color:#60a5fa">📊 Stats Cards</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Total pipelines, success rate, avg duration, steps, alerts, and errors at a glance.</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #8b5cf6">
                            <strong style="color:#a78bfa">🔀 Pipeline Graph</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Visual flow. Click nodes for details. Hover for step info. ◇ Diamond = Condition with TRUE/FALSE branches.</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #06b6d4">
                            <strong style="color:#22d3ee">📋 Pipeline List</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">All executions. Click to view. Use filters or search bar (Ctrl+K) to find specific pipelines.</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #10b981">
                            <strong style="color:#34d399">📝 Steps Details</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Expand any step to see INPUT/OUTPUT data, errors, and execution time.</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #f59e0b">
                            <strong style="color:#fbbf24">📑 Tabs</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Timeline: execution history | Analytics: pie chart & slow steps | Alerts: warnings | Events: annotations</p>
                        </div>
                    </div>
                    <div style="margin-top:1.5rem;padding:1rem;background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(139,92,246,0.1));border-radius:var(--radius-lg);text-align:center;border:1px solid rgba(99,102,241,0.2)">
                        <p style="color:var(--text-primary);font-weight:500">💡 <strong>Pro Tips</strong></p>
                        <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.5rem">
                            <kbd>Ctrl+K</kbd> Search | <kbd>R</kbd> Refresh | <kbd>Esc</kbd> Close
                        </p>
                    </div>
                `
            }},
            es: {{
                tutorial: "Tutorial", refresh: "Actualizar", all: "Todos", completed: "Completado",
                error: "Error", running: "Ejecutando", pending: "Pendiente", graph: "Grafo",
                timeline: "Línea de Tiempo", analytics: "Analíticas", alerts: "Alertas", events: "Eventos",
                totalPipelines: "Total Pipelines", successRate: "Tasa de Éxito", avgDuration: "Duración Promedio",
                activeAlerts: "Alertas Activas", errors: "Errores", totalSteps: "Total Pasos",
                selectPipeline: "Selecciona un pipeline", executionGraph: "Grafo de Ejecución",
                executionSteps: "Pasos de Ejecución", yamlConfig: "Configuración YAML",
                pipelineAlerts: "Alertas del Pipeline", pipelineEvents: "Eventos del Pipeline",
                executionTimeline: "Línea de Tiempo", analyticsOverview: "Resumen de Analíticas",
                statusDistribution: "Distribución de Estados", slowestSteps: "Pasos Más Lentos",
                days: "días", noAlerts: "Sin alertas", noEvents: "Sin eventos", input: "ENTRADA", output: "SALIDA",
                version: "Versión", status: "Estado", duration: "Duración", expression: "Expresión",
                welcome: "Bienvenido al Dashboard de wpipe",
                tutorialContent: `
                    <p style="color:var(--text-secondary);margin-bottom:1.5rem;font-size:0.95rem;line-height:1.7;">
                        Este dashboard proporciona visibilidad completa de sus ejecuciones con características de nivel empresarial.
                    </p>
                    <div style="display:flex;flex-direction:column;gap:0.85rem">
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #3b82f6">
                            <strong style="color:#60a5fa">📊 Tarjetas de Estadísticas</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Total pipelines, tasa de éxito, duración promedio, pasos, alertas y errores de un vistazo.</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #8b5cf6">
                            <strong style="color:#a78bfa">🔀 Grafo del Pipeline</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Flujo visual. Click para detalles. Hover para info. ◇ Diamante = Condición con ramas TRUE/FALSE.</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #06b6d4">
                            <strong style="color:#22d3ee">📋 Lista de Pipelines</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Todas las ejecuciones. Click para ver. Usa filtros o barra de búsqueda (Ctrl+K).</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #10b981">
                            <strong style="color:#34d399">📝 Detalles de Pasos</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Expande cualquier paso para ver datos de ENTRADA/SALIDA, errores y tiempo.</p>
                        </div>
                        <div style="background:var(--bg-secondary);padding:1rem;border-radius:var(--radius-lg);border-left:3px solid #f59e0b">
                            <strong style="color:#fbbf24">📑 Pestañas</strong>
                            <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.35rem">Timeline: historial | Analytics: gráfico circular y pasos lentos | Alerts: advertencias | Events: anotaciones</p>
                        </div>
                    </div>
                    <div style="margin-top:1.5rem;padding:1rem;background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(139,92,246,0.1));border-radius:var(--radius-lg);text-align:center;border:1px solid rgba(99,102,241,0.2)">
                        <p style="color:var(--text-primary);font-weight:500">💡 <strong>Consejos Pro</strong></p>
                        <p style="color:var(--text-muted);font-size:0.8rem;margin-top:0.5rem">
                            <kbd>Ctrl+K</kbd> Buscar | <kbd>R</kbd> Actualizar | <kbd>Esc</kbd> Cerrar
                        </p>
                    </div>
                `
            }}
        }};
        
        let currentLang = localStorage.getItem('wpipe_lang') || 'en';
        function t(key) {{ return translations[currentLang][key] || key; }}
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            document.getElementById('lang-select').value = currentLang;
            refreshData();
            setInterval(refreshData, 10000);
            
            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {{
                if (e.ctrlKey && e.key === 'k') {{
                    e.preventDefault();
                    document.getElementById('search-input').focus();
                }}
                if (e.key === 'r' && !e.ctrlKey && document.activeElement.tagName !== 'INPUT') {{
                    refreshData();
                }}
                if (e.key === 'Escape') {{
                    hideTutorial();
                }}
            }});
            
            // Auto show tutorial
            if (!localStorage.getItem('wpipe_tutorial_seen')) {{
                setTimeout(showTutorial, 1000);
            }}
        }});
        
        function changeLanguage(lang) {{
            currentLang = lang;
            localStorage.setItem('wpipe_lang', lang);
            document.getElementById('lang-select').value = lang;
            refreshData();
        }}
        
        // Refresh Data
        async function refreshData() {{
            try {{
                const [statsRes, pipelinesRes] = await Promise.all([
                    fetch('/api/stats'),
                    fetch('/api/pipelines?status=' + currentFilter)
                ]);
                const stats = await statsRes.json();
                pipelines = await pipelinesRes.json();
                
                // Apply search filter
                let filteredPipelines = pipelines;
                if (searchQuery) {{
                    const q = searchQuery.toLowerCase();
                    filteredPipelines = pipelines.filter(p => 
                        p.name.toLowerCase().includes(q) || p.id.toLowerCase().includes(q)
                    );
                }}
                
                // Update stats
                document.getElementById('s-total').textContent = stats.total_pipelines || 0;
                document.getElementById('s-success').textContent = (stats.success_rate || 0) + '%';
                document.getElementById('s-avg-time').textContent = fmtDuration(stats.avg_duration_ms || 0);
                document.getElementById('s-steps').textContent = stats.total_steps || 0;
                document.getElementById('s-alerts').textContent = stats.unacknowledged_alerts || 0;
                document.getElementById('s-errors').textContent = stats.errors || 0;
                
                // Alert badge
                const badge = document.getElementById('alert-badge');
                if (stats.unacknowledged_alerts > 0) {{
                    badge.style.display = 'inline';
                    badge.textContent = stats.unacknowledged_alerts;
                }} else {{
                    badge.style.display = 'none';
                }}
                
                // Render pipeline list
                renderPipelineList(filteredPipelines);
                
                // Auto select first
                if (filteredPipelines.length > 0 && !selectedPipeline) {{
                    selectPipeline(filteredPipelines[0].id);
                }}
                
            }} catch (e) {{
                console.error(e);
            }}
        }}
        
        function renderPipelineList(pls) {{
            const c = document.getElementById('pipeline-list');
            document.getElementById('pipeline-count').textContent = '(' + pls.length + ')';
            
            if (!pls || pls.length === 0) {{
                c.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>No pipelines found</p></div>';
                return;
            }}
            
            c.innerHTML = pls.map(p => `
                <div class="pipeline-item ${{selectedPipeline && selectedPipeline.id === p.id ? 'active' : ''}}" onclick="selectPipeline('${{p.id}}')">
                    <div class="pipeline-top">
                        <span class="pipeline-id">${{p.id}}</span>
                        <span class="status-badge ${{p.status}}">${{p.status}}</span>
                    </div>
                    <div class="pipeline-name">${{p.name}}</div>
                    <div class="pipeline-meta">
                        <span><i class="fas fa-clock"></i> ${{fmtTime(p.started_at)}}</span>
                        <span class="duration-tag"><i class="fas fa-stopwatch"></i> ${{fmtDuration(p.total_duration_ms)}}</span>
                    </div>
                </div>
            `).join('');
        }}
        
        async function selectPipeline(id) {{
            try {{
                const [pipeRes, graphRes, yamlRes] = await Promise.all([
                    fetch('/api/pipelines/' + id),
                    fetch('/api/pipelines/' + id + '/graph'),
                    fetch('/api/pipelines/' + id + '/yaml').catch(() => ({{ ok: false }}))
                ]);
                
                selectedPipeline = await pipeRes.json();
                const graph = await graphRes.json();
                const yamlText = yamlRes.ok ? await yamlRes.text() : null;
                
                renderPipelineList(searchQuery ? pipelines.filter(p => 
                    p.name.toLowerCase().includes(searchQuery.toLowerCase()) || p.id.toLowerCase().includes(searchQuery.toLowerCase())
                ) : pipelines);
                
                renderGraph(graph);
                renderSteps(selectedPipeline);
                renderError(selectedPipeline);
                renderYaml(yamlText);
                
                document.getElementById('graph-pipeline-info').innerHTML = `
                    <span class="pipeline-id">${{selectedPipeline.id}}</span>
                    <span class="status-badge ${{selectedPipeline.status}}">${{selectedPipeline.status}}</span>
                    ${{selectedPipeline.total_duration_ms ? '<span class="duration-tag" style="margin-left:0.5rem">' + fmtDuration(selectedPipeline.total_duration_ms) + '</span>' : ''}}
                `;
                
            }} catch (e) {{
                console.error(e);
            }}
        }}
        
        // Render Graph
        function renderGraph(graph) {{
            const svg = document.getElementById('graph-svg');
            const edgesG = document.getElementById('graph-edges');
            const nodesG = document.getElementById('graph-nodes');
            const empty = document.getElementById('graph-empty');
            
            if (!graph.nodes || !graph.nodes.length) {{
                svg.style.display = 'none';
                empty.style.display = 'block';
                document.getElementById('steps-section').style.display = 'none';
                return;
            }}
            
            svg.style.display = 'block';
            empty.style.display = 'none';
            document.getElementById('steps-section').style.display = 'block';
            edgesG.innerHTML = '';
            nodesG.innerHTML = '';
            
            const w = svg.clientWidth || 800, h = 380, r = 36;
            const hasConditions = graph.nodes.some(n => n.type === 'condition');
            
            if (hasConditions) {{
                // Layout with conditions
                const condNodes = graph.nodes.filter(n => n.type === 'condition');
                const stepNodes = graph.nodes.filter(n => n.type !== 'condition' && n.type !== 'skipped');
                const skippedNodes = graph.nodes.filter(n => n.type === 'skipped');
                
                const allNodes = [...condNodes, ...stepNodes, ...skippedNodes];
                const spacing = Math.min(130, (w - 100) / Math.max(allNodes.length, 1));
                let x = 60;
                
                allNodes.forEach(nd => {{
                    nd.x = x;
                    const isSkipped = nd.type === 'skipped';
                    nd.y = isSkipped ? h - 90 : h / 2 - 30;
                    x += spacing;
                }});
                
                graph.edges.forEach(e => {{
                    const f = graph.nodes.find(n => n.id === e.from);
                    const t = graph.nodes.find(n => n.id === e.to);
                    if (f && t) {{
                        const color = e.color || (e.style === 'dashed' ? '#475569' : '');
                        const dash = e.style === 'dashed' ? '5,5' : '';
                        edgesG.innerHTML += `<line x1="${{f.x+r}}" y1="${{f.y}}" x2="${{t.x-r}}" y2="${{t.y}}" stroke="${{color}}" stroke-width="${{e.style==='dashed'?1:2}}" stroke-dasharray="${{dash}}" marker-end="url(#arrow)"/>`;
                    }}
                }});
            }} else {{
                // Simple layout
                const n = graph.nodes.length;
                const sp = Math.min(160, (w - 80) / n);
                const sx = (w - (n - 1) * sp) / 2;
                graph.nodes.forEach((nd, i) => {{
                    nd.x = sx + i * sp;
                    nd.y = h / 2;
                }});
                
                graph.edges.forEach(e => {{
                    const f = graph.nodes.find(n => n.id === e.from);
                    const t = graph.nodes.find(n => n.id === e.to);
                    if (f && t) edgesG.innerHTML += `<line x1="${{f.x+r}}" y1="${{f.y}}" x2="${{t.x-r-10}}" y2="${{t.y}}" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>`;
                }});
            }}
            
            // Render nodes
            const gradientMap = {{completed:'url(#gSuccess)', error:'url(#gError)', running:'url(#gRunning)', pending:'url(#gPending)'}};
            const iconMap = {{completed:'\\2713', error:'\\2717', running:'\\25B6', pending:'\\23F3'}};
            
            graph.nodes.forEach(nd => {{
                const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                g.setAttribute('transform', `translate(${{nd.x}},${{nd.y}})`);
                g.style.cursor = 'pointer';
                
                let tooltip = `${{nd.name}}\\nVersion: ${{nd.version||'1.0.0'}}\\nStatus: ${{nd.status}}\\nDuration: ${{fmtDuration(nd.duration_ms)||'N/A'}}`;
                if (nd.type === 'condition') {{
                    const branch = nd.branch_taken === 'true' ? 'TRUE' : 'FALSE';
                    const trueSteps = nd.true_branch_names || [];
                    const falseSteps = nd.false_branch_names || [];
                    tooltip += `\\nExpression: ${{nd.expression||'N/A'}}\\nBranch: ${{branch}}`;
                    if (nd.branch_taken === 'true') {{
                        tooltip += `\\n✓ Executed: ${{trueSteps.join(', ')}}`;
                        if (falseSteps.length) tooltip += `\\n✗ Skipped: ${{falseSteps.join(', ')}}`;
                    }} else {{
                        tooltip += `\\n✓ Executed: ${{falseSteps.join(', ')}}`;
                        if (trueSteps.length) tooltip += `\\n✗ Skipped: ${{trueSteps.join(', ')}}`;
                    }}
                }} else if (nd.type === 'skipped') {{
                    tooltip += '\\n(SKIPPED)';
                }}
                
                if (nd.type === 'condition') {{
                    g.innerHTML = `<polygon points="0,-${{r}} ${{r}},0 0,${{r}} -${{r}},0" fill="url(#gCondition)" stroke="#a78bfa" stroke-width="2"/><text text-anchor="middle" dominant-baseline="central" fill="white" font-size="11" font-weight="bold">?</text><text y="${{r+16}}" text-anchor="middle" fill="#cbd5e1" font-size="9">${{nd.name.substring(0,10)}}</text><text y="${{r+28}}" text-anchor="middle" font-size="8" fill="${{nd.branch_taken==='true'?'#34d399':'#94a3b8'}}" font-weight="bold">${{nd.branch_taken==='true'?'TRUE':'FALSE'}}</text>`;
                }} else if (nd.type === 'skipped') {{
                    g.innerHTML = `<circle r="${{r}}" fill="#1e293b" stroke="#475569" stroke-width="2" stroke-dasharray="5,5"/><text text-anchor="middle" dominant-baseline="central" fill="#64748b" font-size="14">\\u229E</text><text y="${{r+16}}" text-anchor="middle" fill="#64748b" font-size="9">${{nd.name.substring(0,11)}}</text>`;
                }} else {{
                    g.innerHTML = `<circle r="${{r}}" fill="${{gradientMap[nd.status]||gradientMap.pending}}" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.4))"/><circle r="${{r-10}}" fill="rgba(0,0,0,0.3)"/><text text-anchor="middle" dominant-baseline="central" fill="white" font-size="16">${{iconMap[nd.status]||'?'}}</text><text y="${{r+16}}" text-anchor="middle" fill="#cbd5e1" font-size="10">${{nd.name.length>12?nd.name.substring(0,10)+'..':nd.name}}</text>`;
                    if(nd.duration_ms) g.innerHTML += `<text y="${{r+28}}" text-anchor="middle" fill="#64748b" font-size="8">${{fmtDuration(nd.duration_ms)}}</text>`;
                }}
                
                g.onclick = () => toggleStep('step-' + nd.id.replace('step_', ''));
                g.onmouseenter = (e) => showTooltip(e, tooltip);
                g.onmouseleave = hideTooltip;
                
                nodesG.appendChild(g);
            }});
        }}
        
        function renderSteps(p) {{
            const sec = document.getElementById('steps-section');
            const list = document.getElementById('steps-list');
            if (!p.steps || !p.steps.length) {{ sec.style.display = 'none'; return; }}
            
            sec.style.display = 'block';
            list.innerHTML = p.steps.map(s => `
                <div class="step-card" id="step-${{s.id}}">
                    <div class="step-header" onclick="toggleStep('step-${{s.id}}')">
                        <div class="step-icon ${{s.status}}"><i class="fas fa-${{s.status==='completed'?'check':s.status==='error'?'xmark':'play'}}"></i></div>
                        <div class="step-info">
                            <div class="step-name">${{s.step_name}}</div>
                            <div class="step-meta">
                                <span>#${{s.step_order}}</span>
                                ${{s.step_version ? `<span><i class="fas fa-code-branch"></i> ${{s.step_version}}</span>` : ''}}
                                ${{s.duration_ms ? `<span><i class="fas fa-stopwatch"></i> ${{fmtDuration(s.duration_ms)}}</span>` : ''}}
                            </div>
                        </div>
                        <div class="step-chevron"><i class="fas fa-chevron-down"></i></div>
                    </div>
                    <div class="step-details">
                        ${{s.input_data ? `<div class="data-panel"><div class="data-panel-header input"><i class="fas fa-arrow-right"></i> INPUT</div><pre class="data-content">${{JSON.stringify(s.input_data, null, 2)}}</pre></div>` : ''}}
                        ${{s.output_data ? `<div class="data-panel"><div class="data-panel-header output"><i class="fas fa-arrow-left"></i> OUTPUT</div><pre class="data-content">${{JSON.stringify(s.output_data, null, 2)}}</pre></div>` : ''}}
                        ${{s.error_message ? `<div class="data-panel" style="border-color:rgba(244,63,94,0.3)"><div class="data-panel-header" style="color:#fb7185"><i class="fas fa-exclamation"></i> ERROR</div><pre class="data-content" style="color:#fca5a5">${{s.error_message}}</pre></div>` : ''}}
                    </div>
                </div>
            `).join('');
        }}
        
        function toggleStep(id) {{
            const el = document.getElementById(id);
            if (el) el.classList.toggle('expanded');
        }}
        
        function renderError(p) {{
            const panel = document.getElementById('error-panel');
            if (p.status === 'error') {{
                document.getElementById('error-step-name').textContent = p.error_step || 'Pipeline Error';
                document.getElementById('error-content').textContent = p.error_message || 'Unknown error';
                panel.style.display = 'block';
            }} else {{
                panel.style.display = 'none';
            }}
        }}
        
        function renderYaml(text) {{
            const panel = document.getElementById('yaml-panel');
            if (text && text !== '{{"error": "YAML not found"}}') {{
                document.getElementById('yaml-content').textContent = text;
                panel.style.display = 'block';
            }} else {{
                panel.style.display = 'none';
            }}
        }}
        
        // Tabs
        function switchTab(tab) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelector(`.tab[data-tab="${{tab}}"]`).classList.add('active');
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            document.getElementById('tab-' + tab).style.display = 'block';
            
            if (tab === 'timeline') loadTimeline();
            if (tab === 'analytics') loadAnalytics();
            if (tab === 'alerts') loadAlerts();
            if (tab === 'events') loadEvents();
        }}
        
        async function loadTimeline() {{
            const days = document.getElementById('timeline-filter')?.value || 7;
            const res = await fetch('/api/trends?days=' + days);
            const data = await res.json();
            
            const ctx = document.getElementById('timeline-chart').getContext('2d');
            if (timelineChart) timelineChart.destroy();
            
            timelineChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: data.map(d => d.date),
                    datasets: [{{
                        label: 'Executions',
                        data: data.map(d => d.count),
                        backgroundColor: 'rgba(99, 102, 241, 0.6)',
                        borderColor: '#6366f1',
                        borderWidth: 1,
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#64748b' }} }},
                        y: {{ grid: {{ color: 'rgba(100,116,139,0.1)' }}, ticks: {{ color: '#64748b' }} }}
                    }}
                }}
            }});
        }}
        
        async function loadAnalytics() {{
            const [statsRes, slowRes] = await Promise.all([fetch('/api/stats'), fetch('/api/slow-steps')]);
            const stats = await statsRes.json();
            const slow = await slowRes.json();
            
            // Pie chart
            const ctx = document.getElementById('pie-chart').getContext('2d');
            if (pieChart) pieChart.destroy();
            
            pieChart = new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Completed', 'Errors', 'Running', 'Pending'],
                    datasets: [{{
                        data: [stats.completed, stats.errors, stats.running, stats.total_pipelines - stats.completed - stats.errors - stats.running],
                        backgroundColor: ['#10b981', '#f43f5e', '#3b82f6', '#f59e0b'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '65%',
                    plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', padding: 15 }} }} }}
                }}
            }});
            
            // Slow steps
            document.getElementById('slow-steps-list').innerHTML = slow.length ? slow.map((s, i) => `
                <div style="display:flex;justify-content:space-between;padding:0.5rem;background:var(--bg-secondary);border-radius:var(--radius-md);margin-bottom:0.35rem">
                    <span style="font-size:0.8rem">${{i+1}}. ${{s.step_name}}</span>
                    <span style="color:var(--accent-amber);font-size:0.8rem;font-weight:500">${{fmtDuration(s.avg_duration_ms)}}</span>
                </div>
            `).join('') : '<div class="empty-state" style="padding:1rem"><p>No data</p></div>';
        }}
        
        async function loadAlerts(severity = '') {{
            const res = await fetch('/api/alerts?severity=' + severity);
            const alerts = await res.json();
            
            const list = document.getElementById('alerts-list');
            if (!alerts.length) {{
                list.innerHTML = '<div class="empty-state"><i class="fas fa-bell-slash"></i><p data-i18n="noAlerts">No alerts</p></div>';
                return;
            }}
            
            list.innerHTML = alerts.map(a => `
                <div class="alert-item ${{a.severity}}">
                    <div class="alert-icon ${{a.severity}}"><i class="fas fa-${{a.severity==='critical'?'exclamation-triangle':'bell'}}"></i></div>
                    <div class="alert-content">
                        <div class="alert-pipeline">${{a.pipeline_id}}</div>
                        <div class="alert-message">${{a.message}}</div>
                        <div class="alert-time">${{fmtTime(a.fired_at)}}</div>
                    </div>
                </div>
            `).join('');
        }}
        
        async function loadEvents() {{
            const res = await fetch('/api/events?limit=30');
            const events = await res.json();
            
            const list = document.getElementById('events-list');
            if (!events.length) {{
                list.innerHTML = '<div class="empty-state"><i class="fas fa-calendar-xmark"></i><p data-i18n="noEvents">No events</p></div>';
                return;
            }}
            
            list.innerHTML = events.map(e => `
                <div class="event-item">
                    <div class="event-time">${{fmtTime(e.created_at)}}</div>
                    <div class="event-title">${{e.event_name}}</div>
                    <div class="event-desc">${{e.message || ''}}</div>
                </div>
            `).join('');
        }}
        
        // Filters
        function filterPipelines(status) {{
            currentFilter = status;
            document.querySelectorAll('.filter-chips .chip').forEach(c => {{
                c.classList.toggle('active', c.dataset.status === status);
            }});
            selectedPipeline = null;
            refreshData();
        }}
        
        function filterPipelinesBySearch(query) {{
            searchQuery = query;
            refreshData();
        }}
        
        function filterAlerts(severity) {{
            document.querySelectorAll('#tab-alerts .chip').forEach(c => {{
                c.classList.toggle('active', c.dataset.severity === severity);
            }});
            loadAlerts(severity);
        }}
        
        // Tutorial
        function showTutorial() {{
            document.getElementById('tutorial-content').innerHTML = `
                <div class="modal-header">
                    <h2 class="modal-title"><i class="fas fa-rocket"></i> ${{t('welcome')}}</h2>
                    <button class="modal-close" onclick="hideTutorial()"><i class="fas fa-times"></i></button>
                </div>
                ${{t('tutorialContent')}}
                <div style="margin-top:1.5rem;text-align:center">
                    <button onclick="hideTutorial()" class="btn btn-primary" style="padding:0.75rem 2.5rem;font-size:1rem">
                        ${{currentLang === 'en' ? 'Start Exploring' : 'Comenzar'}} <i class="fas fa-arrow-right"></i>
                    </button>
                </div>
            `;
            document.getElementById('tutorial-modal').classList.add('active');
            localStorage.setItem('wpipe_tutorial_seen', 'true');
        }}
        
        function hideTutorial() {{
            document.getElementById('tutorial-modal').classList.remove('active');
        }}
        
        // Tooltip
        let tooltipEl = null;
        function showTooltip(e, text) {{
            if (!tooltipEl) {{
                tooltipEl = document.getElementById('tooltip');
            }}
            tooltipEl.textContent = text;
            tooltipEl.classList.add('visible');
            tooltipEl.style.left = (e.clientX + 15) + 'px';
            tooltipEl.style.top = (e.clientY - 10) + 'px';
        }}
        function hideTooltip() {{
            if (tooltipEl) tooltipEl.classList.remove('visible');
        }}
        
        // Utilities
        function fmtDuration(ms) {{
            if (!ms) return '-';
            if (ms < 1000) return Math.round(ms) + 'ms';
            if (ms < 60000) return (ms / 1000).toFixed(1) + 's';
            return Math.floor(ms / 60000) + 'm ' + Math.floor((ms % 60000) / 1000) + 's';
        }}
        
        function fmtTime(iso) {{
            if (!iso) return '-';
            const d = new Date(iso);
            const diff = Date.now() - d;
            if (diff < 60000) return 'Just now';
            if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
            if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
            return d.toLocaleDateString();
        }}
    </script>
</body>
</html>"""

    return html


def start_dashboard(
    db_path: str = "pipeline.db",
    host: str = "127.0.0.1",
    port: int = 8035,
    open_browser: bool = True,
    config_dir: Optional[str] = None,
) -> None:
    """Start the wpipe dashboard server."""
    import webbrowser
    import uvicorn

    if open_browser:
        webbrowser.open(f"http://{host}:{port}")

    app = create_app(db_path, config_dir)
    uvicorn.run(app, host=host, port=port, log_level="info")
