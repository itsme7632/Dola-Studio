@echo off
title SDola Studio - Created by Sajid AI
color 0E

echo ==============================================================
echo                 SDOLA STUDIO v1.2.9 PORTABLE
echo                   Created by Sajid AI
echo         WhatsApp: https://whatsapp.com/channel/0029Vb96GhE47Xe6BotLE21r
echo ==============================================================
echo.

:: Set current directory
cd /d "%~dp0"

:: Kill any old/stuck processes to release mutex
echo [*] Closing previous instances...
taskkill /F /IM "SDolaStudio.exe" >nul 2>&1
taskkill /F /IM "ZDolaStudio.exe" >nul 2>&1

:: Set bypass paths
set "BYPASS=%~dp0bypass"
set "PYTHONPATH=%BYPASS%"

:: Launch app
echo [*] Launching SDola Studio with Radiant Yellow Theme...
if exist "%~dp0SDolaStudio.exe" (
    start "" "%~dp0SDolaStudio.exe"
) else (
    start "" "%~dp0ZDolaStudio.exe"
)

echo [*] Application started successfully!
echo [*] Closing launcher window in 3 seconds...
timeout /t 3 /nobreak >nul
exit
