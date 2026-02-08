#!/bin/bash
# scripts/update_docs.sh

# Rutas relativas
KB_DIR="../knowledge/specs"
# AQUI ESTA EL CAMBIO: Apuntamos a la skill vecina
EXTRACTOR="../../web-scraper/scripts/extract.py" 

mkdir -p "$KB_DIR"

download_clean() {
    url=$1
    filename=$2
    echo "💎 Destilando: $filename..."
    
    # Llamamos al extractor usando la variable
    python3 "$EXTRACTOR" "$url" | \
    pandoc -f html -t gfm --wrap=none --strip-comments | \
    cat -s > "$KB_DIR/$filename.md"
}

echo "🧠 Iniciando actualización PURISTA..."

download_clean "https://code.visualstudio.com/docs/copilot/customization/agent-skills" "vscode-agent-skills"
download_clean "https://code.visualstudio.com/docs/copilot/customization/custom-agents" "vscode-custom-agents"
download_clean "https://agentskills.io/specification" "agentskills-spec"

echo "✅ Documentación limpia generada en $KB_DIR"