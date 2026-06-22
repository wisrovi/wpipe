import * as vscode from 'vscode';

export interface StepEntry {
    name: string;
    func_name: string;
    namespace: string;
    repo: string;
    file: string;
    author?: string;
    version?: string;
    description?: string;
    how_to_use?: string;
    examples?: string;
    requirements?: string;
    category?: string;
    subcategory1?: string;
    subcategory2?: string;
    subcategory3?: string;
}

export class CatalogManager {
    private static catalog: StepEntry[] = [];
    private static readonly OFFICIAL_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-steps/001-DEVELOPMENT/steps_catalog.json';
    private static readonly COMMUNITY_URL = 'https://raw.githubusercontent.com/wisrovi/wpipe-plugins/001-DEVELOPMENT/steps_catalog.json';

    public static async init(context: vscode.ExtensionContext): Promise<void> {
        const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, 'catalog_cache.json');
        
        // 1. Load local embedded catalog (always trust local file changes/additions)
        let localCatalog: StepEntry[] = [];
        try {
            const catalogUri = vscode.Uri.joinPath(context.extensionUri, 'out', 'steps_catalog.json');
            const catalogData = await vscode.workspace.fs.readFile(catalogUri);
            const raw = JSON.parse(new TextDecoder().decode(catalogData));
            localCatalog = Array.isArray(raw) ? raw : (raw.default || []);
        } catch (e2) {}

        // 2. Load from remote cache
        let cachedCatalog: StepEntry[] = [];
        try {
            const cacheData = await vscode.workspace.fs.readFile(cacheUri);
            const cached = JSON.parse(new TextDecoder().decode(cacheData));
            if (Array.isArray(cached)) cachedCatalog = cached;
        } catch (e) {}

        // 3. Merge: Local properties (such as categories/subcategories) overlay cached metadata
        const mergedMap = new Map<string, StepEntry>();
        
        cachedCatalog.forEach(s => {
            mergedMap.set(`${s.repo}:${s.name}`, s);
        });

        localCatalog.forEach(s => {
            const key = `${s.repo}:${s.name}`;
            const existing = mergedMap.get(key);
            if (existing) {
                // Overlay local metadata to preserve categories
                mergedMap.set(key, { ...existing, ...s });
            } else {
                mergedMap.set(key, s);
            }
        });

        this.catalog = Array.from(mergedMap.values());

        // 2. Trigger background update
        this.update(context, false);
    }

    public static async update(context: vscode.ExtensionContext, manual: boolean = false): Promise<void> {
        const download = async () => {
            const oldNames = new Set(this.catalog.map(s => `${s.repo}:${s.name}`));
            
            const fetchJson = async (url: string, defaultRepo: string): Promise<any[]> => {
                try {
                    const response = await fetch(url);
                    if (!response.ok) return [];
                    const p = await response.json();
                    const items = Array.isArray(p) ? p : [];
                    
                    // Base URL for relative paths (everything before steps_catalog.json)
                    const baseUrl = url.substring(0, url.lastIndexOf('/') + 1);

                    const resolveUrl = (path: string | undefined) => {
                        if (!path) return undefined;
                        if (path.startsWith('http')) return path;
                        // Join base URL with relative path, ensuring no double slashes in the middle
                        return `${baseUrl}${path.startsWith('/') ? path.substring(1) : path}`;
                    };

                    // Force correct repo field and resolve relative URLs
                    return items.map(item => ({ 
                        ...item, 
                        repo: item.repo || defaultRepo,
                        requirements: resolveUrl(item.requirements),
                        examples: resolveUrl(item.examples)
                    }));
                } catch (e) {
                    return [];
                }
            };
            
            const [off, com] = await Promise.all([
                fetchJson(this.OFFICIAL_URL, 'Official'), 
                fetchJson(this.COMMUNITY_URL, 'Community')
            ]);
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
