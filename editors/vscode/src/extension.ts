import * as vscode from 'vscode';
import { CatalogManager, StepEntry } from './core/catalog';
import { WPipeStepProvider, StepItem, LibraryItem, CategoryItem } from './providers/stepProvider';
import { DAGPanel } from './webviews/dagPanel';
import { showCheatSheet } from './webviews/cheatSheet';
import { showAiAssistant } from './webviews/aiAssistant';
import { openDashboard } from './commands/dashboard';
import { replayLogErrors } from './commands/replayLogs';
import { findStepUsage } from './commands/impactAnalysis';
import { WPipeCodeLensProvider } from './providers/codeLensProvider';
import { WPipeHoverProvider } from './providers/hoverProvider';
import { WPipeCodeActionProvider } from './providers/codeActionProvider';
import { WorkspaceIndex } from './core/workspaceIndex';
import { registerDiagnostics } from './core/diagnostics';
import { createNewStepWizard } from './wizards/stepWizard';
import * as path from 'path';

function getPythonModulePath(filePath: string): string {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) return 'states';
    
    const rootPath = workspaceFolders[0].uri.fsPath;
    const relativePath = path.relative(rootPath, filePath);
    
    // Check if the step is inside the states/ folder
    const parts = relativePath.split(/[\\/]/);
    if (parts[0] === 'states') {
        return 'states';
    }
    
    // Otherwise, generate the specific relative module path
    let cleanPath = relativePath;
    if (cleanPath.endsWith('.py')) {
        cleanPath = cleanPath.slice(0, -3);
    }
    let modulePath = cleanPath.replace(/[\\/]/g, '.');
    if (modulePath.endsWith('.__init__')) {
        modulePath = modulePath.slice(0, -9);
    }
    return modulePath || 'states';
}

export async function activate(context: vscode.ExtensionContext) {
    console.log('🚀 WPipe Tools: Activation started...');
    
    // Start Services
    CatalogManager.init(context);
    WorkspaceIndex.indexWorkspace();
    registerDiagnostics(context);

    const stepProvider = new WPipeStepProvider();
    vscode.window.registerTreeDataProvider('wpipeSteps', stepProvider);
    
    // Providers
    context.subscriptions.push(
        vscode.languages.registerCodeLensProvider({ language: 'python' }, new WPipeCodeLensProvider()),
        vscode.languages.registerHoverProvider({ language: 'python' }, new WPipeHoverProvider()),
        vscode.languages.registerCodeActionsProvider({ language: 'python' }, new WPipeCodeActionProvider(), {
            providedCodeActionKinds: WPipeCodeActionProvider.providedCodeActionKinds
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('wpipeSteps.refreshEntry', () => stepProvider.refresh()),
        vscode.commands.registerCommand('wpipe-vscode.refreshCatalog', () => CatalogManager.update(context, true)),
        
        vscode.commands.registerCommand('wpipe-vscode.createNewStep', createNewStepWizard),

        vscode.commands.registerCommand('wpipeSteps.openFile', async (f: string, l: number) => {
            const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(f));
            const editor = await vscode.window.showTextDocument(doc);
            const p = new vscode.Position(l, 0);
            editor.selection = new vscode.Selection(p, p);
            editor.revealRange(new vscode.Range(p, p), vscode.TextEditorRevealType.InCenter);
        }),

        vscode.commands.registerCommand('wpipeSteps.insertStep', (step: StepEntry) => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                editor.edit(eb => {
                    const importCode = `from ${step.namespace} import ${step.func_name}\n`;
                    const documentText = editor.document.getText();
                    if (!documentText.includes(importCode)) {
                        eb.insert(new vscode.Position(0, 0), importCode);
                    }
                    const isClass = /^[A-Z]/.test(step.func_name);
                    eb.insert(editor.selection.active, isClass ? `${step.func_name}(),` : `${step.func_name},`);
                });
                vscode.window.showInformationMessage(`✅ Estado '${step.name}' insertado con éxito.`);
            }
        }),

        vscode.commands.registerCommand('wpipe-vscode.searchSteps', async () => {
            // Index workspace steps to ensure local definitions are included
            await WorkspaceIndex.indexWorkspace();
            
            interface StepQuickPickItem extends vscode.QuickPickItem {
                step: StepEntry;
            }

            const localItems: StepQuickPickItem[] = WorkspaceIndex.getAllSteps().map(s => {
                const catSeq = [s.category, s.subcategory1, s.subcategory2, s.subcategory3]
                    .map(c => c?.trim())
                    .filter(Boolean) as string[];
                const categoryPath = catSeq.length > 0 ? catSeq.join(' ➔ ') : 'Workspace';
                const moduleName = getPythonModulePath(s.filePath);

                return {
                    label: `$(home) ${s.name}`,
                    description: `Workspace | ${categoryPath}`,
                    detail: `Location: ${vscode.workspace.asRelativePath(s.filePath)}:${s.line + 1}`,
                    step: {
                        name: s.name,
                        func_name: s.name,
                        namespace: moduleName,
                        repo: 'Workspace',
                        file: s.filePath,
                        description: s.description || 'Local workspace step',
                        category: s.category,
                        subcategory1: s.subcategory1,
                        subcategory2: s.subcategory2,
                        subcategory3: s.subcategory3
                    } as StepEntry
                };
            });

            const catalogItems: StepQuickPickItem[] = CatalogManager.getSteps().map(s => {
                const catSeq = [s.category, s.subcategory1, s.subcategory2, s.subcategory3]
                    .map(c => c?.trim())
                    .filter(Boolean) as string[];
                const categoryPath = catSeq.length > 0 ? catSeq.join(' ➔ ') : 'General';

                return {
                    label: `$(rocket) ${s.name}`,
                    description: `${s.repo} | ${categoryPath}`,
                    detail: `Module: ${s.namespace} | Author: ${s.author || 'Official'}`,
                    step: s
                };
            });

            const items = [...localItems, ...catalogItems];

            const quickPick = vscode.window.createQuickPick<StepQuickPickItem>();
            quickPick.items = items;
            quickPick.placeholder = 'Buscar estado (Workspace local, Catálogo oficial o Comunidad)...';
            quickPick.matchOnDescription = false;
            quickPick.matchOnDetail = false;

            // Custom multi-term search filtering
            quickPick.onDidChangeValue(value => {
                const searchVal = value.trim().toLowerCase();
                if (!searchVal) {
                    quickPick.items = items;
                    return;
                }

                // Split search query by space, underscore, dash, etc.
                const terms = searchVal.split(/[\s_+.-]+/).filter(Boolean);

                quickPick.items = items.filter(item => {
                    const label = item.label.toLowerCase();
                    const desc = item.description ? item.description.toLowerCase() : '';
                    const detail = item.detail ? item.detail.toLowerCase() : '';
                    const step = item.step;

                    // All terms must match at least one of the fields/metadata of this item
                    return terms.every(term => {
                        // Check main UI fields
                        if (label.includes(term) || desc.includes(term) || detail.includes(term)) {
                            return true;
                        }
                        // Check step specific fields
                        if (step.name.toLowerCase().includes(term) || 
                            (step.func_name && step.func_name.toLowerCase().includes(term)) || 
                            (step.namespace && step.namespace.toLowerCase().includes(term))) {
                            return true;
                        }
                        // Check categories list
                        const categories = [step.category, step.subcategory1, step.subcategory2, step.subcategory3]
                            .map(c => c?.trim().toLowerCase())
                            .filter(Boolean);
                        if (categories.some(cat => cat.includes(term))) {
                            return true;
                        }
                        return false;
                    });
                });
            });

            quickPick.onDidAccept(() => {
                const sel = quickPick.selectedItems[0];
                if (sel) {
                    if (sel.step.repo === 'Workspace') {
                        const editor = vscode.window.activeTextEditor;
                        if (editor) {
                            editor.edit(eb => {
                                const moduleName = getPythonModulePath(sel.step.file);
                                const importCode = `from ${moduleName} import ${sel.step.func_name}\n`;
                                const documentText = editor.document.getText();
                                if (!documentText.includes(importCode)) {
                                    eb.insert(new vscode.Position(0, 0), importCode);
                                }
                                const isClass = /^[A-Z]/.test(sel.step.func_name);
                                eb.insert(editor.selection.active, isClass ? `${sel.step.func_name}(),` : `${sel.step.func_name},`);
                            });
                            vscode.window.showInformationMessage(`✅ Estado local '${sel.step.name}' insertado con éxito.`);
                        }
                    } else {
                        vscode.commands.executeCommand('wpipeSteps.insertStep', sel.step);
                    }
                }
                quickPick.hide();
            });

            quickPick.onDidHide(() => quickPick.dispose());
            quickPick.show();
        }),

        vscode.commands.registerCommand('wpipe-vscode.previewDAG', () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) DAGPanel.createOrShow(context.extensionUri, editor.document);
        }),

        vscode.commands.registerCommand('wpipe-vscode.openDashboard', (dbPath?: any) => openDashboard(context, dbPath)),

        vscode.commands.registerCommand('wpipe-vscode.replayLogs', replayLogErrors),

        vscode.commands.registerCommand('wpipe-vscode.findStepUsage', (stepName?: string) => findStepUsage(stepName)),

        vscode.commands.registerCommand('wpipe-vscode.showCheatSheet', showCheatSheet),

        vscode.commands.registerCommand('wpipe-vscode.openAiAssistant', () => showAiAssistant(context.extensionUri)),

        vscode.commands.registerCommand('wpipe-vscode.runPipeline', async (filePath: string) => {
            if (vscode.env.uiKind === vscode.UIKind.Web) {
                vscode.window.showErrorMessage('Running pipelines requires a local Python environment.');
                return;
            }
            const terminal = vscode.window.createTerminal(`Pipeline: ${path.basename(filePath)}`);
            terminal.show();
            terminal.sendText(`python "${filePath}"`);
        }),

        vscode.commands.registerCommand('wpipe-vscode.addLogicBlock', async (range: vscode.Range) => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const text = editor.document.getText(range);
            const openBracketIndex = text.indexOf('[');
            
            if (openBracketIndex !== -1) {
                const offset = editor.document.offsetAt(range.start) + openBracketIndex + 1;
                const pos = editor.document.positionAt(offset);
                editor.selection = new vscode.Selection(pos, pos);
            }

            const items = [
                { 
                    label: '$(split-horizontal) Condition', 
                    detail: 'Boolean branching (True/False)', 
                    snippet: 'Condition(\n    expression="${1:valor > 100}",\n    branch_true=[${2:step_true}],\n    branch_false=[${3:step_false}]\n)' 
                },
                { 
                    label: '$(sync) For Loop', 
                    detail: 'Iterative loop with validation', 
                    snippet: 'For(\n    iterations=${1:10},\n    validation_expression="${2:status != \'error\'}",\n    steps=[${3:step_to_repeat}]\n)' 
                },
                { 
                    label: '$(zap) Parallel', 
                    detail: 'Concurrent multi-step execution', 
                    snippet: 'Parallel(\n    steps=[${1:step1}, ${2:step2}],\n    max_workers=${3:2}\n)' 
                },
                { 
                    label: '$(run-all) Background', 
                    detail: 'Asynchronous fire-and-forget task', 
                    snippet: 'Background(${1:slow_step})' 
                }
            ];

            const sel = await vscode.window.showQuickPick(items, { placeHolder: 'Select a logic block to insert inside set_steps...' });
            if (sel) {
                editor.insertSnippet(new vscode.SnippetString(sel.snippet));
            }
        }),

        vscode.commands.registerCommand('wpipeSteps.runStep', async (item: StepItem) => {
            if (vscode.env.uiKind === vscode.UIKind.Web) {
                vscode.window.showErrorMessage('Running steps requires a local Python environment.');
                return;
            }
            if (!item || !item.filePath) return;
            
            const terminal = vscode.window.createTerminal(`Run Step: ${item.label}`);
            terminal.show();
            terminal.sendText(`python "${item.filePath}"`);
        }),

        vscode.commands.registerCommand('wpipeSteps.runStepFromCode', async (filePath: string, line: number) => {
            if (vscode.env.uiKind === vscode.UIKind.Web) {
                vscode.window.showErrorMessage('Running steps requires a local Python environment.');
                return;
            }
            const fileName = path.basename(filePath);
            const terminal = vscode.window.createTerminal(`Run Step: ${fileName}`);
            terminal.show();
            terminal.sendText(`python "${filePath}"`);
        }),

        vscode.commands.registerCommand('wpipeSteps.installRequirements', async (item: LibraryItem) => {
            if (vscode.env.uiKind === vscode.UIKind.Web) {
                vscode.window.showErrorMessage('Installing requirements requires a local environment.');
                return;
            }
            if (!item || !item.step || !item.step.requirements) {
                vscode.window.showWarningMessage('Este paso no tiene requerimientos externos definidos.');
                return;
            }
            
            const reqUrl = item.step.requirements;
            const terminal = vscode.window.createTerminal(`Install: ${item.step.name}`);
            terminal.show();
            
            try {
                // Download requirements.txt to a local temporary file first
                const response = await fetch(reqUrl);
                if (!response.ok) throw new Error(`No se pudo descargar el archivo: ${response.statusText}`);
                const content = await response.text();
                
                // Determine save location: Workspace root OR extension's global storage
                let tempReqUri: vscode.Uri;
                const workspaceFolders = vscode.workspace.workspaceFolders;
                
                if (workspaceFolders && workspaceFolders.length > 0) {
                    tempReqUri = vscode.Uri.joinPath(workspaceFolders[0].uri, `requirements_${item.step.name}.txt`);
                } else {
                    // Fallback to global storage if no workspace is open
                    await vscode.workspace.fs.createDirectory(context.globalStorageUri);
                    tempReqUri = vscode.Uri.joinPath(context.globalStorageUri, `requirements_${item.step.name}.txt`);
                }
                
                await vscode.workspace.fs.writeFile(tempReqUri, new TextEncoder().encode(content));
                
                terminal.sendText(`pip install -r "${tempReqUri.fsPath}"`);
                vscode.window.showInformationMessage(`⏳ Descargado e instalando dependencias para '${item.step.name}'...`);
            } catch (error) {
                vscode.window.showErrorMessage(`❌ Error al preparar requerimientos: ${error}`);
            }
        }),

        vscode.commands.registerCommand('wpipeSteps.viewExamples', async (item: LibraryItem) => {
            if (!item || !item.step || !item.step.examples) {
                vscode.window.showWarningMessage('Este paso no tiene ejemplos configurados.');
                return;
            }

            // Convert RAW URL to Browsable GitHub URL
            // Raw: https://raw.githubusercontent.com/owner/repo/branch/path/to/
            // UI:  https://github.com/owner/repo/tree/branch/path/to/
            let uiUrl = item.step.examples
                .replace('raw.githubusercontent.com', 'github.com');
            
            const parts = uiUrl.split('/');
            if (parts.length >= 6) {
                const owner = parts[3];
                const repo = parts[4];
                const branch = parts[5];
                const rest = parts.slice(6).join('/');
                
                // GitHub uses /tree/ for directories and /blob/ for files
                const type = item.step.examples.endsWith('/') ? 'tree' : 'blob';
                uiUrl = `https://github.com/${owner}/${repo}/${type}/${branch}/${rest}`;
            }

            vscode.env.openExternal(vscode.Uri.parse(uiUrl));
        }),

        vscode.commands.registerCommand('wpipeSteps.downloadExample', async (item: LibraryItem) => {
            if (!item || !item.step || !item.step.examples) {
                vscode.window.showWarningMessage('Este paso no tiene ejemplos configurados.');
                return;
            }

            let rawUrl = item.step.examples;
            
            try {
                // Check if it's a directory (ends with /)
                if (rawUrl.endsWith('/')) {
                    // It's a directory, we need to list files. 
                    // We'll use the GitHub API to list the directory content
                    // Extract owner, repo, and path from the raw URL
                    // Example: https://raw.githubusercontent.com/wisrovi/wpipe-plugins/001-DEVELOPMENT/src/.../examples/
                    const parts = rawUrl.split('/');
                    const owner = parts[3];
                    const repo = parts[4];
                    const branch = parts[5];
                    const pathInRepo = parts.slice(6).join('/');
                    
                    const apiUrl = `https://api.github.com/repos/${owner}/${repo}/contents/${pathInRepo}?ref=${branch}`;
                    
                    const apiResponse = await fetch(apiUrl);
                    if (!apiResponse.ok) throw new Error(`No se pudo listar el contenido de la carpeta: ${apiResponse.statusText}`);
                    
                    const files = await apiResponse.json();
                    if (!Array.isArray(files)) throw new Error('Respuesta inesperada de la API de GitHub.');
                    
                    const pyFiles = files.filter((f: any) => f.name.endsWith('.py') && f.name !== '__init__.py').map((f: any) => ({
                        label: `$(file-code) ${f.name}`,
                        url: f.download_url,
                        name: f.name
                    }));
                    
                    if (pyFiles.length === 0) {
                        vscode.window.showInformationMessage('No se encontraron archivos de ejemplo (.py) en la carpeta.');
                        return;
                    }
                    
                    const selected = await vscode.window.showQuickPick(pyFiles, { 
                        placeHolder: 'Selecciona un ejemplo para usar como plantilla:' 
                    });
                    
                    if (!selected) return;
                    rawUrl = selected.url;
                }

                await vscode.window.withProgress({
                    location: vscode.ProgressLocation.Notification,
                    title: `Descargando plantilla...`,
                    cancellable: false
                }, async () => {
                    const response = await fetch(rawUrl);
                    if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
                    
                    const content = await response.text();
                    if (content.trim().startsWith('<!DOCTYPE html>')) {
                        throw new Error('La URL no apunta a un archivo RAW válido.');
                    }

                    const doc = await vscode.workspace.openTextDocument({
                        content: content,
                        language: 'python'
                    });
                    await vscode.window.showTextDocument(doc);
                    vscode.window.showInformationMessage(`✅ Plantilla cargada con éxito.`);
                });
            } catch (error) {
                vscode.window.showErrorMessage(`❌ Fallo al procesar plantilla: ${error}`);
            }
        })
    );
}

export function deactivate() {}
