import os, sys, json, shutil
from pathlib import Path
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = Path(r"C:\Users\swann\Documents\Proejt gravity\Site 2026-2027")
COURSES_DIR = PROJECT_DIR / "courses_data"

print("=== 1. NETTOYAGE DES DOUBLONS ET FICHIERS ÉGARÉS SUR LE DISQUE ===")

# 1.1 Supprimer SYSTECH3/TD (contenant le TD ANANUM égaré)
st_td = COURSES_DIR / "SYSTECH3" / "TD"
if st_td.exists():
    shutil.rmtree(st_td)
    print("  ✔ Supprimé : SYSTECH3/TD (dossier égaré)")

# 1.2 Supprimer les corrigés isolés déjà fusionnés dans EXAMENS_ANNALES
exam_dir = COURSES_DIR / "EXAMENS_ANNALES"
redundant_exams = [
    "2024-2025 correction midterms Outils maths spé.pdf",
    "EA1-MidTerm-2025-2026-FR-bonnes-réponses.pdf",
    "Méca_Fluide_MidTerms_CorrectionV1.pdf"
]
for f in redundant_exams:
    p = exam_dir / f
    if p.exists():
        p.unlink()
        print(f"  ✔ Supprimé corrigé isolé (déjà fusionné) : {f}")

# 1.3 Supprimer les corrigés isolés déjà fusionnés dans SIGNAUXSYS annales
sig_annales = COURSES_DIR / "SIGNAUXSYS" / "Cours_26-27_Signaux_et_systme..._.79432" / "Dossier_Annales_.79437" / "content"
redundant_sig = [
    "2025-2026-Examen-Réponses.pdf",
    "MidtermBis-2024-2025-Barème-Corrigé.pdf",
    "Test-Rentrée-2025-2026-Réponses-Barème.pdf",
    "Test_rentrée_2024_2025_Réponse.pdf"
]
for f in redundant_sig:
    p = sig_annales / f
    if p.exists():
        p.unlink()
        print(f"  ✔ Supprimé corrigé isolé (déjà fusionné) dans Signaux : {f}")

# 1.4 Supprimer les doublons de partiel dans ENJEUXENV1 (conserver une seule version de EE1_Exam_2024-2025_VF.pdf)
ee1_dir = COURSES_DIR / "ENJEUXENV1"
ee1_partiels = list(ee1_dir.rglob("EE1_Exam_2024-2025_VF.pdf"))
if len(ee1_partiels) > 1:
    # Keep the largest (which has the merged correction) and delete duplicates
    ee1_partiels.sort(key=lambda x: x.stat().st_size, reverse=True)
    for dup in ee1_partiels[1:]:
        dup.unlink()
        print(f"  ✔ Supprimé doublon partiel EE1 : {dup.parent.name}")

# 1.5 Supprimer les corrigés isolés déjà fusionnés dans SYSTECH3
redundant_systech = [
    "td_01_corrige (1).pdf", "td_02_corrige (1).pdf", "td_03_corrige.pdf",
    "td_04_corrige.pdf", "td_07_corrige.pdf", "td_08_corrige.pdf"
]
for fname in redundant_systech:
    for f in (COURSES_DIR / "SYSTECH3").rglob(fname):
        f.unlink()
        print(f"  ✔ Supprimé corrigé isolé (déjà fusionné) dans SYSTECH3 : {f.name}")

print("\nNettoyage physique terminé avec succès !")
