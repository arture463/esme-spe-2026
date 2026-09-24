import os
import sys
from pathlib import Path
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"c:\Users\swann\Desktop\Proejt gravity\Site 2026-2027")
TEMP_DIR = BASE_DIR / "scripts" / "temp_solutions"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def build_pdf(pdf_out):
    doc = SimpleDocTemplate(
        str(pdf_out),
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    styles = getSampleStyleSheet()
    
    st_title = ParagraphStyle('T', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0f172a'), alignment=1)
    st_sub = ParagraphStyle('S', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#2563eb'), alignment=1)
    st_badge = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#166534'), alignment=1)
    
    st_h1 = ParagraphStyle('H1', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor('#1e3a8a'), spaceBefore=12, spaceAfter=6)
    st_h2 = ParagraphStyle('H2', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#0369a1'), spaceBefore=8, spaceAfter=4)
    st_body = ParagraphStyle('Txt', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#1e293b'), spaceAfter=5)
    st_code = ParagraphStyle('Code', parent=styles['Normal'], fontName='Courier', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#0f172a'), backColor=colors.HexColor('#f1f5f9'), spaceBefore=4, spaceAfter=6, leftIndent=8)

    def boxed(title, html_content):
        p_t = Paragraph(f"<b>{title}</b>", ParagraphStyle('BT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#166534')))
        p_c = Paragraph(html_content, ParagraphStyle('BC', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#0f172a')))
        t = Table([[p_t], [p_c]], colWidths=[540])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#22c55e')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = [
        Spacer(1, 15),
        Paragraph("CORRECTION OFFICIELLE ET ANALYTIQUE RIGOUREUSE", st_title),
        Paragraph("SYSTÈMES TECHNIQUES 3 — TD 9 : MODÉLISATION D'UN MOTEUR À COURANT CONTINU (MCC)", st_sub),
        Paragraph("✔ Modélisation électromécanique, Schémas-blocs Simulink & Régime Permanent", st_badge),
        HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563eb'), spaceBefore=10, spaceAfter=15),
    ]

    # Rappel du modèle
    story.append(Paragraph("1. Modélisation Théorique du Moteur à Courant Continu", st_h1))
    story.append(Paragraph(
        "Le système est régi par le couplage de deux domaines physiques fondamentaux :<br/>"
        "• <b>Équation électrique (Loi des mailles d'induit) :</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;u(t) = R·i(t) + L·(di(t)/dt) + e(t)<br/>"
        "• <b>Équation mécanique (Principe Fondamental de la Dynamique en rotation) :</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;I<sub>eq</sub>·(d&omega;<sub>m</sub>(t)/dt) = c<sub>m</sub>(t) - f·&omega;<sub>m</sub>(t) - c<sub>r</sub>(t)<br/>"
        "• <b>Couplages électromécaniques (Loi de Laplace & Loi de Faraday) :</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;e(t) = K<sub>em</sub>·&omega;<sub>m</sub>(t)&nbsp;&nbsp;et&nbsp;&nbsp;c<sub>m</sub>(t) = K<sub>em</sub>·i(t)",
        st_body
    ))
    story.append(Spacer(1, 6))

    # Tâches 1 & 2
    story.append(Paragraph("2. Résolution des Tâches MATLAB / Simulink", st_h1))
    story.append(Paragraph("<b>Tâche 1 : Déclaration des paramètres physiques du moteur</b>", st_h2))
    code_t1 = (
        "% Paramètres physiques du moteur (issus des essais experimentaux)<br/>"
        "R   = 1.2;               % Resistance d'induit [Ohm]<br/>"
        "L   = 1.5e-3;            % Inductance d'induit [H] (1.5 mH)<br/>"
        "Ieq = 6.0e-5;            % Inertie equivalente [kg.m^2]<br/>"
        "f   = 4.0e-5;            % Coefficient de frottement visqueux [kg.m^2/s]<br/>"
        "Kem = 60e-3;             % Constante de couple et fcem [N.m/A ou V.s/rad]"
    )
    story.append(Paragraph(code_t1, st_code))

    story.append(Paragraph("<b>Tâche 2 : Paramètres canoniques des systèmes du 1er ordre</b>", st_h2))
    story.append(Paragraph(
        "En transformée de Laplace (conditions initiales nulles), on met chaque sous-système sous forme canonique :<br/>"
        "• Circuit électrique : I(s) = [K<sub>e</sub> / (1 + &tau;<sub>e</sub>·s)] · [U(s) - E(s)] avec <b>K<sub>e</sub> = 1/R</b> et <b>&tau;<sub>e</sub> = L/R</b><br/>"
        "• Partie mécanique : &Omega;<sub>m</sub>(s) = [K<sub>m</sub> / (1 + &tau;<sub>m</sub>·s)] · [C<sub>m</sub>(s) - C<sub>r</sub>(s)] avec <b>K<sub>m</sub> = 1/f</b> et <b>&tau;<sub>m</sub> = I<sub>eq</sub>/f</b>",
        st_body
    ))
    code_t2 = (
        "Ke   = 1 / R;             % Gain statique electrique = 1 / 1.2 = 0.8333 A/V<br/>"
        "tau_e= L / R;             % Constante de temps electrique = 1.5e-3 / 1.2 = 1.25 ms<br/>"
        "Km   = 1 / f;             % Gain statique mecanique = 1 / 4e-5 = 25000 (N.m.s)^-1<br/>"
        "tau_m= Ieq / f;           % Constante de temps mecanique = 6e-5 / 4e-5 = 1.5 s"
    )
    story.append(Paragraph(code_t2, st_code))
    story.append(boxed("Valeurs numériques exactes calculées :",
                       "<b>K<sub>e</sub> = 0.8333 A·V<sup>-1</sup></b>&nbsp;&nbsp;|&nbsp;&nbsp;"
                       "<b>&tau;<sub>e</sub> = 1.25·10<sup>-3</sup> s = 1.25 ms</b><br/>"
                       "<b>K<sub>m</sub> = 25 000 (N·m·s)<sup>-1</sup></b>&nbsp;&nbsp;|&nbsp;&nbsp;"
                       "<b>&tau;<sub>m</sub> = 1.50 s</b><br/>"
                       "<i>Remarque physique : &tau;<sub>e</sub> &ll; &tau;<sub>m</sub> (rapport > 1000). La dynamique électrique est ultra-rapide devant l'inertie mécanique.</i>"))
    story.append(Spacer(1, 8))

    # Tâches 4 & 5
    story.append(Paragraph("<b>Tâche 4 & 5 : Simulation temporelle & Vitesse en régime permanent</b>", st_h2))
    story.append(Paragraph(
        "Paramètres du test : Échelon de tension d'entrée <b>U<sub>0</sub> = 12 V</b>, Couple résistant perturbateur <b>C<sub>r</sub> = 10<sup>-2</sup> N·m = 0.01 N·m</b>.<br/>"
        "En régime permanent (t &rarr; &infin;, s &rarr; 0, dérivées nulles) :<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1) u = R·I + e = R·I + K<sub>em</sub>·&Omega;<sub>m</sub><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2) c<sub>m</sub> = K<sub>em</sub>·I = c<sub>r</sub> + f·&Omega;<sub>m</sub> &rArr; I = (C<sub>r</sub> + f·&Omega;<sub>m</sub>) / K<sub>em</sub><br/>"
        "En injectant I dans l'équation de maille :<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;u = (R / K<sub>em</sub>)·(C<sub>r</sub> + f·&Omega;<sub>m</sub>) + K<sub>em</sub>·&Omega;<sub>m</sub> = (R·C<sub>r</sub> / K<sub>em</sub>) + [(R·f + K<sub>em</sub><sup>2</sup>) / K<sub>em</sub>]·&Omega;<sub>m</sub>",
        st_body
    ))
    story.append(Spacer(1, 4))
    story.append(boxed("Expression analytique littérale et valeur numérique de la vitesse :",
                       "&Omega;<sub>m, perm</sub> = [ K<sub>em</sub>·u - R·C<sub>r</sub> ] / [ K<sub>em</sub><sup>2</sup> + R·f ]<br/>"
                       "• Numérateur : (0.060 &times; 12) - (1.2 &times; 0.01) = 0.72 - 0.012 = <b>0.708 V·s</b><br/>"
                       "• Dénominateur : (0.060)<sup>2</sup> + (1.2 &times; 4·10<sup>-5</sup>) = 0.0036 + 0.000048 = <b>0.003648 N·m·s</b><br/>"
                       "<b>&Omega;<sub>m, perm</sub> = 0.708 / 0.003648 = 194.08 rad/s</b><br/>"
                       "En vitesse de rotation usuelle : <b>N = (194.08 &times; 60) / (2&pi;) &asymp; 1853.3 tr/min</b>.<br/>"
                       "• Courant permanent : I<sub>perm</sub> = (0.01 + 4·10<sup>-5</sup> &times; 194.08) / 0.060 = <b>0.296 A</b>.<br/>"
                       "• Couple moteur : C<sub>m, perm</sub> = 0.060 &times; 0.296 = <b>0.01776 N·m</b> (équilibrant C<sub>r</sub> + frottements)."))
    story.append(Spacer(1, 8))

    # Tâche 6 & Question 1
    story.append(Paragraph("<b>Tâche 6 & Question 1 : Rôle du bloc 1/s</b>", st_h2))
    story.append(Paragraph(
        "<b>Question 1 :</b> Quel est le rôle du bloc 1/s entre la vitesse et la position du moteur ?<br/>"
        "<b>Réponse argumentée :</b><br/>"
        "Dans le formalisme de la transformée de Laplace, l'opérateur <b>1/s</b> (ou 1/p) représente l'opérateur d'<b>intégration temporelle</b> (∫ dt) sous conditions initiales nulles.<br/>"
        "Physiquement, la vitesse angulaire instantanée &omega;<sub>m</sub>(t) est la dérivée temporelle de la position angulaire &theta;<sub>m</sub>(t) :<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&omega;<sub>m</sub>(t) = d&theta;<sub>m</sub>(t) / dt<br/>"
        "Par conséquent, l'intégration de la vitesse permet d'obtenir la position angulaire du rotor :<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&theta;<sub>m</sub>(t) = &int;<sub>0</sub><sup>t</sup> &omega;<sub>m</sub>(&tau;) d&tau; + &theta;<sub>m</sub>(0) &hArr; &Theta;<sub>m</sub>(s) = (1/s)·&Omega;<sub>m</sub>(s)<br/>"
        "Ce bloc convertit donc la grandeur cinématique 'vitesse' (rad/s) en grandeur cinématique 'position angulaire' (rad).",
        st_body
    ))

    doc.build(story)
    print(f"✔ Solution TD9 générée : {pdf_out}")

def main():
    sol_out = TEMP_DIR / "Solution_TD9_MCC_Simulink.pdf"
    build_pdf(sol_out)
    
    systech_dir = BASE_DIR / "courses_data" / "SYSTECH3"
    print("=== INSERTION DU CORRIGÉ DANS TOUS LES EXEMPLAIRES DE TD_09.PDF ===")
    
    for f in systech_dir.rglob("td_09.pdf"):
        writer = pypdf.PdfWriter()
        with open(f, "rb") as f_subj, open(sol_out, "rb") as f_sol:
            r_subj = pypdf.PdfReader(f_subj)
            r_sol = pypdf.PdfReader(f_sol)
            
            # Check if already has solution
            has_sol = False
            for p in r_subj.pages[-2:]:
                txt = (p.extract_text() or '').upper()
                if "MODÉLISATION D'UN MOTEUR À COURANT CONTINU" in txt or "CORRECTION OFFICIELLE ET ANALYTIQUE" in txt:
                    has_sol = True
                    break
            if has_sol:
                print(f"  ⏭ Déjà présent : {f.relative_to(systech_dir)}")
                continue
                
            for p in r_subj.pages:
                writer.add_page(p)
            for p in r_sol.pages:
                writer.add_page(p)
                
            temp_out = f.parent / "temp_merged.pdf"
            with open(temp_out, "wb") as f_out:
                writer.write(f_out)
        temp_out.replace(f)
        print(f"  ✔ Corrigé fusionné dans {f.relative_to(systech_dir)} ({len(writer.pages)} pages)")

if __name__ == "__main__":
    main()
