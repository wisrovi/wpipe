import * as vscode from 'vscode';
import { parser } from '@lezer/python';

export interface WorkspaceStep {
    name: string;
    version: string;
    filePath: string;
    line: number;
    description?: string;
    tags?: string[];
    category?: string;
    subcategory1?: string;
    subcategory2?: string;
    subcategory3?: string;
}

export class WorkspaceIndex {
    private static steps: Map<string, WorkspaceStep> = new Map();

    public static async indexWorkspace() {
        const config = vscode.workspace.getConfiguration('wpipe');
        const userExcludes = config.get<string[]>('excludePaths', []);
        const maxFiles = config.get<number>('maxSearchFiles', 500);

        const defaultExcludes = [
            '**/node_modules/**', '**/.venv/**', '**/venv/**', '**/.env/**', '**/env/**',
            '**/.conda/**', '**/conda/**', '**/site-packages/**', '**/wpipe/wpipe/**',
            '**/__pycache__/**', '**/.pytest_cache/**', '**/.mypy_cache/**',
            '**/.ruff_cache/**', '**/.tox/**', '**/build/**', '**/dist/**', '**/*.egg-info/**'
        ];

        const combinedExcludes = Array.from(new Set([...defaultExcludes, ...userExcludes]));
        const excludePattern = `{${combinedExcludes.join(',')}}`;

        const files = await vscode.workspace.findFiles('**/*.py', excludePattern, maxFiles);
        
        const newSteps: Map<string, WorkspaceStep> = new Map();

        for (const f of files) {
            try {
                const contentData = await vscode.workspace.fs.readFile(f);
                if (contentData.length > 500000) continue;
                
                const content = new TextDecoder().decode(contentData);
                const tree = parser.parse(content);
                
                tree.iterate({
                    enter: (node) => {
                        if (node.name === 'Decorator') {
                            const decText = content.substring(node.from, node.to);
                            if (decText.startsWith('@step')) {
                                 let name = '';
                                 let version = 'v1.0';
                                 let description = '';
                                 let category = '';
                                 let subcategory1 = '';
                                 let subcategory2 = '';
                                 let subcategory3 = '';
                                 
                                 const nameMatch = decText.match(/name\s*=\s*['"](.*?)['"]/);
                                 if (nameMatch) name = nameMatch[1];

                                 const verMatch = decText.match(/version\s*=\s*['"](.*?)['"]/);
                                 if (verMatch) version = verMatch[1];

                                 const descMatch = decText.match(/description\s*=\s*['"](.*?)['"]/);
                                 if (descMatch) description = descMatch[1];

                                 const catMatch = decText.match(/category\s*=\s*['"](.*?)['"]/);
                                 if (catMatch) category = catMatch[1];

                                 const sub1Match = decText.match(/subcategory1\s*=\s*['"](.*?)['"]/);
                                 if (sub1Match) subcategory1 = sub1Match[1];

                                 const sub2Match = decText.match(/subcategory2\s*=\s*['"](.*?)['"]/);
                                 if (sub2Match) subcategory2 = sub2Match[1];

                                 const sub3Match = decText.match(/subcategory3\s*=\s*['"](.*?)['"]/);
                                 if (sub3Match) subcategory3 = sub3Match[1];
                                 
                                 if (!name && node.node.parent) {
                                     let funcDef = node.node.parent.getChild('FunctionDefinition') || node.node.parent.getChild('ClassDefinition');
                                     if (funcDef) {
                                         let varName = funcDef.getChild('VariableName');
                                         if (varName) name = content.substring(varName.from, varName.to);
                                     }
                                 }
                                 
                                 if (name) {
                                     const line = content.substring(0, node.from).split('\n').length - 1;
                                     newSteps.set(name, { 
                                         name, 
                                         version, 
                                         filePath: f.fsPath, 
                                         line, 
                                         description,
                                         category,
                                         subcategory1,
                                         subcategory2,
                                         subcategory3
                                     });
                                 }
                            }
                        }
                    }
                });
            } catch (e) {}
        }
        this.steps = newSteps;
    }

    public static getStep(name: string): WorkspaceStep | undefined {
        return this.steps.get(name);
    }

    public static getAllSteps(): WorkspaceStep[] {
        return Array.from(this.steps.values());
    }
}
