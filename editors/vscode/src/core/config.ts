import * as vscode from 'vscode';

export class ConfigManager {
    /**
     * Obtiene una configuración priorizando un archivo local 'wpipe.config.json' 
     * en la raíz del workspace, y cayendo de vuelta a las configuraciones de VS Code.
     */
    public static async getSetting<T>(key: string, defaultValue: T): Promise<T> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders) {
            const configPath = vscode.Uri.joinPath(workspaceFolders[0].uri, 'wpipe.config.json');
            try {
                const data = await vscode.workspace.fs.readFile(configPath);
                const config = JSON.parse(new TextDecoder().decode(data));
                if (config[key] !== undefined) {
                    return config[key];
                }
            } catch (e) {
                // El archivo no existe o no es JSON válido, ignorar.
            }
        }

        // Si no está en el JSON, buscar en la configuración de VS Code.
        const vscodeConfig = vscode.workspace.getConfiguration('wpipe');
        return vscodeConfig.get<T>(key, defaultValue);
    }

    /**
     * Indica si la creación de archivos de respaldo (.wpipe.mermaid) está habilitada.
     */
    public static async isBackupEnabled(): Promise<boolean> {
        return await this.getSetting<boolean>('enableBackupFile', true);
    }
}
