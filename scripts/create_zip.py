import os
import sys
import zipfile
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

SOURCE_DIR = Path(__file__).parent.parent.resolve()
TARGET_ZIP = SOURCE_DIR.parent / "Site 2026-2027.zip"

print(f"📦 Compression du dossier : {SOURCE_DIR} ...")

TEMP_ZIP = SOURCE_DIR.parent / "temp_site.zip"
if TEMP_ZIP.exists():
    TEMP_ZIP.unlink()

excluded_names = {".git", ".DS_Store", "Thumbs.db", "__pycache__"}

with zipfile.ZipFile(TEMP_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for root, dirs, files in os.walk(SOURCE_DIR):
        dirs[:] = [d for d in dirs if d not in excluded_names]
        for f in files:
            if f in excluded_names or f.endswith(".tmp"):
                continue
            full_path = Path(root) / f
            # Arcname relative to parent so inside the zip it starts with 'Site 2026-2027/'
            arc_name = full_path.relative_to(SOURCE_DIR.parent)
            zf.write(full_path, arc_name)

zip_size_mb = TEMP_ZIP.stat().st_size / (1024 * 1024)
print(f"✔ Archive temporaire générée : {zip_size_mb:.1f} Mo")

# Verify the zip
with zipfile.ZipFile(TEMP_ZIP, "r") as zf:
    test_res = zf.testzip()
    if test_res is not None:
        raise RuntimeError(f"Erreur d'intégrité ZIP sur {test_res}")
    print(f"✔ Test d'intégrité ZIP : 100% PARFAIT ({len(zf.namelist())} éléments vérifiés)")

# Copy to targets
TARGET_ZIP.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(TEMP_ZIP, TARGET_ZIP)
print(f"✔ Mis à jour : {TARGET_ZIP} ({zip_size_mb:.1f} Mo)")

# Cleanup temp
TEMP_ZIP.unlink()
print("🎉 Exportation terminée avec succès !")
