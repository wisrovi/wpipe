import * as vscode from 'vscode';

export function showCheatSheet() {
    const panel = vscode.window.createWebviewPanel('wpipeCheatSheet', '🚀 WPipe Professional Cheat Sheet', vscode.ViewColumn.Beside, { enableScripts: true });
    panel.webview.html = `
        <html>
        <head>
            <style>
                :root {
                    --bg: #0d1117;
                    --card-bg: #161b22;
                    --border: #30363d;
                    --text: #c9d1d9;
                    --accent: #58a6ff;
                    --secondary: #7ee787;
                    --orange: #ffa657;
                    --code-bg: #000;
                }
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; padding: 0; margin: 0; background: var(--bg); color: var(--text); }
                .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
                header { border-bottom: 1px solid var(--border); padding-bottom: 20px; margin-bottom: 40px; display: flex; align-items: center; justify-content: space-between; }
                h1 { font-size: 28px; margin: 0; color: var(--accent); display: flex; align-items: center; gap: 10px; }
                h2 { font-size: 20px; color: var(--secondary); margin-top: 30px; border-left: 4px solid var(--secondary); padding-left: 10px; }
                h3 { font-size: 16px; color: var(--orange); margin-top: 20px; }
                .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
                .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 20px; transition: transform 0.2s; }
                .card:hover { border-color: var(--accent); }
                code { background: var(--code-bg); padding: 2px 6px; border-radius: 4px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; color: var(--orange); }
                .snippet-list { list-style: none; padding: 0; }
                .snippet-list li { margin-bottom: 15px; border-bottom: 1px solid #21262d; padding-bottom: 10px; }
                .snippet-name { font-weight: bold; color: var(--accent); font-size: 14px; }
                .snippet-desc { font-size: 12px; color: #8b949e; margin-top: 4px; }
                .command-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                .command-table td { padding: 10px; border-bottom: 1px solid var(--border); font-size: 13px; }
                .command-table .cmd { color: var(--secondary); font-weight: bold; }
                .footer { margin-top: 60px; text-align: center; font-size: 12px; color: #8b949e; border-top: 1px solid var(--border); padding-top: 20px; }
                .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase; background: #238636; color: white; margin-left: 5px; }
                .warning-box { background: rgba(255, 166, 87, 0.1); border-left: 4px solid var(--orange); padding: 15px; margin: 20px 0; border-radius: 4px; font-size: 13px; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>🚀 WPipe Tools <span style="font-size:14px; color:#8b949e; font-weight:normal;">v0.8.2 Professional Edition</span></h1>
                    <div style="font-size: 12px; color: var(--accent);">By William Rodriguez (wisrovi)</div>
                </header>

                <div class="warning-box">
                    <b>💡 Pro Tip:</b> Always initialize your <code>Pipeline</code> with a <code>tracking_db</code> to enable forensic error capture, event logging, and real-time dashboard monitoring.
                </div>

                <h2>🛠️ Commands & Automation</h2>
                <div class="grid">
                    <div class="card">
                        <h3>Visual Analysis</h3>
                        <table class="command-table">
                            <tr><td class="cmd">Preview DAG</td><td>Watch your architecture come to life. Refreshes on save.</td></tr>
                            <tr><td class="cmd">Dashboard</td><td>Launch the real-time web monitoring interface.</td></tr>
                        </table>
                    </div>
                    <div class="card">
                        <h3>Step Management</h3>
                        <table class="command-table">
                            <tr><td class="cmd">Cloud Catalog</td><td>Search & import 130+ community steps instantly.</td></tr>
                            <tr><td class="cmd">Run Step</td><td>Test individual <code>@step</code> functions without running the whole pipe.</td></tr>
                        </table>
                    </div>
                </div>

                <h2>🐍 Python Snippets (Speed Up Development)</h2>
                <div class="grid">
                    <div class="card">
                        <h3>✨ Core Components</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpstep</span> <span class="badge">Common</span><div class="snippet-desc">Function-based step. Best for simple logic.</div></li>
                            <li><span class="snippet-name">wpstate</span><div class="snippet-desc">Class-based step with typed <code>PipelineContext</code>.</div></li>
                            <li><span class="snippet-name">wpstepadv</span> <span class="badge">Enterprise</span><div class="snippet-desc">Professional class with retries, timeouts, and rich metadata.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>🌀 Flow Control</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpparallel</span><div class="snippet-desc">Execute multiple steps simultaneously with thread management.</div></li>
                            <li><span class="snippet-name">wpcondition</span><div class="snippet-desc">Boolean branching (True/False) based on data content.</div></li>
                            <li><span class="snippet-name">wpfor</span><div class="snippet-desc">Iterative loops with early exit validation.</div></li>
                            <li><span class="snippet-name">wpbackground</span><div class="snippet-desc">Fire-and-forget asynchronous execution.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>🏗️ Orchestration</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wppipe</span><div class="snippet-desc">Basic pipeline skeleton with error handling.</div></li>
                            <li><span class="snippet-name">wppipeadv</span> <span class="badge">LTS</span><div class="snippet-desc">Full production setup: Metrics, Resource Monitor, Task Timer.</div></li>
                            <li><span class="snippet-name">wperrorcapture</span><div class="snippet-desc">Custom global error handler for forensic analysis.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>🛡️ Resilience & Tracking</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpevent</span><div class="snippet-desc">Log custom markers in the execution timeline.</div></li>
                            <li><span class="snippet-name">wpalert</span><div class="snippet-desc">Set thresholds (CPU, RAM, Time) to trigger alerts.</div></li>
                            <li><span class="snippet-name">wpcheckpoint</span><div class="snippet-desc">Save points for resumable long-running pipelines.</div></li>
                        </ul>
                    </div>
                </div>

                <h2>📜 YAML Configuration</h2>
                <div class="grid">
                    <div class="card">
                        <h3>Structure</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">wpyaml</span><div class="snippet-desc">Main pipeline YAML header.</div></li>
                            <li><span class="snippet-name">ypstep</span><div class="snippet-desc">Standard task definition in config files.</div></li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>Blocks</h3>
                        <ul class="snippet-list">
                            <li><span class="snippet-name">ypparallel / ypcondition</span><div class="snippet-desc">Logic blocks for data-driven configuration.</div></li>
                            <li><span class="snippet-name">ypfor / ypbackground</span><div class="snippet-desc">Advanced flow control in YAML.</div></li>
                        </ul>
                    </div>
                </div>

                <div class="footer">
                    Engineered for excellence in data orchestration.<br/>
                    Copyright &copy; 2026 WPipe Tools | <a href="https://github.com/wisrovi/wpipe" style="color:var(--accent);">Official Docs</a>
                </div>
            </div>
        </body>
        </html>
    `;
}
