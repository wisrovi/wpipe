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
        this.description = step.version ? `v${step.version}` : step.namespace;
        
        const tooltip = new vscode.MarkdownString();
        tooltip.isTrusted = true;
        tooltip.appendMarkdown(`### 📦 ${step.name} \n`);
        if (step.version) tooltip.appendMarkdown(`*Version: ${step.version}*\n\n`);
        
        if (step.description) {
            tooltip.appendMarkdown(`> ${step.description}\n\n`);
        }

        tooltip.appendMarkdown(`---\n`);
        tooltip.appendMarkdown(`**Author:** ${step.author || "Official"}\n\n`);
        tooltip.appendMarkdown(`**Repo:** ${step.repo}\n\n`);
        tooltip.appendMarkdown(`**Module:** \`${step.namespace}\`\n\n`);

        if (step.requirements) {
            tooltip.appendMarkdown(`**Requirements:** \`${step.requirements}\`\n\n`);
        }

        if (step.how_to_use) {
            tooltip.appendMarkdown(`**Usage:**\n\`\`\`python\n${step.how_to_use}\n\`\`\`\n\n`);
        }

        if (step.examples) {
            tooltip.appendMarkdown(`[Explore Examples](${step.examples})\n\n`);
        }

        tooltip.appendMarkdown(`---\n*Click to insert import and usage.*`);
        
        this.tooltip = tooltip;
        this.contextValue = 'libraryStep';
        this.command = { command: 'wpipeSteps.insertStep', title: 'Insert', arguments: [step] };
    }
}
