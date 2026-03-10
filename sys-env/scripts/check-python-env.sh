#!/bin/bash
# check-python-env.sh - Validate Python environment safety before package operations
# Usage: ./check-python-env.sh [--auto-fix]
# Location: /home/p3g4sus/.copilot/skills/sys-env/scripts/

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SAFE=true
CONDA_ACTIVE=""
PYTHON_EXECUTABLE=""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Python Environment Safety Check${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if conda/miniforge is active
echo -e "${BLUE}[1/4]${NC} Checking for active Python environments..."

if [ -n "$CONDA_DEFAULT_ENV" ]; then
    CONDA_ACTIVE="$CONDA_DEFAULT_ENV"
    echo -e "${YELLOW}⚠️  Conda environment active: ${CONDA_ACTIVE}${NC}"
    SAFE=false
elif [ -n "$VIRTUAL_ENV" ]; then
    CONDA_ACTIVE="$VIRTUAL_ENV"
    echo -e "${YELLOW}⚠️  Virtual environment active: ${CONDA_ACTIVE}${NC}"
    SAFE=false
else
    echo -e "${GREEN}✅ No conda/venv active${NC}"
fi

# Check which Python is in PATH
echo -e "\n${BLUE}[2/4]${NC} Checking Python executable in PATH..."
PYTHON_EXECUTABLE=$(which python3 2>/dev/null || echo "NOT FOUND")

if [[ "$PYTHON_EXECUTABLE" == *"miniforge3"* ]]; then
    echo -e "${YELLOW}⚠️  Python from miniforge3: ${PYTHON_EXECUTABLE}${NC}"
    SAFE=false
elif [[ "$PYTHON_EXECUTABLE" == *"usr/bin"* ]]; then
    echo -e "${GREEN}✅ Using system Python: ${PYTHON_EXECUTABLE}${NC}"
else
    echo -e "${YELLOW}⚠️  Unexpected Python path: ${PYTHON_EXECUTABLE}${NC}"
    SAFE=false
fi

# Check for common package locations
echo -e "\n${BLUE}[3/4]${NC} Checking package install locations..."
PACMAN_SITE=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null || echo "UNKNOWN")

if [[ "$PACMAN_SITE" == *"miniforge3"* ]]; then
    echo -e "${YELLOW}⚠️  pip would install to miniforge: ${PACMAN_SITE}${NC}"
    SAFE=false
else
    echo -e "${GREEN}✅ pip configured for system: ${PACMAN_SITE}${NC}"
fi

# Summary and recommendations
echo -e "\n${BLUE}[4/4]${NC} Environment Safety Assessment..."

if [ "$SAFE" = true ]; then
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ SAFE - Ready for pacman/yay operations${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    exit 0
else
    echo -e "${RED}════════════════════════════════════════${NC}"
    echo -e "${RED}❌ UNSAFE - Conda/venv active!${NC}"
    echo -e "${RED}════════════════════════════════════════${NC}\n"
    
    if [ -n "$CONDA_ACTIVE" ]; then
        echo -e "${YELLOW}Recommendation:${NC}"
        echo -e "  ${YELLOW}Run:${NC} ${BLUE}conda deactivate${NC}"
        echo -e "  ${YELLOW}Then:${NC} ${BLUE}yay -S package-name${NC}"
        echo -e "  ${YELLOW}Finally:${NC} ${BLUE}conda activate $CONDA_ACTIVE${NC}\n"
    fi
    
    # Auto-fix option
    if [ "$1" = "--auto-fix" ]; then
        echo -e "${BLUE}Auto-fixing...${NC}"
        if [ -n "$CONDA_DEFAULT_ENV" ]; then
            conda deactivate 2>/dev/null && echo -e "${GREEN}✅ Conda deactivated${NC}" || echo -e "${RED}❌ Failed to deactivate conda${NC}"
        fi
    else
        echo -e "${YELLOW}Use ${BLUE}--auto-fix${YELLOW} flag to automatically deactivate:${NC}"
        echo -e "  ${BLUE}./check-python-env.sh --auto-fix${NC}\n"
    fi
    
    exit 1
fi
