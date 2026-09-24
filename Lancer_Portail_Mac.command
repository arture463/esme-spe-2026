#!/bin/bash
# Script de lancement en 1 clic pour Mac / Linux
cd "$(dirname "$0")"
echo "========================================================"
echo "  Lancement du Portail des Cours ESME Spe sur Mac"
echo "========================================================"
# Ouvre automatiquement le navigateur par defaut sur Mac
open "http://localhost:8000" 2>/dev/null || xdg-open "http://localhost:8000" 2>/dev/null
# Demarre le serveur web local python
python3 -m http.server 8000
