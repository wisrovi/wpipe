import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
    console.log('WPipe Tools extension is now active');

    const stepProvider = new WPipeStepProvider();
    vscode.window.registerTreeDataProvider('wpipeSteps', stepProvider);
    vscode.commands.registerCommand('wpipeSteps.refreshEntry', () => stepProvider.refresh());
    vscode.commands.registerCommand('wpipeSteps.openFile', (filePath: string, line: number) => {
        vscode.workspace.openTextDocument(filePath).then(doc => {
            vscode.window.showTextDocument(doc).then(editor => {
                const pos = new vscode.Position(line, 0);
                editor.selection = new vscode.Selection(pos, pos);
                editor.revealRange(new vscode.Range(pos, pos));
            });
        });
    });

    vscode.commands.registerCommand('wpipeSteps.runStep', (item: StepItem) => {
        const terminal = vscode.window.createTerminal(`Test Step: ${item.label}`);
        terminal.show();
        const script = `from wpipe import Pipeline; from ${path.basename(item.filePath, '.py')} import ${item.funcName || item.label}; p = Pipeline('Test'); p.set_steps([${item.funcName || item.label}]); print(p.run({}))`;
        terminal.sendText(`python3 -c "${script}"`);
    });

    let showCheatSheet = vscode.commands.registerCommand('wpipe-vscode.showCheatSheet', () => {
        const panel = vscode.window.createWebviewPanel('wpipeCheatSheet', 'WPipe: Quick Help', vscode.ViewColumn.Beside, {});
        panel.webview.html = `<html>
        <body style="font-family: sans-serif; padding: 20px; background-color: #1e1e1e; color: #d4d4d4;">
            <h1 style="color: #4fc1ff;">🚀 WPipe VS Code Cheat Sheet</h1>
            <p>Utiliza estos atajos (snippets) escribiendo el prefijo en cualquier archivo Python y presionando <b>Tab</b> o <b>Enter</b>.</p>

            <h2 style="color: #ce9178; border-bottom: 1px solid #444; padding-bottom: 5px;">🏗️ Pipelines</h2>
            <ul>
                <li><b><code style="color:#569cd6;">wppipe</code></b>: Crea un Pipeline básico con DB y recolección de métricas.</li>
                <li><b><code style="color:#569cd6;">wppipeadv</code></b>: Pipeline avanzado (reintentos globales, métricas, config externa).</li>
            </ul>

            <h2 style="color: #ce9178; border-bottom: 1px solid #444; padding-bottom: 5px;">🧩 Steps (Pasos)</h2>
            <ul>
                <li><b><code style="color:#569cd6;">wpstep</code></b>: Función básica decorada con <code>@step</code>.</li>
                <li><b><code style="color:#569cd6;">wpstate</code></b>: Clase básica decorada con <code>@step</code> y <code>@to_obj</code>.</li>
                <li><b><code style="color:#569cd6;">wpstepadv</code></b>: Clase avanzada (Timeout, Retries, Tags, Contexto tipado).</li>
                <li><b><code style="color:#569cd6;">wperrorcapture</code></b>: Plantilla para un capturador de errores global del pipeline.</li>
            </ul>

            <h2 style="color: #ce9178; border-bottom: 1px solid #444; padding-bottom: 5px;">🔀 Flujo y Lógica</h2>
            <ul>
                <li><b><code style="color:#569cd6;">wpcondition</code></b>: Bifurcación condicional (If/Else).</li>
                <li><b><code style="color:#569cd6;">wpparallel</code></b>: Ejecución de pasos en paralelo (Hilos/Procesos).</li>
                <li><b><code style="color:#569cd6;">wpfor</code></b>: Bucle iterativo con condición de validación.</li>
                <li><b><code style="color:#569cd6;">wpbackground</code></b>: Tarea no bloqueante (Fire and forget).</li>
                <li><b><code style="color:#569cd6;">wpcheckpoint</code></b>: Punto de control para reanudar ejecuciones fallidas.</li>
            </ul>

            <h2 style="color: #ce9178; border-bottom: 1px solid #444; padding-bottom: 5px;">📊 Monitoreo y Alertas</h2>
            <ul>
                <li><b><code style="color:#569cd6;">wpevent</code></b>: Registrar un evento personalizado (Requiere DB).</li>
                <li><b><code style="color:#569cd6;">wpalert</code></b>: Configurar un umbral de alerta de rendimiento (Requiere DB).</li>
            </ul>

            <h2 style="color: #ce9178; border-bottom: 1px solid #444; padding-bottom: 5px;">🖥️ Comandos de VS Code</h2>
            <ul>
                <li><b>Preview DAG</b> (Icono de Grafo): Genera un grafo de Mermaid del pipeline actual y lo exporta a <code>.mermaid</code>.</li>
                <li><b>Open Dashboard</b>: Levanta el servidor local del Dashboard pidiendo parámetros (DB, config, puerto).</li>
                <li><b>Run this Step</b> (Icono Play en el Panel Lateral): Ejecuta un paso de forma aislada para probarlo rápidamente.</li>
            </ul>
        </body>
        </html>`;
    });

    let openDashboard = vscode.commands.registerCommand('wpipe-vscode.openDashboard', async () => {
        const dbUris = await vscode.window.showOpenDialog({
            canSelectMany: false,
            openLabel: 'Seleccionar BD de Tracking',
            filters: {
                'Archivos de Base de Datos': ['db', 'sqlite', 'db-wal', 'db-shm'],
                'Todos los archivos': ['*']
            },
            title: "Selecciona la base de datos de tracking de WPipe"
        });

        if (!dbUris || dbUris.length === 0) return;
        const dbPath = dbUris[0].fsPath;

        const configDir = await vscode.window.showInputBox({
            prompt: "Ingresa el directorio de configuración (vacío si no usas)",
            placeHolder: "Ej. configs",
            value: "configs"
        });

        const port = await vscode.window.showInputBox({
            prompt: "Ingresa el puerto para el dashboard",
            placeHolder: "Ej. 8035",
            value: "8035"
        });
        if (!port) return;

        const terminal = vscode.window.createTerminal("WPipe Dashboard");
        let cmd = `python -m wpipe.dashboard --db "${dbPath}" --port ${port} --open`;
        if (configDir && configDir.trim() !== "") {
            cmd += ` --config-dir "${configDir}"`;
        }
        terminal.sendText(cmd);
        terminal.show();
    });

    let previewDAG = vscode.commands.registerCommand('wpipe-vscode.previewDAG', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            DAGPanel.createOrShow(context.extensionUri, editor.document);
        }
    });

    context.subscriptions.push(showCheatSheet, openDashboard, previewDAG);
}

class WPipeStepProvider implements vscode.TreeDataProvider<StepItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<StepItem | undefined | void> = new vscode.EventEmitter<StepItem | undefined | void>();
    readonly onDidChangeTreeData: vscode.Event<StepItem | undefined | void> = this._onDidChangeTreeData.event;
    refresh(): void { this._onDidChangeTreeData.fire(); }
    getTreeItem(element: StepItem): vscode.TreeItem { return element; }
    getChildren(element?: StepItem): Thenable<StepItem[]> { return this.searchStepsInWorkspace(); }

    private async searchStepsInWorkspace(): Promise<StepItem[]> {
        const steps: StepItem[] = [];
        const folders = vscode.workspace.workspaceFolders;
        if (!folders) return [];
        for (const folder of folders) {
            const files = await vscode.workspace.findFiles(new vscode.RelativePattern(folder, '**/*.py'), '**/node_modules/**');
            for (const file of files) {
                try {
                    const content = fs.readFileSync(file.fsPath, 'utf8');
                    const lines = content.split('\n');
                    lines.forEach((line, idx) => {
                        if (line.includes('@step')) {
                            const match = line.match(/name=["'](.*?)["']/);
                            const stepName = match ? match[1] : "Unnamed Step";
                            let funcName = "";
                            if (lines[idx + 1]) {
                                const funcMatch = lines[idx + 1].match(/(def|class)\s+(\w+)/);
                                if (funcMatch) funcName = funcMatch[2];
                            }
                            steps.push(new StepItem(stepName, file.fsPath, idx, funcName, vscode.TreeItemCollapsibleState.None));
                        }
                    });
                } catch (e) {}
            }
        }
        return steps;
    }
}

class StepItem extends vscode.TreeItem {
    constructor(public readonly label: string, public readonly filePath: string, public readonly line: number, public readonly funcName: string, public readonly collapsibleState: vscode.TreeItemCollapsibleState) {
        super(label, collapsibleState);
        this.contextValue = 'step';
        this.description = path.basename(this.filePath);
        this.iconPath = new vscode.ThemeIcon('rocket');
        this.command = { command: 'wpipeSteps.openFile', title: 'Open File', arguments: [this.filePath, this.line] };
    }
}

class DAGPanel {
    public static currentPanel: DAGPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    public static createOrShow(extensionUri: vscode.Uri, document: vscode.TextDocument) {
        if (DAGPanel.currentPanel) {
            DAGPanel.currentPanel._panel.reveal();
            DAGPanel.currentPanel._update(document);
            return;
        }
        const panel = vscode.window.createWebviewPanel('wpipeDAG', 'WPipe Pipeline Preview', vscode.ViewColumn.Two, { enableScripts: true });
        DAGPanel.currentPanel = new DAGPanel(panel, document);
    }

    private constructor(panel: vscode.WebviewPanel, document: vscode.TextDocument) {
        this._panel = panel;
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._update(document);
        vscode.workspace.onDidChangeTextDocument(e => { if (e.document === document) this._update(document); }, null, this._disposables);
        vscode.window.onDidChangeActiveTextEditor(e => { if (e && (e.document.languageId === 'yaml' || e.document.languageId === 'python')) this._update(e.document); }, null, this._disposables);
    }

    private _update(document: vscode.TextDocument) {
        const content = document.getText();
        const mermaidGraph = (document.languageId === 'yaml' ? this.parseYaml(content) : this.parsePython(content));
        
        try {
            const filePath = document.fileName;
            if (filePath && !filePath.includes('extension-output')) {
                const dir = path.dirname(filePath);
                const baseName = path.basename(filePath, path.extname(filePath));
                const mermaidPath = path.join(dir, `${baseName}.mermaid`);
                fs.writeFileSync(mermaidPath, mermaidGraph);
            }
        } catch (e) {
            console.error("Error writing mermaid file:", e);
        }

        this._panel.webview.html = this._getHtmlForWebview(document, mermaidGraph);
    }

    private _getHtmlForWebview(document: vscode.TextDocument, mermaidGraph: string) {
        return `<html><head><script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script><script>mermaid.initialize({startOnLoad:true, theme: 'dark', securityLevel: 'loose'});</script><style>body { background-color: #1e1e1e; color: white; padding: 20px; font-family: sans-serif; }</style></head><body><h3>Visualización de Pipeline: ${path.basename(document.fileName)}</h3><div class="mermaid">${mermaidGraph}</div></body></html>`;
    }

    private sanitizeID(id: string, suffix?: string): string {
        return "n_" + id.replace(/[^a-zA-Z0-9]/g, '_') + (suffix ? "_" + suffix : "");
    }

    private parseYaml(content: string): string {
        let g = "flowchart TD\n";
        g += "  Start((Start))\n";
        let p = "Start";
        const lines = content.split('\n');
        let inSteps = false;

        for (let i = 0; i < lines.length; i++) {
            const t = lines[i].trim();
            if (t.startsWith('steps:')) {
                inSteps = true;
                continue;
            }
            if (inSteps && t.startsWith('-')) {
                const nameMatch = t.match(/name:\s*["']?(.*?)["']?$/) || 
                                 t.match(/function:\s*["']?(.*?)["']?$/) ||
                                 lines[i+1]?.match(/name:\s*["']?(.*?)["']?$/);
                
                if (nameMatch) {
                    const name = nameMatch[1];
                    const n = this.sanitizeID(name, i.toString());
                    g += `  ${p} --> ${n}["${name}"]\n`;
                    p = n;
                }
            }
        }
        return g;
    }

    private parsePython(content: string): string {
        let g = "flowchart TD\n";
        g += "  Inicio((Inicio))\n";
        
        // Remover comentarios de Python para que no rompan el parser
        const cleanContent = content.replace(/#.*$/gm, '');
        
        const startRegex = /(?:set_steps\s*\(\s*|steps\s*=\s*)\[/g;
        let match;
        let bestContent = "";
        
        while ((match = startRegex.exec(cleanContent)) !== null) {
            let start = match.index + match[0].length;
            let depth = 1;
            let i = start;
            for (; i < cleanContent.length; i++) {
                if (cleanContent[i] === '[') depth++;
                else if (cleanContent[i] === ']') depth--;
                if (depth === 0) break;
            }
            const currentContent = cleanContent.substring(start, i);
            if (currentContent.length > bestContent.length) {
                bestContent = currentContent;
            }
        }

        if (bestContent) {
            const result = this.parseRecursive(bestContent, "Inicio");
            g += result.graph;
        }
        return g || "flowchart TD\n  Inicio --> DefineSteps";
    }

    private parseRecursive(content: string, prevId: string, levelPrefix = "L"): { graph: string, lastId: string } {
        let graph = "";
        let currentPrev = prevId;
        const steps = this.smartSplit(content);

        steps.forEach((stepText, idx) => {
            const trimmed = stepText.trim();
            if (!trimmed) return;

            const uniqueSuffix = levelPrefix + idx;

            if (trimmed.startsWith('Condition(')) {
                const condExpr = (trimmed.match(/expression=["'](.*?)["']/) || ["", "Condition"])[1];
                const id = this.sanitizeID("Cond", uniqueSuffix);
                const mergeId = this.sanitizeID("Merge", uniqueSuffix);

                graph += `  ${currentPrev} --> ${id}{"${condExpr}"}\n`;
                
                const branchEnds: string[] = [];
                const trueContent = this.extractArg(trimmed, 'branch_true');
                if (trueContent) {
                    const res = this.parseRecursive(trueContent, id + " -- True", uniqueSuffix + "T");
                    graph += res.graph;
                    branchEnds.push(res.lastId);
                }
                
                const falseContent = this.extractArg(trimmed, 'branch_false');
                if (falseContent) {
                    const res = this.parseRecursive(falseContent, id + " -- False", uniqueSuffix + "F");
                    graph += res.graph;
                    branchEnds.push(res.lastId);
                } else {
                    branchEnds.push(id);
                }
                
                graph += `  ${mergeId}(( ))\n`;
                branchEnds.forEach(endId => { graph += `  ${endId} --> ${mergeId}\n`; });
                currentPrev = mergeId;

            } else if (trimmed.startsWith('Parallel(')) {
                const subId = this.sanitizeID("SubPar", uniqueSuffix);
                const callId = this.sanitizeID("ParCall", uniqueSuffix);
                const workers = (trimmed.match(/max_workers=(\d+|[a-zA-Z_]+)/) || ["", "auto"])[1];

                graph += `  ${currentPrev} --> ${callId}[Parallel]\n`;
                graph += `  ${callId} --> ${subId}\n`;
                graph += `  subgraph ${subId} [Parallel max_workers=${workers}]\n`;
                
                const parallelSteps = this.extractArg(trimmed, 'steps');
                const branchEnds: string[] = [];
                if (parallelSteps) {
                    this.smartSplit(parallelSteps).forEach((ps, pIdx) => {
                        const psId = this.sanitizeID("PStart_" + pIdx, uniqueSuffix);
                        graph += `    ${psId}(( ))\n`;
                        const res = this.parseRecursive(ps, psId, uniqueSuffix + "P" + pIdx);
                        graph += res.graph.split('\n').map(l => l.trim() ? "    " + l.trim() : "").join('\n') + "\n";
                        branchEnds.push(res.lastId);
                    });
                }
                graph += `  end\n`;
                
                const mergeId = this.sanitizeID("PMerge", uniqueSuffix);
                graph += `  ${mergeId}(( ))\n`;
                branchEnds.forEach(endId => { graph += `  ${endId} --> ${mergeId}\n`; });
                currentPrev = mergeId;

            } else if (trimmed.startsWith('For(')) {
                const subId = this.sanitizeID("SubFor", uniqueSuffix);
                const callId = this.sanitizeID("ForCall", uniqueSuffix);
                const iters = (trimmed.match(/iterations=(\d+|[a-zA-Z_]+)/) || ["", "?"])[1];
                const cond = (trimmed.match(/validation_expression=["'](.*?)["']/) || ["", ""])[1];
                const label = `For iterations=${iters}${cond ? '<br/>' + cond : ''}`;

                graph += `  ${currentPrev} --> ${callId}[For Loop]\n`;
                graph += `  ${callId} --> ${subId}\n`;
                graph += `  subgraph ${subId} [${label}]\n`;
                
                const forSteps = this.extractArg(trimmed, 'steps');
                let lastInFor = subId;
                if (forSteps) {
                    const innerStart = this.sanitizeID("ForInner", uniqueSuffix);
                    graph += `    ${innerStart}(( ))\n`;
                    const res = this.parseRecursive(forSteps, innerStart, uniqueSuffix + "F");
                    graph += res.graph.split('\n').map(l => l.trim() ? "    " + l.trim() : "").join('\n') + "\n";
                    lastInFor = res.lastId;
                }
                graph += `  end\n`;
                currentPrev = subId;

            } else if (trimmed.startsWith('Background(')) {
                const subId = this.sanitizeID("SubBG", uniqueSuffix);
                const callId = this.sanitizeID("BGCall", uniqueSuffix);
                const labelMatch = trimmed.match(/Background\((.*?)\)/);
                const inner = labelMatch ? labelMatch[1].split(',')[0].trim() : "Background";
                
                let label = inner;
                if (inner.startsWith('(')) {
                    const parts = this.smartSplit(inner.substring(1, inner.length - 1));
                    if (parts.length > 1) label = parts[1].replace(/['"]/g, '').trim();
                }

                graph += `  ${currentPrev} --> ${callId}["Background ${label}"]\n`;
                graph += `  subgraph ${subId} [Background Execution]\n`;
                const execId = this.sanitizeID("BGExec", uniqueSuffix);
                graph += `    ${execId}["${label}"]\n`;
                graph += `  end\n`;
                graph += `  ${callId} -. async .-> ${execId}\n`;
                currentPrev = callId;

            } else {
                let label = "";
                if (trimmed.startsWith('(')) {
                    const inner = trimmed.substring(1, trimmed.length - 1);
                    const parts = this.smartSplit(inner);
                    if (parts.length > 1) {
                        label = parts[1].replace(/['"]/g, '').trim();
                    } else if (parts.length > 0) {
                        label = parts[0].trim();
                    }
                } else {
                    label = trimmed.split('(')[0].replace(/[\[\]]/g, '').trim();
                }

                if (label) {
                    label = label.replace(/"/g, "'"); // Escape double quotes for mermaid
                    const id = this.sanitizeID(label, uniqueSuffix);
                    graph += `  ${currentPrev} --> ${id}["${label}"]\n`;
                    currentPrev = id;
                }
            }
        });
        return { graph, lastId: currentPrev };
    }

    private extractArg(content: string, argName: string): string | null {
        const listRegex = new RegExp(`${argName}\\s*=\\s*\\[`);
        const listMatch = content.match(listRegex);
        if (listMatch) {
            let start = listMatch.index! + listMatch[0].length;
            let depth = 1;
            for (let i = start; i < content.length; i++) {
                if (content[i] === '[') depth++;
                else if (content[i] === ']') depth--;
                if (depth === 0) return content.substring(start, i);
            }
        }
        const singleRegex = new RegExp(`${argName}\\s*=\\s*([^,)]+)`);
        const singleMatch = content.match(singleRegex);
        if (singleMatch) return singleMatch[1].trim();
        return null;
    }

    private smartSplit(content: string): string[] {
        const result: string[] = [];
        let current = ""; let depth = 0;
        for (let i = 0; i < content.length; i++) {
            const char = content[i];
            if (char === '[' || char === '(') depth++;
            else if (char === ']' || char === ')') depth--;
            if (char === ',' && depth === 0) { result.push(current.trim()); current = ""; }
            else current += char;
        }
        if (current.trim()) result.push(current.trim());
        return result;
    }

    public dispose() {
        DAGPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) this._disposables.pop()?.dispose();
    }
}

export function deactivate() {}
