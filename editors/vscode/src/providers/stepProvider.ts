import * as vscode from 'vscode';
import { CatalogManager, StepEntry } from '../core/catalog';
import { WorkspaceIndex } from '../core/workspaceIndex';

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
        await WorkspaceIndex.indexWorkspace();
        return WorkspaceIndex.getAllSteps().map(s => new StepItem(s.name, s.filePath, s.line));
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
