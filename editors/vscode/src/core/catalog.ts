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

    private static normalizeStep(s: StepEntry): StepEntry {
        const step = { ...s };
        step.repo = step.repo || 'Official';
        
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

        // Extract from namespace if missing
        if (!step.category && step.namespace) {
            const parts = step.namespace.split('.');
            if (parts[0] === 'wpipe_steps' || parts[0] === 'wpipe_plugins') {
                parts.shift();
            }
            
            if (parts.length > 0) step.category = parts[0];
            if (parts.length > 1) step.subcategory1 = parts[1];
            if (parts.length > 2) step.subcategory2 = parts[2];
            if (parts.length > 3) step.subcategory3 = parts[3];
        }

        // Format and capitalize categories for premium aesthetics
        if (step.category) step.category = capitalize(step.category);
        if (step.subcategory1) step.subcategory1 = capitalize(step.subcategory1);
        if (step.subcategory2) step.subcategory2 = capitalize(step.subcategory2);
        if (step.subcategory3) step.subcategory3 = capitalize(step.subcategory3);

        // Remove redundant folder layers that match the step name
        if (step.subcategory3 && (isSameTerm(step.subcategory3, step.name) || isSameTerm(step.subcategory3, step.func_name))) {
            step.subcategory3 = '';
        }
        if (step.subcategory2 && (isSameTerm(step.subcategory2, step.name) || isSameTerm(step.subcategory2, step.func_name))) {
            step.subcategory2 = '';
        }
        if (step.subcategory1 && (isSameTerm(step.subcategory1, step.name) || isSameTerm(step.subcategory1, step.func_name))) {
            step.subcategory1 = '';
        }

        return step;
    }

    private static mergeCatalogs(base: StepEntry[], incoming: StepEntry[]): StepEntry[] {
        const mergedMap = new Map<string, StepEntry>();
        
        base.forEach(s => {
            const normalized = this.normalizeStep(s);
            mergedMap.set(`${normalized.repo}:${normalized.name}`, normalized);
        });

        incoming.forEach(s => {
            const normalized = this.normalizeStep(s);
            const key = `${normalized.repo}:${normalized.name}`;
            const existing = mergedMap.get(key);
            if (existing) {
                // Merge properties, prioritizing incoming properties
                mergedMap.set(key, { ...existing, ...normalized });
            } else {
                mergedMap.set(key, normalized);
            }
        });

        return Array.from(mergedMap.values());
    }

    public static async init(context: vscode.ExtensionContext): Promise<void> {
        const cacheUri = vscode.Uri.joinPath(context.globalStorageUri, 'catalog_cache.json');
        
        // 1. Load from remote cache
        let cachedCatalog: StepEntry[] = [];
        try {
            const cacheData = await vscode.workspace.fs.readFile(cacheUri);
            const cached = JSON.parse(new TextDecoder().decode(cacheData));
            if (Array.isArray(cached)) cachedCatalog = cached;
        } catch (e) {}

        // 2. Normalize and populate categories of cached steps
        this.catalog = this.mergeCatalogs([], cachedCatalog);

        // 3. Trigger background update
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
                    
                    const baseUrl = url.substring(0, url.lastIndexOf('/') + 1);

                    const resolveUrl = (path: string | undefined) => {
                        if (!path) return undefined;
                        if (path.startsWith('http')) return path;
                        return `${baseUrl}${path.startsWith('/') ? path.substring(1) : path}`;
                    };

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
                const merged = this.mergeCatalogs(this.catalog, newCatalog);
                const newItems = merged.filter(s => !oldNames.has(`${s.repo}:${s.name}`));
                this.catalog = merged;
                
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
