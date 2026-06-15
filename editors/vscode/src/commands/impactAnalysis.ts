import * as vscode from 'vscode';
import * as path from 'path';

export async function findStepUsage(arg?: any) {
    let stepName: string | undefined;

    if (typeof arg === 'string') {
        stepName = arg;
    } else if (arg instanceof vscode.TreeItem) {
        stepName = arg.label as string;
    }

    if (!stepName) {
        stepName = await vscode.window.showInputBox({
            prompt: 'Enter the name of the step to analyze impact',
            placeHolder: 'e.g. download_data'
        });
    }

    if (!stepName) return;

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `Analyzing impact for step: ${stepName}`,
        cancellable: false
    }, async (progress) => {
        // Search for the step name in all .py files
        const files = await vscode.workspace.findFiles('**/*.py', '**/node_modules/**');
        const usages: { file: vscode.Uri, line: number, text: string }[] = [];

        for (const file of files) {
            const doc = await vscode.workspace.openTextDocument(file);
            const content = doc.getText();
            const lines = content.split('\n');

            lines.forEach((line, index) => {
                // Look for the step name being used in a list of steps or as a function call
                // Simple heuristic: word boundary
                const regex = new RegExp(`\\b${stepName}\\b`);
                if (regex.test(line)) {
                    // Exclude the definition itself (approximate)
                    if (!line.includes(`def ${stepName}`) && !line.includes(`@step`)) {
                        usages.push({ file, line: index, text: line.trim() });
                    }
                }
            });
        }

        if (usages.length === 0) {
            vscode.window.showInformationMessage(`✅ Step '${stepName}' is not used in any other pipeline.`);
            return;
        }

        // Show results in a QuickPick or Output Channel
        const items = usages.map(u => ({
            label: `${path.basename(u.file.fsPath)}:L${u.line + 1}`,
            description: u.text,
            uri: u.file,
            line: u.line
        }));

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: `Found ${usages.length} usages of '${stepName}'. Select to open.`
        });

        if (selected) {
            const doc = await vscode.workspace.openTextDocument(selected.uri);
            const editor = await vscode.window.showTextDocument(doc);
            const pos = new vscode.Position(selected.line, 0);
            editor.selection = new vscode.Selection(pos, pos);
            editor.revealRange(new vscode.Range(pos, pos), vscode.TextEditorRevealType.InCenter);
        }
    });
}
