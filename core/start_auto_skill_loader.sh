#!/bin/bash
# Auto Skill Loader Startup Script
# This script starts the MCP server for autonomous skill loading in OpenCode

echo "Starting Auto Skill Loader MCP Server..."
echo "This server enables automatic skill activation without @ mentions"
echo ""

cd "$(dirname "$0")"

# Check if fastmcp is available
if ! command -v ~/.local/bin/fastmcp &> /dev/null; then
    echo "Error: fastmcp not found. Please install it with: pipx install fastmcp"
    exit 1
fi

# Check if auto_skill_loader.py exists
if [ ! -f "auto_skill_loader.py" ]; then
    echo "Error: auto_skill_loader.py not found in current directory"
    exit 1
fi

echo "Server will be available at http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the server"
echo ""

~/.local/bin/fastmcp run auto_skill_loader.py