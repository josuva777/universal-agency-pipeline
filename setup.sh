#!/usr/bin/env bash
# Universal Agency Pipeline - Enterprise Auto-Setup Script (macOS / Linux)
# Installs uv, Python 3.13, MemPalace, Headroom, and safely merges MCP configs across all AI agents.

set -e

echo "=========================================================="
echo "   Universal Agency Pipeline - Enterprise Multi-Agent Setup"
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

# 4. Optional GitHub Token Check
echo "[4/5] Checking GITHUB_TOKEN..."
if [ -z "$GITHUB_TOKEN" ]; then
    echo " -> GITHUB_TOKEN not detected in environment (Optional: add 'export GITHUB_TOKEN=ghp_...' to your ~/.bashrc or ~/.zshrc for GitHub integration)."
else
    echo " -> GITHUB_TOKEN detected in environment."
fi

# 5. Non-Destructive Config Merger
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

merge_mcp_config() {
    local src="$1"
    local dest="$2"
    local client="$3"

    if [ ! -f "$src" ]; then return; fi

    local dest_dir
    dest_dir="$(dirname "$dest")"
    mkdir -p "$dest_dir"

    if [ ! -f "$dest" ]; then
        cp "$src" "$dest"
        echo " -> $client: Fresh configuration installed!"
    else
        local timestamp
        timestamp="$(date +%Y%m%d_%H%M%S)"
        cp "$dest" "${dest}.bak_${timestamp}"
        
        # Merge if python is available, otherwise copy safely
        if command -v python3 &> /dev/null; then
            python3 -c "
import json, sys
try:
    with open('$src') as f: s = json.load(f)
    with open('$dest') as f: d = json.load(f)
    d.setdefault('mcpServers', {})
    for k, v in s.get('mcpServers', {}).items():
        if k not in d['mcpServers']:
            d['mcpServers'][k] = v
    with open('$dest', 'w') as f: json.dump(d, f, indent=2)
except Exception as e:
    sys.exit(1)
" && echo " -> $client: Merged new MCP servers safely (Backup: ${dest}.bak_${timestamp})!" || cp "$src" "$dest"
        else
            cp "$src" "$dest"
        fi
    fi
}

echo "[5/5] Safely configuring AI Clients..."

# Antigravity
mkdir -p "$HOME/.gemini/config/skills"
merge_mcp_config "$SCRIPT_DIR/configs/antigravity/mcp_config.json" "$HOME/.gemini/config/mcp_config.json" "Antigravity"
cp "$SCRIPT_DIR/AGENTS.md" "$HOME/.gemini/config/AGENTS.md"
cp -r "$SCRIPT_DIR/skills/"* "$HOME/.gemini/config/skills/"

# Claude Desktop (macOS)
if [ -d "$HOME/Library/Application Support/Claude" ]; then
    merge_mcp_config "$SCRIPT_DIR/configs/claude-desktop/claude_desktop_config.json" "$HOME/Library/Application Support/Claude/claude_desktop_config.json" "Claude Desktop"
fi

# Cursor
if [ -d "$HOME/.cursor" ]; then
    merge_mcp_config "$SCRIPT_DIR/configs/cursor/mcp.json" "$HOME/.cursor/mcp.json" "Cursor"
fi

# Windsurf
if [ -d "$HOME/.codeium/windsurf" ]; then
    merge_mcp_config "$SCRIPT_DIR/configs/windsurf/mcp_config.json" "$HOME/.codeium/windsurf/mcp_config.json" "Windsurf"
fi

# Claude Code CLI
merge_mcp_config "$SCRIPT_DIR/configs/claude-code/mcp_config.json" "$HOME/.claude.json" "Claude Code CLI"

# VS Code
if [ -d "$HOME/.vscode" ]; then
    merge_mcp_config "$SCRIPT_DIR/configs/vscode/mcp.json" "$HOME/.vscode/mcp.json" "VS Code"
fi

echo "=========================================================="
echo "  Setup Complete! All AI Agents Connected with Safe Merge! "
echo "=========================================================="
