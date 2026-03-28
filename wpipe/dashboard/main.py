"""
wpipe Dashboard - Professional Pipeline Visualization System.

Ultra-modern dashboard with:
- Real-time pipeline visualization
- Interactive execution graphs
- Step-by-step input/output inspection
- Execution timeline and analytics
- Professional dark theme UI
"""

import json
import webbrowser
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from wpipe.tracking import PipelineTracker


def create_app(db_path: str, config_dir: Optional[str] = None) -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(title="wpipe Dashboard", docs_url=None, redoc_url=None)

    # Store paths for use in routes
    app.state.db_path = db_path
    app.state.config_dir = config_dir

    @app.get("/", response_class=HTMLResponse)
    async def home():
        return get_dashboard_html()

    @app.get("/api/stats")
    async def get_stats():
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_stats()

    @app.get("/api/pipelines")
    async def get_pipelines(limit: int = 50, status: Optional[str] = None):
        tracker = PipelineTracker(db_path, config_dir)
        return tracker.get_pipelines(limit=limit, status=status)

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
            if yaml_path.exists():
                return yaml_path.read_text(encoding="utf-8")
        return {"error": "YAML not found"}

    @app.delete("/api/pipelines/{pipeline_id}")
    async def delete_pipeline(pipeline_id: str):
        tracker = PipelineTracker(db_path, config_dir)
        tracker.delete_pipeline(pipeline_id)
        return {"status": "deleted"}

    return app


def get_dashboard_html() -> str:
    """Generate ultra-modern dashboard HTML."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>wpipe Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-void: #030712;
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --bg-card: rgba(30, 41, 59, 0.8);
            --bg-hover: rgba(51, 65, 85, 0.5);
            --bg-glass: rgba(15, 23, 42, 0.8);
            
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #64748b;
            
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            
            --gradient-hero: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
            --gradient-error: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            --gradient-blue: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            --gradient-purple: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
            --gradient-cyan: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
            
            --border-subtle: rgba(51, 65, 85, 0.5);
            --border-accent: rgba(99, 102, 241, 0.3);
            
            --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
            --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.4);
            --shadow-elevated: 0 8px 30px rgba(0, 0, 0, 0.6);
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-void);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        /* Header */
        .header {
            position: sticky;
            top: 0;
            z-index: 100;
            background: var(--bg-glass);
            backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid var(--border-subtle);
        }
        
        .header-content {
            max-width: 1800px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .brand {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .brand-icon {
            width: 48px;
            height: 48px;
            background: var(--gradient-hero);
            border-radius: var(--radius-md);
            display: grid;
            place-items: center;
            font-size: 1.4rem;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        }
        
        .brand-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .brand-text span {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .header-actions {
            display: flex;
            gap: 0.75rem;
        }
        
        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.6rem 1.2rem;
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
        }
        
        .btn-primary {
            background: var(--gradient-hero);
            color: white;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        }
        
        .btn-ghost {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
        }
        
        .btn-ghost:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
        }
        
        /* Main container */
        .container {
            position: relative;
            z-index: 1;
            max-width: 1800px;
            margin: 0 auto;
            padding: 1.5rem 2rem;
        }
        
        /* Stats Row */
        .stats-row {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        @media (max-width: 1400px) { .stats-row { grid-template-columns: repeat(3, 1fr); } }
        @media (max-width: 900px) { .stats-row { grid-template-columns: repeat(2, 1fr); } }
        
        .stat-card {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-glow);
            border-color: var(--border-accent);
        }
        
        .stat-card:hover::before { opacity: 1; }
        
        .stat-card.blue::before { background: var(--gradient-blue); }
        .stat-card.green::before { background: var(--gradient-success); }
        .stat-card.purple::before { background: var(--gradient-purple); }
        .stat-card.cyan::before { background: var(--gradient-cyan); }
        .stat-card.rose::before { background: var(--gradient-error); }
        
        .stat-icon {
            width: 44px;
            height: 44px;
            border-radius: var(--radius-md);
            display: grid;
            place-items: center;
            font-size: 1.1rem;
            margin-bottom: 0.75rem;
        }
        
        .stat-icon.blue { background: rgba(59, 130, 246, 0.15); color: var(--accent-blue); }
        .stat-icon.green { background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); }
        .stat-icon.purple { background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); }
        .stat-icon.cyan { background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); }
        .stat-icon.rose { background: rgba(244, 63, 94, 0.15); color: var(--accent-rose); }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Main Grid */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 1.5rem;
        }
        
        @media (max-width: 1200px) { .main-grid { grid-template-columns: 1fr; } }
        
        /* Cards */
        .card {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            overflow: hidden;
        }
        
        .card-header {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0, 0, 0, 0.2);
        }
        
        .card-title {
            font-size: 0.95rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        
        .card-title i { color: var(--accent-blue); }
        .card-body { padding: 1.25rem; }
        
        /* Graph */
        .graph-container {
            background: var(--bg-void);
            border-radius: var(--radius-md);
            min-height: 400px;
            position: relative;
            border: 1px solid var(--border-subtle);
        }
        
        .graph-svg { width: 100%; height: 400px; }
        
        .graph-empty {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: var(--text-muted);
        }
        
        .graph-empty i { font-size: 4rem; opacity: 0.3; margin-bottom: 1rem; display: block; }
        
        /* Pipeline List */
        .pipeline-list {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 550px;
            overflow-y: auto;
        }
        
        .pipeline-list::-webkit-scrollbar { width: 4px; }
        .pipeline-list::-webkit-scrollbar-track { background: transparent; }
        .pipeline-list::-webkit-scrollbar-thumb { background: var(--bg-tertiary); border-radius: 2px; }
        
        .pipeline-item {
            background: var(--bg-primary);
            border-radius: var(--radius-md);
            padding: 0.9rem 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }
        
        .pipeline-item:hover {
            background: var(--bg-hover);
            border-color: var(--border-accent);
        }
        
        .pipeline-item.active {
            border-color: var(--accent-blue);
            background: rgba(59, 130, 246, 0.1);
            box-shadow: 0 0 0 1px var(--accent-blue);
        }
        
        .pipeline-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }
        
        .pipeline-id {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }
        
        .pipeline-name {
            font-weight: 600;
            font-size: 0.9rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 200px;
        }
        
        .status-badge {
            padding: 0.25rem 0.6rem;
            border-radius: 20px;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-badge.completed { background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); }
        .status-badge.error { background: rgba(244, 63, 94, 0.15); color: var(--accent-rose); }
        .status-badge.running { background: rgba(59, 130, 246, 0.15); color: var(--accent-blue); animation: pulse 2s infinite; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        .pipeline-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        
        .pipeline-meta span { display: flex; align-items: center; gap: 0.3rem; }
        .duration-tag { color: var(--accent-purple); font-weight: 500; }
        
        /* Steps */
        .steps-section { margin-top: 1.5rem; }
        .steps-title {
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .steps-title i { color: var(--accent-blue); }
        
        .step-card {
            background: var(--bg-primary);
            border-radius: var(--radius-md);
            margin-bottom: 0.75rem;
            border: 1px solid var(--border-subtle);
            overflow: hidden;
            transition: all 0.2s ease;
        }
        
        .step-card:hover { border-color: var(--border-accent); }
        
        .step-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            cursor: pointer;
        }
        
        .step-icon {
            width: 42px;
            height: 42px;
            border-radius: var(--radius-md);
            display: grid;
            place-items: center;
            flex-shrink: 0;
        }
        
        .step-icon.completed { background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); }
        .step-icon.error { background: rgba(244, 63, 94, 0.15); color: var(--accent-rose); }
        .step-icon.running { background: rgba(59, 130, 246, 0.15); color: var(--accent-blue); }
        
        .step-info { flex: 1; min-width: 0; }
        .step-name { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.2rem; }
        
        .step-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        
        .step-meta span { display: flex; align-items: center; gap: 0.3rem; }
        .step-duration { color: var(--accent-purple); font-weight: 500; }
        
        .step-expand {
            color: var(--text-muted);
            transition: transform 0.2s ease;
        }
        
        .step-card.expanded .step-expand { transform: rotate(180deg); }
        
        .step-details {
            display: none;
            padding: 0 1rem 1rem;
            border-top: 1px solid var(--border-subtle);
        }
        
        .step-card.expanded .step-details { display: block; }
        
        .data-panel {
            margin-top: 0.75rem;
            background: var(--bg-void);
            border-radius: var(--radius-sm);
            padding: 0.75rem;
            border: 1px solid var(--border-subtle);
        }
        
        .data-panel-header {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }
        
        .data-panel-header.input { color: var(--accent-blue); }
        .data-panel-header.output { color: var(--accent-emerald); }
        
        .data-content {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--text-secondary);
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 200px;
            overflow-y: auto;
        }
        
        /* Error Panel */
        .error-panel {
            background: rgba(244, 63, 94, 0.1);
            border: 1px solid rgba(244, 63, 94, 0.3);
            border-radius: var(--radius-md);
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .error-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--accent-rose);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .error-message {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            background: rgba(0, 0, 0, 0.3);
            padding: 0.75rem;
            border-radius: var(--radius-sm);
            color: var(--text-secondary);
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
        }
        
        /* Filter tabs */
        .filter-tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .filter-tab {
            padding: 0.4rem 0.8rem;
            border-radius: var(--radius-sm);
            font-size: 0.8rem;
            cursor: pointer;
            background: var(--bg-primary);
            color: var(--text-muted);
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }
        
        .filter-tab:hover { color: var(--text-primary); border-color: var(--border-subtle); }
        .filter-tab.active { background: var(--accent-blue); color: white; border-color: var(--accent-blue); }
        
        /* Loading */
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 3rem;
        }
        
        .spinner {
            width: 32px;
            height: 32px;
            border: 3px solid var(--border-subtle);
            border-top-color: var(--accent-blue);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
        }
        
        .empty-state i { font-size: 3rem; opacity: 0.3; margin-bottom: 1rem; display: block; }
        
        /* SVG Graph */
        .edge-line {
            stroke: var(--bg-tertiary);
            stroke-width: 2;
            fill: none;
        }
        
        .edge-arrow { fill: var(--bg-tertiary); }
        
        .node-group { cursor: pointer; }
        
        .node-circle {
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.4));
            transition: all 0.2s ease;
        }
        
        .node-group:hover .node-circle {
            filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.6));
        }
        
        .node-label {
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            fill: var(--text-secondary);
        }
        
        .node-duration {
            font-family: 'JetBrains Mono', monospace;
            fill: var(--text-muted);
        }
        
        /* YAML Panel */
        .yaml-panel {
            background: var(--bg-void);
            border-radius: var(--radius-md);
            padding: 1rem;
            margin-top: 1rem;
            border: 1px solid var(--border-subtle);
        }
        
        .yaml-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }
        
        .yaml-title {
            font-size: 0.8rem;
            color: var(--accent-cyan);
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .yaml-content {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: var(--text-secondary);
            white-space: pre-wrap;
            background: var(--bg-primary);
            padding: 0.75rem;
            border-radius: var(--radius-sm);
            max-height: 200px;
            overflow-y: auto;
        }
        
        /* Tooltip */
        .tooltip {
            position: absolute;
            background: var(--bg-secondary);
            border: 1px solid var(--border-accent);
            border-radius: var(--radius-sm);
            padding: 0.5rem 0.75rem;
            font-size: 0.75rem;
            z-index: 1000;
            pointer-events: none;
            box-shadow: var(--shadow-elevated);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="brand">
                <div class="brand-icon">
                    <i class="fas fa-diagram-project"></i>
                </div>
                <div class="brand-text">
                    <h1>wpipe</h1>
                    <span>Pipeline Dashboard</span>
                </div>
            </div>
            <div class="header-actions">
                <button class="btn btn-ghost" onclick="refreshData()">
                    <i class="fas fa-arrows-rotate"></i>
                    Refresh
                </button>
            </div>
        </div>
    </header>
    
    <main class="container">
        <!-- Stats Row -->
        <div class="stats-row">
            <div class="stat-card blue">
                <div class="stat-icon blue"><i class="fas fa-diagram-project"></i></div>
                <div class="stat-value" id="stat-total">-</div>
                <div class="stat-label">Total Pipelines</div>
            </div>
            <div class="stat-card green">
                <div class="stat-icon green"><i class="fas fa-circle-check"></i></div>
                <div class="stat-value" id="stat-success">-</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card purple">
                <div class="stat-icon purple"><i class="fas fa-clock"></i></div>
                <div class="stat-value" id="stat-duration">-</div>
                <div class="stat-label">Avg Duration</div>
            </div>
            <div class="stat-card cyan">
                <div class="stat-icon cyan"><i class="fas fa-layer-group"></i></div>
                <div class="stat-value" id="stat-steps">-</div>
                <div class="stat-label">Total Steps</div>
            </div>
            <div class="stat-card rose">
                <div class="stat-icon rose"><i class="fas fa-triangle-exclamation"></i></div>
                <div class="stat-value" id="stat-errors">-</div>
                <div class="stat-label">Errors</div>
            </div>
        </div>
        
        <!-- Main Grid -->
        <div class="main-grid">
            <!-- Graph Panel -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-diagram-project"></i>
                        Execution Graph
                    </div>
                    <div id="pipeline-badge"></div>
                </div>
                <div class="card-body">
                    <div class="graph-container">
                        <svg id="graph-svg" class="graph-svg">
                            <defs>
                                <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                    <polygon points="0 0, 10 3.5, 0 7" fill="var(--bg-tertiary)" />
                                </marker>
                            </defs>
                            <g id="edges"></g>
                            <g id="nodes"></g>
                        </svg>
                        <div id="graph-empty" class="graph-empty">
                            <i class="fas fa-diagram-project"></i>
                            <p>Select a pipeline to visualize</p>
                        </div>
                    </div>
                    
                    <div id="steps-section" class="steps-section" style="display:none;">
                        <div class="steps-title">
                            <i class="fas fa-list-check"></i>
                            Execution Steps
                        </div>
                        <div id="steps-list"></div>
                    </div>
                    
                    <div id="error-panel" class="error-panel" style="display:none;">
                        <div class="error-title">
                            <i class="fas fa-circle-exclamation"></i>
                            <span id="error-step-name">Error</span>
                        </div>
                        <div id="error-message" class="error-message"></div>
                    </div>
                    
                    <div id="yaml-panel" class="yaml-panel" style="display:none;">
                        <div class="yaml-header">
                            <div class="yaml-title">
                                <i class="fas fa-file-code"></i>
                                Configuration YAML
                            </div>
                        </div>
                        <div id="yaml-content" class="yaml-content"></div>
                    </div>
                </div>
            </div>
            
            <!-- Pipeline List -->
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <i class="fas fa-clock-rotate-left"></i>
                        Pipeline History
                    </div>
                </div>
                <div class="card-body">
                    <div class="filter-tabs">
                        <div class="filter-tab active" data-filter="">All</div>
                        <div class="filter-tab" data-filter="completed">Done</div>
                        <div class="filter-tab" data-filter="error">Errors</div>
                        <div class="filter-tab" data-filter="running">Running</div>
                    </div>
                    <div id="pipeline-list" class="pipeline-list">
                        <div class="loading"><div class="spinner"></div></div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        let pipelines = [];
        let selectedPipeline = null;
        let currentFilter = '';
        
        const statusConfig = {
            completed: { icon: '✓', gradient: 'url(#gradSuccess)' },
            error: { icon: '✗', gradient: 'url(#gradError)' },
            running: { icon: '▶', gradient: 'url(#gradRunning)' },
            pending: { icon: '◌', gradient: 'url(#gradPending)' }
        };
        
        async function refreshData() {
            try {
                const [statsRes, pipelinesRes] = await Promise.all([
                    fetch('/api/stats'),
                    fetch('/api/pipelines?status=' + currentFilter)
                ]);
                
                const stats = await statsRes.json();
                pipelines = await pipelinesRes.json();
                
                // Update stats
                document.getElementById('stat-total').textContent = stats.total_pipelines || 0;
                document.getElementById('stat-success').textContent = (stats.success_rate || 0) + '%';
                document.getElementById('stat-duration').textContent = formatDuration(stats.avg_duration_ms || 0);
                document.getElementById('stat-steps').textContent = stats.total_steps || 0;
                document.getElementById('stat-errors').textContent = stats.errors || 0;
                
                renderPipelineList();
                
                if (pipelines.length > 0 && !selectedPipeline) {
                    selectPipeline(pipelines[0].id);
                } else if (pipelines.length === 0) {
                    clearSelection();
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        function renderPipelineList() {
            const container = document.getElementById('pipeline-list');
            
            if (pipelines.length === 0) {
                container.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>No pipelines</p></div>';
                return;
            }
            
            container.innerHTML = pipelines.map(p => `
                <div class="pipeline-item ${selectedPipeline?.id === p.id ? 'active' : ''}" 
                     onclick="selectPipeline('${p.id}')">
                    <div class="pipeline-header">
                        <span class="pipeline-id">${p.id}</span>
                        <span class="status-badge ${p.status}">${p.status}</span>
                    </div>
                    <div class="pipeline-name" title="${p.name}">${p.name}</div>
                    <div class="pipeline-meta">
                        <span><i class="fas fa-clock"></i> ${formatTime(p.started_at)}</span>
                        ${p.total_duration_ms ? `<span class="duration-tag">${formatDuration(p.total_duration_ms)}</span>` : ''}
                    </div>
                </div>
            `).join('');
        }
        
        async function selectPipeline(id) {
            try {
                const [detailRes, graphRes, yamlRes] = await Promise.all([
                    fetch('/api/pipelines/' + id),
                    fetch('/api/pipelines/' + id + '/graph'),
                    fetch('/api/pipelines/' + id + '/yaml').catch(() => null)
                ]);
                
                selectedPipeline = await detailRes.json();
                const graph = await graphRes.json();
                const yamlText = yamlRes ? await yamlRes.text() : null;
                
                renderPipelineList();
                renderGraph(graph);
                renderSteps(selectedPipeline);
                renderError(selectedPipeline);
                renderYaml(yamlText);
                
                // Update badge
                document.getElementById('pipeline-badge').innerHTML = `
                    <span class="pipeline-id">${selectedPipeline.id}</span>
                    <span class="status-badge ${selectedPipeline.status}">${selectedPipeline.status}</span>
                `;
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        function renderGraph(graph) {
            const svg = document.getElementById('graph-svg');
            const edgesGroup = document.getElementById('edges');
            const nodesGroup = document.getElementById('nodes');
            const emptyState = document.getElementById('graph-empty');
            
            if (!graph.nodes || graph.nodes.length === 0) {
                svg.style.display = 'none';
                emptyState.style.display = 'block';
                document.getElementById('steps-section').style.display = 'none';
                return;
            }
            
            svg.style.display = 'block';
            emptyState.style.display = 'none';
            document.getElementById('steps-section').style.display = 'block';
            
            edgesGroup.innerHTML = '';
            nodesGroup.innerHTML = '';
            
            const width = svg.clientWidth || 800;
            const height = 400;
            const radius = 45;
            const count = graph.nodes.length;
            const spacing = Math.min(180, (width - 100) / count);
            const startX = (width - (count - 1) * spacing) / 2;
            
            // Add gradient definitions
            const defs = svg.querySelector('defs');
            defs.innerHTML += `
                <linearGradient id="gradSuccess" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#10b981"/>
                    <stop offset="100%" style="stop-color:#059669"/>
                </linearGradient>
                <linearGradient id="gradError" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#ef4444"/>
                    <stop offset="100%" style="stop-color:#dc2626"/>
                </linearGradient>
                <linearGradient id="gradRunning" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#3b82f6"/>
                    <stop offset="100%" style="stop-color:#2563eb"/>
                </linearGradient>
                <linearGradient id="gradPending" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#f59e0b"/>
                    <stop offset="100%" style="stop-color:#d97706"/>
                </linearGradient>
            `;
            
            // Position nodes
            graph.nodes.forEach((node, i) => {
                node.x = startX + i * spacing;
                node.y = height / 2;
            });
            
            // Draw edges
            graph.edges.forEach(edge => {
                const from = graph.nodes.find(n => n.id === edge.from);
                const to = graph.nodes.find(n => n.id === edge.to);
                if (from && to) {
                    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('x1', from.x + radius);
                    line.setAttribute('y1', from.y);
                    line.setAttribute('x2', to.x - radius - 12);
                    line.setAttribute('y2', to.y);
                    line.setAttribute('class', 'edge-line');
                    line.setAttribute('marker-end', 'url(#arrow)');
                    edgesGroup.appendChild(line);
                }
            });
            
            // Draw nodes
            graph.nodes.forEach(node => {
                const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                g.setAttribute('class', 'node-group');
                g.setAttribute('transform', `translate(${node.x}, ${node.y})`);
                g.onclick = () => toggleStep(node.id);
                
                // Glow effect for running
                if (node.status === 'running') {
                    const glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                    glow.setAttribute('r', radius + 8);
                    glow.setAttribute('fill', 'none');
                    glow.setAttribute('stroke', 'var(--accent-blue)');
                    glow.setAttribute('stroke-width', '2');
                    glow.setAttribute('opacity', '0.3');
                    g.appendChild(glow);
                }
                
                // Main circle
                const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circle.setAttribute('r', radius);
                circle.setAttribute('fill', statusConfig[node.status]?.gradient || statusConfig.pending.gradient);
                circle.setAttribute('class', 'node-circle');
                g.appendChild(circle);
                
                // Inner ring
                const inner = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                inner.setAttribute('r', radius - 10);
                inner.setAttribute('fill', 'rgba(0,0,0,0.25)');
                g.appendChild(inner);
                
                // Icon
                const icon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                icon.setAttribute('text-anchor', 'middle');
                icon.setAttribute('dominant-baseline', 'central');
                icon.setAttribute('fill', 'white');
                icon.setAttribute('font-size', '20');
                icon.textContent = statusConfig[node.status]?.icon || '?';
                g.appendChild(icon);
                
                // Name
                const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                label.setAttribute('y', radius + 20);
                label.setAttribute('text-anchor', 'middle');
                label.setAttribute('class', 'node-label');
                label.setAttribute('font-size', '12');
                label.textContent = node.name.length > 16 ? node.name.substring(0, 14) + '...' : node.name;
                g.appendChild(label);
                
                // Duration
                if (node.duration_ms) {
                    const dur = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    dur.setAttribute('y', radius + 35);
                    dur.setAttribute('text-anchor', 'middle');
                    dur.setAttribute('class', 'node-duration');
                    dur.setAttribute('font-size', '10');
                    dur.textContent = formatDuration(node.duration_ms);
                    g.appendChild(dur);
                }
                
                nodesGroup.appendChild(g);
            });
        }
        
        function renderSteps(pipeline) {
            const section = document.getElementById('steps-section');
            const list = document.getElementById('steps-list');
            
            if (!pipeline.steps || pipeline.steps.length === 0) {
                section.style.display = 'none';
                return;
            }
            
            section.style.display = 'block';
            list.innerHTML = pipeline.steps.map((step, i) => `
                <div class="step-card" id="step-${step.id}">
                    <div class="step-header" onclick="toggleStep('step-${step.id}')">
                        <div class="step-icon ${step.status}">
                            <i class="fas fa-${step.status === 'completed' ? 'check' : step.status === 'error' ? 'xmark' : 'play'}"></i>
                        </div>
                        <div class="step-info">
                            <div class="step-name">${step.step_name}</div>
                            <div class="step-meta">
                                <span><i class="fas fa-hashtag"></i> Step ${step.step_order}</span>
                                ${step.step_version ? `<span><i class="fas fa-code-branch"></i> ${step.step_version}</span>` : ''}
                                ${step.duration_ms ? `<span class="step-duration"><i class="fas fa-stopwatch"></i> ${formatDuration(step.duration_ms)}</span>` : ''}
                            </div>
                        </div>
                        <div class="step-expand">
                            <i class="fas fa-chevron-down"></i>
                        </div>
                    </div>
                    <div class="step-details">
                        ${step.input_data ? `
                            <div class="data-panel">
                                <div class="data-panel-header input"><i class="fas fa-arrow-right"></i> Input</div>
                                <div class="data-content">${JSON.stringify(step.input_data, null, 2)}</div>
                            </div>
                        ` : ''}
                        ${step.output_data ? `
                            <div class="data-panel">
                                <div class="data-panel-header output"><i class="fas fa-arrow-left"></i> Output</div>
                                <div class="data-content">${JSON.stringify(step.output_data, null, 2)}</div>
                            </div>
                        ` : ''}
                        ${step.error_message ? `
                            <div class="data-panel" style="border-color: rgba(244,63,94,0.3);">
                                <div class="data-panel-header" style="color: var(--accent-rose);"><i class="fas fa-exclamation"></i> Error</div>
                                <div class="data-content" style="color: var(--accent-rose);">${step.error_message}</div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            `).join('');
        }
        
        function toggleStep(id) {
            const el = document.getElementById(id);
            if (el) el.classList.toggle('expanded');
        }
        
        function renderError(pipeline) {
            const panel = document.getElementById('error-panel');
            if (pipeline.error_message) {
                panel.style.display = 'block';
                document.getElementById('error-step-name').textContent = 'Error in: ' + (pipeline.error_step || 'Unknown');
                document.getElementById('error-message').textContent = pipeline.error_message;
            } else {
                panel.style.display = 'none';
            }
        }
        
        function renderYaml(yamlText) {
            const panel = document.getElementById('yaml-panel');
            if (yamlText) {
                panel.style.display = 'block';
                document.getElementById('yaml-content').textContent = yamlText;
            } else {
                panel.style.display = 'none';
            }
        }
        
        function clearSelection() {
            selectedPipeline = null;
            document.getElementById('pipeline-badge').innerHTML = '';
            document.getElementById('graph-svg').style.display = 'none';
            document.getElementById('graph-empty').style.display = 'block';
            document.getElementById('steps-section').style.display = 'none';
            document.getElementById('error-panel').style.display = 'none';
            document.getElementById('yaml-panel').style.display = 'none';
            renderPipelineList();
        }
        
        function formatDuration(ms) {
            if (!ms) return '-';
            if (ms < 1000) return Math.round(ms) + 'ms';
            if (ms < 60000) return (ms / 1000).toFixed(2) + 's';
            return Math.floor(ms / 60000) + 'm ' + Math.floor((ms % 60000) / 1000) + 's';
        }
        
        function formatTime(iso) {
            if (!iso) return '-';
            const d = new Date(iso);
            const diff = Date.now() - d;
            if (diff < 60000) return 'Just now';
            if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
            if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
            return d.toLocaleDateString();
        }
        
        // Filter tabs
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentFilter = tab.dataset.filter;
                selectedPipeline = null;
                refreshData();
            });
        });
        
        // Initialize
        refreshData();
        setInterval(refreshData, 10000);
    </script>
</body>
</html>"""


def start_dashboard(
    db_path: str = "pipeline.db",
    host: str = "127.0.0.1",
    port: int = 8035,
    open_browser: bool = True,
    config_dir: Optional[str] = None,
) -> None:
    """Start the wpipe dashboard server."""
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")

    app = create_app(db_path, config_dir)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="wpipe Dashboard")
    parser.add_argument("--db", default="pipeline.db", help="Path to SQLite database")
    parser.add_argument(
        "--config-dir", default=None, help="Path to YAML configs directory"
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8035, help="Port to bind to")
    parser.add_argument(
        "--open", action="store_true", help="Open browser automatically"
    )

    args = parser.parse_args()
    start_dashboard(
        db_path=args.db,
        host=args.host,
        port=args.port,
        open_browser=args.open,
        config_dir=args.config_dir,
    )
