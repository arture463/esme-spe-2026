import os
import sys
import math
from pathlib import Path
import pypdf
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
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
    st_sub = ParagraphStyle('S', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#0284c7'), alignment=1)
    st_badge = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#166534'), alignment=1)
    
    st_exo = ParagraphStyle('Exo', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor('#0369a1'), spaceBefore=10, spaceAfter=4)
    st_q = ParagraphStyle('Q', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#1e293b'), spaceBefore=4, spaceAfter=2)
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
        Paragraph("CORRECTION INTÉGRALE ET DÉTAILLÉE", st_title),
        Paragraph("MÉCANIQUE DES FLUIDES (MECAFLU) — TD 1 : STATIQUE DES FLUIDES", st_sub),
        Paragraph("✔ Résolution analytique et applications numériques des 12 exercices", st_badge),
        HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0284c7'), spaceBefore=8, spaceAfter=12),
    ]

    # Exo 1
    story.append(Paragraph("Exercice 1 : Poussée d'Archimède — Applications Simples", st_exo))
    story.append(Paragraph("<b>1er cas (Iceberg) :</b> À l'équilibre de flottaison, le poids de l'iceberg équilibre la poussée d'Archimède :<br/>"
                           "P = &Pi; &rArr; M·g = &rho;<sub>eau</sub>·V<sub>imm</sub>·g &rArr; &rho;<sub>glace</sub>·V<sub>tot</sub> = &rho;<sub>eau</sub>·V<sub>imm</sub>.<br/>"
                           "La fraction immergée est donc : <b>f = V<sub>imm</sub> / V<sub>tot</sub> = &rho;<sub>glace</sub> / &rho;<sub>eau</sub> = d = 0.90 (soit 90%)</b>.<br/>"
                           "<i>Seuls 10% du volume de l'iceberg émergent au-dessus de l'eau.</i>", st_body))
    story.append(Paragraph("<b>2e cas (Pierre dans la bassine flottante) :</b><br/>"
                           "• <i>État initial (pierre dans la bassine) :</i> Le système {bassine + pierre} flotte. Le volume d'eau déplacé par le système équilibre son poids total : "
                           "V<sub>déplacé, 1</sub> = (M<sub>bassine</sub> + M<sub>pierre</sub>) / &rho;<sub>eau</sub> = V<sub>bassine</sub> + (M<sub>pierre</sub> / &rho;<sub>eau</sub>).<br/>"
                           "• <i>État final (pierre au fond de la baignoire) :</i> La bassine flotte seule (volume déplacé V'<sub>bassine</sub> = M<sub>bassine</sub> / &rho;<sub>eau</sub>) et la pierre est immergée au fond, déplaçant son <b>volume propre</b> V<sub>pierre</sub> = M<sub>pierre</sub> / &rho;<sub>pierre</sub>.<br/>"
                           "Le volume total déplacé devient : V<sub>déplacé, 2</sub> = (M<sub>bassine</sub> / &rho;<sub>eau</sub>) + (M<sub>pierre</sub> / &rho;<sub>pierre</sub>).<br/>"
                           "Comme la pierre est plus dense que l'eau (&rho;<sub>pierre</sub> &gt; &rho;<sub>eau</sub>), on a M<sub>pierre</sub> / &rho;<sub>pierre</sub> &lt; M<sub>pierre</sub> / &rho;<sub>eau</sub>, donc :<br/>"
                           "<b>V<sub>déplacé, 2</sub> &lt; V<sub>déplacé, 1</sub> &rArr; Le niveau de l'eau dans la baignoire BAISSE.</b>", st_body))
    story.append(Spacer(1, 4))

    # Exo 2
    story.append(Paragraph("Exercice 2 : Le Radeau", st_exo))
    story.append(Paragraph(
        "Données : 3 poutres cylindriques (diamètre d = 0.50 m, L = 4 m), &rho;<sub>bois</sub> = 700 kg/m<sup>3</sup>, "
        "&rho;<sub>mer</sub> = 1027 kg/m<sup>3</sup>, M<sub>plaque</sub> = 350 kg, g = 9.81 m/s<sup>2</sup>.<br/>"
        "1) <b>Poids total à vide P<sub>0</sub> :</b><br/>"
        "Volume d'une poutre : V<sub>1</sub> = &pi;·(d/2)<sup>2</sup>·L = &pi;·(0.25)<sup>2</sup>·4 = 0.25&pi; &asymp; 0.7854 m<sup>3</sup>.<br/>"
        "Volume des 3 poutres : V<sub>poutres</sub> = 3 &times; 0.7854 &asymp; 2.3562 m<sup>3</sup>.<br/>"
        "Masse des poutres : M<sub>poutres</sub> = &rho;<sub>bois</sub>·V<sub>poutres</sub> = 700 &times; 2.3562 &asymp; 1649.34 kg.<br/>"
        "Masse totale : M<sub>0</sub> = M<sub>plaque</sub> + M<sub>poutres</sub> = 350 + 1649.34 = <b>1999.34 kg</b>.<br/>"
        "Poids total : <b>P<sub>0</sub> = M<sub>0</sub>·g = 1999.34 &times; 9.81 = 19 613.5 N &asymp; 19.61 kN</b>.<br/>"
        "2) <b>Équation d'équilibre :</b> P<sub>0</sub> = &Pi;<sub>Archimède</sub> = &rho;<sub>mer</sub>·V<sub>imm</sub>·g &rArr; M<sub>0</sub> = &rho;<sub>mer</sub>·V<sub>imm</sub>.<br/>"
        "3) <b>Fraction immergée F(%) :</b><br/>"
        "F = V<sub>imm</sub> / V<sub>poutres</sub> = M<sub>0</sub> / (&rho;<sub>mer</sub>·V<sub>poutres</sub>) = 1999.34 / (1027 &times; 2.3562) = 1999.34 / 2419.81 = <b>0.8262 (soit 82.6%)</b>.<br/>"
        "4) <b>Masse maximale admissible M<sub>c</sub> :</b><br/>"
        "À l'immersion complète des poutres sans couler : (M<sub>0</sub> + M<sub>c</sub>) = &rho;<sub>mer</sub>·V<sub>poutres</sub> = 2419.81 kg.<br/>"
        "<b>M<sub>c</sub> = 2419.81 - 1999.34 = 420.47 kg</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 3
    story.append(Paragraph("Exercice 3 : Boule et Bill", st_exo))
    story.append(Paragraph(
        "Rayon extérieur r = 0.20 m &rArr; Volume extérieur V<sub>ext</sub> = (4/3)&pi; r<sup>3</sup> = (4/3)&pi;·(0.2)<sup>3</sup> = 0.03351 m<sup>3</sup> = 33.51 L.<br/>"
        "1) <b>Poids de chaque sphère :</b><br/>"
        "• <i>Sphère en bois pleine :</i> M<sub>bois</sub> = &rho;<sub>bois</sub>·V<sub>ext</sub> = 700 &times; 0.03351 = <b>23.46 kg</b> &rArr; <b>P<sub>bois</sub> = 23.46 &times; 9.81 = 230.1 N</b>.<br/>"
        "• <i>Sphère en acier creuse (épaisseur e = 8 mm = 0.008 m) :</i> r<sub>int</sub> = 0.20 - 0.008 = 0.192 m.<br/>"
        "Volume de métal : V<sub>acier</sub> = (4/3)&pi; (r<sub>ext</sub><sup>3</sup> - r<sub>int</sub><sup>3</sup>) = (4/3)&pi; (0.008 - 0.007078) &asymp; 3.861·10<sup>-3</sup> m<sup>3</sup>.<br/>"
        "Masse acier : M<sub>acier</sub> = 7800 &times; 3.861·10<sup>-3</sup> &asymp; <b>30.12 kg</b> &rArr; <b>P<sub>acier</sub> = 30.12 &times; 9.81 = 295.4 N</b>.<br/>"
        "2) <b>Poussée d'Archimède maximale (sphère totalement immergée) :</b><br/>"
        "&Pi;<sub>max</sub> = &rho;<sub>eau</sub>·V<sub>ext</sub>·g = 1000 &times; 0.03351 &times; 9.81 = <b>328.7 N</b>.<br/>"
        "Comme P<sub>bois</sub> (230.1 N) &lt; &Pi;<sub>max</sub> et P<sub>acier</sub> (295.4 N) &lt; &Pi;<sub>max</sub>, <b>les deux sphères FLOTTENT</b>.<br/>"
        "3) <b>Fraction de volume immergée F(%) :</b><br/>"
        "• Bois : F<sub>bois</sub> = M<sub>bois</sub> / (&rho;<sub>eau</sub>·V<sub>ext</sub>) = 23.46 / 33.51 = <b>70.0%</b>.<br/>"
        "• Acier : F<sub>acier</sub> = M<sub>acier</sub> / (&rho;<sub>eau</sub>·V<sub>ext</sub>) = 30.12 / 33.51 = <b>89.9%</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 4
    story.append(Paragraph("Exercice 4 : Soupape Automatique", st_exo))
    story.append(Paragraph(
        "Soupape circulaire de diamètre d = 0.10 m (S<sub>s</sub> = &pi; d<sup>2</sup> / 4 &asymp; 7.854·10<sup>-3</sup> m<sup>2</sup>), masse m = 1.0 kg.<br/>"
        "1) <b>Diamètre D du cylindre vide pour ouverture à h = 1.0 m :</b><br/>"
        "La force de pression exercée par l'eau sur la soupape vers le bas est F<sub>p</sub> = &rho;·g·h·S<sub>s</sub>.<br/>"
        "Le piston cylindrique vide immergé subit une poussée d'Archimède vers le haut &Pi; = &rho;·g·V<sub>piston</sub> = &rho;·g·(h - h<sub>base</sub>)·(&pi; D<sup>2</sup> / 4).<br/>"
        "À la limite de l'ouverture : &Pi; = F<sub>p</sub> + m·g &rArr; &rho; g h<sub>cyl</sub> (&pi; D<sup>2</sup> / 4) = &rho; g h S<sub>s</sub> + m g.<br/>"
        "Application numérique : <b>D &asymp; 0.113 m = 11.3 cm</b>.<br/>"
        "2) <b>Hauteur H de mercure pour ouverture à h = 1.20 m (D = 15 cm) :</b><br/>"
        "La masse de mercure ajoutée est M<sub>Hg</sub> = &rho;<sub>Hg</sub>·(&pi; D<sup>2</sup> / 4)·H. L'équilibre à h = 1.2 m donne :<br/>"
        "&Pi;<sub>eau</sub> = F<sub>p, eau</sub> + (m + M<sub>Hg</sub>)·g &rArr; <b>H &asymp; 2.45 cm</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 5
    story.append(Paragraph("Exercice 5 : Équilibre Hydrostatique de l'Atmosphère Terrestre", st_exo))
    story.append(Paragraph(
        "1) <b>Atmosphère isotherme (T(z) = T<sub>0</sub> = 293.15 K) :</b><br/>"
        "a) Équation hydrostatique : dp/dz = -&rho;(z)·g. Gaz parfait : p·M = &rho;·R·T<sub>0</sub> &rArr; &rho; = (M·p) / (R·T<sub>0</sub>).<br/>"
        "&rArr; <b>dp/dz + [ (M·g) / (R·T<sub>0</sub>) ]·p = 0</b>.<br/>"
        "b) Solution : <b>p(z) = p<sub>0</sub>·exp(-z / H)</b> avec l'échelle de hauteur <b>H = (R·T<sub>0</sub>) / (M·g)</b>.<br/>"
        "A.N. : H = (8.314 &times; 293.15) / (0.029 &times; 9.81) &asymp; <b>8565 m = 8.565 km</b>. Masse volumique : <b>&rho;(z) = &rho;<sub>0</sub>·exp(-z / H)</b>.<br/>"
        "c) Pression à z = 5 km : p(5000) = 1013 &times; exp(-5000 / 8565) = 1013 &times; 0.5578 &asymp; <b>565 hPa</b>.<br/>"
        "Comparaison : La valeur réelle est de 540 hPa. L'écart est d'environ +4.6% dû à l'hypothèse isotherme.<br/>"
        "d) Limites : La température réelle décroît avec l'altitude dans la troposphère (-6.5 °C/km).<br/>"
        "2) <b>Atmosphère à gradient thermique T(z) = T<sub>0</sub> - a·z :</b><br/>"
        "dp/p = - [ (M·g) / R ] · dz / (T<sub>0</sub> - a·z) &rArr; <b>p(z) = p<sub>0</sub> · [ 1 - (a·z / T<sub>0</sub>) ]<sup>M·g / (R·a)</sup></b>.<br/>"
        "Pour a = 0.0098 K/m (atmosphère sèche), l'exposant vaut : (0.029 &times; 9.81) / (8.314 &times; 0.0098) &asymp; <b>3.492</b>.<br/>"
        "À z = 5 km : 1 - (0.0098 &times; 5000 / 293.15) = 1 - 0.1671 = 0.8329.<br/>"
        "p(5000) = 1013 &times; (0.8329)<sup>3.492</sup> &asymp; 1013 &times; 0.5303 &asymp; <b>537 hPa</b> (en parfait accord avec la réalité de 540 hPa !).",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 6
    story.append(Paragraph("Exercice 6 : Barrage-Poids", st_exo))
    story.append(Paragraph(
        "Données : h = 100 m, L = 200 m, mur incliné de &alpha; = 45° avec la verticale, &rho;<sub>e</sub> = 1000 kg/m<sup>3</sup>, g = 10 m/s<sup>2</sup>.<br/>"
        "1) <b>Pression dans l'eau selon z (axe vertical ascendant, sol en z = 0, surface en z = h) :</b><br/>"
        "<b>p(z) = p<sub>atm</sub> + &rho;<sub>e</sub>·g·(h - z)</b>.<br/>"
        "2) <b>Force élémentaire sur une bande de longueur L :</b><br/>"
        "La longueur élémentaire le long de la pente est ds = dz / cos(&alpha;). Surface élémentaire dS = L·ds = L·dz / cos(&alpha;).<br/>"
        "En pression relative (la pression atmosphérique s'exerçant des deux côtés du barrage s'annule globalement) :<br/>"
        "<b>dF<sub>e</sub>(z) = &rho;<sub>e</sub>·g·(h - z) · [ L / cos(&alpha;) ] dz</b>.<br/>"
        "3) <b>Force totale exercée par l'eau F<sub>e</sub> :</b><br/>"
        "F<sub>e</sub> = &int;<sub>0</sub><sup>h</sup> [ &rho;<sub>e</sub> g (h - z) L / cos(&alpha;) ] dz = [ &rho;<sub>e</sub> g L / cos(&alpha;) ] &times; (h<sup>2</sup> / 2).<br/>"
        "A.N. : F<sub>e</sub> = [ 1000 &times; 10 &times; 200 / cos(45°) ] &times; (100<sup>2</sup> / 2) = (2·10<sup>6</sup> &times; &radic;2) &times; 5000 = <b>1.414·10<sup>10</sup> N = 14.14 GN</b>.<br/>"
        "4) <b>Point d'application z<sub>e</sub> :</b><br/>"
        "z<sub>e</sub>·F<sub>e</sub> = &int;<sub>0</sub><sup>h</sup> z dF<sub>e</sub>(z) = [ &rho;<sub>e</sub> g L / cos(&alpha;) ] &int;<sub>0</sub><sup>h</sup> z(h - z) dz = [ &rho;<sub>e</sub> g L / cos(&alpha;) ] &times; (h<sup>3</sup> / 6).<br/>"
        "<b>z<sub>e</sub> = [ h<sup>3</sup> / 6 ] / [ h<sup>2</sup> / 2 ] = h / 3 = 100 / 3 &asymp; 33.33 m</b> (situé au tiers inférieur du barrage).",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 7
    story.append(Paragraph("Exercice 7 : Poussez les Portes (Panneaux A, B, C)", st_exo))
    story.append(Paragraph(
        "Bassin de profondeur H = 9 m, 3 panneaux plans superposés A (haut), B (milieu), C (bas) de largeur L = 1 m.<br/>"
        "La force hydrostatique exercée de la surface z = 0 jusqu'à une profondeur z est : F(z) = &int;<sub>0</sub><sup>z</sup> &rho; g y L dy = (1/2)&rho; g L z<sup>2</sup>.<br/>"
        "Pour que chaque panneau supporte le même effort total : F<sub>A</sub> = F<sub>B</sub> = F<sub>C</sub> = F<sub>tot</sub> / 3.<br/>"
        "• Pour le panneau A : F(z<sub>1</sub>) = F<sub>tot</sub> / 3 &rArr; (1/2)&rho; g L z<sub>1</sub><sup>2</sup> = (1/3) [ (1/2)&rho; g L H<sup>2</sup> ] &rArr; <b>z<sub>1</sub> = H / &radic;3</b>.<br/>"
        "A.N. : <b>z<sub>1</sub> = 9 / &radic;3 &asymp; 5.20 m &rArr; Hauteur h<sub>1</sub> = 5.20 m</b>.<br/>"
        "• Pour les panneaux A+B : F(z<sub>2</sub>) = 2·F<sub>tot</sub> / 3 &rArr; <b>z<sub>2</sub> = H &radic;(2/3)</b>.<br/>"
        "A.N. : <b>z<sub>2</sub> = 9 &times; &radic;(2/3) &asymp; 7.35 m &rArr; Hauteur h<sub>2</sub> = z<sub>2</sub> - z<sub>1</sub> = 7.35 - 5.20 = 2.15 m</b>.<br/>"
        "• Pour le panneau C : <b>h<sub>3</sub> = H - z<sub>2</sub> = 9 - 7.35 = 1.65 m</b>.<br/>"
        "2) <b>Valeur de la force agissant sur chaque panneau :</b><br/>"
        "F<sub>tot</sub> = (1/2) &times; 1000 &times; 9.81 &times; 1 &times; 9<sup>2</sup> = 397.3 kN &rArr; <b>F<sub>A</sub> = F<sub>B</sub> = F<sub>C</sub> = 397.3 / 3 = 132.4 kN</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 8
    story.append(Paragraph("Exercice 8 : Pression sur une Vanne Semi-Circulaire", st_exo))
    story.append(Paragraph(
        "Réservoir de hauteur h = 8 m, vanne semi-circulaire de rayon R = 2 m au fond (de z = 0 à z = R, largeur 2&radic;(R<sup>2</sup> - z<sup>2</sup>)).<br/>"
        "(a) Pression : <b>p(z) = &rho;·g·(h - z)</b>.<br/>"
        "(b) Résultante des forces : F = &int; p(z) dS = &rho; g &int;<sub>0</sub><sup>R</sup> (h - z) · 2&radic;(R<sup>2</sup> - z<sup>2</sup>) dz = &rho; g h &int;<sub>0</sub><sup>R</sup> 2&radic;(R<sup>2</sup> - z<sup>2</sup>) dz - &rho; g &int;<sub>0</sub><sup>R</sup> 2z &radic;(R<sup>2</sup> - z<sup>2</sup>) dz.<br/>"
        "La première intégrale vaut la surface de la vanne : S = &pi; R<sup>2</sup> / 2.<br/>"
        "La seconde intégrale s'intègre directement : [- (2/3)(R<sup>2</sup> - z<sup>2</sup>)<sup>3/2</sup>]<sub>0</sub><sup>R</sup> = (2/3) R<sup>3</sup>.<br/>"
        "<b>F = &rho; g [ h·(&pi; R<sup>2</sup> / 2) - (2/3) R<sup>3</sup> ]</b>.<br/>"
        "(c) A.N. : F = 1000 &times; 9.81 &times; [ 8 &times; (2&pi;) - (2/3)&times;8 ] = 9810 &times; [ 50.265 - 5.333 ] = <b>440.8 kN</b>.<br/>"
        "(d) Moment par rapport au sol (z = 0) : M = &int;<sub>0</sub><sup>R</sup> z·p(z) dS &rArr; d = M / F &asymp; <b>0.82 m du sol</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 9 & 10
    story.append(Paragraph("Exercice 9 : Vérin Hydraulique", st_exo))
    story.append(Paragraph(
        "1) PFS sur chaque piston : Piston A : F + p<sub>0</sub>·S<sub>A</sub> = p<sub>A</sub>·S<sub>A</sub> &rArr; p<sub>A</sub> = p<sub>0</sub> + F / S<sub>A</sub>.<br/>"
        "Piston B : m·g + p<sub>0</sub>·S<sub>B</sub> = p<sub>B</sub>·S<sub>B</sub> &rArr; p<sub>B</sub> = p<sub>0</sub> + m·g / S<sub>B</sub>.<br/>"
        "2) PFH entre A et B : p<sub>A</sub> - p<sub>B</sub> = &rho;·g·(z<sub>B</sub> - z<sub>A</sub>). À même altitude (z<sub>A</sub> = z<sub>B</sub>), <b>p<sub>A</sub> = p<sub>B</sub></b>.<br/>"
        "3) Égalité des pressions : F / S<sub>A</sub> = m·g / S<sub>B</sub> &rArr; <b>F = m·g · (S<sub>A</sub> / S<sub>B</sub>)</b>.<br/>"
        "Comme S<sub>B</sub> &gg; S<sub>A</sub>, on a <b>F &ll; m·g</b> : le principe de démultiplication de la force est parfaitement vérifié.",
        st_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Exercice 10 : Sphères de Magdebourg", st_exo))
    story.append(Paragraph(
        "1) <i>Explication :</i> La pression atmosphérique p<sub>0</sub> s'exerce sur la surface extérieure de l'hémisphère alors que la pression interne est nulle. La résultante plaque fortement les deux demi-sphères l'une contre l'autre.<br/>"
        "2) <i>Symétrie :</i> La géométrie est de révolution autour de l'axe vertical (Oz). Par symétrie, pour tout élément de surface dS, il existe un élément symétrique dS' dont les composantes horizontales de force s'annulent. La résultante est donc purement verticale portée par l'axe de symétrie.<br/>"
        "3) <i>Force de séparation :</i> F = &int;&int; p<sub>0</sub>·cos(&theta;) dS = p<sub>0</sub>·S<sub>projetée</sub> = <b>p<sub>0</sub>·(&pi; R<sup>2</sup>)</b>.<br/>"
        "A.N. : R = 0.28 m &rArr; F = 10<sup>5</sup> &times; &pi; &times; (0.28)<sup>2</sup> &asymp; <b>24 630 N = 24.63 kN</b>.<br/>"
        "4) <i>Masse équivalente :</i> M = F / g = 24630 / 9.8 = <b>2 513 kg &asymp; 2.5 tonnes</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    # Exo 11 & 12
    story.append(Paragraph("Exercice 11 : Dôme de Colmatage (Deepwater Horizon)", st_exo))
    story.append(Paragraph(
        "Dôme hémisphérique de rayon a = 12 m à la profondeur h = 1500 m, &rho; = 1020 kg/m<sup>3</sup>.<br/>"
        "1) a) Pression à l'altitude z = a·cos(&phi;) : p(&phi;) = p<sub>0</sub> + &rho; g [ h - a·cos(&phi;) ].<br/>"
        "b) Composante verticale descendante : dF<sub>z</sub> = p(&phi;) · cos(&phi;) · a<sup>2</sup> sin(&phi;) d&phi; d&theta;.<br/>"
        "c) Intégration sur l'hémisphère : F<sub>z</sub> = &rho; g h · (&pi; a<sup>2</sup>) - (2/3) &rho; g &pi; a<sup>3</sup> (poussée vers le bas équivalente au cylindre d'eau diminué du volume de l'hémisphère selon Archimède).<br/>"
        "d) Pour a &ll; h (12 m &ll; 1500 m), le terme volumique est négligeable devant le terme de profondeur : <b>F<sub>z</sub> &asymp; &rho;·g·h·(&pi; a<sup>2</sup>)</b> (force sur le disque horizontal projeté).<br/>"
        "2) <b>Pression maximale d'hydrocarbures admissible :</b><br/>"
        "Pour que le dôme ne soit pas soulevé : &Delta;P · (&pi; a<sup>2</sup>) &le; F<sub>ancrages</sub> = T<sub>lin</sub> · (2&pi; a) &rArr; &Delta;P &le; 2 T<sub>lin</sub> / a = 2 &times; 10 000 / 12 = <b>1.67 kPa au-dessus de la pression hydrostatique</b>.",
        st_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Exercice 12 : Flotteur Oscillant", st_exo))
    story.append(Paragraph(
        "1) PFH : dp/dz = &rho; g &rArr; <b>p(z) = p<sub>0</sub> + &rho;<sub>0</sub> g z</b>.<br/>"
        "2) & 3) Équilibre : Poids P = &rho;·S·H·g, Poussée &Pi; = &rho;<sub>0</sub>·S·h<sub>eq</sub>·g. À l'équilibre P = &Pi; &rArr; <b>h<sub>eq</sub> = (&rho; / &rho;<sub>0</sub>)·H</b>.<br/>"
        "4) Force pour immerger totalement : F = &Pi;<sub>tot</sub> - P = (&rho;<sub>0</sub> - &rho;)·S·H·g.<br/>"
        "5) Oscillations : En écartant d'une cote x de la position d'équilibre, la force de rappel nette est &delta;F = -&rho;<sub>0</sub>·S·g·x.<br/>"
        "PFD : M·d<sup>2</sup>x/dt<sup>2</sup> = -&rho;<sub>0</sub>·S·g·x &rArr; (&rho; S H)·d<sup>2</sup>x/dt<sup>2</sup> + (&rho;<sub>0</sub> S g)·x = 0.<br/>"
        "Équation canonique d'un oscillateur harmonique : <b>d<sup>2</sup>x/dt<sup>2</sup> + &omega;<sub>0</sub><sup>2</sup>·x = 0</b> avec <b>&omega;<sub>0</sub> = &radic;[ (&rho;<sub>0</sub>·g) / (&rho;·H) ]</b>.<br/>"
        "Période des oscillations : <b>T<sub>0</sub> = 2&pi; / &omega;<sub>0</sub> = 2&pi; &radic;[ (&rho;·H) / (&rho;<sub>0</sub>·g) ]</b>.",
        st_body
    ))

    doc.build(story)
    print(f"✔ Solution MECAFLU TD1 générée : {pdf_out}")

def main():
    sol_out = TEMP_DIR / "Solution_MecaFlu_TD1.pdf"
    build_pdf(sol_out)
    
    mecaflu_dir = BASE_DIR / "courses_data" / "MECAFLU"
    print("=== INSERTION DU CORRIGÉ DANS MECA FLU - TD1.PDF ===")
    
    td1_files = list(mecaflu_dir.rglob("*TD1*.pdf"))
    for f in td1_files:
        writer = pypdf.PdfWriter()
        with open(f, "rb") as f_subj, open(sol_out, "rb") as f_sol:
            r_subj = pypdf.PdfReader(f_subj)
            r_sol = pypdf.PdfReader(f_sol)
            
            # Check if already merged
            has_sol = False
            for p in r_subj.pages[-2:]:
                txt = (p.extract_text() or '').upper()
                if "STATIQUE DES FLUIDES" in txt and "CORRECTION INTÉGRALE" in txt:
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
