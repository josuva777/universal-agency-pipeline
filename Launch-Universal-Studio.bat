@echo off
title Universal Studio Engine — Google AI Studio x Lovable x Cursor
echo ======================================================================
echo    UNIVERSAL STUDIO ENGINE // LIVE WEB WORKSPACE
echo ======================================================================
echo Launching Universal Studio in Google Chrome / Web Browser...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%~dp0studio\index.html"
) else (
    start "" "%~dp0studio\index.html"
)
exit

