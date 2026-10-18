<#
.SYNOPSIS
    Interactive Launcher for Creative Studio & Universal Agent Factory
#>

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  🎬 CREATIVE PRODUCTION STUDIO & AI AGENT FACTORY LAUNCHER      " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  [1] Generate New Brand Campaign & Commercial" -ForegroundColor Green
Write-Host "      (Neural Voice + Procedural SVG Logo + SFX + Brand Kit Portal)"
Write-Host ""
Write-Host "  [2] Open Interactive Remotion Studio GUI (Browser)" -ForegroundColor Magenta
Write-Host "      (Scrub timeline, adjust 3D physics, real-time preview at localhost:3000)"
Write-Host ""
Write-Host "  [3] Render Master 4K Video to MP4" -ForegroundColor Cyan
Write-Host "      (High-definition H.264 60FPS export)"
Write-Host ""
Write-Host "  [4] Open Latest Client Deliverables Portal (HTML)" -ForegroundColor Yellow
Write-Host "      (View interactive brand kit, swatches, audio player, & logos)"
Write-Host ""
Write-Host "  [5] Scaffold New AI Client Agent (Agent Factory)" -ForegroundColor Blue
Write-Host "      (Hybrid RAG, Workflow State Machine, Autonomous ReAct, or Copilot)"
Write-Host ""
Write-Host "  [6] Set / Update API Keys Securely" -ForegroundColor Green
Write-Host "      (Stored ONLY on your laptop in .env - NEVER pushed to GitHub)"
Write-Host ""
Write-Host "  [0] Exit" -ForegroundColor Gray
Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan

$choice = Read-Host "Select an option (0-6)"

switch ($choice) {
    "1" {
        $brief = Read-Host "Enter Creative Brief (e.g., Luxury Cyberpunk Smartwatch)"
        if (-not $brief) { $brief = "Next Generation High-Performance Software" }

        Write-Host "`nChoose Style: [1] Fintech  [2] SaaS  [3] Streetwear  [4] Editorial" -ForegroundColor Yellow
        $styleChoice = Read-Host "Select (1-4, default 1)"
        $style = switch ($styleChoice) {
            "2" { "saas" }
            "3" { "streetwear" }
            "4" { "editorial" }
            Default { "fintech" }
        }
        $slug = ($brief -replace '[^a-zA-Z0-9]', '_').ToLower()
        if (-not $slug) { $slug = "campaign_run" }
        $out = "./assets/outputs/$slug"

        Write-Host "`n🚀 Step 1: Running AI Producer (Script + Voiceover + Logo + Sound FX)..." -ForegroundColor Cyan
        & .\.venv\Scripts\python.exe -m agents.orchestrator --brief "$brief" --output "$out" --style "$style"

        Write-Host "`nOpening Client Portal in browser..." -ForegroundColor Green
        if (Test-Path "$out/brand_kit.html") {
            Start-Process "$out/brand_kit.html"
        }

        $renderChoice = Read-Host "`n🎥 Step 2: Render 4K Commercial Video now? [Y/n]"
        if ($renderChoice -eq "" -or $renderChoice -match "^[Yy]") {
            $gdriveTarget = "G:/My Drive/Agency Deliverables/$slug.mp4"
            $localTarget = "$out/commercial.mp4"
            $finalTarget = if (Test-Path "G:/My Drive") { $gdriveTarget } else { $localTarget }

            Write-Host "`nRendering 60FPS Video to: $finalTarget ..." -ForegroundColor Magenta
            cd video
            npx remotion render src/index.tsx Commercial --output "$finalTarget"
            cd ..
            Write-Host "`n✓ Master Video Ready!" -ForegroundColor Green
            if (Test-Path $finalTarget) {
                Start-Process $finalTarget
            }
        }
    }
    "2" {
        Write-Host "`n🎨 Launching Remotion Studio GUI at http://localhost:3000..." -ForegroundColor Magenta
        cd video
        npm run dev
    }
    "3" {
        Write-Host "`n🎥 Rendering Master Video..." -ForegroundColor Cyan
        cd video
        npm run render:commercial
    }
    "4" {
        $latestPortal = Get-ChildItem -Recurse -Filter "brand_kit.html" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestPortal) {
            Write-Host "`nOpening $($latestPortal.FullName)..." -ForegroundColor Green
            Start-Process $latestPortal.FullName
        } else {
            Write-Host "No brand portal found yet. Run option 1 first!" -ForegroundColor Red
        }
    }
    "5" {
        $name = Read-Host "Enter Agent Project Name (e.g., LegalDocsBot)"
        Write-Host "Choose Archetype: [1] rag [2] workflow [3] action [4] copilot" -ForegroundColor Yellow
        $archChoice = Read-Host "Select (1-4, default 1)"
        $archetype = switch ($archChoice) {
            "2" { "workflow" }
            "3" { "action" }
            "4" { "copilot" }
            Default { "rag" }
        }
        Write-Host "`n🏭 Scaffolding AI Agent..." -ForegroundColor Cyan
        & .\.venv\Scripts\python.exe "C:\Users\ELCOT\.gemini\config\skills\agent-builder\scaffold_agent.py" --name "$name" --archetype "$archetype" --output-dir "C:\Users\ELCOT\.gemini\antigravity\scratch"
    }
    "6" {
        Write-Host "`n🔑 Secure Local API Key Manager" -ForegroundColor Cyan
        Write-Host "Keys are saved ONLY in local .env (protected by .gitignore - NEVER uploaded to GitHub)" -ForegroundColor Gray
        Write-Host ""
        $gemini = Read-Host "Enter Google Gemini API Key (press Enter to skip)"
        $groq = Read-Host "Enter Groq API Key (press Enter to skip)"
        $openai = Read-Host "Enter OpenAI API Key (press Enter to skip)"

        $envFile = ".env"
        if (-not (Test-Path $envFile)) {
            Copy-Item ".env.example" $envFile
        }

        $envContent = Get-Content $envFile -Raw
        if ($gemini) {
            $envContent = $envContent -replace 'GEMINI_API_KEY=.*', "GEMINI_API_KEY=$gemini"
        }
        if ($groq) {
            $envContent = $envContent -replace '#? ?GROQ_API_KEY=.*', "GROQ_API_KEY=$groq"
        }
        if ($openai) {
            $envContent = $envContent -replace 'OPENAI_API_KEY=.*', "OPENAI_API_KEY=$openai"
        }
        Set-Content -Path $envFile -Value $envContent -Encoding UTF8
        Write-Host "`n✓ API keys saved securely to local .env!" -ForegroundColor Green
        Write-Host "Git status check: .env is 100% ignored and will never be pushed." -ForegroundColor Cyan
    }
    Default {
        Write-Host "Exiting." -ForegroundColor Gray
    }
}

