import * as vscode from 'vscode';
import { DashboardPanel } from '../webviews/dashboardPanel';

export async function openDashboard(context: vscode.ExtensionContext, dbPath?: any) {
    console.log('🚀 WPipe: openDashboard called with:', dbPath);

    if (vscode.env.uiKind === vscode.UIKind.Web) {
        vscode.window.showErrorMessage('WPipe Dashboard requires a local Python environment.');
        return;
    }

    let finalDbPath: string | undefined;

    // Handle cases where VS Code might pass a URI or other object as the first arg
    let potentialDbPath = '';
    if (typeof dbPath === 'string' && dbPath.length > 0) {
        potentialDbPath = dbPath;
    } else if (dbPath && typeof dbPath === 'object' && 'fsPath' in dbPath) {
        potentialDbPath = dbPath.fsPath;
    }

    // Only auto-use the path if it actually looks like a database file
    if (potentialDbPath && (potentialDbPath.endsWith('.db') || potentialDbPath.endsWith('.sqlite') || potentialDbPath.endsWith('.sqlite3'))) {
        finalDbPath = potentialDbPath;
    }

    if (!finalDbPath) {
        const dbUri = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: false,
            canSelectMany: false,
            filters: { 'Database': ['db', 'sqlite', 'sqlite3'], 'All Files': ['*'] },
            title: 'Select WPipe Tracking Database'
        });
        if (!dbUri) return; // User cancelled
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
    let cmd = `wpipe dashboard --db "${finalDbPath}" --port ${port}`;
    if (configPath) cmd += ` --config-dir "${configPath}"`;

    terminal.show();
    terminal.sendText(cmd);

    vscode.window.showInformationMessage(`🚀 Starting WPipe Dashboard inside VS Code...`);
    
    // Open the native Webview panel
    // We wait a bit for the server to start (similar to the previous timeout)
    setTimeout(() => {
        DashboardPanel.createOrShow(context.extensionUri, port);
    }, 2500);
}
