#!/bin/bash
# Compile LaTeX document to PDF
# Usage: ./compile_latex.sh <file.tex>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file.tex>"
    exit 1
fi

FILE=$1
BASENAME="${FILE%.tex}"

# Compile with xelatex for better Unicode support
xelatex -interaction=nonstopmode "$FILE"
xelatex -interaction=nonstopmode "$FILE"  # Run twice for references

# Clean auxiliary files
rm -f "$BASENAME".aux "$BASENAME".log "$BASENAME".out "$BASENAME".fls "$BASENAME".fdb_latexmk

echo "Compiled $FILE to $BASENAME.pdf"