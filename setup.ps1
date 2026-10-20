param(
    [switch]$DryRun,
    [switch]$Force
)

# Universal Agency Pipeline - Enterprise Auto-Setup Script (Windows PowerShell)
# Installs Python 3.13 via uv, MemPalace, Headroom, and safely merges MCP configs across all AI agents.

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Universal Agency Pipeline - Enterprise Multi-Agent Setup" -ForegroundColor Yellow
if ($DryRun) {
    Write-Host "   [DRY-RUN MODE ACTIVATED: No files will be modified]   " -ForegroundColor Magenta
}
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check or install uv package manager
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    if ($DryRun) {
        Write-Host " [DRY-RUN] Would install uv package manager" -ForegroundColor Cyan
    } else {
        Write-Host "[1/5] Installing uv package manager..." -ForegroundColor Yellow
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        $env:Path = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;" + $env:Path
    }
} else {
    Write-Host "[1/5] uv package manager detected." -ForegroundColor Green
}

# 2. Install isolated Python 3.13 runtime via uv
if ($DryRun) {
    Write-Host " [DRY-RUN] Would verify/install Python 3.13 via uv" -ForegroundColor Cyan
} else {
    Write-Host "[2/5] Installing isolated Python 3.13 runtime via uv..." -ForegroundColor Yellow
    uv python install 3.13
}

# 3. Install MemPalace & Headroom MCP tools
if ($DryRun) {
    Write-Host " [DRY-RUN] Would verify/install MemPalace & Headroom AI MCP tools" -ForegroundColor Cyan
} else {
    Write-Host "[3/5] Installing MemPalace & Headroom AI memory & token compressor..." -ForegroundColor Yellow
    uv tool install mempalace --upgrade
    uv tool install --python 3.13 "headroom-ai[mcp]" --upgrade
}

# 4. Optional GitHub Token Configuration (Masked & Non-Exposed)
$existingToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if ([string]::IsNullOrWhiteSpace($existingToken)) {
    Write-Host "`n[4/5] GitHub MCP Integration (Optional)" -ForegroundColor Yellow
    Write-Host "GitHub integration enables automatic PR creation and issue tracking." -ForegroundColor Gray
    $setupGh = Read-Host "Would you like to configure a GitHub Token now? [y/N]"
    if ($setupGh -match "^[Yy]") {
        Write-Host "Enter your GitHub Token (input will be masked):" -ForegroundColor Cyan
        $secureToken = Read-Host -AsSecureString
        $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
        $token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

        if (-not [string]::IsNullOrWhiteSpace($token)) {
            $token = $token.Trim()
            [System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $token, "User")
            [System.Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", $token, "User")
            $env:GITHUB_TOKEN = $token
            Write-Host "[OK] GITHUB_TOKEN configured securely in User environment." -ForegroundColor Green
        }
    } else {
        Write-Host "[OK] Skipping GitHub token setup (can be configured later)." -ForegroundColor Gray
    }
} else {
    Write-Host "[4/5] GITHUB_TOKEN already configured." -ForegroundColor Green
}

# 5. Non-Destructive JSON Merge Function for MCP Configs
function Merge-McpConfig {
    param (
        [string]$SourceFile,
        [string]$DestFile,
        [string]$ClientName
    )

    if (-not (Test-Path $SourceFile)) { return }

    if ($DryRun) {
        Write-Host " [DRY-RUN] Would merge $ClientName MCP configuration: $SourceFile -> $DestFile" -ForegroundColor Cyan
        return
    }

    $destDir = Split-Path -Parent $DestFile
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    if (-not (Test-Path $DestFile)) {
        # Brand new installation
        Copy-Item $SourceFile $DestFile -Force
        Write-Host " -> ${ClientName}: Installed fresh configuration!" -ForegroundColor Green
        return
    }

    try {
        # Safe merge without destroying existing user tools
        $sourceContent = Get-Content $SourceFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $destContent = Get-Content $DestFile -Raw -Encoding UTF8 | ConvertFrom-Json

        if (-not $destContent.mcpServers) {
            $destContent | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value ([PSCustomObject]@{}) -Force
        }

        # Backup existing file with timestamp
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupPath = "$DestFile.bak_$timestamp"
        Copy-Item $DestFile $backupPath -Force

        # Merge server entries
        $addedCount = 0
        foreach ($serverProp in $sourceContent.mcpServers.PSObject.Properties) {
            $serverName = $serverProp.Name
            $serverVal = $serverProp.Value
            if (-not ($destContent.mcpServers.PSObject.Properties | Where-Object { $_.Name -eq $serverName })) {
                $destContent.mcpServers | Add-Member -MemberType NoteProperty -Name $serverName -Value $serverVal
                $addedCount++
            }
        }

        $destContent | ConvertTo-Json -Depth 10 | Set-Content $DestFile -Encoding UTF8
        Write-Host " -> ${ClientName}: Merged $addedCount new MCP servers safely (Backup: $backupPath)!" -ForegroundColor Green
    } catch {
        Write-Host " -> ${ClientName}: Warning: Failed to merge JSON ($($_)). Preserving existing configuration." -ForegroundColor Yellow
    }
}

# 6. Configure All 6 Supported AI Clients Safely
Write-Host "`n[5/5] Safely configuring AI Clients..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Antigravity
$antigravityDir = "$env:USERPROFILE\.gemini\config"
if ($DryRun) {
    Write-Host " [DRY-RUN] Would safely configure Antigravity, AGENTS.md, and skills" -ForegroundColor Cyan
} else {
    Merge-McpConfig "$scriptDir\configs\antigravity\mcp_config.json" "$antigravityDir\mcp_config.json" "Antigravity"
    
    # Safe AGENTS.md backup before copying
    if (Test-Path "$antigravityDir\AGENTS.md") {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Copy-Item "$antigravityDir\AGENTS.md" "$antigravityDir\AGENTS.md.bak_$timestamp" -Force
    }
    Copy-Item "$scriptDir\AGENTS.md" "$antigravityDir\AGENTS.md" -Force
    
    if (-not (Test-Path "$antigravityDir\skills")) { New-Item -ItemType Directory -Path "$antigravityDir\skills" -Force | Out-Null }
    Copy-Item "$scriptDir\skills\*" "$antigravityDir\skills\" -Recurse -Force
}

# 2. Claude Desktop
$claudeDesktopFile = "$env:APPDATA\Claude\claude_desktop_config.json"
Merge-McpConfig "$scriptDir\configs\claude-desktop\claude_desktop_config.json" $claudeDesktopFile "Claude Desktop"

# 3. Cursor
$cursorFile = "$env:USERPROFILE\.cursor\mcp.json"
Merge-McpConfig "$scriptDir\configs\cursor\mcp.json" $cursorFile "Cursor"

# 4. Windsurf
$windsurfFile = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
Merge-McpConfig "$scriptDir\configs\windsurf\mcp_config.json" $windsurfFile "Windsurf"

# 5. Claude Code CLI
$claudeCodeFile = "$env:USERPROFILE\.claude.json"
Merge-McpConfig "$scriptDir\configs\claude-code\mcp_config.json" $claudeCodeFile "Claude Code CLI"

# 6. VS Code / Cline / Roo Code
$vscodeFile = "$env:USERPROFILE\.vscode\mcp.json"
Merge-McpConfig "$scriptDir\configs\vscode\mcp.json" $vscodeFile "VS Code"

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Setup Complete! All AI Agents Connected with Safe Merge! " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
