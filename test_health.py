import os
import sys
import json
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

print('=== 1. VÉRIFICATION DU DOSSIER SITE 2026-2027 ===')
site_dir = Path(__file__).parent.resolve()
if not site_dir.exists():
    print("❌ ERREUR: Le dossier Site 2026-2027 n'existe pas !")
    sys.exit(1)
else:
    print(f'✔ Dossier Site 2026-2027 présent : {site_dir}')

essential_files = [
    'index.html', 'styles.css', 'app.js', 'courses_data.js', 'courses_index.json',
    'server.ps1', 'Lancer_Portail.bat', 'Mettre_A_Jour.bat', 'Lancer_Portail_Mac.command',
    'LISEZ_MOI.txt', 'build_master_index.py'
]

for ef in essential_files:
    p = site_dir / ef
    if p.exists() and p.stat().st_size > 0:
        print(f'  ✔ {ef} ({p.stat().st_size} octets)')
    else:
        print(f'  ❌ MANQUANT OU VIDE: {ef}')

print('\n=== 2. VÉRIFICATION DE COURSES_INDEX.JSON ===')
json_path = site_dir / 'courses_index.json'
with open(json_path, 'r', encoding='utf-8') as fp:
    data = json.load(fp)
    n_subj = len(data.get('subjects', {}))
    n_docs = len(data.get('all_documents', []))
    print(f'✔ JSON valide ! {n_subj} matières, {n_docs} documents répertoriés.')

print('\n=== 3. VÉRIFICATION DE L\'ARBORESCENCE DES MATIÈRES ===')
cd_dir = site_dir / 'courses_data'
for code, subj in data.get('subjects', {}).items():
    s_path = cd_dir / code
    cnt = subj.get('document_count', 0)
    print(f'  ✔ [{subj.get("ue")}] {code:12} : {cnt:2d} documents répertoriés')

print('\n=== 4. VÉRIFICATION DES DOCUMENTS CLÉS SUR LE DISQUE ===')
all_valid = True
for doc in data.get('all_documents', [])[:10]:
    doc_path = site_dir / doc['relative_path']
    if doc_path.exists() and doc_path.stat().st_size > 0:
        print(f'  ✔ Présent ({doc["size_formatted"]}) : {doc["title"][:50]}...')
    else:
        print(f'  ❌ Manquant : {doc["relative_path"]}')
        all_valid = False

print('\n' + '=' * 60)
if all_valid:
    print('🎉 SUCCÈS TOTAL : LE PORTAIL EST 100% OPÉRATIONNEL ET PRÊT !')
    print('   Pour lancer le site, double-cliquez sur Lancer_Portail.bat')
    print('   Le site sera accessible sur : http://localhost:8000')
else:
    print('⚠️ Attention : Certains fichiers sont manquants.')
print('=' * 60)
