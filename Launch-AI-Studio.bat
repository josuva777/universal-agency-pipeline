@echo off
title AI Studio & Generative Workspace — Live Preview
echo ======================================================================
echo    AI STUDIO & GENERATIVE WORKSPACE // LIVE BROWSER PREVIEW
echo ======================================================================
echo Launching ai_studio_live.html in Google Chrome / Web Browser...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%~dp0ai_studio_live.html"
) else (
    start "" "%~dp0ai_studio_live.html"
)
exit
