import * as vscode from 'vscode';
import { CatalogManager, StepEntry } from '../core/catalog';

import { parser } from '@lezer/python';

export class WPipeStepProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<vscode.TreeItem | undefined | void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    refresh() {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(e: vscode.TreeItem): vscode.TreeItem {
        return e;
    }

    async getChildren(e?: vscode.TreeItem): Promise<vscode.TreeItem[]> {
        if (!e) {
            return [
                new vscode.TreeItem('🛠️ Workspace Steps', vscode.TreeItemCollapsibleState.Expanded),
                new vscode.TreeItem('📦 Official Library', vscode.TreeItemCollapsibleState.Collapsed),
                new vscode.TreeItem('🤝 Community Plugins', vscode.TreeItemCollapsibleState.Collapsed)
            ];
        }

        const label = e.label as string;
        if (label.includes('Workspace')) return this.searchWorkspace();
        if (label.includes('Official')) return this.getLibItems('Official');
        if (label.includes('Community')) return this.getLibItems('Community');
        return [];
    }

    private getLibItems(repo: string): LibraryItem[] {
        return CatalogManager.getSteps()
            .filter(s => s.repo === repo)
            .map(s => new LibraryItem(s));
    }

    private async searchWorkspace(): Promise<StepItem[]> {
        const steps: StepItem[] = [];
        const config = vscode.workspace.getConfiguration('wpipe');
        const userExcludes = config.get<string[]>('excludePaths', []);
        const maxFiles = config.get<number>('maxSearchFiles', 500);

        const defaultExcludes = [
            '**/node_modules/**',
            '**/.venv/**',
            '**/venv/**',
            '**/.env/**',
            '**/env/**',
            '**/.conda/**',
            '**/conda/**',
            '**/site-packages/**',
            '**/wpipe/wpipe/**',
            '**/__pycache__/**',
            '**/.pytest_cache/**',
            '**/.mypy_cache/**',
            '**/.ruff_cache/**',
            '**/.tox/**',
            '**/build/**',
            '**/dist/**',
            '**/*.egg-info/**'
        ];

        const combinedExcludes = Array.from(new Set([...defaultExcludes, ...userExcludes]));
        const excludePattern = `{${combinedExcludes.join(',')}}`;

        const files = await vscode.workspace.findFiles('**/*.py', excludePattern, maxFiles);
        
        for (const f of files) {
            try {
                const contentData = await vscode.workspace.fs.readFile(f);
                if (contentData.length > 500000) continue; // Skip huge files
                
                const content = new TextDecoder().decode(contentData);
                const tree = parser.parse(content);
                
                tree.iterate({
                    enter: (node) => {
                        if (node.name === 'Decorator') {
                            const decText = content.substring(node.from, node.to);
                            if (decText.startsWith('@step')) {
                                let name = '';
                                const match = decText.match(/name\s*=\s*['"](.*?)['"]/);
                                if (match) name = match[1];
                                
                                if (!name && node.node.parent) {
                                    let funcDef = node.node.parent.getChild('FunctionDefinition') || node.node.parent.getChild('ClassDefinition');
                                    if (funcDef) {
                                        let varName = funcDef.getChild('VariableName');
                                        if (varName) name = content.substring(varName.from, varName.to);
                                    }
                                }
                                
                                const line = content.substring(0, node.from).split('\n').length - 1;
                                steps.push(new StepItem(name || 'Step', f.fsPath, line));
                            }
                        } else if (node.name === 'CallExpression') {
                            const callText = content.substring(node.from, node.to);
                            if (callText.includes('.add_state(')) {
                                const m = callText.match(/\.add_state\s*\((?:name\s*=\s*)?["'](.*?)["']/);
                                const line = content.substring(0, node.from).split('\n').length - 1;
                                if (m) {
                                    steps.push(new StepItem(m[1], f.fsPath, line));
                                } else {
                                    const m2 = callText.match(/\.add_state\s*\(\s*(\w+)/);
                                    if (m2 && !['name', 'state', 'func', 'Condition', 'Parallel', 'For', 'Background'].includes(m2[1])) {
                                        steps.push(new StepItem(m2[1], f.fsPath, line));
                                    }
                                }
                            }
                        }
                    }
                });
            } catch (e) {
                console.error('Error parsing file:', f.fsPath, e);
            }
        }
        return steps;
    }
}

export class StepItem extends vscode.TreeItem {
    constructor(label: string, public filePath: string, public line: number) {
        super(label);
        this.iconPath = new vscode.ThemeIcon('rocket');
        this.description = label; // Simplified for web compatibility
        this.contextValue = 'workspaceStep';
        this.command = { command: 'wpipeSteps.openFile', title: 'Open', arguments: [filePath, line] };
    }
    public funcName: string = '';
}

export class LibraryItem extends vscode.TreeItem {
    constructor(public step: StepEntry) {
        super(step.name);
        this.iconPath = new vscode.ThemeIcon('cloud');
        this.description = step.namespace;
        this.tooltip = new vscode.MarkdownString(`**Step:** ${step.name}\n**Author:** ${step.author || "Official"}\n**Repo:** ${step.repo}\n**Module:** ${step.namespace}\n\n---\nClick to insert import and usage.`);
        this.contextValue = 'libraryStep';
        this.command = { command: 'wpipeSteps.insertStep', title: 'Insert', arguments: [step] };
    }
}
