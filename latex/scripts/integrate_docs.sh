#!/bin/bash
# Integrate LaTeX output with other document skills using pandoc
# Usage: ./integrate_docs.sh <file.tex> [format]

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file.tex> [docx|pdf]"
    exit 1
fi

FILE=$1
FORMAT=${2:-docx}
BASENAME="${FILE%.tex}"

# First compile to PDF if needed
if [ ! -f "$BASENAME.pdf" ]; then
    ./compile_latex.sh "$FILE"
fi

case $FORMAT in
    docx)
        pandoc "$BASENAME.pdf" -o "$BASENAME.docx"
        echo "Converted to $BASENAME.docx"
        ;;
    pdf)
        echo "PDF already exists: $BASENAME.pdf"
        ;;
    *)
        echo "Supported formats: docx, pdf"
        ;;
esac