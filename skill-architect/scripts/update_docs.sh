#!/bin/bash
KB_DIR="../knowledge/specs"
mkdir -p "$KB_DIR"

download_clean() {
    url=$1
    filename=$2
    echo "💎 Destilando: $filename..."
    
    # 1. Python extrae SOLO etiquetas semánticas (h1, p, pre...) y texto.
    # 2. Pandoc convierte ese HTML simplificado a Markdown.
    # 3. 'cat -s' elimina los múltiples saltos de línea que dejan los divs borrados.
    
    python3 extract_clean.py "$url" | \
    pandoc -f html -t gfm --wrap=none --strip-comments | \
    cat -s > "$KB_DIR/$filename.md"
}

echo "🧠 Iniciando actualización PURISTA..."

download_clean "https://code.visualstudio.com/docs/copilot/customization/agent-skills" "vscode-agent-skills"
download_clean "https://code.visualstudio.com/docs/copilot/customization/custom-agents" "vscode-custom-agents"
download_clean "https://agentskills.io/specification" "agentskills-spec"

echo "✅ Documentación limpia generada en $KB_DIR"