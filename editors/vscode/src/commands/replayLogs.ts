import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { DAGPanel } from '../webviews/dagPanel';

interface LogError {
    module: string;
    function: string;
    line: number;
    message: string;
    level: string;
}

const errorDecorationType = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(255, 0, 0, 0.2)',
    isWholeLine: true,
    overviewRulerColor: 'red',
    overviewRulerLane: vscode.OverviewRulerLane.Full,
    after: {
        contentText: ' ⚠️ WPipe Error',
        color: 'red',
        margin: '0 0 0 1em'
    }
});

export async function replayLogErrors() {
    const logUri = await vscode.window.showOpenDialog({
        canSelectFiles: true,
        canSelectFolders: false,
        canSelectMany: false,
        filters: { 'Log Files': ['log'] },
        title: 'Select WPipe Log File'
    });

    if (!logUri || logUri.length === 0) return;

    const logPath = logUri[0].fsPath;
    const content = fs.readFileSync(logPath, 'utf8');
    const lines = content.split('\n');

    const errors: LogError[] = [];
    const logPattern = /^.*? \| (ERROR|CRITICAL) \| (.*?):(.*?):(\d+) \| (.*)$/;

    for (const line of lines) {
        const match = line.match(logPattern);
        if (match) {
            errors.push({
                level: match[1],
                module: match[2],
                function: match[3],
                line: parseInt(match[4]) - 1, // 0-indexed for VS Code
                message: match[5]
            });
        }
    }

    if (errors.length === 0) {
        vscode.window.showInformationMessage('✅ No errors found in the selected log.');
        return;
    }

    vscode.window.showWarningMessage(`🔍 Found ${errors.length} errors in log. Highlighting in editor...`);

    // Group errors by file
    // Note: Log module usually doesn't have the full path. We'll try to match it in the workspace.
    for (const error of errors) {
        const files = await vscode.workspace.findFiles(`**/${error.module}.py`);
        if (files.length > 0) {
            const doc = await vscode.workspace.openTextDocument(files[0]);
            const editor = await vscode.window.showTextDocument(doc, { preview: false });
            
            const decoration = {
                range: new vscode.Range(error.line, 0, error.line, 0),
                hoverMessage: `**[WPipe ${error.level}]** ${error.message}`
            };
            
            editor.setDecorations(errorDecorationType, [decoration]);
            
            // Also reveal the first error
            if (error === errors[0]) {
                editor.revealRange(decoration.range, vscode.TextEditorRevealType.InCenter);
            }
        }
    }
    
    // Highlight nodes in the DAG if open
    if (DAGPanel.currentPanel) {
        const stepNames = errors.map(e => e.function);
        DAGPanel.currentPanel.highlightNodes(stepNames, 'error');
    }
}
