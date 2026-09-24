"""
Script to merge existing official exam and TD subjects with their corresponding solutions.
Inserts a clean, professional separator page between the subject and the correction.
"""
import os
import sys
import pypdf
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"c:\Users\swann\Desktop\Proejt gravity\Site 2026-2027")
EXAMS_DIR = BASE_DIR / "courses_data" / "EXAMENS_ANNALES"
SEPARATOR_PATH = BASE_DIR / "scripts" / "separator_page.pdf"

def create_separator_page(title="CORRECTION OFFICIELLE & DÉTAILLÉE", subtitle="ESME Sudria • Cycle Ingénieur Spé"):
    SEPARATOR_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(SEPARATOR_PATH), pagesize=A4, topMargin=180, bottomMargin=180, leftMargin=50, rightMargin=50)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'SeparatorTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=1, # Center
        textColor=colors.HexColor('#1E1B4B')
    )
    
    sub_style = ParagraphStyle(
        'SeparatorSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#4F46E5')
    )

    badge_style = ParagraphStyle(
        'SeparatorBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#059669')
    )

    story = [
        Spacer(1, 100),
        Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", sub_style),
        Spacer(1, 15),
        Paragraph(title, title_style),
        Spacer(1, 15),
        Paragraph(subtitle, sub_style),
        Spacer(1, 10),
        Paragraph("✔ DÉMONSTRATIONS & RÉPONSES VÉRIFIÉES", badge_style),
        Spacer(1, 15),
        Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", sub_style)
    ]
    doc.build(story)

def merge_pdf_pair(subject_path, solution_path, output_path=None, custom_separator_title=None):
    if not output_path:
        output_path = subject_path
        
    s_path = Path(subject_path)
    sol_path = Path(solution_path)
    
    if not s_path.exists() or not sol_path.exists():
        print(f"Erreur : fichier introuvable ({s_path} ou {sol_path})")
        return False
        
    # Create separator
    sep_title = custom_separator_title or "CORRECTION OFFICIELLE ET DÉTAILLÉE"
    create_separator_page(title=sep_title, subtitle="À la suite du sujet • ESME Spé (S03)")
    
    writer = pypdf.PdfWriter()
    
    # 1. Add Subject pages
    with open(s_path, "rb") as f_subj:
        r_subj = pypdf.PdfReader(f_subj)
        for page in r_subj.pages:
            writer.add_page(page)
            
    # 2. Add Separator page
    with open(SEPARATOR_PATH, "rb") as f_sep:
        r_sep = pypdf.PdfReader(f_sep)
        writer.add_page(r_sep.pages[0])
        
    # 3. Add Solution pages
    with open(sol_path, "rb") as f_sol:
        r_sol = pypdf.PdfReader(f_sol)
        for page in r_sol.pages:
            writer.add_page(page)
            
    temp_out = s_path.parent / (s_path.stem + "_temp_merged.pdf")
    with open(temp_out, "wb") as f_out:
        writer.write(f_out)
        
    # Replace original subject file with merged version
    temp_out.replace(output_path)
    print(f"✔ Fusion réussie pour : {s_path.name} (Total: {len(writer.pages)} pages)")
    return True

def main():
    print("=== FUSION DES PAIRES SUJET + CORRIGE EXISTANTES ===")
    
    # Pair 1: Outils Maths Midterms 2024-2025
    subj_om = EXAMS_DIR / "2024-2025 midterms outils maths.pdf"
    sol_om = EXAMS_DIR / "2024-2025 correction midterms Outils maths spé.pdf"
    merge_pdf_pair(subj_om, sol_om, custom_separator_title="CORRECTION OFFICIELLE : OUTILS MATHS SPÉ")

    # Pair 2: Electronique Analogique 1 MidTerm 2025-2026
    subj_ea1 = EXAMS_DIR / "EA1-MidTerm-2025-2026-FR.pdf"
    sol_ea1 = EXAMS_DIR / "EA1-MidTerm-2025-2026-FR-bonnes-réponses.pdf"
    merge_pdf_pair(subj_ea1, sol_ea1, custom_separator_title="BONNES RÉPONSES & CORRECTION : ÉLECTRONIQUE ANALOGIQUE 1")

    # Pair 3: Meca Fluide / Spé Midterms 24-25
    subj_meca = EXAMS_DIR / "SPE_MIDTERMS_SP3_FR_2425 (version2).pdf"
    sol_meca = EXAMS_DIR / "Méca_Fluide_MidTerms_CorrectionV1.pdf"
    merge_pdf_pair(subj_meca, sol_meca, custom_separator_title="CORRECTION OFFICIELLE COMPLÈTE : MÉCANIQUE DES FLUIDES")

    # Pair 4: Signaux et Systèmes Annales (in SIGNAUXSYS folder)
    sig_dir = BASE_DIR / "courses_data" / "SIGNAUXSYS" / "Cours_26-27_Signaux_et_systme..._.79432" / "Dossier_Annales_.79437" / "content"
    if sig_dir.exists():
        # Examen 2025-2026
        s_sig1 = sig_dir / "2025-2026-Examen.pdf"
        sol_sig1 = sig_dir / "2025-2026-Examen-Réponses.pdf"
        if s_sig1.exists() and sol_sig1.exists():
            merge_pdf_pair(s_sig1, sol_sig1, custom_separator_title="CORRIGÉ OFFICIEL : EXAMEN SIGNAUX ET SYSTÈMES 2025-2026")
            
        # Midterm 2024-2025
        s_sig2 = sig_dir / "Midterm-2024-2025.pdf"
        sol_sig2 = sig_dir / "MidtermBis-2024-2025-Barème-Corrigé.pdf"
        if s_sig2.exists() and sol_sig2.exists():
            merge_pdf_pair(s_sig2, sol_sig2, custom_separator_title="CORRIGÉ & BARÈME : MIDTERM SIGNAUX ET SYSTÈMES")
            
        # Test rentrée 2025-2026
        s_sig3 = sig_dir / "Test-rentrée-2025-2026.pdf"
        sol_sig3 = sig_dir / "Test-Rentrée-2025-2026-Réponses-Barème.pdf"
        if s_sig3.exists() and sol_sig3.exists():
            merge_pdf_pair(s_sig3, sol_sig3, custom_separator_title="CORRIGÉ & BARÈME : TEST DE RENTRÉE SIGNAUX")

        # Test rentrée 2024-2025
        s_sig4 = sig_dir / "Test-rentrée-2024-2025.pdf"
        sol_sig4 = sig_dir / "Test_rentrée_2024_2025_Réponse.pdf"
        if s_sig4.exists() and sol_sig4.exists():
            merge_pdf_pair(s_sig4, sol_sig4, custom_separator_title="CORRIGÉ : TEST DE RENTRÉE 2024-2025")

    # Pair 5: Systèmes Technologiques 3 (TD1)
    systech_dir = BASE_DIR / "courses_data" / "SYSTECH3" / "Cours_26-27_Systmes_technique..._.80052"
    if systech_dir.exists():
        for td1_folder in systech_dir.glob("Fichier_TD1_.*"):
            td1_file = td1_folder / "content" / "td 01.pdf"
            if not td1_file.exists():
                candidates = list((td1_folder / "content").glob("*.pdf"))
                td1_file = candidates[0] if candidates else None
                
            corr_folders = list(systech_dir.glob("Fichier_TD1_Corrig_.*"))
            if td1_file and corr_folders:
                corr_file = list((corr_folders[0] / "content").glob("*.pdf"))
                if corr_file:
                    merge_pdf_pair(td1_file, corr_file[0], custom_separator_title="CORRIGÉ OFFICIEL : TD 01 SYSTÈMES TECHNOLOGIQUES")
                    break

    print("\n✔ Fusions de premier niveau terminées avec succès.")

if __name__ == "__main__":
    main()
