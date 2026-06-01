#!/bin/bash

# Script para empaquetar e instalar la extensión localmente

echo "🚀 Iniciando build e instalación de WPipe Tools..."

# 1. Instalar dependencias si no existen
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias de Node..."
    npm install
fi

# 2. Compilar TypeScript
echo "🏗️ Compilando código..."
npm run compile

# 3. Verificar si vsce está instalado
if ! command -v vsce &> /dev/null
then
    echo "⚠️ vsce no está instalado. Instalándolo globalmente..."
    npm install -g @vscode/vsce
fi

# 4. Generar el paquete .vsix
echo "📦 Generando archivo .vsix..."
# Extraemos la versión del package.json para saber el nombre del archivo
VERSION=$(grep '"version"' package.json | cut -d'"' -f4)
PACKAGE_NAME="wpipe-vscode-$VERSION.vsix"

# Ejecutamos el empaquetado (con --allow-missing-repository para evitar el prompt interactivo)
vsce package --allow-missing-repository --no-git-tag-version

# 5. Instalar automáticamente en VS Code
if [ -f "$PACKAGE_NAME" ]; then
    echo "📥 Instalando extensión $PACKAGE_NAME en VS Code..."
    code --install-extension "$PACKAGE_NAME" --force
    echo "✅ ¡Extensión instalada y lista para usar!"
else
    echo "❌ Error: No se pudo encontrar el archivo $PACKAGE_NAME."
    ls -l *.vsix
fi
