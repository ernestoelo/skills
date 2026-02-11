#!/bin/bash
#
# Setup script for OpenCode Integration Manager
# Sigue las mejores prácticas de sys-env para gestión de dependencias
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}🚀 Setting up OpenCode Integration Manager${NC}"
echo "========================================"

# Function to check command availability
check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo -e "  ✅ $1 found"
        return 0
    else
        echo -e "  ❌ $1 not found"
        return 1
    fi
}

# Function to install package
install_package() {
    local package="$1"
    local description="$2"

    echo -e "${YELLOW}📦 Installing $description...${NC}"

    if command -v apt-get >/dev/null 2>&1; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y "$package"
    elif command -v pacman >/dev/null 2>&1; then
        # Arch Linux
        sudo pacman -S --noconfirm "$package"
    elif command -v dnf >/dev/null 2>&1; then
        # Fedora/RHEL
        sudo dnf install -y "$package"
    else
        echo -e "${RED}❌ Unsupported package manager${NC}"
        return 1
    fi
}

# Check operating system
echo "🔍 Detecting system..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_NAME=$NAME
    OS_ID=$ID
    echo -e "  Detected: $OS_NAME ($OS_ID)"
else
    echo -e "${YELLOW}  ⚠️ Could not detect OS, assuming Linux${NC}"
    OS_ID="linux"
fi

# Check Python
echo ""
echo "🐍 Checking Python..."
if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "  Version: $PYTHON_VERSION"
else
    echo -e "${RED}❌ Python 3 is required${NC}"
    exit 1
fi

# Check Git
echo ""
echo "📚 Checking Git..."
if ! check_command git; then
    echo -e "${YELLOW}Installing Git...${NC}"
    install_package git "Git"
fi

GIT_VERSION=$(git --version 2>&1 | cut -d' ' -f3)
echo -e "  Version: $GIT_VERSION"

# Check GitHub CLI
echo ""
echo "🐙 Checking GitHub CLI..."
if ! check_command gh; then
    echo -e "${YELLOW}Installing GitHub CLI...${NC}"

    if [ "$OS_ID" = "ubuntu" ] || [ "$OS_ID" = "debian" ]; then
        install_package curl "curl"
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg >/dev/null 2>&1
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null >/dev/null 2>&1
        sudo apt update
        sudo apt install gh -y
    elif [ "$OS_ID" = "arch" ]; then
        install_package github-cli "GitHub CLI"
    else
        echo -e "${RED}❌ Please install GitHub CLI manually for your OS${NC}"
        echo "  Visit: https://cli.github.com/"
        exit 1
    fi
fi

GH_VERSION=$(gh --version 2>&1 | head -1 | cut -d' ' -f3)
echo -e "  Version: $GH_VERSION"

# Setup Python virtual environment
echo ""
echo "🔧 Setting up Python environment..."
cd "$PROJECT_ROOT"

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

echo -e "${YELLOW}Activating virtual environment and installing dependencies...${NC}"
source venv/bin/activate

pip install --upgrade pip
pip install pydantic requests pyyaml

# Create required directories
echo ""
echo "📁 Creating project structure..."
mkdir -p "$PROJECT_ROOT/opencode-integration-manager/config"
mkdir -p "$PROJECT_ROOT/opencode-integration-manager/logs"

# Setup Git hooks for automation
echo ""
echo "🔗 Setting up Git hooks..."
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
if [ -d "$HOOKS_DIR" ]; then
    # Create post-commit hook for automatic integration
    cat > "$HOOKS_DIR/post-commit" << 'EOF'
#!/bin/bash
#
# Post-commit hook for OpenCode integration
# Automatically triggers integration when commits are made to integration branches
#

BRANCH=$(git branch --show-current)

if [[ $BRANCH == integration/opencode* ]] || [[ $BRANCH == feature/opencode* ]]; then
    echo "🔄 Detected OpenCode integration commit"
    echo "🚀 Triggering integration workflow..."

    # Trigger GitHub Actions workflow
    if command -v gh >/dev/null 2>&1; then
        gh workflow run opencode-integration.yml
        echo "✅ Integration workflow triggered"
    else
        echo "⚠️ GitHub CLI not available, manual trigger required"
    fi
fi
EOF

    chmod +x "$HOOKS_DIR/post-commit"
    echo -e "  ✅ Post-commit hook configured"
else
    echo -e "  ⚠️ Git hooks directory not found (not a git repository?)"
fi

# Validate configuration
echo ""
echo "🔍 Validating configuration..."
CONFIG_FILE="$PROJECT_ROOT/opencode-integration-manager/config/opencode_config.json"
if [ -f "$CONFIG_FILE" ]; then
    echo -e "  ✅ Configuration file exists"

    # Validate JSON
    if python3 -m json.tool "$CONFIG_FILE" >/dev/null 2>&1; then
        echo -e "  ✅ Configuration is valid JSON"
    else
        echo -e "  ❌ Configuration file is not valid JSON"
    fi
else
    echo -e "  ❌ Configuration file missing: $CONFIG_FILE"
    echo -e "  Run setup again after creating the config file"
fi

# Final instructions
echo ""
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""
echo "🎯 Next steps:"
echo "1. Authenticate with GitHub:"
echo "   gh auth login"
echo ""
echo "2. Configure GitHub token in repository secrets:"
echo "   - Go to repository Settings > Secrets and variables > Actions"
echo "   - Add GITHUB_TOKEN secret"
echo ""
echo "3. Run integration:"
echo "   cd opencode-integration-manager"
echo "   python scripts/run_integration.py --target-repo https://github.com/opencode-ai/opencode --changes-dir ../types"
echo ""
echo "4. Monitor the GitHub Actions workflow for progress"
echo ""
echo -e "${BLUE}📚 For more information, see OPENCODE_PR_README.md${NC}"