import os
import sys
from pathlib import Path
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"c:\Users\swann\Desktop\Proejt gravity\Site 2026-2027")
TEMP_DIR = BASE_DIR / "scripts" / "temp_solutions"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def create_separator(title, subtitle, out_path):
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'SepTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=15
    )
    sub_style = ParagraphStyle(
        'SepSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=25
    )
    badge_style = ParagraphStyle(
        'SepBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#166534'),
        alignment=1,
        spaceAfter=15
    )
    note_style = ParagraphStyle(
        'SepNote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    )
    
    story = [
        Spacer(1, 150),
        HRFlowable(width="80%", thickness=3, color=colors.HexColor('#2563eb'), spaceBefore=20, spaceAfter=25),
        Paragraph(title, title_style),
        Paragraph(subtitle, sub_style),
        Paragraph("✔ CORRECTION OFFICIELLE INTÉGRÉE", badge_style),
        HRFlowable(width="50%", thickness=1, color=colors.HexColor('#94a3b8'), spaceBefore=10, spaceAfter=20),
        Paragraph("Le document original se termine ci-dessus. La correction complète et détaillée de l'enseignant est présentée ci-après.", note_style),
        Spacer(1, 150)
    ]
    doc.build(story)

def merge_pdf_with_sep(subject_path, corrig_path, sep_title, sep_sub):
    sep_pdf = TEMP_DIR / f"sep_{subject_path.stem}.pdf"
    create_separator(sep_title, sep_sub, sep_pdf)
    
    writer = pypdf.PdfWriter()
    with open(subject_path, 'rb') as f_subj, open(sep_pdf, 'rb') as f_sep, open(corrig_path, 'rb') as f_corr:
        r_subj = pypdf.PdfReader(f_subj)
        r_sep = pypdf.PdfReader(f_sep)
        r_corr = pypdf.PdfReader(f_corr)
        
        # Check if already merged (look for CORRECTION in last pages)
        is_already_merged = False
        for p in r_subj.pages[-3:]:
            txt = (p.extract_text() or '').upper()
            if "CORRECTION OFFICIELLE" in txt or "CORRIGÉ" in txt:
                is_already_merged = True
                break
        if is_already_merged:
            print(f"  ⏭ Déjà fusionné : {subject_path.name}")
            return
            
        for p in r_subj.pages:
            writer.add_page(p)
        for p in r_sep.pages:
            writer.add_page(p)
        for p in r_corr.pages:
            writer.add_page(p)
            
        temp_out = subject_path.parent / "temp_merged.pdf"
        with open(temp_out, 'wb') as f_out:
            writer.write(f_out)
            
    temp_out.replace(subject_path)
    print(f"  ✔ Fusionné : {subject_path.name} ({len(writer.pages)} pages au total)")

def main():
    systech_dir = BASE_DIR / "courses_data" / "SYSTECH3"
    print("=== FUSION DES CORRIGÉS OFFICIELS SYSTÈMES TECHNIQUES (SYSTECH3) ===")
    
    # Map of TD pairs: (subject pattern, corrigé pattern, title, subtitle)
    td_pairs = [
        ("td_01 2.pdf", "td_01_corrige (1).pdf", "TD 1 : Modélisation des Systèmes", "Systèmes Linéaires Continus Invariants"),
        ("td_02 1.pdf", "td_02_corrige (1).pdf", "TD 2 : Caractérisation Temporelle & Fonctions de Transfert", "Systèmes du 1er et 2nd ordre"),
        ("td_03 (1).pdf", "td_03_corrige.pdf", "TD 3 : Systèmes Linéaires et Réduction de Schémas Fonctionnels", "Schémas blocs et transmittance"),
        ("td_04.pdf", "td_04_corrige.pdf", "TD 4 : Stabilité, Rapidité et Précision des Systèmes", "Performances en boucle fermée"),
        ("td_07.pdf", "td_07_corrige.pdf", "TD 7 : Modélisation et Schémas-Blocs Approfondis", "Automatismes industriels"),
        ("td_08.pdf", "td_08_corrige.pdf", "TD 8 : Identification & Réponses Temporelles", "Modèles de Strejc, Broida et réponses fréquentielles")
    ]
    
    # Locate all corrigés first
    corriges_map = {}
    for f in systech_dir.rglob("*.pdf"):
        for subj_name, corr_name, title, sub in td_pairs:
            if f.name.lower() == corr_name.lower():
                corriges_map[corr_name] = f
                break
                
    print(f"Trouvé {len(corriges_map)} fichiers de corrigés de référence.")
    for k, v in corriges_map.items():
        print(f"  - {k} -> {v.relative_to(systech_dir)}")
        
    # Now merge each subject
    for f in systech_dir.rglob("*.pdf"):
        for subj_name, corr_name, title, sub in td_pairs:
            if f.name.lower() == subj_name.lower():
                if corr_name in corriges_map:
                    corr_file = corriges_map[corr_name]
                    print(f"Traitement de {f.name} dans {f.parent.name}...")
                    merge_pdf_with_sep(f, corr_file, title, sub)

if __name__ == "__main__":
    main()
