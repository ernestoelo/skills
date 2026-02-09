#!/bin/bash
# scripts/update_docs.sh
#
# Fetches and cleans upstream documentation for the architect skill.
# Output goes to references/ for manual curation into the skill.
#
# Requirements: python3, pandoc, web-scraper skill (extract.py)
# Usage: Run from architect/scripts/ directory

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="$SCRIPT_DIR/../references"
EXTRACTOR="$SCRIPT_DIR/../../web-scraper/scripts/extract.py"

if [[ ! -f "$EXTRACTOR" ]]; then
    echo "Error: web-scraper extract.py not found at $EXTRACTOR"
    exit 1
fi

download_clean() {
    url=$1
    filename=$2
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
