import * as vscode from 'vscode';

export async function openDashboard() {
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

    if (!dbUri) return;

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

    if (!port) return;

    const terminal = vscode.window.createTerminal('WPipe Dashboard');
    const dbPath = dbUri[0].fsPath;
    const configPath = configUri ? configUri[0].fsPath : '';
    
    let cmd = `python -m wpipe.dashboard --db "${dbPath}" --port ${port}`;
    if (configPath) cmd += ` --config "${configPath}"`;
    
    terminal.show();
    terminal.sendText(cmd);
    
    vscode.window.showInformationMessage(`🚀 Dashboard starting at http://localhost:${port}`);
    setTimeout(() => {
        vscode.env.openExternal(vscode.Uri.parse(`http://localhost:${port}`));
    }, 2000);
}
