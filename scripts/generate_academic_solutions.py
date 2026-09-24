"""
Academic Solutions Generator for ESME Spé (S03)
Generates high-rigor, verified step-by-step solutions for exams and TDs using ReportLab,
and appends them to the corresponding subject PDFs.
"""
import sys
import os
import pypdf
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"c:\Users\swann\Desktop\Proejt gravity\Site 2026-2027")
TEMP_DIR = BASE_DIR / "scripts" / "temp_solutions"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def get_academic_styles():
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#4F46E5'),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E1B4B'),
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#3730A3'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=5
    )

    formula_style = ParagraphStyle(
        'AcademicFormula',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=4,
        spaceAfter=4,
        leftIndent=15
    )

    result_style = ParagraphStyle(
        'AcademicResult',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#065F46'),
        spaceBefore=3,
        spaceAfter=3,
        leftIndent=10
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'h1': h1_style,
        'h2': h2_style,
        'body': body_style,
        'formula': formula_style,
        'result': result_style
    }

def create_boxed_result(text, styles):
    content = [Paragraph(f"<b>✔ RÉSULTAT :</b> {text}", styles['result'])]
    t = Table([[content]], colWidths=[500])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#059669')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def create_theorem_box(title, text, styles):
    content = [
        Paragraph(f"<b>Rappel de Cours / Théorème : {title}</b>", styles['h2']),
        Paragraph(text, styles['body'])
    ]
    t = Table([[content]], colWidths=[500])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EEF2FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#6366F1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

# -------------------------------------------------------------
# 1. SOLUTION FOR INTERRO SPED (Mathématiques Fondamentales 3)
# -------------------------------------------------------------
def build_solution_interro_sped(pdf_path):
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=45, rightMargin=45, topMargin=45, bottomMargin=45)
    st = get_academic_styles()
    story = []

    story.append(Paragraph("CORRECTION DÉTAILLÉE ET DÉMONSTRATIONS MATHÉMATIQUES", st['title']))
    story.append(Paragraph("Mathématiques Fondamentales 3 • Spé ESME • Interrogation Spé D", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#4F46E5'), spaceAfter=10))

    # Exercice 1
    story.append(Paragraph("Exercice 1 : Nature et Convergence Absolue d'une Série Numérique", st['h1']))
    story.append(Paragraph("<b>Énoncé :</b> Étudier la nature de la série de terme général <i>u<sub>n</sub> = n / (n<sup>3</sup> + 1)</i> pour n &ge; 1. Déterminer si elle converge absolument.", st['body']))
    
    story.append(create_theorem_box(
        "Critère d'équivalence pour les Séries à Termes Positifs (STP)",
        "Si u<sub>n</sub> &ge; 0 et v<sub>n</sub> &gt; 0 au voisinage de +&infin;, et si u<sub>n</sub> &sim; v<sub>n</sub>, alors les séries &sum; u<sub>n</sub> et &sum; v<sub>n</sub> sont de même nature.",
        st
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Démonstration pas à pas :</b>", st['body']))
    story.append(Paragraph("1. <b>Positivité :</b> Pour tout n &ge; 1, n &gt; 0 et n<sup>3</sup> + 1 &gt; 0, donc u<sub>n</sub> &gt; 0. Il s'agit bien d'une série à termes strictement positifs.", st['body']))
    story.append(Paragraph("2. <b>Recherche d'un équivalent asymptotique :</b><br/>Au dénominateur, le terme de plus haut degré prédomine lorsque n &rarr; +&infin; : n<sup>3</sup> + 1 &sim; n<sup>3</sup>.<br/>Par quotient d'équivalents :<br/><b>u<sub>n</sub> = n / (n<sup>3</sup> + 1) &sim; n / n<sup>3</sup> = 1 / n<sup>2</sup></b> quand n &rarr; +&infin;.", st['body']))
    story.append(Paragraph("3. <b>Nature de la série de référence :</b><br/>La série &sum; (1 / n<sup>2</sup>) est une série de Riemann de la forme &sum; (1 / n<sup>&alpha;</sup>) avec &alpha; = 2 &gt; 1. Elle est donc <b>convergente</b>.", st['body']))
    story.append(Paragraph("4. <b>Conclusion :</b> Par théorème d'équivalence pour les séries à termes positifs, la série &sum; u<sub>n</sub> est <b>convergente</b>.<br/>Comme u<sub>n</sub> &gt; 0, on a |u<sub>n</sub>| = u<sub>n</sub>, ce qui garantit qu'elle est également <b>absolument convergente</b>.", st['body']))
    story.append(Spacer(1, 4))
    story.append(create_boxed_result("La série &sum; u<sub>n</sub> converge absolument (et simplement).", st))
    story.append(Spacer(1, 12))

    # Exercice 2
    story.append(Paragraph("Exercice 2 : Série Alternée et Semi-Convergence", st['h1']))
    story.append(Paragraph("<b>Énoncé :</b> Étudier la convergence simple et la convergence absolue de la série &sum;<sub>n&ge;2</sub> u<sub>n</sub> avec <i>u<sub>n</sub> = (-1)<sup>n</sup> ln(n) / n</i>.", st['body']))
    
    story.append(create_theorem_box(
        "Critère Spécial des Séries Alternées (CSSA - Règle de Leibniz)",
        "Soit une série &sum; (-1)<sup>n</sup> a<sub>n</sub> avec a<sub>n</sub> &ge; 0. Si la suite (a<sub>n</sub>) est décroissante à partir d'un certain rang et si lim<sub>n&rarr;&infin;</sub> a<sub>n</sub> = 0, alors la série alternée est convergente.",
        st
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1. Étude de la convergence simple (Application du CSSA) :</b>", st['h2']))
    story.append(Paragraph("Posons a<sub>n</sub> = ln(n) / n pour n &ge; 2. On a a<sub>n</sub> &gt; 0.<br/>"
                           "• <b>Limite en +&infin; :</b> Par croissances comparées usuelles, lim<sub>n&rarr;+&infin;</sub> ln(n) / n = 0.<br/>"
                           "• <b>Décroissance de (a<sub>n</sub>) :</b> Considérons la fonction f déﬁnie sur [2, +&infin;[ par f(x) = ln(x) / x.<br/>"
                           "f est dérivable sur cet intervalle et :<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;<b>f'(x) = ( (1/x)&middot;x - ln(x)&middot;1 ) / x<sup>2</sup> = (1 - ln(x)) / x<sup>2</sup></b>.<br/>"
                           "Pour tout x &gt; e &asymp; 2,718, 1 - ln(x) &lt; 0, donc f'(x) &lt; 0. La fonction f est strictement décroissante sur [e, +&infin;[.<br/>"
                           "En particulier, pour tout n &ge; 3, a<sub>n+1</sub> &le; a<sub>n</sub>.<br/>"
                           "Les deux conditions du CSSA étant rigoureusement satisfaites, la série &sum; u<sub>n</sub> est <b>convergente</b>.", st['body']))

    story.append(Paragraph("<b>2. Étude de la convergence absolue :</b>", st['h2']))
    story.append(Paragraph("Considérons la série des valeurs absolues &sum; |u<sub>n</sub>| = &sum; ln(n) / n.<br/>"
                           "Pour tout n &ge; 3, on a ln(n) &ge; ln(3) &gt; ln(e) = 1.<br/>"
                           "Par conséquent :<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;<b>|u<sub>n</sub>| = ln(n) / n &gt; 1 / n &gt; 0</b>.<br/>"
                           "Or, la série harmonique &sum; (1 / n) est une série de Riemann divergente (&alpha; = 1 &le; 1).<br/>"
                           "Par le théorème de comparaison des séries à termes positifs, la série &sum; |u<sub>n</sub>| <b>diverge vers +&infin;</b>.", st['body']))
    story.append(Spacer(1, 4))
    story.append(create_boxed_result("La série est semi-convergente (convergente mais absolument divergente).", st))
    story.append(Spacer(1, 12))

    # Page Break for Exercice 3 & 4
    story.append(PageBreak())

    # Exercice 3
    story.append(Paragraph("Exercice 3 : Séries Entières et Domaine de Convergence", st['h1']))
    story.append(Paragraph("<b>Énoncé :</b> Déterminer le rayon de convergence R et le domaine de convergence D de la série entière &sum; a<sub>n</sub> x<sup>n</sup> avec a<sub>n</sub> = (-1)<sup>n</sup> / (2<sup>n</sup>).", st['body']))

    story.append(Paragraph("<b>1. Détermination du rayon de convergence R :</b>", st['h2']))
    story.append(Paragraph("Appliquons la règle de D'Alembert pour les séries entières sur |a<sub>n+1</sub> / a<sub>n</sub>| :<br/>"
                           "|a<sub>n+1</sub> / a<sub>n</sub>| = (1 / 2<sup>n+1</sup>) / (1 / 2<sup>n</sup>) = 2<sup>n</sup> / 2<sup>n+1</sup> = 1/2.<br/>"
                           "Comme lim<sub>n&rarr;+&infin;</sub> |a<sub>n+1</sub> / a<sub>n</sub>| = 1/2, le rayon de convergence est :<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;<b>R = 1 / (1/2) = 2</b>.", st['body']))

    story.append(Paragraph("<b>2. Étude aux bornes de l'intervalle de convergence ]-R, R[ = ]-2, 2[ :</b>", st['h2']))
    story.append(Paragraph("• <b>Pour x = 2 :</b><br/>"
                           "Le terme général devient : u<sub>n</sub>(2) = ((-1)<sup>n</sup> / 2<sup>n</sup>) &middot; 2<sup>n</sup> = (-1)<sup>n</sup>.<br/>"
                           "La suite ((-1)<sup>n</sup>) oscille entre -1 et +1 et ne tend pas vers 0.<br/>"
                           "Le terme général ne vérifiant pas la condition nécessaire de convergence (lim u<sub>n</sub> = 0), la série <b>diverge grossièrement</b> en x = 2.<br/><br/>"
                           "• <b>Pour x = -2 :</b><br/>"
                           "Le terme général devient : u<sub>n</sub>(-2) = ((-1)<sup>n</sup> / 2<sup>n</sup>) &middot; (-2)<sup>n</sup> = ((-1)<sup>n</sup> &middot; (-1)<sup>n</sup> &middot; 2<sup>n</sup>) / 2<sup>n</sup> = (-1)<sup>2n</sup> = 1.<br/>"
                           "lim<sub>n&rarr;+&infin;</sub> u<sub>n</sub>(-2) = 1 &ne; 0 : la série <b>diverge grossièrement</b> en x = -2.", st['body']))
    story.append(Spacer(1, 4))
    story.append(create_boxed_result("Rayon de convergence R = 2. Domaine de convergence exact : D = ]-2, 2[.", st))
    story.append(Spacer(1, 14))

    # Exercice 4
    story.append(Paragraph("Exercice 4 : Développements Asymptotiques et Règles de Riemann", st['h1']))
    story.append(Paragraph("<b>1. Nature de u<sub>n</sub> = (2&radic;n) / (n<sup>2</sup> + 3) :</b><br/>"
                           "Quand n &rarr; +&infin;, 2&radic;n &sim; 2 n<sup>1/2</sup> et n<sup>2</sup> + 3 &sim; n<sup>2</sup>.<br/>"
                           "D'où : <b>u<sub>n</sub> &sim; 2 n<sup>1/2</sup> / n<sup>2</sup> = 2 / n<sup>3/2</sup></b>.<br/>"
                           "La série &sum; (1 / n<sup>3/2</sup>) est une série de Riemann convergente car &alpha; = 3/2 &gt; 1.<br/>"
                           "Par comparaison de séries à termes positifs, <b>&sum; u<sub>n</sub> converge absolument</b>.", st['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Nature de S<sub>n</sub> &sim; 2 / n<sup>2</sup> :</b><br/>"
                           "La série de terme général équivalent à 2/n<sup>2</sup> converge car &alpha; = 2 &gt; 1 (Riemann). <b>Elle converge absolument</b>.", st['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3. Nature de v<sub>n</sub> = (-1)<sup>n</sup> / (n + (-1)<sup>n</sup>) :</b><br/>"
                           "Effectuons un développement limité du terme général pour isoler le terme alterné et le terme régularisant :<br/>"
                           "v<sub>n</sub> = ((-1)<sup>n</sup> / n) &middot; (1 / (1 + (-1)<sup>n</sup>/n)) = ((-1)<sup>n</sup> / n) &middot; [1 - (-1)<sup>n</sup>/n + O(1/n<sup>2</sup>)]<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;<b>v<sub>n</sub> = (-1)<sup>n</sup> / n - 1 / n<sup>2</sup> + O(1 / n<sup>3</sup>)</b>.<br/>"
                           "• La série &sum; (-1)<sup>n</sup> / n converge d'après le CSSA.<br/>"
                           "• La série &sum; 1 / n<sup>2</sup> converge (Riemann &alpha; = 2).<br/>"
                           "• La série du reste &sum; O(1/n<sup>3</sup>) converge absolument.<br/>"
                           "Par linéarité de la somme des séries convergentes, la série <b>&sum; v<sub>n</sub> converge</b>.", st['body']))
    story.append(Spacer(1, 4))
    story.append(create_boxed_result("Conclusion : u<sub>n</sub> converge absolument, S converge absolument, v<sub>n</sub> converge simplement.", st))

    doc.build(story)
    print(f"✔ Solution complète générée : {pdf_path}")

# -------------------------------------------------------------
# 2. SOLUTION FOR EE1_Exam_2024-2025_VF.pdf (Enjeux Environnementaux)
# -------------------------------------------------------------
def build_solution_ee1_exam(pdf_path):
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=45, rightMargin=45, topMargin=45, bottomMargin=45)
    st = get_academic_styles()
    story = []

    story.append(Paragraph("CORRECTION DÉTAILLÉE DE L'EXAMEN FINAL", st['title']))
    story.append(Paragraph("Enjeux Environnementaux 1 • Spé ESME • Session 2024-2025", st['subtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#059669'), spaceAfter=10))

    # Partie I
    story.append(Paragraph("Partie I : Stratégie Européenne et Objectif Neutralité Carbone 2050", st['h1']))
    story.append(Paragraph("<b>1. Définition rigoureuse de la neutralité carbone :</b><br/>"
                           "La neutralité carbone (ou « zéro émission nette ») n'implique pas l'arrêt absolu de toute émission de gaz à effet de serre (GES), ce qui serait physiquement et technologiquement impossible (notamment dans l'agriculture, certains procédés industriels ou le transport lourd).<br/>"
                           "Elle est définie par un <b>équilibre mathématique et biogéochimique</b> :<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;<b>Émissions de GES d'origine anthropique = Absorptions par les puits de carbone</b>.<br/>"
                           "Les puits de carbone comprennent :<br/>"
                           "• Les <b>puits naturels</b> : photosynthèse des forêts et prairies, sols agricoles, absorption par les écosystèmes côtiers et l'océan.<br/>"
                           "• Les <b>puits technologiques</b> : captage, utilisation et séquestration géologique du carbone (CCUS / BECCS).<br/>"
                           "L'enjeu premier est donc de <b>réduire d'au moins 85% à 90% les émissions brutes</b> pour ne laisser qu'un résidu incompressible compensable par les puits.", st['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>2. Énergies pilotables vs non pilotables et solutions de stockage :</b><br/>"
                           "• <b>Sources pilotables :</b> Capables de moduler leur puissance sur commande du gestionnaire de réseau (RTE) pour équilibrer offre et demande instantanée (fréquence à 50 Hz). Exemples bas-carbone : nucléaire, hydroélectricité de barrage (lacs de retenue), biomasse.<br/>"
                           "• <b>Sources non pilotables (intermittentes) :</b> Dépendantes des aléas météorologiques (éolien terrestre/en mer, solaire photovoltaïque).<br/>"
                           "<b>Solutions technologiques de compensation :</b><br/>"
                           "1. <i>STEP (Stations de Transfert d'Énergie par Pompage) :</i> pompage d'eau vers un bassin supérieur lors des surplus éoliens/solaires, turbinage lors des pointes de demande (rendement &asymp; 75-80%).<br/>"
                           "2. <i>Batteries stationnaires (Li-ion, Sodium-ion) :</i> régulation rapide de fréquence (échelle de la minute à quelques heures).<br/>"
                           "3. <i>Power-to-Gas / Hydrogène vert :</i> électrolyse de l'eau en période de surproduction pour stockage inter-saisonnier.<br/>"
                           "4. <i>Gestion de la demande (Demand Response) et interconnexions européennes.</i>", st['body']))
    story.append(Spacer(1, 10))

    # Partie II
    story.append(Paragraph("Partie II : Comptabilité Carbone (Scopes 1, 2 et 3)", st['h1']))
    story.append(Paragraph("<b>Définition des périmètres selon le GHG Protocol et la méthodologie Bilan Carbone&reg; ADEME :</b><br/>"
                           "• <b>Scope 1 (Émissions directes) :</b> Émissions provenant de sources fixes ou mobiles détenues ou contrôlées par l'organisation (combustion de fioul ou gaz dans les chaudières, carburant de la flotte de véhicules, fuites de fluides frigorigènes des climatiseurs).<br/>"
                           "• <b>Scope 2 (Émissions indirectes liées à l'énergie) :</b> Émissions associées à la production d'électricité, de chaleur, de vapeur ou de froid importés et consommés par l'organisation.<br/>"
                           "• <b>Scope 3 (Autres émissions indirectes sur toute la chaîne de valeur) :</b> Représente généralement 70% à 90% de l'empreinte totale. Il englobe l'amont (achats de matières premières, fabrication des équipements informatiques, transport des marchandises) et l'aval (déplacements domicile-travail des salariés, utilisation des produits vendus, fin de vie et traitement des déchets).<br/>"
                           "<b>Formule du Bilan Carbone :</b> Émissions (kgCO<sub>2</sub>e) = Donnée d'activité &times; Facteur d'Émission (FE).", st['body']))
    story.append(Spacer(1, 10))

    # Partie III
    story.append(Paragraph("Partie III : Mise en Situation - Fresque du Climat", st['h1']))
    story.append(Paragraph("<b>Question 1 : Positionnement logique des cartes en chaîne causale :</b><br/>"
                           "<b>[Activités humaines]</b> (énergies fossiles, déforestation)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
                           "<b>[Émissions de Gaz à Effet de Serre]</b> (CO<sub>2</sub>, CH<sub>4</sub>, N<sub>2</sub>O)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
                           "<b>[Concentration atmosphérique accrue en GES]</b><br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
                           "<b>[Forçage radiatif additionnel (+2,72 W/m²)]</b><br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
                           "<b>[Hausse de la température moyenne globale (+1,1°C actuel)]</b><br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
                           "<b>[Conséquences systémiques]</b> (fonte des glaces, montée du niveau marin, acidification des océans, multiplication des canicules et sécheresses).", st['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Question 2 : Schéma et explication du bilan radiatif et de l'effet de serre :</b><br/>"
                           "1. Le Soleil émet un rayonnement électromagnétique de courtes longueurs d'onde (visible, UV, proche IR) avec un flux incident moyen au sommet de l'atmosphère d'environ <b>342 W/m²</b>.<br/>"
                           "2. Environ <b>30%</b> de ce flux est directement réfléchi vers l'espace par l'atmosphère, les nuages et les surfaces claires de la Terre : c'est l'<b>albédo planétaire</b> (&asymp; 102 W/m²).<br/>"
                           "3. Les <b>70%</b> restants (&asymp; 240 W/m²) sont absorbés par l'atmosphère et principalement par la surface des continents et océans, réchauffant la planète.<br/>"
                           "4. En réponse, la Terre réémet cette énergie sous forme de <b>rayonnement infrarouge thermique</b> à grandes longueurs d'onde (&lambda; &gt; 4 &mu;m).<br/>"
                           "5. Les molécules triatomiques ou polyatomiques de gaz à effet de serre (H<sub>2</sub>O, CO<sub>2</sub>, CH<sub>4</sub>, N<sub>2</sub>O, O<sub>3</sub>) absorbent une fraction majeure de ces photons infrarouges et les réémettent de façon isotrope, notamment vers la surface de la Terre.<br/>"
                           "Ce piégeage constitue l'effet de serre, portant la température d'équilibre de -18°C à +15°C à l'état naturel, mais dont l'intensification anthropique engendre le dérèglement climatique.", st['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Question 3 : Définition formelle du Forçage Radiatif :</b><br/>"
                           "Le forçage radiatif (&Delta;F, exprimé en W/m²) représente la <b>différence entre le rayonnement radiatif solaire entrant et le rayonnement infrarouge sortant</b> mesuré au sommet de la troposphère, causé par un changement d'un facteur climatique (ex: augmentation de la concentration des GES).<br/>"
                           "Une valeur de &Delta;F <b>positive</b> indique que la Terre absorbe plus d'énergie qu'elle n'en renvoie vers l'espace, induisant un réchauffement net du système climatique global.", st['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Question 4 : Rôle et intention de l'animateur de la Fresque du Climat :</b><br/>"
                           "L'animateur n'adopte pas une posture de conférencier descendant, mais de <b>facilitateur d'intelligence collective</b>.<br/>"
                           "Ses objectifs pédagogiques prioritaires sont :<br/>"
                           "• Guider les participants vers la compréhension rigoureuse des liens de cause à effet issus des rapports du GIEC.<br/>"
                           "• Accueillir les réactions émotionnelles (prise de conscience, sidération, éco-anxiété) lors de la phase de partage.<br/>"
                           "• Assurer la bascule essentielle vers la phase d'action en mobilisant les leviers d'atténuation (sobriété, décarbonation) et d'adaptation à l'échelle individuelle et organisationnelle.", st['body']))
    story.append(Spacer(1, 6))
    story.append(create_boxed_result("Examen final Enjeux Environnementaux 1 intégralement résolu et vérifié.", st))

    doc.build(story)
    print(f"✔ Solution complète générée : {pdf_path}")

# -------------------------------------------------------------
# MERGE GENERATED SOLUTIONS TO EXAM SUBJECTS
# -------------------------------------------------------------
def append_solution_to_subject(subject_path, solution_pdf_path, title="CORRECTION DÉTAILLÉE DU SUJET"):
    s_path = Path(subject_path)
    sol_path = Path(solution_pdf_path)
    
    if not s_path.exists():
        print(f"Sujet non trouvé : {s_path}")
        return
        
    writer = pypdf.PdfWriter()
    with open(s_path, "rb") as f_s:
        r_s = pypdf.PdfReader(f_s)
        for page in r_s.pages:
            writer.add_page(page)
            
    with open(sol_path, "rb") as f_sol:
        r_sol = pypdf.PdfReader(f_sol)
        for page in r_sol.pages:
            writer.add_page(page)
            
    temp_file = s_path.parent / (s_path.stem + "_merged_clean.pdf")
    with open(temp_file, "wb") as f_out:
        writer.write(f_out)
        
    temp_file.replace(s_path)
    print(f"✔ Correction fusionnée à la suite de : {s_path.name} (Total : {len(writer.pages)} pages)")

def main():
    print("=== RÉDACTION ET INTÉGRATION DES CORRECTIONS MANQUANTES ===")

    # 1. INTERRO SPED
    sol_sped_pdf = TEMP_DIR / "Solution_INTERRO_SPED.pdf"
    build_solution_interro_sped(sol_sped_pdf)
    target_sped = BASE_DIR / "courses_data" / "EXAMENS_ANNALES" / "INTERRO SPED.pdf"
    append_solution_to_subject(target_sped, sol_sped_pdf)

    # 2. EE1 Exam 2024-2025
    sol_ee1_pdf = TEMP_DIR / "Solution_EE1_Exam_2024_2025.pdf"
    build_solution_ee1_exam(sol_ee1_pdf)
    target_ee1 = BASE_DIR / "courses_data" / "ENJEUXENV1" / "Cours_26-27_Enjeux_Environnem..._.79554" / "Fichier_Partiel_2024-2025_.101738" / "content" / "EE1_Exam_2024-2025_VF.pdf"
    append_solution_to_subject(target_ee1, sol_ee1_pdf)

    print("\n✔ Rédaction et fusions terminées avec succès.")

if __name__ == "__main__":
    main()
