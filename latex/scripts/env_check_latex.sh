#!/bin/bash
# Check LaTeX environment compatibility with sys-env

echo "Checking LaTeX packages..."

# Check texlive-core
if pacman -Q texlive-core &>/dev/null; then
    echo "✓ texlive-core installed"
else
    echo "✗ texlive-core missing. Install with: sudo pacman -S texlive-core"
fi

# Check texlive-latexextra
if pacman -Q texlive-latexextra &>/dev/null; then
    echo "✓ texlive-latexextra installed"
else
    echo "✗ texlive-latexextra missing. Install with: sudo pacman -S texlive-latexextra"
fi

# Check pandoc
if pacman -Q pandoc &>/dev/null; then
    echo "✓ pandoc installed"
else
    echo "✗ pandoc missing. Install with: sudo pacman -S pandoc"
fi

echo "Environment check complete."