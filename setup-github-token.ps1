# Setup GitHub Personal Access Token (PAT) for GitHub MCP
# Run this script in PowerShell whenever you generate your token.

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         GitHub Personal Access Token (PAT) Setup         " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "How to create your free GitHub PAT (takes 30 seconds):" -ForegroundColor White
Write-Host "1. Go to: https://github.com/settings/tokens" -ForegroundColor Green
Write-Host "2. Click 'Generate new token' -> 'Generate new token (classic)'" -ForegroundColor Green
Write-Host "3. Note: 'Antigravity Agency MCP'" -ForegroundColor Green
Write-Host "4. Select scopes:" -ForegroundColor Green
Write-Host "   [x] repo          (Full control of private repositories)" -ForegroundColor White
Write-Host "   [x] workflow      (Update GitHub Action workflows)" -ForegroundColor White
Write-Host "   [x] read:org      (Read org and team membership)" -ForegroundColor White
Write-Host "5. Click 'Generate token' at the bottom and copy it (starts with ghp_...)" -ForegroundColor Green
Write-Host ""

$token = Read-Host "Paste your GitHub token here"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "`nNo token entered. Setup skipped." -ForegroundColor Red
} else {
    $token = $token.Trim()
    [System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $token, "User")
    $env:GITHUB_TOKEN = $token
    Write-Host "`n[SUCCESS] GITHUB_TOKEN has been saved to your Windows User environment variables!" -ForegroundColor Green
    Write-Host "The GitHub MCP server will now automatically authenticate with this token." -ForegroundColor Cyan
}

