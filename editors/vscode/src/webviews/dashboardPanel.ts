import * as vscode from 'vscode';

export class DashboardPanel {
    public static currentPanel: DashboardPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    public static createOrShow(extensionUri: vscode.Uri, port: string) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (DashboardPanel.currentPanel) {
            DashboardPanel.currentPanel._panel.reveal(column);
            DashboardPanel.currentPanel._update(port);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'wpipeDashboard',
            'WPipe Dashboard',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
            }
        );

        DashboardPanel.currentPanel = new DashboardPanel(panel, port);
    }

    private constructor(panel: vscode.WebviewPanel, port: string) {
        this._panel = panel;

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

        this._update(port);
    }

    public dispose() {
        DashboardPanel.currentPanel = undefined;

        this._panel.dispose();

        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }

    private _update(port: string) {
        this._panel.title = `WPipe Dashboard (Port ${port})`;
        this._panel.webview.html = this._getHtmlForWebview(port);
    }

    private _getHtmlForWebview(port: string) {
        const url = `http://localhost:${port}`;
        
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>WPipe Dashboard</title>
            <style>
                body, html {
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    width: 100%;
                    overflow: hidden;
                    background-color: #1e1e1e;
                }
                iframe {
                    border: none;
                    width: 100%;
                    height: 100%;
                    background-color: #fff;
                }
                .loading-container {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #ccc;
                    font-family: sans-serif;
                    z-index: -1;
                }
            </style>
        </head>
        <body>
            <div class="loading-container">
                Connecting to WPipe Dashboard on port ${port}...
            </div>
            <iframe src="${url}" allow="autoplay; clipboard-read; clipboard-write;"></iframe>
            <script>
                // Handle potential connection issues or iframe loading
                const iframe = document.querySelector('iframe');
                iframe.onload = () => {
                    console.log('Dashboard iframe loaded');
                };
            </script>
        </body>
        </html>`;
    }
}
