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
            await WorkspaceIndex.indexWorkspace();
            return this.getCategoryChildren('Workspace', []);
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
        let rawSteps: any[] = [];
        if (repo === 'Workspace') {
            rawSteps = WorkspaceIndex.getAllSteps();
        } else {
            rawSteps = CatalogManager.getSteps().filter(s => s.repo === repo);
        }

        const subcategoriesMap = new Map<string, string>(); // lowercase key -> original case value
        const directItems: vscode.TreeItem[] = [];

        const capitalize = (str: string) => {
            if (!str) return '';
            return str.split(/[_-]/)
                .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                .join(' ');
        };

        const isSameTerm = (a: string | undefined, b: string | undefined) => {
            if (!a || !b) return false;
            const clean = (str: string) => str.toLowerCase().replace(/[_\s-]/g, '').trim();
            return clean(a) === clean(b);
        };

        for (const step of rawSteps) {
            // Normalize and capitalize categories on the fly to guarantee case-insensitive merge and formatting
            let cat = step.category ? capitalize(step.category) : '';
            let sub1 = step.subcategory1 ? capitalize(step.subcategory1) : '';
            let sub2 = step.subcategory2 ? capitalize(step.subcategory2) : '';
            let sub3 = step.subcategory3 ? capitalize(step.subcategory3) : '';

            // Prune redundant same-term folders (matching name or func_name)
            if (sub3 && (isSameTerm(sub3, step.name) || (step.func_name && isSameTerm(sub3, step.func_name)))) sub3 = '';
            if (sub2 && (isSameTerm(sub2, step.name) || (step.func_name && isSameTerm(sub2, step.func_name)))) sub2 = '';
            if (sub1 && (isSameTerm(sub1, step.name) || (step.func_name && isSameTerm(sub1, step.func_name)))) sub1 = '';

            let catSeq = [cat, sub1, sub2, sub3].filter(Boolean) as string[];
            if (catSeq.length === 0) {
                catSeq = ['General'];
            }

            // Compare category paths case-insensitively
            const pathMatches = categoryPath.length <= catSeq.length &&
                categoryPath.every((val, idx) => catSeq[idx].toLowerCase() === val.toLowerCase());

            if (pathMatches) {
                if (catSeq.length === categoryPath.length) {
                    // Leaf node in this folder level
                    if (repo === 'Workspace') {
                        directItems.push(new StepItem(step.name, step.filePath, step.line));
                    } else {
                        directItems.push(new LibraryItem(step));
                    }
                } else {
                    // Subcategory branch: identify the next nesting folder
                    const nextSubcat = catSeq[categoryPath.length];
                    const lower = nextSubcat.toLowerCase();
                    if (!subcategoriesMap.has(lower)) {
                        subcategoriesMap.set(lower, nextSubcat);
                    }
                }
            }
        }

        // Map subcategories to CategoryItems
        const categoryItems = Array.from(subcategoriesMap.values()).map(subcat => 
            new CategoryItem(subcat, repo, [...categoryPath, subcat])
        );

        // Sort both collections alphabetically for premium UX
        categoryItems.sort((a, b) => (a.label as string).localeCompare(b.label as string));
        directItems.sort((a, b) => (a.label as string).localeCompare(b.label as string));

        return [...categoryItems, ...directItems];
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
