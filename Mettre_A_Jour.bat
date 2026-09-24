@echo off
title Mise a jour du Portail ESME Spe
cd /d "%~dp0"
echo ========================================================
echo   Mise a jour automatique du Portail ESME Spe
echo ========================================================
echo Scan et generation de l'index des cours...
python build_master_index.py
echo.
echo ========================================================
echo   MISE A JOUR REUSSIE !
echo   Vous pouvez rafraichir votre navigateur (F5).
echo ========================================================
pause
