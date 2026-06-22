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

    async getChildren(element?: vscode.TreeItem): Promise<vscode.TreeItem[]> {
        if (!element) {
            return [
                new vscode.TreeItem('🛠️ Workspace Steps', vscode.TreeItemCollapsibleState.Expanded),
                new vscode.TreeItem('📦 Official Library', vscode.TreeItemCollapsibleState.Collapsed),
                new vscode.TreeItem('🤝 Community Plugins', vscode.TreeItemCollapsibleState.Collapsed)
            ];
        }

        if (element instanceof CategoryItem) {
            return this.getCategoryChildren(element.repo, element.path);
        }

        const label = element.label as string;
        if (label.includes('Workspace')) {
            return this.searchWorkspace();
        }
        if (label.includes('Official')) {
            return this.getCategoryChildren('Official', []);
        }
        if (label.includes('Community')) {
            return this.getCategoryChildren('Community', []);
        }
        return [];
    }

    /**
     * Resolves the child categories and library items for a given path and repository.
     */
    private getCategoryChildren(repo: string, categoryPath: string[]): vscode.TreeItem[] {
        const steps = CatalogManager.getSteps().filter(s => s.repo === repo);
        const subcategoriesSet = new Set<string>();
        const directLibraryItems: LibraryItem[] = [];

        for (const step of steps) {
            // Build the classification sequence for the step
            let catSeq = [step.category, step.subcategory1, step.subcategory2, step.subcategory3]
                .map(s => s?.trim())
                .filter(Boolean) as string[];
            
            // If the step lacks any category, group it in a virtual "General" folder
            if (catSeq.length === 0) {
                catSeq = ['General'];
            }

            // Check if step's category path starts with the requested categoryPath
            if (categoryPath.length <= catSeq.length && categoryPath.every((val, idx) => catSeq[idx] === val)) {
                if (catSeq.length === categoryPath.length) {
                    // Exact match: this step is a leaf node in the current folder level
                    directLibraryItems.push(new LibraryItem(step));
                } else {
                    // Subcategory branch: identify the next nesting folder
                    const nextSubcat = catSeq[categoryPath.length];
                    subcategoriesSet.add(nextSubcat);
                }
            }
        }

        // Map subcategories to CategoryItems
        const categoryItems = Array.from(subcategoriesSet).map(subcat => 
            new CategoryItem(subcat, repo, [...categoryPath, subcat])
        );

        // Sort both collections alphabetically for premium UX
        categoryItems.sort((a, b) => (a.label as string).localeCompare(b.label as string));
        directLibraryItems.sort((a, b) => (a.label as string).localeCompare(b.label as string));

        return [...categoryItems, ...directLibraryItems];
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

/**
 * Represents a virtual directory node for hierarchical sorting in the step sidebar.
 */
export class CategoryItem extends vscode.TreeItem {
    constructor(
        label: string,
        public readonly repo: string,
        public readonly path: string[]
    ) {
        super(label, vscode.TreeItemCollapsibleState.Collapsed);
        this.iconPath = new vscode.ThemeIcon('folder');
        this.contextValue = 'categoryItem';
    }
}
