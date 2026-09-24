@echo off
title Mise en ligne GitHub - ESME Spe S03
cd /d "%~dp0"
echo ========================================================
echo   Mise en ligne du site sur GitHub (arture463)
echo ========================================================
echo.
echo Envoi en cours vers https://github.com/arture463/esme-spe-2026.git ...
echo (Si GitHub vous demande de vous connecter, validez dans votre navigateur)
echo.
git push -u origin main
echo.
echo ========================================================
if %ERRORLEVEL% equ 0 (
    echo   SUCCES TOTAL : Votre site est en ligne sur GitHub !
    echo.
    echo   Pour activer le lien web de vos amis :
    echo   1. Allez sur https://github.com/arture463/esme-spe-2026/settings/pages
    echo   2. Sous "Branch", choisissez "main" et "/ (root)", puis cliquez sur "Save"
    echo   3. Votre lien sera : https://arture463.github.io/esme-spe-2026/
) else (
    echo   Une erreur s'est produite lors de l'authentification Git.
)
echo ========================================================
pause
