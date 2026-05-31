import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as https from 'https';
import * as stepsCatalogRaw from './steps_catalog.json';

// --- CATALOG MANAGEMENT ---
interface StepEntry {
    name: string;
    func_name: string;
    namespace: string;
    repo: string;
    file: string;
    author?: string;
}

class CatalogManager {
    private static catalog: StepEntry[] = [];
    private static readonly OFFICIAL_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-steps/001-DEVELOPMENT/steps_catalog.json';
    private static readonly COMMUNITY_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-plugins/001-DEVELOPMENT/steps_catalog.json';

    public static async init(context: vscode.ExtensionContext): Promise<void> {
        const cachePath = path.join(context.globalStorageUri.fsPath, 'catalog_cache.json');
        
        // Ensure storage directory exists
        if (!fs.existsSync(context.globalStorageUri.fsPath)) {
            try { fs.mkdirSync(context.globalStorageUri.fsPath, { recursive: true }); } catch (e) {}
        }
        
        // 1. Load from cache immediately (Synchronous feel)
        if (fs.existsSync(cachePath)) {
            try {
                const cached = JSON.parse(fs.readFileSync(cachePath, 'utf8'));
                if (Array.isArray(cached)) this.catalog = cached;
            } catch (e) {}
        }
        
        // 2. If cache empty, use embedded data
        if (this.catalog.length === 0) {
            const raw: any = stepsCatalogRaw;
            this.catalog = Array.isArray(raw) ? raw : (raw.default || []);
        }

        // 3. Trigger background update (DO NOT AWAIT in activate)
        this.update(context, false);
    }

    public static async update(context: vscode.ExtensionContext, manual: boolean = false): Promise<void> {
        const download = async () => {
            const oldNames = new Set(this.catalog.map(s => `${s.repo}:${s.name}`));
            const fetchJson = (url: string): Promise<any[]> => new Promise(res => {
                const req = https.get(url, { timeout: 10000 }, r => {
                    let b = ''; r.on('data', d => b += d);
                    r.on('end', () => { try { const p = JSON.parse(b); res(Array.isArray(p) ? p : []); } catch (e) { res([]); } });
                });
                req.on('error', () => res([]));
                req.on('timeout', () => { req.destroy(); res([]); });
            });
            
            const [off, com] = await Promise.all([fetchJson(this.OFFICIAL_URL), fetchJson(this.COMMUNITY_URL)]);
            const newCatalog = [...off, ...com];

            if (newCatalog.length > 0) {
                const newItems = newCatalog.filter(s => !oldNames.has(`${s.repo}:${s.name}`));
                this.catalog = newCatalog;
                try {
                    const cachePath = path.join(context.globalStorageUri.fsPath, 'catalog_cache.json');
                    fs.writeFileSync(cachePath, JSON.stringify(this.catalog));
                } catch (e) {}
                
                if (newItems.length > 0) {
                    vscode.window.showInformationMessage(`🚀 ¡Hay ${newItems.length} nuevos estados en WPipe!`, "Ver Catálogo").then(selection => {
                        if (selection === "Ver Catálogo") vscode.commands.executeCommand('wpipe-vscode.searchSteps');
                    });
                } else if (manual) {
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
        } else {
            download();
        }
    }

    public static getSteps(): StepEntry[] {
        return this.catalog;
    }
}

export async function activate(context: vscode.ExtensionContext) {
    // Start Catalog Manager (Non-blocking)
    CatalogManager.init(context);

    const stepProvider = new WPipeStepProvider();
    vscode.window.registerTreeDataProvider('wpipeSteps', stepProvider);
    
    context.subscriptions.push(
        vscode.commands.registerCommand('wpipeSteps.refreshEntry', () => stepProvider.refresh()),
        vscode.commands.registerCommand('wpipe-vscode.refreshCatalog', () => CatalogManager.update(context, true)),
        
        vscode.commands.registerCommand('wpipeSteps.openFile', (f, l) => {
            vscode.workspace.openTextDocument(f).then(d => vscode.window.showTextDocument(d).then(e => {
                const p = new vscode.Position(l, 0);
                e.selection = new vscode.Selection(p, p);
                e.revealRange(new vscode.Range(p, p), vscode.TextEditorRevealType.InCenter);
            }));
        }),

        vscode.commands.registerCommand('wpipeSteps.insertStep', (step: StepEntry) => {
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
        }),

        vscode.commands.registerCommand('wpipe-vscode.searchSteps', async () => {
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
        }),

        vscode.commands.registerCommand('wpipe-vscode.previewDAG', () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) DAGPanel.createOrShow(context.extensionUri, editor.document);
        })
    );
}

class WPipeStepProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<vscode.TreeItem | undefined | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    refresh() {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(e: vscode.TreeItem): vscode.TreeItem {
        return e;
    }

    async getChildren(e?: vscode.TreeItem): Promise<vscode.TreeItem[]> {
        if (!e) {
            return [
                new vscode.TreeItem('🛠️ Workspace Steps', vscode.TreeItemCollapsibleState.Expanded),
                new vscode.TreeItem('📦 Official Library', vscode.TreeItemCollapsibleState.Collapsed),
                new vscode.TreeItem('🤝 Community Plugins', vscode.TreeItemCollapsibleState.Collapsed)
            ];
        }

        const label = e.label as string;
        if (label.includes('Workspace')) return this.searchWorkspace();
        if (label.includes('Official')) return this.getLibItems('Official');
        if (label.includes('Community')) return this.getLibItems('Community');
        return [];
    }

    private getLibItems(repo: string): LibraryItem[] {
        return CatalogManager.getSteps()
            .filter(s => s.repo === repo)
            .map(s => new LibraryItem(s));
    }

    private async searchWorkspace(): Promise<StepItem[]> {
        const steps: StepItem[] = [];
        const exclude = '**/node_modules/**, **/.venv/**, **/site-packages/**, **/wpipe/wpipe/**';
        const files = await vscode.workspace.findFiles('**/*.py', exclude, 50); // Limit to 50 files for performance
        
        for (const f of files) {
            try {
                const content = fs.readFileSync(f.fsPath, 'utf8');
                if (content.length > 500000) continue; // Skip huge files
                
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
                                if (lm) { name = lm[1]; target = n; break; }
                            }
                        }
                        steps.push(new StepItem(name || 'Step', f.fsPath, target));
                    }
                    if (trimmed.includes('.add_state')) {
                        const m = trimmed.match(/\.add_state\s*\((?:name\s*=\s*)?["'](.*?)["']/);
                        if (m) steps.push(new StepItem(m[1], f.fsPath, i));
                        else {
                            const m2 = trimmed.match(/\.add_state\s*\(\s*(\w+)/);
                            if (m2 && !['name', 'state', 'func', 'Condition', 'Parallel', 'For', 'Background'].includes(m2[1])) {
                                steps.push(new StepItem(m2[1], f.fsPath, i));
                            }
                        }
                    }
                });
            } catch (e) {}
        }
        return steps;
    }
}

class StepItem extends vscode.TreeItem {
    constructor(label: string, public filePath: string, public line: number) {
        super(label);
        this.iconPath = new vscode.ThemeIcon('rocket');
        this.description = path.basename(filePath);
        this.contextValue = 'workspaceStep';
        this.command = { command: 'wpipeSteps.openFile', title: 'Open', arguments: [filePath, line] };
    }
    public funcName: string = '';
}

class LibraryItem extends vscode.TreeItem {
    constructor(public step: StepEntry) {
        super(step.name);
        this.iconPath = new vscode.ThemeIcon('cloud');
        this.description = step.namespace;
        this.tooltip = new vscode.MarkdownString(`**Step:** ${step.name}\n**Author:** ${step.author || "Official"}\n**Repo:** ${step.repo}\n**Module:** ${step.namespace}\n\n---\nClick to insert import and usage.`);
        this.contextValue = 'libraryStep';
        this.command = { command: 'wpipeSteps.insertStep', title: 'Insert', arguments: [step] };
    }
}

class DAGPanel {
    public static currentPanel: DAGPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    public static createOrShow(uri: vscode.Uri, doc: vscode.TextDocument) {
        if (DAGPanel.currentPanel) { DAGPanel.currentPanel._panel.reveal(); DAGPanel.currentPanel._update(doc); return; }
        const p = vscode.window.createWebviewPanel('wpipeDAG', 'WPipe Analysis', vscode.ViewColumn.Two, { enableScripts: true });
        DAGPanel.currentPanel = new DAGPanel(p, doc);
    }

    private constructor(p: vscode.WebviewPanel, doc: vscode.TextDocument) {
        this._panel = p;
        this._panel.onDidDispose(() => { DAGPanel.currentPanel = undefined; }, null, this._disposables);
        this._update(doc);
        vscode.workspace.onDidChangeTextDocument(e => { if (e.document === doc) this._update(doc); }, null, this._disposables);
        vscode.window.onDidChangeActiveTextEditor(e => { if (e && e.document.languageId === 'python') this._update(e.document); }, null, this._disposables);
    }

    private _update(doc: vscode.TextDocument) {
        const fileName = path.basename(doc.fileName);
        const res = this.parse(doc.getText(), fileName);
        this._panel.webview.html = this._getHtml(fileName, res.graph, res.stats, res.bigO);
    }

    private _getHtml(fileName: string, graph: string, stats: any, bigO: string) {
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
            <div class="footer"><div>Copyright &copy; 2026 William Rodriguez (wisrovi)</div><div>Engine: <b>WPipe v2.3.6 LTS</b> | UI v0.7.8-HD</div></div>
        </body>
        </html>`;
    }

    private parse(content: string, fileName: string): any {
        let g = "flowchart TD\n  classDef step fill:#1e1e1e,stroke:#007acc,stroke-width:2px,color:#fff,rx:5,ry:5\n  classDef logic fill:#1e1e1e,stroke:#ce9178,stroke-width:2px,color:#fff,rx:2,ry:2\n  classDef startN fill:#007acc,stroke:#007acc,color:#fff\n";
        const clean = content.replace(/#.*$/gm, '');
        const startRegex = /(\w*)\.?(?:set_steps\s*\(\s*|steps\s*=\s*)\[/g;
        let m; let pipeCount = 0; let totalSteps = 0; let totalLogic = 0; let maxDepth = 0;
        while ((m = startRegex.exec(clean)) !== null) {
            pipeCount++; const pipeVar = m[1] || "Pipeline"; const uid = Math.random().toString(36).substr(2, 5);
            g += `  subgraph sg_${uid} ["📦 ${pipeVar} (in ${fileName})"]\n    direction TD\n    start_${uid}(( )):::startN\n`;
            let s = m.index + m[0].length; let d = 1; let i = s;
            for (; i < clean.length; i++) { if (clean[i] === '[') d++; else if (clean[i] === ']') d--; if (d === 0) break; }
            const res = this.parseRec(clean.substring(s, i), `start_${uid}`, "L" + uid, 0);
            g += res.graph.split('\n').map((l: string) => l.trim() ? "    " + l : "").join('\n') + "\n";
            totalSteps += res.steps; totalLogic += res.logic; if (res.depth > maxDepth) maxDepth = res.depth;
            let lastId = res.lastId;
            if (m[1]) {
                const addRegex = new RegExp(`\\s*${m[1]}\\.add_state\\s*\\(`, 'g'); addRegex.lastIndex = i; let am;
                while ((am = addRegex.exec(clean)) !== null) {
                    let as = am.index + am[0].length; let ad = 1; let j = as;
                    for (; j < clean.length; j++) { if (clean[j] === '(') ad++; else if (clean[j] === ')') ad--; if (ad === 0) break; }
                    const res2 = this.parseRec(clean.substring(as, j), lastId, "A" + Math.random().toString(36).substr(2, 3), 0);
                    g += res2.graph.split('\n').map((l: string) => l.trim() ? "    " + l : "").join('\n') + "\n";
                    totalSteps += res2.steps; totalLogic += res2.logic; if (res2.depth > maxDepth) maxDepth = res2.depth; lastId = res2.lastId;
                    const nextS = clean.substring(j).search(startRegex); if (nextS !== -1 && nextS < (clean.substring(j).search(addRegex) || Infinity)) break;
                }
            }
            g += "  end\n";
        }
        let bigO = "O(n)"; if (maxDepth === 1) bigO = "O(n²)"; else if (maxDepth > 1) bigO = `O(n^${maxDepth + 1})`;
        return { graph: pipeCount > 0 ? g : "flowchart TD\n  NoPipe[No pipeline detected]", stats: { steps: totalSteps, logic: totalLogic, pipes: pipeCount }, bigO };
    }

    private parseRec(content: string, prev: string, prefix: string, depth: number): any {
        let graph = ""; let curr = prev; let sCount = 0; let lCount = 0; let maxSubDepth = depth;
        const split = (c: string) => {
            const r: string[] = []; let cur = ""; let d = 0;
            for (let i = 0; i < c.length; i++) {
                if (c[i] === '[' || c[i] === '(') d++; else if (c[i] === ']' || c[i] === ')') d--; else if (c[i] === ')') d--;
                if (c[i] === ',' && d === 0) { r.push(cur.trim()); cur = ""; } else cur += c[i];
            }
            if (cur.trim()) r.push(cur.trim()); return r;
        };
        split(content).forEach((t, i) => {
            const tr = t.trim(); if (!tr) return;
            const id = "n" + prefix + i;
            if (tr.startsWith('Condition(')) {
                lCount++; const expr = (tr.match(/expression\s*=\s*(["'])(.*?)\1/) || ["", "", "Condition"])[2];
                graph += `  ${curr} --> ${id}{"${expr}"}:::logic\n`;
                const tCont = this.ext(tr, 'branch_true'); const fCont = this.ext(tr, 'branch_false'); const mid = id + "_m";
                if (tCont) { const r = this.parseRec(tCont, id, id + "T", depth); graph += r.graph + `  ${r.lastId} -- True --> ${mid}(( ))\n`; sCount += r.steps; lCount += r.logic; if (r.depth > maxSubDepth) maxSubDepth = r.depth; }
                else graph += `  ${id} -- True --> ${mid}(( ))\n`;
                if (fCont) { const r = this.parseRec(fCont, id, id + "F", depth); graph += r.graph + `  ${r.lastId} -- False --> ${mid}(( ))\n`; sCount += r.steps; lCount += r.logic; if (r.depth > maxSubDepth) maxSubDepth = r.depth; }
                else graph += `  ${id} -- False --> ${mid}(( ))\n`;
                curr = mid;
            } else if (tr.startsWith('Parallel(')) {
                lCount++; graph += `  ${curr} --> ${id}[[" ⚡ Parallel "]]:::logic\n`;
                const pCont = this.ext(tr, 'steps'); const mid = id + "_m";
                if (pCont) {
                    const steps = this.smartSplit(pCont);
                    steps.forEach((ps, pi) => {
                        const r = this.parseRec(ps, id, id + "P" + pi, depth);
                        graph += r.graph + `  ${r.lastId} -- Flow --> ${mid}(( ))\n`;
                        sCount += r.steps; lCount += r.logic; if (r.depth > maxSubDepth) maxSubDepth = r.depth;
                    });
                } else { graph += `  ${id} --> ${mid}(( ))\n`; }
                curr = mid;
            } else if (tr.startsWith('For(')) {
                lCount++; graph += `  ${curr} --> ${id}[[" 🔄 For Loop "]]:::logic\n`;
                const fCont = this.ext(tr, 'steps');
                if (fCont) { const r = this.parseRec(fCont, id, id + "F", depth + 1); graph += r.graph + `  ${r.lastId} --> ${id}\n`; sCount += r.steps; lCount += r.logic; if (r.depth > maxSubDepth) maxSubDepth = r.depth; }
                curr = id;
            } else if (tr.startsWith('Background(')) {
                lCount++; const lbl = tr.match(/Background\((.*?)\)/)?.[1]?.split(',')[0].trim() || "BG Task";
                graph += `  ${curr} -. async .-> ${id}((" ⚡ ${lbl} ")):::step\n`;
            } else {
                let lbl = tr.split('(')[0].replace(/[\[\]]/g, '').trim();
                if (lbl) { sCount++; graph += `  ${curr} --> ${id}[" 🚀 ${lbl} "]:::step\n`; curr = id; }
            }
        });
        return { graph, lastId: curr, steps: sCount, logic: lCount, depth: maxSubDepth };
    }
    private ext(c: string, a: string): string | null {
        const m = c.match(new RegExp(`${a}\\s*=\\s*\\[`));
        if (m) {
            let s = m.index! + m[0].length; let d = 1;
            for (let i = s; i < c.length; i++) { if (c[i] === '[') d++; else if (c[i] === ']') d--; if (d === 0) return c.substring(s, i); }
        }
        return null;
    }
    private smartSplit(c: string): string[] {
        const r: string[] = []; let cur = ""; let d = 0;
        for (let i = 0; i < c.length; i++) {
            if (c[i] === '[' || c[i] === '(') d++; else if (c[i] === ']' || c[i] === ')') d--;
            if (c[i] === ',' && d === 0) { r.push(cur.trim()); cur = ""; } else cur += c[i];
        }
        if (cur.trim()) r.push(cur.trim()); return r;
    }
}

export function deactivate() {}
