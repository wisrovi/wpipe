import * as vscode from 'vscode';

export interface StepEntry {
    name: string;
    func_name: string;
    namespace: string;
    repo: string;
    file: string;
    author?: string;
}

export class CatalogManager {
    private static catalog: StepEntry[] = [];
    private static readonly OFFICIAL_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-steps/001-DEVELOPMENT/steps_catalog.json';
    private static readonly COMMUNITY_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-plugins/001-DEVELOPMENT/steps_catalog.json';

    public static async init(context: vscode.ExtensionContext): Promise<void> {
        const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, 'catalog_cache.json');
        
        // 1. Load from cache
        try {
            const cacheData = await vscode.workspace.fs.readFile(cacheUri);
            const cached = JSON.parse(new TextDecoder().decode(cacheData));
            if (Array.isArray(cached)) this.catalog = cached;
        } catch (e) {
            // Cache doesn't exist or is invalid, load embedded data
            try {
                const catalogUri = vscode.Uri.joinPath(context.extensionUri, 'out', 'steps_catalog.json');
                const catalogData = await vscode.workspace.fs.readFile(catalogUri);
                const raw = JSON.parse(new TextDecoder().decode(catalogData));
                this.catalog = Array.isArray(raw) ? raw : (raw.default || []);
            } catch (e2) {}
        }

        // 2. Trigger background update
        this.update(context, false);
    }

    public static async update(context: vscode.ExtensionContext, manual: boolean = false): Promise<void> {
        const download = async () => {
            const oldNames = new Set(this.catalog.map(s => `${s.repo}:${s.name}`));
            
            const fetchJson = async (url: string): Promise<any[]> => {
                try {
                    const response = await fetch(url);
                    if (!response.ok) return [];
                    const p = await response.json();
                    return Array.isArray(p) ? p : [];
                } catch (e) {
                    return [];
                }
            };
            
            const [off, com] = await Promise.all([fetchJson(this.OFFICIAL_URL), fetchJson(this.COMMUNITY_URL)]);
            const newCatalog = [...off, ...com];

            if (newCatalog.length > 0) {
                const newItems = newCatalog.filter(s => !oldNames.has(`${s.repo}:${s.name}`));
                this.catalog = newCatalog;
                try {
                    const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, 'catalog_cache.json');
                    await vscode.workspace.fs.writeFile(cacheUri, new TextEncoder().encode(JSON.stringify(this.catalog)));
                } catch (e) {}
                
                if (newItems.length > 0) {
                    vscode.window.showInformationMessage(`🚀 ¡Hay ${newItems.length} nuevos estados en WPipe!`, "Ver Catálogo").then(selection => {
                        if (selection === "Ver Catálogo") vscode.commands.executeCommand('wpipe-vscode.searchSteps');
                    });
                } else if (manual) {
                    vscode.window.setStatusBarMessage("✅ WPipe: Catálogo al día", 3000);
                }
                vscode.commands.executeCommand('wpipeSteps.refreshEntry');
            }
        };

        if (manual) {
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "Actualizando catálogo...",
                cancellable: false
            }, download);
        } else {
            download();
        }
    }

    public static getSteps(): StepEntry[] {
        return this.catalog;
    }
}
