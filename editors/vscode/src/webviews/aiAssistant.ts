import * as vscode from 'vscode';

export function showAiAssistant(extensionUri: vscode.Uri) {
    const panel = vscode.window.createWebviewPanel(
        'wpipeAI',
        'WPipe AI Assistant',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true,
            retainContextWhenHidden: true
        }
    );

    panel.webview.html = getHtml(panel.webview);

    panel.webview.onDidReceiveMessage(message => {
        if (message.command === 'generate') {
            const prompt = message.text.toLowerCase();
            let code = '';

            if (prompt.includes('download') && prompt.includes('sqlite')) {
                code = `from wpipe import Pipeline, step, SQLiteTracking\n\n@step(name="fetch_data")\ndef fetch_data():\n    return {"data": "..."}\n\n@step(name="save_to_db")\ndef save_to_db(context):\n    # logic to save\n    pass\n\npipe = Pipeline(name="AI Generated Pipeline", tracking_db=SQLiteTracking("data.db"))\npipe.set_steps([fetch_data, save_to_db])\npipe.run()`;
            } else if (prompt.includes('parallel')) {
                code = `from wpipe import Pipeline, step, Parallel\n\n@step(name="task_1")\ndef task_1(): pass\n\n@step(name="task_2")\ndef task_2(): pass\n\npipe = Pipeline(name="Parallel Pipeline")\npipe.set_steps([\n    Parallel(steps=[task_1, task_2])\n])\npipe.run()`;
            } else {
                code = `# AI suggest: Try asking for "download and sqlite" or "parallel pipeline"\n@step(name="my_step")\ndef my_step():\n    pass`;
            }

            panel.webview.postMessage({ command: 'result', code: code });
        } else if (message.command === 'insert') {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                editor.edit(eb => {
                    eb.insert(editor.selection.active, message.code);
                });
            }
        }
    });
}

function getHtml(webview: vscode.Webview) {
    return `<!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: sans-serif; padding: 20px; background: #1e1e1e; color: #ccc; }
            input { width: 100%; padding: 10px; background: #333; color: white; border: 1px solid #444; border-radius: 4px; margin-bottom: 10px; }
            button { background: #007acc; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
            pre { background: #000; padding: 15px; border-radius: 4px; overflow-x: auto; color: #9cdcfe; border: 1px solid #333; }
            .chat-msg { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h2>🤖 WPipe AI Assistant</h2>
        <div class="chat-msg">
            <p>Describe what you want to build:</p>
            <input type="text" id="prompt" placeholder="e.g. A pipeline with parallel tasks...">
            <button onclick="generate()">Generate Structure</button>
        </div>
        <div id="output" style="display:none;">
            <h3>Generated Code:</h3>
            <pre id="code-block"></pre>
            <button onclick="insert()">Insert into Editor</button>
        </div>
        <script>
            const vscode = acquireVsCodeApi();
            function generate() {
                const text = document.getElementById('prompt').value;
                vscode.postMessage({ command: 'generate', text: text });
            }
            function insert() {
                const code = document.getElementById('code-block').innerText;
                vscode.postMessage({ command: 'insert', code: code });
            }
            window.addEventListener('message', event => {
                const message = event.data;
                if (message.command === 'result') {
                    document.getElementById('output').style.display = 'block';
                    document.getElementById('code-block').innerText = message.code;
                }
            });
        </script>
    </body>
    </html>`;
}
