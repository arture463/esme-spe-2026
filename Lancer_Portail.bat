@echo off
title Portail ESME Spe - S03
echo ========================================================
echo   Lancement du Portail des Cours ESME Spe (S03)
echo ========================================================

:: 1. Detection automatique du dossier Site 2026-2027
set "TARGET_DIR="
if exist "%~dp0server.ps1" (
    set "TARGET_DIR=%~dp0"
) else if exist "%~dp0Site 2026-2027\server.ps1" (
    set "TARGET_DIR=%~dp0Site 2026-2027"
) else if exist "%USERPROFILE%\Documents\Proejt gravity\Site 2026-2027\server.ps1" (
    set "TARGET_DIR=%USERPROFILE%\Documents\Proejt gravity\Site 2026-2027"
) else if exist "%USERPROFILE%\Desktop\Proejt gravity\Site 2026-2027\server.ps1" (
    set "TARGET_DIR=%USERPROFILE%\Desktop\Proejt gravity\Site 2026-2027"
)

if "%TARGET_DIR%"=="" (
    echo [ERREUR] Le dossier 'Site 2026-2027' est introuvable.
    echo Verifiez qu'il est bien dans vos Documents ou sur votre Bureau.
    pause
    exit /b 1
)

cd /d "%TARGET_DIR%"
powershell -NoProfile -ExecutionPolicy Bypass -File "server.ps1" -Port 8000
pause
