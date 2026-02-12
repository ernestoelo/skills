#!/usr/bin/env bash

# shared/scripts/update-docs.sh
#
# Fetches y limpia documentación upstream para la skill architect.
# Output va a shared/references/ para curación manual.
#
# Requisitos: python3, pandoc, web-scraper skill (extract.py)
# Uso: Ejecutar desde shared/scripts/ o ajustar rutas relativas.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="$SCRIPT_DIR/../../shared/references"
EXTRACTOR="$SCRIPT_DIR/../../../web-scraper/scripts/extract.py"

# Verify dependencies
for cmd in python3 pandoc; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Error: required command '$cmd' not found in PATH"
        exit 1
    fi
done

if [[ ! -f "$EXTRACTOR" ]]; then
    echo "Error: web-scraper extract.py not found at $EXTRACTOR"
    exit 1
fi

mkdir -p "$OUT_DIR"

download_clean() {
    local url="$1"
    local filename="$2"
    echo "Fetching: $filename..."

    python3 "$EXTRACTOR" "$url" | \
    pandoc -f html -t gfm --wrap=none --strip-comments | \
    cat -s > "$OUT_DIR/$filename.md"
}

echo "Updating upstream documentation..."

download_clean "https://code.visualstudio.com/docs/copilot/customization/agent-skills" "upstream-vscode-agent-skills"
download_clean "https://code.visualstudio.com/docs/copilot/customization/custom-agents" "upstream-vscode-custom-agents"
download_clean "https://agentskills.io/specification" "upstream-agentskills-spec"

echo "Done. Files written to $OUT_DIR"
echo "Review and curate into agents-spec.md as needed."
