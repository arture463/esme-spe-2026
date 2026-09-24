@echo off
title Mise a jour du Portail ESME Spe
cd /d "%~dp0"
echo ========================================================
echo   Mise a jour automatique du Portail ESME Spe
echo ========================================================
echo.
echo 1. Synchronisation avec GitHub (recuperation des cours des camarades)...
git pull origin main
echo.
echo 2. Scan et generation du catalogue de cours...
python build_master_index.py
echo.
echo ========================================================
echo   MISE A JOUR REUSSIE !
echo   Vous pouvez rafraichir votre navigateur (F5).
echo ========================================================
pause
