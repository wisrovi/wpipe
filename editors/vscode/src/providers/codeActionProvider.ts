import * as vscode from 'vscode';
import { parser } from '@lezer/python';

export class WPipeCodeActionProvider implements vscode.CodeActionProvider {
    public static readonly providedCodeActionKinds = [
        vscode.CodeActionKind.QuickFix
    ];

    public provideCodeActions(document: vscode.TextDocument, range: vscode.Range, context: vscode.CodeActionContext, token: vscode.CancellationToken): vscode.CodeAction[] {
        const actions: vscode.CodeAction[] = [];
        const content = document.getText();
        
        try {
            const tree = parser.parse(content);
            tree.iterate({
                enter: (node) => {
                    if (node.name === 'FunctionDefinition') {
                        const funcRange = new vscode.Range(
                            document.positionAt(node.from),
                            document.positionAt(node.to)
                        );
                        
                        // Check if the current range (cursor) is within this function definition
                        if (range.intersection(funcRange)) {
                            // Check if it already has a @step decorator
                            let hasStepDecorator = false;
                            let parent = node.node.parent;
                            if (parent) {
                                // In some parsers, decorators are siblings or children of a parent wrapper
                                // For lezer-python, we might need to check the parent's children
                                parent.getChildren('Decorator').forEach(dec => {
                                    const decText = content.substring(dec.from, dec.to);
                                    if (decText.startsWith('@step')) {
                                        hasStepDecorator = true;
                                    }
                                });
                            }

                            if (!hasStepDecorator) {
                                const action = new vscode.CodeAction('Convert to WPipe Step', vscode.CodeActionKind.QuickFix);
                                action.edit = new vscode.WorkspaceEdit();
                                
                                const nameNode = node.node.getChild('VariableName');
                                const funcName = nameNode ? content.substring(nameNode.from, nameNode.to) : 'my_step';
                                
                                const decorator = `@step(name="${funcName}", version="1.0.0")\n`;
                                action.edit.insert(document.uri, document.positionAt(node.from), decorator);
                                
                                // Check if wpipe is imported
                                if (!content.includes('from wpipe import step')) {
                                    action.edit.insert(document.uri, new vscode.Position(0, 0), 'from wpipe import step\n');
                                }
                                
                                actions.push(action);
                            }
                        }
                    }
                }
            });
        } catch (e) {}

        return actions;
    }
}
