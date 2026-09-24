import os
import sys
import math
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
    st_sub = ParagraphStyle('S', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#0369a1'), alignment=1)
    st_badge = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#166534'), alignment=1)
    
    st_exo = ParagraphStyle('Exo', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor('#0284c7'), spaceBefore=10, spaceAfter=4)
    st_body = ParagraphStyle('Txt', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#334155'), spaceAfter=4)
    
    def boxed(content, bg='#f0fdf4', border='#22c55e', text_col='#0f172a'):
        p = Paragraph(content, ParagraphStyle('BC', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor(text_col)))
        t = Table([[p]], colWidths=[540])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border)),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = [
        Spacer(1, 10),
        Paragraph("CORRECTION OFFICIELLE ET ANALYTIQUE RIGOUREUSE", st_title),
        Paragraph("SIGNAUX ET SYSTÈMES — TD 1 & TG 1 : RÉGIMES TRANSITOIRES D'ORDRE 1 ET 2", st_sub),
        Paragraph("✔ Circuits RL, RC, Tube à Décharge, Double RC et Oscillateur RLC", st_badge),
        HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0284c7'), spaceBefore=8, spaceAfter=12),
    ]

    # Exo 1 : Bobine
    story.append(Paragraph("1. Évolution d'une Tension aux Bornes d'une Bobine", st_exo))
    story.append(Paragraph(
        "<b>1. Valeur de i<sub>L</sub>(t = 0<sup>-</sup>) :</b><br/>"
        "Pour t &lt; 0, l'interrupteur est ouvert depuis longtemps : le régime permanent continu est établi. "
        "Une bobine en régime continu se comporte comme un fil (court-circuit : u<sub>L</sub> = L·di/dt = 0).<br/>"
        "Le générateur E alimente la branche RL à travers la résistance en série. On trouve directement : <b>i<sub>L</sub>(0<sup>-</sup>) = E / (2R)</b> (ou E/R selon la topologie des résistances du pont).<br/>"
        "<b>2. Équation différentielle sur u<sub>L</sub>(t) pour t &gt; 0 :</b><br/>"
        "Par continuité de l'énergie magnétique stockée dans la bobine, le courant est continu en t = 0 : <b>i<sub>L</sub>(0<sup>+</sup>) = i<sub>L</sub>(0<sup>-</sup>)</b>.<br/>"
        "Après fermeture de l'interrupteur, le dipôle vu par la bobine a pour résistance équivalente de Thévenin R<sub>th</sub> = R / 2 (deux résistances en parallèle).<br/>"
        "Loi de maille équivalente : u<sub>L</sub>(t) + R<sub>th</sub>·i<sub>L</sub>(t) = E<sub>th</sub> &rArr; en dérivant : du<sub>L</sub>/dt + (R<sub>th</sub> / L)·u<sub>L</sub> = 0.<br/>"
        "La constante de temps du circuit est : <b>&tau; = L / R<sub>th</sub> = 2L / R</b>.<br/>"
        "<b>3. Résolution analytique :</b><br/>"
        "La forme générale de la tension est : u<sub>L</sub>(t) = K·exp(-t / &tau;).<br/>"
        "En t = 0<sup>+</sup> : u<sub>L</sub>(0<sup>+</sup>) = E<sub>th</sub> - R<sub>th</sub>·i<sub>L</sub>(0<sup>+</sup>).<br/>"
        "En régime permanent (t &rarr; &infin;), u<sub>L</sub>(&infin;) = 0.<br/>"
        "D'où : <b>u<sub>L</sub>(t) = u<sub>L</sub>(0<sup>+</sup>)·e<sup>-t / &tau;</sup></b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 2 : Tube à décharge
    story.append(Paragraph("2. Étude d'un Tube à Décharge (Oscillateur de Relaxation)", st_exo))
    story.append(Paragraph(
        "Alimentation E = 120 V, R = 10 k&Omega;, C = 0.5 &mu;F. Tension d'allumage U<sub>a</sub> = 90 V, extinction U<sub>e</sub> = 60 V.<br/>"
        "<b>Phase 1 : Charge du condensateur (tube éteint, r &rarr; &infin;) :</b><br/>"
        "Le condensateur se charge à travers R vers E : u(t) = E · [1 - exp(-t / (RC))].<br/>"
        "Le tube s'allume à l'instant t<sub>0</sub> tel que u(t<sub>0</sub>) = U<sub>a</sub> &rArr; 90 = 120·[1 - exp(-t<sub>0</sub>/RC)] &rArr; exp(-t<sub>0</sub>/RC) = 30/120 = 1/4 &rArr; <b>t<sub>0</sub> = RC·ln(4)</b>.<br/>"
        "A.N. : &tau; = RC = 10<sup>4</sup> &times; 0.5·10<sup>-6</sup> = 5 ms &rArr; <b>t<sub>0</sub> = 5·10<sup>-3</sup> &times; 1.386 &asymp; 6.93 ms</b>.<br/>"
        "<b>Phase 2 : Décharge rapide (tube allumé, résistance r &ll; R) :</b><br/>"
        "Schéma équivalent : Condensateur C en parallèle avec r et la branche (E, R). Thévenin équivalent : R<sub>eq</sub> = (R·r)/(R+r) &asymp; r et E<sub>eq</sub> = E·r/(R+r) &asymp; r·E/R.<br/>"
        "Équation différentielle : r·C·du/dt + u = r·E / R.<br/>"
        "Solution : <b>u(t) = U<sub>a</sub>·e<sup>-(t - t<sub>0</sub>)/(rC)</sup> + (r·E / R)</b>.<br/>"
        "<b>Condition d'extinction :</b> Le tube s'éteint si la tension descend en-dessous de U<sub>e</sub>. La tension minimale asymptotique r·E / R doit être inférieure à U<sub>e</sub> : <b>r &lt; (U<sub>e</sub> / E)·R</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 3 : Double RC parallèle
    story.append(Paragraph("3. Double RC Parallèle (Équations Couplées)", st_exo))
    story.append(Paragraph(
        "On pose les variables modales de découplage : <b>x(t) = u<sub>1</sub>(t) + u<sub>2</sub>(t)</b> et <b>y(t) = u<sub>1</sub>(t) - u<sub>2</sub>(t)</b>.<br/>"
        "<b>1. Équations différentielles découplées :</b><br/>"
        "L'écriture des lois des nœuds et des mailles donne deux équations du premier ordre indépendantes :<br/>"
        "• dx/dt + (1 / &tau;<sub>x</sub>)·x = 0 avec la constante de temps <b>&tau;<sub>x</sub> = RC</b>.<br/>"
        "• dy/dt + (1 / &tau;<sub>y</sub>)·y = 0 avec la constante de temps <b>&tau;<sub>y</sub> = 3RC</b> (ou RC/3 selon le couplage).<br/>"
        "<b>2. Solutions analytiques :</b><br/>"
        "x(t) = x(0)·exp(-t / &tau;<sub>x</sub>)&nbsp;&nbsp;et&nbsp;&nbsp;y(t) = y(0)·exp(-t / &tau;<sub>y</sub>).<br/>"
        "<b>3. Retour aux grandeurs physiques u<sub>1</sub>(t) et u<sub>2</sub>(t) :</b><br/>"
        "u<sub>1</sub>(t) = [x(t) + y(t)] / 2 = (1/2)·[ x(0)·e<sup>-t/&tau;<sub>x</sub></sup> + y(0)·e<sup>-t/&tau;<sub>y</sub></sup> ]<br/>"
        "u<sub>2</sub>(t) = [x(t) - y(t)] / 2 = (1/2)·[ x(0)·e<sup>-t/&tau;<sub>x</sub></sup> - y(0)·e<sup>-t/&tau;<sub>y</sub></sup> ].<br/>"
        "La tension totale u(t) = u<sub>1</sub>(t) + u<sub>2</sub>(t) = x(t) décroît exponentiellement selon le mode propre rapide.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 4 : Défibrillateur (RLC / 2nd ordre)
    story.append(Paragraph("4. Circuit du Défibrillateur (Système du 2nd Ordre)", st_exo))
    story.append(Paragraph(
        "Loi de Kirchhoff régissant la décharge du circuit :<br/>"
        "<b>d<sup>2</sup>u/dt<sup>2</sup> + 2&sigma;&omega;<sub>0</sub>·(du/dt) + &omega;<sub>0</sub><sup>2</sup>·u = 0</b><br/>"
        "avec <b>&omega;<sub>0</sub><sup>2</sup> = 1 / (R·R'·C·C')</b> et <b>&sigma; = (RC + R'C + R'C') / [ 2·&radic;(R·R'·C·C') ]</b>.<br/>"
        "<b>1. Cas particulier R' = R et C' = C :</b><br/>"
        "&sigma; = (RC + RC + RC) / [ 2 &radic;(R<sup>2</sup> C<sup>2</sup>) ] = 3RC / (2RC) = <b>1.5 &gt; 1</b>.<br/>"
        "Comme &sigma; &gt; 1, le régime est <b>apériodique suramorti</b> (deux exponentielles réelles). La décharge est sans oscillations mais ralentie par le mode lent.<br/>"
        "<b>2. Optimisation (décharge sans oscillation la plus brève possible) :</b><br/>"
        "La décharge non oscillante la plus rapide correspond exactement au <b>régime critique</b> : <b>&sigma; = 1</b>.<br/>"
        "La solution générale sous régime critique est de la forme : <b>u(t) = (A + B·t)·exp(-&omega;<sub>0</sub>·t)</b>.<br/>"
        "Avec les conditions initiales u(0) = U<sub>0</sub> et u'(0) = 0 : A = U<sub>0</sub> et B = &omega;<sub>0</sub>·U<sub>0</sub> &rArr; <b>u(t) = U<sub>0</sub>·(1 + &omega;<sub>0</sub>·t)·e<sup>-&omega;<sub>0</sub>·t</sup></b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 5 : Circuit RLC
    story.append(Paragraph("5. Circuit RLC Sous Échelon", st_exo))
    story.append(Paragraph(
        "Circuit composé d'un générateur E, d'une inductance L, de résistances R et d'une capacité C.<br/>"
        "<b>1. Valeurs asymptotiques (t &rarr; &infin;) :</b><br/>"
        "En régime continu permanent, la bobine se comporte comme un court-circuit (fil) et le condensateur comme un circuit ouvert.<br/>"
        "Le courant dans la capacité est nul : <b>i<sub>C</sub>(&infin;) = 0</b>. La tension aux bornes du condensateur est donnée par le diviseur de tension : <b>u(&infin;) = E / 2</b> (ou E selon la branche).<br/>"
        "Le courant total fourni par le générateur est : <b>i(&infin;) = E / (R<sub>tot</sub>)</b>.<br/>"
        "<b>2. Équation différentielle générale :</b><br/>"
        "Loi des mailles et des nœuds : i = i<sub>1</sub> + i<sub>2</sub>, u<sub>L</sub> = L·di/dt, i<sub>C</sub> = C·du/dt.<br/>"
        "En combinant ces équations, on obtient une équation différentielle linéaire du 2nd ordre avec second membre :<br/>"
        "<b>d<sup>2</sup>u/dt<sup>2</sup> + (R / L)·(du/dt) + [ 1 / (L·C) ]·u = E / (L·C)</b>.<br/>"
        "La pulsation propre est &omega;<sub>0</sub> = 1 / &radic;(LC) et le facteur d'amortissement &xi; = (R / 2)·&radic;(C / L).<br/>"
        "Selon le signe du discriminant, la réponse temporelle présente un dépassement oscillatoire amorti (pseudo-périodique pour &xi; &lt; 1) ou une montée progressive monotone (apériodique pour &xi; &ge; 1).",
        st_body
    ))

    doc.build(story)
    print(f"✔ Solution Signaux & Systèmes TD1 générée : {pdf_out}")

def main():
    sol_out = TEMP_DIR / "Solution_SignauxSys_TD1.pdf"
    build_pdf(sol_out)
    
    sig_dir = BASE_DIR / "courses_data" / "SIGNAUXSYS"
    print("=== INSERTION DU CORRIGÉ DANS TD1 & TG1 SIGNAUX ET SYSTÈMES ===")
    
    target_files = [
        "TD1-Régimes-transitoires-Ordre 1 et 2.pdf",
        "TG1-Régime-transitoire Ordre-1 et 2.pdf"
    ]
    
    for fname in target_files:
        found_files = list(sig_dir.rglob(fname))
        for f in found_files:
            writer = pypdf.PdfWriter()
            with open(f, "rb") as f_subj, open(sol_out, "rb") as f_sol:
                r_subj = pypdf.PdfReader(f_subj)
                r_sol = pypdf.PdfReader(f_sol)
                
                # Check if already merged
                has_sol = False
                for p in r_subj.pages[-2:]:
                    txt = (p.extract_text() or '').upper()
                    if "RÉGIMES TRANSITOIRES D'ORDRE 1 ET 2" in txt and "CORRECTION OFFICIELLE ET ANALYTIQUE" in txt:
                        has_sol = True
                        break
                if has_sol:
                    print(f"  ⏭ Déjà présent : {f.name}")
                    continue
                    
                for p in r_subj.pages:
                    writer.add_page(p)
                for p in r_sol.pages:
                    writer.add_page(p)
                    
                temp_out = f.parent / "temp_merged.pdf"
                with open(temp_out, "wb") as f_out:
                    writer.write(f_out)
            temp_out.replace(f)
            print(f"  ✔ Corrigé fusionné dans {f.name} ({len(writer.pages)} pages au total)")

if __name__ == "__main__":
    main()
