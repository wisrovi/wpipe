import * as vscode from 'vscode';
import { CatalogManager, StepEntry } from './core/catalog';
import { WPipeStepProvider, StepItem } from './providers/stepProvider';
import { DAGPanel } from './webviews/dagPanel';
import { showCheatSheet } from './webviews/cheatSheet';
import { openDashboard } from './commands/dashboard';

export async function activate(context: vscode.ExtensionContext) {
    console.log('🚀 WPipe Tools: Activation started...');
    // Start Catalog Manager (Non-blocking)
    CatalogManager.init(context);

    const stepProvider = new WPipeStepProvider();
    vscode.window.registerTreeDataProvider('wpipeSteps', stepProvider);
    
    context.subscriptions.push(
        vscode.commands.registerCommand('wpipeSteps.refreshEntry', () => stepProvider.refresh()),
        vscode.commands.registerCommand('wpipe-vscode.refreshCatalog', () => CatalogManager.update(context, true)),
        
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

        vscode.commands.registerCommand('wpipeSteps.runStep', async (item: StepItem) => {
            if (vscode.env.uiKind === vscode.UIKind.Web) {
                vscode.window.showErrorMessage('Running steps requires a local Python environment.');
                return;
            }
            if (!item || !item.filePath) return;
            
            const terminal = vscode.window.createTerminal(`Run Step: ${item.label}`);
            terminal.show();
            terminal.sendText(`python "${item.filePath}"`);
        })
    );
}

export function deactivate() {}
