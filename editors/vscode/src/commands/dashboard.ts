import * as vscode from 'vscode';
export async function openDashboard(dbPath?: any) {
    console.log('🚀 WPipe: openDashboard called with:', dbPath);

    if (vscode.env.uiKind === vscode.UIKind.Web) {
        vscode.window.showErrorMessage('WPipe Dashboard requires a local Python environment.');
        return;
    }

    let finalDbPath: string | undefined;

    // Handle cases where VS Code might pass a URI or other object as the first arg
    if (typeof dbPath === 'string' && dbPath.length > 0) {
        finalDbPath = dbPath;
    } else if (dbPath && typeof dbPath === 'object' && 'fsPath' in dbPath) {
        finalDbPath = dbPath.fsPath;
    }

    if (!finalDbPath) {
        const dbUri = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: false,
            canSelectMany: false,
            filters: { 'Database': ['db', 'sqlite', 'sqlite3'] },
            title: 'Select WPipe Tracking Database'
        });
        if (!dbUri) return;
        finalDbPath = dbUri[0].fsPath;
    }

    // Quick Pick for optional config instead of full dialog for better flow
    const useConfig = await vscode.window.showQuickPick(['No', 'Yes'], { placeHolder: 'Select WPipe Config Directory? (Optional)' });
    let configPath = '';
    if (useConfig === 'Yes') {
        const configUri = await vscode.window.showOpenDialog({
            canSelectFiles: false,
            canSelectFolders: true,
            canSelectMany: false,
            title: 'Select WPipe Config Directory'
        });
        if (configUri) configPath = configUri[0].fsPath;
    }

    const port = await vscode.window.showInputBox({
        placeHolder: '5000',
        prompt: 'Enter port for the dashboard',
        value: '5000'
    }) || '5000';

    const terminal = vscode.window.createTerminal('WPipe Dashboard');
    let cmd = `python -m wpipe.dashboard --db "${finalDbPath}" --port ${port}`;
    if (configPath) cmd += ` --config "${configPath}"`;

    terminal.show();
    terminal.sendText(cmd);

    vscode.window.showInformationMessage(`🚀 Dashboard starting at http://localhost:${port}`);
    setTimeout(() => {
        vscode.env.openExternal(vscode.Uri.parse(`http://localhost:${port}`));
    }, 2000);
}
