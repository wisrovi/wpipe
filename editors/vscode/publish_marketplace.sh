#!/bin/bash

# Script para publicar la extensión en el VS Code Marketplace

echo "🌍 Preparando publicación en el Marketplace..."

# 1. Verificar si se proporcionó un Token
if [ -z "$1" ]; then
    echo "❌ Error: Debes proporcionar tu Personal Access Token (PAT) como argumento."
    echo "Uso: ./publish_marketplace.sh TU_TOKEN_AQUI"
    exit 1
fi

TOKEN=$1

# 2. Compilar antes de publicar
echo "🏗️ Compilando última versión..."
npm run compile

# 3. Publicar
echo "🚀 Publicando extensión..."
vsce publish -p $TOKEN

if [ $? -eq 0 ]; then
    echo "✅ ¡Éxito! La extensión ha sido enviada al Marketplace."
else
    echo "❌ Falló la publicación. Revisa los errores arriba."
fi
