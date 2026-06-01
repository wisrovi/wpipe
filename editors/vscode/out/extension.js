"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
class CatalogManager {
    static async init(context) {
        const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, 'catalog_cache.json');
        // 1. Load from cache
        try {
            const cacheData = await vscode.workspace.fs.readFile(cacheUri);
            const cached = JSON.parse(new TextDecoder().decode(cacheData));
            if (Array.isArray(cached))
                this.catalog = cached;
        }
        catch (e) {
            // Cache doesn't exist or is invalid, load embedded data
            try {
                const catalogUri = vscode.Uri.joinPath(context.extensionUri, 'out', 'steps_catalog.json');
                const catalogData = await vscode.workspace.fs.readFile(catalogUri);
                const raw = JSON.parse(new TextDecoder().decode(catalogData));
                this.catalog = Array.isArray(raw) ? raw : (raw.default || []);
            }
            catch (e2) { }
        }
        // 2. Trigger background update
        this.update(context, false);
    }
    static async update(context, manual = false) {
        const download = async () => {
            const oldNames = new Set(this.catalog.map(s => `${s.repo}:${s.name}`));
            const fetchJson = async (url) => {
                try {
                    const response = await fetch(url);
                    if (!response.ok)
                        return [];
                    const p = await response.json();
                    return Array.isArray(p) ? p : [];
                }
                catch (e) {
                    return [];
                }
            };
            const [off, com] = await Promise.all([fetchJson(this.OFFICIAL_URL), fetchJson(this.COMMUNITY_URL)]);
            const newCatalog = [...off, ...com];
            if (newCatalog.length > 0) {
                const newItems = newCatalog.filter(s => !oldNames.has(`${s.repo}:${s.name}`));
                this.catalog = newCatalog;
                try {
                    const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, 'catalog_cache.json');
                    await vscode.workspace.fs.writeFile(cacheUri, new TextEncoder().encode(JSON.stringify(this.catalog)));
                }
                catch (e) { }
                if (newItems.length > 0) {
                    vscode.window.showInformationMessage(`🚀 ¡Hay ${newItems.length} nuevos estados en WPipe!`, "Ver Catálogo").then(selection => {
                        if (selection === "Ver Catálogo")
                            vscode.commands.executeCommand('wpipe-vscode.searchSteps');
                    });
                }
                else if (manual) {
                    vscode.window.setStatusBarMessage("✅ WPipe: Catálogo al día", 3000);
                }
                vscode.commands.executeCommand('wpipeSteps.refreshEntry');
            }
        };
        if (manual) {
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "Actualizando catálogo...",
                cancellable: false
            }, download);
        }
        else {
            download();
        }
    }
    static getSteps() {
        return this.catalog;
    }
}
CatalogManager.catalog = [];
CatalogManager.OFFICIAL_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-steps/001-DEVELOPMENT/steps_catalog.json';
CatalogManager.COMMUNITY_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-plugins/001-DEVELOPMENT/steps_catalog.json';
async function activate(context) {
    // Start Catalog Manager (Non-blocking)
    CatalogManager.init(context);
    const stepProvider = new WPipeStepProvider();
    vscode.window.registerTreeDataProvider('wpipeSteps', stepProvider);
    context.subscriptions.push(vscode.commands.registerCommand('wpipeSteps.refreshEntry', () => stepProvider.refresh()), vscode.commands.registerCommand('wpipe-vscode.refreshCatalog', () => CatalogManager.update(context, true)), vscode.commands.registerCommand('wpipeSteps.openFile', async (f, l) => {
        const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(f));
        const editor = await vscode.window.showTextDocument(doc);
        const p = new vscode.Position(l, 0);
        editor.selection = new vscode.Selection(p, p);
        editor.revealRange(new vscode.Range(p, p), vscode.TextEditorRevealType.InCenter);
    }), vscode.commands.registerCommand('wpipeSteps.insertStep', (step) => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            editor.edit(eb => {
                const importCode = `from ${step.namespace} import ${step.func_name}\n`;
                eb.insert(new vscode.Position(0, 0), importCode);
                const isClass = /^[A-Z]/.test(step.func_name);
                eb.insert(editor.selection.active, isClass ? `${step.func_name}(),` : `${step.func_name},`);
            });
            vscode.window.showInformationMessage(`✅ Estado '${step.name}' insertado con éxito.`);
        }
    }), vscode.commands.registerCommand('wpipe-vscode.searchSteps', async () => {
        const items = CatalogManager.getSteps().map(s => ({
            label: `$(rocket) ${s.name}`,
            description: `${s.repo} | Author: ${s.author || 'Official'}`,
            detail: `Module: ${s.namespace}`,
            step: s
        }));
        const sel = await vscode.window.showQuickPick(items, { placeHolder: 'Buscar estado en el catálogo oficial o comunidad...' });
        if (sel) {
            vscode.commands.executeCommand('wpipeSteps.insertStep', sel.step);
        }
    }), vscode.commands.registerCommand('wpipe-vscode.previewDAG', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor)
            DAGPanel.createOrShow(context.extensionUri, editor.document);
    }), vscode.commands.registerCommand('wpipe-vscode.openDashboard', async () => {
        if (vscode.env.uiKind === vscode.UIKind.Web) {
            vscode.window.showErrorMessage('WPipe Dashboard requires a local Python environment and is not available in VS Code for Web.');
            return;
        }
        const dbUri = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: false,
            canSelectMany: false,
            filters: { 'Database': ['db', 'sqlite', 'sqlite3'] },
            title: 'Select WPipe Tracking Database'
        });
        if (!dbUri)
            return;
        const configUri = await vscode.window.showOpenDialog({
            canSelectFiles: false,
            canSelectFolders: true,
            canSelectMany: false,
            title: 'Select WPipe Config Directory (Optional)'
        });
        const port = await vscode.window.showInputBox({
            placeHolder: '5000',
            prompt: 'Enter port for the dashboard',
            value: '5000'
        });
        if (!port)
            return;
        const terminal = vscode.window.createTerminal('WPipe Dashboard');
        const dbPath = dbUri[0].fsPath;
        const configPath = configUri ? configUri[0].fsPath : '';
        let cmd = `python -m wpipe.dashboard --db "${dbPath}" --port ${port}`;
        if (configPath)
            cmd += ` --config "${configPath}"`;
        terminal.show();
        terminal.sendText(cmd);
        vscode.window.showInformationMessage(`🚀 Dashboard starting at http://localhost:${port}`);
        setTimeout(() => {
            vscode.env.openExternal(vscode.Uri.parse(`http://localhost:${port}`));
        }, 2000);
    }), vscode.commands.registerCommand('wpipe-vscode.showCheatSheet', () => {
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
    }), vscode.commands.registerCommand('wpipeSteps.runStep', async (item) => {
        if (vscode.env.uiKind === vscode.UIKind.Web) {
            vscode.window.showErrorMessage('Running steps requires a local Python environment.');
            return;
        }
        if (!item || !item.filePath)
            return;
        const terminal = vscode.window.createTerminal(`Run Step: ${item.label}`);
        terminal.show();
        terminal.sendText(`python "${item.filePath}"`);
    }));
}
exports.activate = activate;
class WPipeStepProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(e) {
        return e;
    }
    async getChildren(e) {
        if (!e) {
            return [
                new vscode.TreeItem('🛠️ Workspace Steps', vscode.TreeItemCollapsibleState.Expanded),
                new vscode.TreeItem('📦 Official Library', vscode.TreeItemCollapsibleState.Collapsed),
                new vscode.TreeItem('🤝 Community Plugins', vscode.TreeItemCollapsibleState.Collapsed)
            ];
        }
        const label = e.label;
        if (label.includes('Workspace'))
            return this.searchWorkspace();
        if (label.includes('Official'))
            return this.getLibItems('Official');
        if (label.includes('Community'))
            return this.getLibItems('Community');
        return [];
    }
    getLibItems(repo) {
        return CatalogManager.getSteps()
            .filter(s => s.repo === repo)
            .map(s => new LibraryItem(s));
    }
    async searchWorkspace() {
        const steps = [];
        const exclude = '{**/node_modules/**,**/.venv/**,**/venv/**,**/.env/**,**/env/**,**/.conda/**,**/conda/**,**/site-packages/**,**/wpipe/wpipe/**}';
        const files = await vscode.workspace.findFiles('**/*.py', exclude, 500); // Increased limit with better exclusion
        for (const f of files) {
            try {
                const contentData = await vscode.workspace.fs.readFile(f);
                if (contentData.length > 500000)
                    continue; // Skip huge files
                const content = new TextDecoder().decode(contentData);
                const lines = content.split('\n');
                lines.forEach((l, i) => {
                    const trimmed = l.trim();
                    if (trimmed.startsWith('@step')) {
                        const m = trimmed.match(/name=["'](.*?)["']/);
                        let name = m ? m[1] : '';
                        let target = i;
                        if (!name) {
                            for (let n = i + 1; n < i + 5 && n < lines.length; n++) {
                                const lm = lines[n].match(/(?:def|class)\s+(\w+)/);
                                if (lm) {
                                    name = lm[1];
                                    target = n;
                                    break;
                                }
                            }
                        }
                        steps.push(new StepItem(name || 'Step', f.fsPath, target));
                    }
                    if (trimmed.includes('.add_state')) {
                        const m = trimmed.match(/\.add_state\s*\((?:name\s*=\s*)?["'](.*?)["']/);
                        if (m)
                            steps.push(new StepItem(m[1], f.fsPath, i));
                        else {
                            const m2 = trimmed.match(/\.add_state\s*\(\s*(\w+)/);
                            if (m2 && !['name', 'state', 'func', 'Condition', 'Parallel', 'For', 'Background'].includes(m2[1])) {
                                steps.push(new StepItem(m2[1], f.fsPath, i));
                            }
                        }
                    }
                });
            }
            catch (e) { }
        }
        return steps;
    }
}
class StepItem extends vscode.TreeItem {
    constructor(label, filePath, line) {
        super(label);
        this.filePath = filePath;
        this.line = line;
        this.funcName = '';
        this.iconPath = new vscode.ThemeIcon('rocket');
        this.description = label; // Simplified for web compatibility
        this.contextValue = 'workspaceStep';
        this.command = { command: 'wpipeSteps.openFile', title: 'Open', arguments: [filePath, line] };
    }
}
class LibraryItem extends vscode.TreeItem {
    constructor(step) {
        super(step.name);
        this.step = step;
        this.iconPath = new vscode.ThemeIcon('cloud');
        this.description = step.namespace;
        this.tooltip = new vscode.MarkdownString(`**Step:** ${step.name}\n**Author:** ${step.author || "Official"}\n**Repo:** ${step.repo}\n**Module:** ${step.namespace}\n\n---\nClick to insert import and usage.`);
        this.contextValue = 'libraryStep';
        this.command = { command: 'wpipeSteps.insertStep', title: 'Insert', arguments: [step] };
    }
}
class DAGPanel {
    static createOrShow(uri, doc) {
        if (DAGPanel.currentPanel) {
            DAGPanel.currentPanel._panel.reveal();
            DAGPanel.currentPanel._update(doc);
            return;
        }
        const p = vscode.window.createWebviewPanel('wpipeDAG', 'WPipe Analysis', vscode.ViewColumn.Two, { enableScripts: true });
        DAGPanel.currentPanel = new DAGPanel(p, doc);
    }
    constructor(p, doc) {
        this._disposables = [];
        this._panel = p;
        this._panel.onDidDispose(() => { DAGPanel.currentPanel = undefined; }, null, this._disposables);
        this._update(doc);
        vscode.workspace.onDidChangeTextDocument(e => { if (e.document === doc)
            this._update(doc); }, null, this._disposables);
        vscode.window.onDidChangeActiveTextEditor(e => { if (e && e.document.languageId === 'python')
            this._update(e.document); }, null, this._disposables);
    }
    _update(doc) {
        const fileName = doc.fileName.split(/[\\/]/).pop() || 'Untitled';
        const res = this.parse(doc.getText(), fileName);
        this._panel.webview.html = this._getHtml(fileName, res.graph, res.stats, res.bigO);
    }
    _getHtml(fileName, graph, stats, bigO) {
        const now = new Date().toLocaleTimeString();
        return `<html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
            <script>
                window.addEventListener('load', () => {
                    mermaid.initialize({
                        startOnLoad:true, 
                        theme:'base',
                        themeVariables: {
                            primaryColor: '#007acc',
                            primaryTextColor: '#fff',
                            primaryBorderColor: '#005a9e',
                            lineColor: '#555',
                            secondaryColor: '#ce9178',
                            tertiaryColor: '#1e1e1e'
                        },
                        securityLevel:'loose',
                        flowchart: { curve: 'basis', htmlLabels: true }
                    });

                    const observer = new MutationObserver(() => {
                        const svg = document.querySelector('.mermaid svg');
                        if (svg) {
                            svg.style.width = '100%'; svg.style.height = '100%';
                            const pz = svgPanZoom(svg, { zoomEnabled: true, controlIconsEnabled: false, fit: true, center: true });
                            document.getElementById('zoom-in').onclick = () => pz.zoomIn();
                            document.getElementById('zoom-out').onclick = () => pz.zoomOut();
                            document.getElementById('zoom-reset').onclick = () => { pz.resetZoom(); pz.center(); };
                            observer.disconnect();
                        }
                    });
                    observer.observe(document.body, { childList: true, subtree: true });
                });
            </script>
            <style>
                body { background: #0a0a0a; color: #d4d4d4; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; display: flex; flex-direction: column; height: 100vh; }
                .glass-header { background: #1a1a1a; padding: 15px 30px; border-bottom: 2px solid #007acc; display: flex; justify-content: space-between; align-items: center; z-index: 100; }
                .main-layout { display: flex; flex: 1; overflow: hidden; }
                .sidebar { width: 280px; background: #161616; border-right: 1px solid #222; padding: 20px; display: flex; flex-direction: column; gap: 20px; }
                .canvas { flex: 1; position: relative; background: #0f0f0f; }
                .card { background: #1e1e1e; border: 1px solid #333; border-radius: 8px; padding: 15px; }
                .stat-item { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px; }
                .complexity-box { text-align: center; padding: 15px; border-radius: 10px; background: #111; border-left: 4px solid #ce9178; }
                .footer { background: #161616; padding: 10px 30px; border-top: 1px solid #222; font-size: 11px; color: #555; display: flex; justify-content: space-between; }
                .toolbar { position: absolute; bottom: 20px; right: 20px; display: flex; gap: 5px; background: rgba(30,30,30,0.8); padding: 5px; border-radius: 8px; border: 1px solid #444; z-index: 1000; }
                .toolbar button { background: #333; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="glass-header">
                <div><h1 style="margin:0;font-size:18px;font-weight:600;color:#4fc1ff;">🚀 WPipe Analysis Mode</h1></div>
                <div style="text-align:right"><div style="font-size:13px;color:#fff;">${fileName}</div><div style="font-size:10px;color:#666;">Sync at ${now}</div></div>
            </div>
            <div class="main-layout">
                <div class="sidebar">
                    <div class="card">
                        <h3 style="margin:0 0 10px 0; font-size:12px; color: #888;">PIPELINE STATS</h3>
                        <div class="stat-item"><span>Steps</span><b>${stats.steps}</b></div>
                        <div class="stat-item"><span>Logic Blocks</span><b>${stats.logic}</b></div>
                        <div class="stat-item"><span>Pipelines</span><b>${stats.pipes}</b></div>
                    </div>
                    <div class="complexity-box"><span style="font-size:10px;color:#888;">COMPUTATIONAL COST</span><div style="font-size:24px;font-weight:bold;color:#ce9178;margin:5px 0;">${bigO}</div><span style="font-size:10px;color:#666;">Structural Analysis</span></div>
                </div>
                <div class="canvas">
                    <div class="mermaid" id="mermaid-container">${graph}</div>
                    <div class="toolbar"><button id="zoom-in">+</button><button id="zoom-out">-</button><button id="zoom-reset">⟲</button></div>
                </div>
            </div>
            <div class="footer"><div>Copyright &copy; 2026 William Rodriguez (wisrovi)</div><div>Engine: <b>WPipe v2.4.0 LTS</b> | UI v0.7.8-HD</div></div>
        </body>
        </html>`;
    }
    parse(content, fileName) {
        let g = "flowchart TD\n  classDef step fill:#1e1e1e,stroke:#007acc,stroke-width:2px,color:#fff,rx:5,ry:5\n  classDef logic fill:#1e1e1e,stroke:#ce9178,stroke-width:2px,color:#fff,rx:2,ry:2\n  classDef startN fill:#007acc,stroke:#007acc,color:#fff\n";
        const clean = content.replace(/#.*$/gm, '');
        const startRegex = /(\w*)\.?(?:set_steps\s*\(\s*|steps\s*=\s*)\[/g;
        let m;
        let pipeCount = 0;
        let totalSteps = 0;
        let totalLogic = 0;
        let maxDepth = 0;
        while ((m = startRegex.exec(clean)) !== null) {
            pipeCount++;
            const pipeVar = m[1] || "Pipeline";
            const uid = Math.random().toString(36).substr(2, 5);
            g += `  subgraph sg_${uid} ["📦 ${pipeVar} (in ${fileName})"]\n    direction TD\n    start_${uid}(( )):::startN\n`;
            let s = m.index + m[0].length;
            let d = 1;
            let i = s;
            for (; i < clean.length; i++) {
                if (clean[i] === '[')
                    d++;
                else if (clean[i] === ']')
                    d--;
                if (d === 0)
                    break;
            }
            const res = this.parseRec(clean.substring(s, i), `start_${uid}`, "L" + uid, 0);
            g += res.graph.split('\n').map((l) => l.trim() ? "    " + l : "").join('\n') + "\n";
            totalSteps += res.steps;
            totalLogic += res.logic;
            if (res.depth > maxDepth)
                maxDepth = res.depth;
            let lastId = res.lastId;
            if (m[1]) {
                const addRegex = new RegExp(`\\s*${m[1]}\\.add_state\\s*\\(`, 'g');
                addRegex.lastIndex = i;
                let am;
                while ((am = addRegex.exec(clean)) !== null) {
                    let as = am.index + am[0].length;
                    let ad = 1;
                    let j = as;
                    for (; j < clean.length; j++) {
                        if (clean[j] === '(')
                            ad++;
                        else if (clean[j] === ')')
                            ad--;
                        if (ad === 0)
                            break;
                    }
                    const res2 = this.parseRec(clean.substring(as, j), lastId, "A" + Math.random().toString(36).substr(2, 3), 0);
                    g += res2.graph.split('\n').map((l) => l.trim() ? "    " + l : "").join('\n') + "\n";
                    totalSteps += res2.steps;
                    totalLogic += res2.logic;
                    if (res2.depth > maxDepth)
                        maxDepth = res2.depth;
                    lastId = res2.lastId;
                    const nextS = clean.substring(j).search(startRegex);
                    if (nextS !== -1 && nextS < (clean.substring(j).search(addRegex) || Infinity))
                        break;
                }
            }
            g += "  end\n";
        }
        let bigO = "O(n)";
        if (maxDepth === 1)
            bigO = "O(n²)";
        else if (maxDepth > 1)
            bigO = `O(n^${maxDepth + 1})`;
        return { graph: pipeCount > 0 ? g : "flowchart TD\n  NoPipe[No pipeline detected]", stats: { steps: totalSteps, logic: totalLogic, pipes: pipeCount }, bigO };
    }
    parseRec(content, prev, prefix, depth) {
        let graph = "";
        let curr = prev;
        let sCount = 0;
        let lCount = 0;
        let maxSubDepth = depth;
        const split = (c) => {
            const r = [];
            let cur = "";
            let d = 0;
            for (let i = 0; i < c.length; i++) {
                if (c[i] === '[' || c[i] === '(')
                    d++;
                else if (c[i] === ']' || c[i] === ')')
                    d--;
                else if (c[i] === ')')
                    d--;
                if (c[i] === ',' && d === 0) {
                    r.push(cur.trim());
                    cur = "";
                }
                else
                    cur += c[i];
            }
            if (cur.trim())
                r.push(cur.trim());
            return r;
        };
        split(content).forEach((t, i) => {
            const tr = t.trim();
            if (!tr)
                return;
            const id = "n" + prefix + i;
            if (tr.startsWith('Condition(')) {
                lCount++;
                const expr = (tr.match(/expression\s*=\s*(["'])(.*?)\1/) || ["", "", "Condition"])[2];
                graph += `  ${curr} --> ${id}{"${expr}"}:::logic\n`;
                const tCont = this.ext(tr, 'branch_true');
                const fCont = this.ext(tr, 'branch_false');
                const mid = id + "_m";
                if (tCont) {
                    const r = this.parseRec(tCont, id, id + "T", depth);
                    graph += r.graph + `  ${r.lastId} -- True --> ${mid}(( ))\n`;
                    sCount += r.steps;
                    lCount += r.logic;
                    if (r.depth > maxSubDepth)
                        maxSubDepth = r.depth;
                }
                else
                    graph += `  ${id} -- True --> ${mid}(( ))\n`;
                if (fCont) {
                    const r = this.parseRec(fCont, id, id + "F", depth);
                    graph += r.graph + `  ${r.lastId} -- False --> ${mid}(( ))\n`;
                    sCount += r.steps;
                    lCount += r.logic;
                    if (r.depth > maxSubDepth)
                        maxSubDepth = r.depth;
                }
                else
                    graph += `  ${id} -- False --> ${mid}(( ))\n`;
                curr = mid;
            }
            else if (tr.startsWith('Parallel(')) {
                lCount++;
                graph += `  ${curr} --> ${id}[[" ⚡ Parallel "]]:::logic\n`;
                const pCont = this.ext(tr, 'steps');
                const mid = id + "_m";
                if (pCont) {
                    const steps = this.smartSplit(pCont);
                    steps.forEach((ps, pi) => {
                        const r = this.parseRec(ps, id, id + "P" + pi, depth);
                        graph += r.graph + `  ${r.lastId} -- Flow --> ${mid}(( ))\n`;
                        sCount += r.steps;
                        lCount += r.logic;
                        if (r.depth > maxSubDepth)
                            maxSubDepth = r.depth;
                    });
                }
                else {
                    graph += `  ${id} --> ${mid}(( ))\n`;
                }
                curr = mid;
            }
            else if (tr.startsWith('For(')) {
                lCount++;
                graph += `  ${curr} --> ${id}[[" 🔄 For Loop "]]:::logic\n`;
                const fCont = this.ext(tr, 'steps');
                if (fCont) {
                    const r = this.parseRec(fCont, id, id + "F", depth + 1);
                    graph += r.graph + `  ${r.lastId} --> ${id}\n`;
                    sCount += r.steps;
                    lCount += r.logic;
                    if (r.depth > maxSubDepth)
                        maxSubDepth = r.depth;
                }
                curr = id;
            }
            else if (tr.startsWith('Background(')) {
                lCount++;
                const lbl = tr.match(/Background\((.*?)\)/)?.[1]?.split(',')[0].trim() || "BG Task";
                graph += `  ${curr} -. async .-> ${id}((" ⚡ ${lbl} ")):::step\n`;
            }
            else {
                let lbl = tr.split('(')[0].replace(/[\[\]]/g, '').trim();
                if (lbl) {
                    sCount++;
                    graph += `  ${curr} --> ${id}[" 🚀 ${lbl} "]:::step\n`;
                    curr = id;
                }
            }
        });
        return { graph, lastId: curr, steps: sCount, logic: lCount, depth: maxSubDepth };
    }
    ext(c, a) {
        const m = c.match(new RegExp(`${a}\\s*=\\s*\\[`));
        if (m) {
            let s = m.index + m[0].length;
            let d = 1;
            for (let i = s; i < c.length; i++) {
                if (c[i] === '[')
                    d++;
                else if (c[i] === ']')
                    d--;
                if (d === 0)
                    return c.substring(s, i);
            }
        }
        return null;
    }
    smartSplit(c) {
        const r = [];
        let cur = "";
        let d = 0;
        for (let i = 0; i < c.length; i++) {
            if (c[i] === '[' || c[i] === '(')
                d++;
            else if (c[i] === ']' || c[i] === ')')
                d--;
            if (c[i] === ',' && d === 0) {
                r.push(cur.trim());
                cur = "";
            }
            else
                cur += c[i];
        }
        if (cur.trim())
            r.push(cur.trim());
        return r;
    }
}
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map