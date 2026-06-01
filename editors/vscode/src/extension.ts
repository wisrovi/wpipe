import * as vscode from 'vscode';
import { CatalogManager, StepEntry } from './core/catalog';
import { WPipeStepProvider, StepItem } from './providers/stepProvider';
import { DAGPanel } from './webviews/dagPanel';
import { showCheatSheet } from './webviews/cheatSheet';
import { openDashboard } from './commands/dashboard';
import { WPipeCodeLensProvider } from './providers/codeLensProvider';
import { WPipeHoverProvider } from './providers/hoverProvider';
import { WorkspaceIndex } from './core/workspaceIndex';
import { createNewStepWizard } from './wizards/stepWizard';
import * as path from 'path';

export async function activate(context: vscode.ExtensionContext) {
    console.log('🚀 WPipe Tools: Activation started...');
    
    // Start Services
    CatalogManager.init(context);
    WorkspaceIndex.indexWorkspace();

    const stepProvider = new WPipeStepProvider();
    vscode.window.registerTreeDataProvider('wpipeSteps', stepProvider);
    
    // Providers
    context.subscriptions.push(
        vscode.languages.registerCodeLensProvider({ language: 'python' }, new WPipeCodeLensProvider()),
        vscode.languages.registerHoverProvider({ language: 'python' }, new WPipeHoverProvider())
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
        }),

        vscode.commands.registerCommand('wpipe-vscode.openDashboard', openDashboard),

        vscode.commands.registerCommand('wpipe-vscode.showCheatSheet', showCheatSheet),

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
        })
    );
}

export function deactivate() {}
