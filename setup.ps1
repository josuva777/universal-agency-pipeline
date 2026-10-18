# Universal Agency Pipeline - Setup Script (Windows PowerShell)
# Installs Python 3.13 via uv, MemPalace, Headroom, and links MCP configs for all AI agents.

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Universal Agency Pipeline - Multi-Agent Auto-Setup    " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check or install uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[1/5] Installing uv package manager..." -ForegroundColor Yellow
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;" + $env:Path
} else {
    Write-Host "[1/5] uv package manager detected." -ForegroundColor Green
}

# 2. Install Python 3.13 via uv
Write-Host "[2/5] Installing isolated Python 3.13 runtime via uv..." -ForegroundColor Yellow
uv python install 3.13

# 3. Install MemPalace & Headroom MCP tools
Write-Host "[3/5] Installing MemPalace & Headroom AI memory & token compressor..." -ForegroundColor Yellow
uv tool install mempalace --upgrade
uv tool install --python 3.13 "headroom-ai[mcp]" --upgrade

# 4. Prompt for GitHub Token if missing
$existingToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if ([string]::IsNullOrWhiteSpace($existingToken)) {
    Write-Host "`n[GitHub Token Required]" -ForegroundColor Yellow
    Write-Host "Create a classic token at https://github.com/settings/tokens (scopes: repo, workflow, read:org)"
    $token = Read-Host "Paste your GitHub Token (ghp_...)"
    if (-not [string]::IsNullOrWhiteSpace($token)) {
        $token = $token.Trim()
        [System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $token, "User")
        [System.Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", $token, "User")
        $env:GITHUB_TOKEN = $token
        Write-Host "GITHUB_TOKEN saved to User environment variables." -ForegroundColor Green
    }
} else {
    Write-Host "[4/5] GITHUB_TOKEN already configured." -ForegroundColor Green
}

# 5. Connect configs for installed AI clients
Write-Host "[5/5] Configuring AI clients..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Antigravity
$antigravityDir = "$env:USERPROFILE\.gemini\config"
if (-not (Test-Path $antigravityDir)) { New-Item -ItemType Directory -Path $antigravityDir -Force | Out-Null }
Copy-Item "$scriptDir\configs\antigravity\mcp_config.json" "$antigravityDir\mcp_config.json" -Force
Copy-Item "$scriptDir\AGENTS.md" "$antigravityDir\AGENTS.md" -Force
if (-not (Test-Path "$antigravityDir\skills")) { New-Item -ItemType Directory -Path "$antigravityDir\skills" -Force | Out-Null }
Copy-Item "$scriptDir\skills\*" "$antigravityDir\skills\" -Recurse -Force
Write-Host " -> Antigravity: Configured!" -ForegroundColor Green

# Claude Desktop
$claudeDesktopDir = "$env:APPDATA\Claude"
if (Test-Path $claudeDesktopDir) {
    Copy-Item "$scriptDir\configs\claude-desktop\claude_desktop_config.json" "$claudeDesktopDir\claude_desktop_config.json" -Force
    Write-Host " -> Claude Desktop: Configured!" -ForegroundColor Green
}

# Cursor
$cursorDir = "$env:USERPROFILE\.cursor"
if (Test-Path $cursorDir) {
    Copy-Item "$scriptDir\configs\cursor\mcp.json" "$cursorDir\mcp.json" -Force
    Write-Host " -> Cursor: Configured!" -ForegroundColor Green
}

# Windsurf
$windsurfDir = "$env:USERPROFILE\.codeium\windsurf"
if (Test-Path $windsurfDir) {
    Copy-Item "$scriptDir\configs\windsurf\mcp_config.json" "$windsurfDir\mcp_config.json" -Force
    Write-Host " -> Windsurf: Configured!" -ForegroundColor Green
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Setup Complete! All AI Agents are Connected and Ready!  " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
