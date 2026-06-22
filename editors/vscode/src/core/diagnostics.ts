import * as vscode from 'vscode';
import { parser } from '@lezer/python';
import { WorkspaceIndex } from './workspaceIndex';
import { CatalogManager } from './catalog';

export function registerDiagnostics(context: vscode.ExtensionContext) {
    const diagnosticCollection = vscode.languages.createDiagnosticCollection('wpipe');
    context.subscriptions.push(diagnosticCollection);

    if (vscode.window.activeTextEditor) {
        updateDiagnostics(vscode.window.activeTextEditor.document, diagnosticCollection);
    }

    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(e => updateDiagnostics(e.document, diagnosticCollection)),
        vscode.window.onDidChangeActiveTextEditor(editor => {
            if (editor) updateDiagnostics(editor.document, diagnosticCollection);
        })
    );
}

function updateDiagnostics(document: vscode.TextDocument, collection: vscode.DiagnosticCollection): void {
    if (document.languageId !== 'python') return;

    const diagnostics: vscode.Diagnostic[] = [];
    const content = document.getText();
    const tree = parser.parse(content);

    const workspaceSteps = new Set(WorkspaceIndex.getAllSteps().map(s => s.name));
    const catalogSteps = new Set(CatalogManager.getSteps().map(s => s.name));
    const knownSteps = new Set([...workspaceSteps, ...catalogSteps]);

    tree.iterate({
        enter: (node) => {
            if (node.name === 'CallExpression') {
                const callText = content.substring(node.from, node.to);
                if (callText.includes('.set_steps(') || (callText.includes('Pipeline(') && callText.includes('steps='))) {
                    // Extract step names from set_steps([ ... ])
                    const match = callText.match(/(?:set_steps|steps)\s*\(\s*\[([\s\S]*?)\]\s*\)/) || 
                                  callText.match(/steps\s*=\s*\[([\s\S]*?)\]/);
                    
                    if (match) {
                        const stepsContent = match[1];
                        const baseOffset = node.from + callText.indexOf(match[1]);
                        
                        // Simple split by comma, ignoring nested brackets
                        const parts = splitWithOffsets(stepsContent, baseOffset);
                        parts.forEach(part => {
                            const name = part.text.split('(')[0].trim();
                            // Ignore common WPipe logic blocks
                            const logicBlocks = ['Condition', 'Parallel', 'For', 'Background'];
                            if (name && !logicBlocks.includes(name) && !knownSteps.has(name)) {
                                // Extra check: maybe it's imported but not indexed yet? 
                                // For now, if it's not in knownSteps, we warn.
                                const range = new vscode.Range(
                                    document.positionAt(part.offset),
                                    document.positionAt(part.offset + name.length)
                                );
                                diagnostics.push(new vscode.Diagnostic(
                                    range,
                                    `Step '${name}' not found in workspace or catalog.`,
                                    vscode.DiagnosticSeverity.Warning
                                ));
                            }
                        });
                    }
                }
            }
        }
    });

    collection.set(document.uri, diagnostics);
}

function splitWithOffsets(c: string, baseOffset: number) {
    const r: {text: string, offset: number}[] = []; let cur = ""; let d = 0; let start = 0;
    for (let i = 0; i < c.length; i++) {
        if (c[i] === '[' || c[i] === '(') d++; else if (c[i] === ']' || c[i] === ')') d--;
        if (c[i] === ',' && d === 0) { 
            r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) }); 
            cur = ""; start = i + 1; 
        } else cur += c[i];
    }
    if (cur.trim()) r.push({ text: cur.trim(), offset: baseOffset + start + (cur.length - cur.trimStart().length) }); 
    return r;
}
