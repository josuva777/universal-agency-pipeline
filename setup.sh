#!/usr/bin/env bash
# Universal Agency Pipeline - Setup Script (macOS / Linux)
# Installs uv, Python 3.13, MemPalace, Headroom, and links MCP configs for all AI agents.

set -e

echo "=========================================================="
echo "   Universal Agency Pipeline - Multi-Agent Auto-Setup    "
echo "=========================================================="

# 1. Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "[1/5] Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

# 2. Python 3.13 via uv
echo "[2/5] Installing Python 3.13 via uv..."
uv python install 3.13

# 3. MemPalace & Headroom
echo "[3/5] Installing MemPalace & Headroom..."
uv tool install mempalace --upgrade
uv tool install --python 3.13 "headroom-ai[mcp]" --upgrade

# 4. Check GitHub Token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "[!] GITHUB_TOKEN not detected in environment."
    echo "    Add 'export GITHUB_TOKEN=ghp_...' to your ~/.bashrc or ~/.zshrc."
fi

# 5. Link Configs
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Antigravity
mkdir -p "$HOME/.gemini/config/skills"
cp "$SCRIPT_DIR/configs/antigravity/mcp_config.json" "$HOME/.gemini/config/mcp_config.json"
cp "$SCRIPT_DIR/AGENTS.md" "$HOME/.gemini/config/AGENTS.md"
cp -r "$SCRIPT_DIR/skills/"* "$HOME/.gemini/config/skills/"
echo " -> Antigravity: Configured!"

# Claude Desktop (macOS)
if [ -d "$HOME/Library/Application Support/Claude" ]; then
    cp "$SCRIPT_DIR/configs/claude-desktop/claude_desktop_config.json" "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    echo " -> Claude Desktop: Configured!"
fi

# Cursor
if [ -d "$HOME/.cursor" ]; then
    cp "$SCRIPT_DIR/configs/cursor/mcp.json" "$HOME/.cursor/mcp.json"
    echo " -> Cursor: Configured!"
fi

# Windsurf
if [ -d "$HOME/.codeium/windsurf" ]; then
    cp "$SCRIPT_DIR/configs/windsurf/mcp_config.json" "$HOME/.codeium/windsurf/mcp_config.json"
    echo " -> Windsurf: Configured!"
fi

echo "=========================================================="
echo "  Setup Complete! All AI Agents are Connected and Ready!  "
echo "=========================================================="
