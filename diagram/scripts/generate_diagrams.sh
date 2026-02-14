#!/bin/bash
# Script to generate all PNG/SVG diagrams from .puml (PlantUML) and .dot (Graphviz) files
# Usage: ./generate_diagrams.sh [directory]
# If no directory is specified, searches in the current directory and subfolders

set -e

DIR=${1:-.}

# Check if PlantUML is installed
if ! command -v plantuml &> /dev/null; then
  echo "Error: PlantUML is not installed. Install it with 'sudo pacman -S plantuml' (see @sys-env)."
  exit 1
fi
# Check if Graphviz (dot) is installed
if ! command -v dot &> /dev/null; then
  echo "Error: Graphviz (dot) is not installed. Install it with 'sudo pacman -S graphviz' (see @sys-env)."
  exit 1
fi

# Find and process all .puml files (PlantUML)
echo "Searching for .puml files in $DIR ..."
find "$DIR" -type f -name '*.puml' | while read -r file; do
  echo "Generating PlantUML diagram for $file ..."
  plantuml "$file"
done
# Find and process all .dot files (Graphviz)
echo "Searching for .dot files in $DIR ..."
find "$DIR" -type f -name '*.dot' | while read -r file; do
  echo "Generating Graphviz diagram for $file ..."
  dot -Tpng "$file" -o "${file%.dot}.png"
  dot -Tsvg "$file" -o "${file%.dot}.svg"
done

echo "Diagrams generated successfully."
