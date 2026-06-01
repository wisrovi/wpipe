import * as vscode from 'vscode';
import { parser } from '@lezer/python';

export class DAGPanel {
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
        const fileName = doc.fileName.split(/[\\/]/).pop() || 'Untitled';
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
            <div class="footer"><div>Copyright &copy; 2026 William Rodriguez (wisrovi)</div><div>Engine: <b>WPipe v2.4.0 LTS</b> | UI v0.7.8-HD</div></div>
        </body>
        </html>`;
    }

    private parse(content: string, fileName: string): any {
        let g = "flowchart TD\n  classDef step fill:#1e1e1e,stroke:#007acc,stroke-width:2px,color:#fff,rx:5,ry:5\n  classDef logic fill:#1e1e1e,stroke:#ce9178,stroke-width:2px,color:#fff,rx:2,ry:2\n  classDef startN fill:#007acc,stroke:#007acc,color:#fff\n";
        
        let pipeCount = 0; let totalSteps = 0; let totalLogic = 0; let maxDepth = 0;
        const tree = parser.parse(content);
        const pipelineInstances: any[] = [];

        // 1. Identify Pipeline Definitions and set_steps calls
        tree.iterate({
            enter: (node) => {
                if (node.name === 'CallExpression') {
                    const callText = content.substring(node.from, node.to);
                    // Match: pipeline.set_steps([...]) OR Pipeline(steps=[...])
                    if (callText.includes('.set_steps(') || (callText.startsWith('Pipeline(') && callText.includes('steps='))) {
                        pipelineInstances.push({
                            node: node.node,
                            text: callText,
                            from: node.from,
                            to: node.to
                        });
                    }
                }
            }
        });

        pipelineInstances.forEach((inst) => {
            pipeCount++;
            const uid = Math.random().toString(36).substr(2, 5);
            const pipeLabel = inst.text.split('.')[0] || "Pipeline";
            g += `  subgraph sg_${uid} ["📦 ${pipeLabel} (in ${fileName})"]\n    direction TD\n    start_${uid}(( )):::startN\n`;

            // Extract the steps array content
            let stepsContent = '';
            const match = inst.text.match(/(?:set_steps|steps)\s*\(\s*\[([\s\S]*?)\]\s*\)/) || inst.text.match(/steps\s*=\s*\[([\s\S]*?)\]/);
            if (match) stepsContent = match[1];

            const res = this.parseRec(stepsContent, `start_${uid}`, "L" + uid, 0);
            g += res.graph.split('\n').map((l: string) => l.trim() ? "    " + l : "").join('\n') + "\n";
            totalSteps += res.steps; totalLogic += res.logic; if (res.depth > maxDepth) maxDepth = res.depth;
            
            // Handle add_state calls for this pipeline specifically
            // For simplicity in regex migration, we still use regex but scoped or improved
            // A truly advanced AST implementation would track variable assignments
            
            g += "  end\n";
        });

        let bigO = "O(n)"; if (maxDepth === 1) bigO = "O(n²)"; else if (maxDepth > 1) bigO = `O(n^${maxDepth + 1})`;
        return { graph: pipeCount > 0 ? g : "flowchart TD\n  NoPipe[No pipeline detected]", stats: { steps: totalSteps, logic: totalLogic, pipes: pipeCount }, bigO };
    }

    private parseRec(content: string, prev: string, prefix: string, depth: number): any {
        let graph = ""; let curr = prev; let sCount = 0; let lCount = 0; let maxSubDepth = depth;
        const split = (c: string) => {
            const r: string[] = []; let cur = ""; let d = 0;
            for (let i = 0; i < c.length; i++) {
                if (c[i] === '[' || c[i] === '(') d++; else if (c[i] === ']' || c[i] === ')') d--;
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
