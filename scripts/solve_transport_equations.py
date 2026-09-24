"""
Generates complete mathematical solution for:
Equations différentielles_Problèmes de transports.pdf (OUTILSMATH3)
Appends the 5-page solution directly to the document.
"""
import sys
import pypdf
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(r"c:\Users\swann\Desktop\Proejt gravity\Site 2026-2027")
TEMP_DIR = BASE_DIR / "scripts" / "temp_solutions"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def get_styles():
    styles = getSampleStyleSheet()
    title = ParagraphStyle('T', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0F172A'), spaceAfter=4)
    subtitle = ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#4F46E5'), spaceAfter=12)
    h1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor('#1E1B4B'), spaceBefore=12, spaceAfter=5)
    h2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10.5, leading=14.5, textColor=colors.HexColor('#3730A3'), spaceBefore=8, spaceAfter=3)
    body = ParagraphStyle('B', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#1F2937'), spaceAfter=4)
    result = ParagraphStyle('R', fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor('#065F46'), leftIndent=8)
    return {'title': title, 'sub': subtitle, 'h1': h1, 'h2': h2, 'body': body, 'result': result}

def boxed_res(text, st):
    t = Table([[Paragraph(f"<b>✔ SOLUTION :</b> {text}", st['result'])]], colWidths=[500])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#059669')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def build_pdf(pdf_out):
    doc = SimpleDocTemplate(str(pdf_out), pagesize=A4, leftMargin=45, rightMargin=45, topMargin=45, bottomMargin=45)
    st = get_styles()
    story = []

    story.append(Paragraph("CORRECTION DÉTAILLÉE : PROBLÈMES DE TRANSPORT & ÉQUATIONS DIFFÉRENTIELLES", st['title']))
    story.append(Paragraph("Outils Mathématiques 3 • Spé ESME • Exercices de Synthèse et Problèmes de Raccordement", st['sub']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#4F46E5'), spaceAfter=10))

    # --- Exercice 3.8 ---
    story.append(Paragraph("Exercice 3.8 : Équations aux Dérivées Partielles de Transport (Méthode des Caractéristiques)", st['h1']))
    story.append(Paragraph("La méthode des courbes caractéristiques consiste à trouver les courbes le long desquelles l'EDP se réduit à un système d'équations différentielles ordinaires (EDO).", st['body']))

    # Question 1
    story.append(Paragraph("<b>Question 1 : Résolution de &part;<sub>t</sub> u + (x + t)&part;<sub>x</sub> u = t<sup>2</sup> avec u(x, 0) = x</b>", st['h2']))
    story.append(Paragraph("• <b>Étape 1 : Système caractéristique</b><br/>"
                           "Paramétrons les courbes caractéristiques par le paramètre s. On pose :<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;dt/ds = 1 &rArr; t(s) = s (avec t(0) = 0).<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;dx/ds = x + t = x + s, avec x(0) = x<sub>0</sub>.<br/>"
                           "• <b>Étape 2 : Résolution de l'EDO en x(s)</b><br/>"
                           "L'équation x' - x = s a pour solution homogène x<sub>h</sub>(s) = C e<sup>s</sup>.<br/>"
                           "Une solution particulière polynomiale x<sub>p</sub>(s) = As + B donne A - (As+B) = s &rArr; A = -1, B = -1.<br/>"
                           "Donc x(s) = C e<sup>s</sup> - s - 1. En s = 0 : x(0) = C - 1 = x<sub>0</sub> &rArr; C = x<sub>0</sub> + 1.<br/>"
                           "D'où la trajectoire caractéristique : <b>x(s) = (x<sub>0</sub> + 1)e<sup>s</sup> - s - 1</b>.<br/>"
                           "Comme s = t, on inverse pour exprimer l'abscisse initiale x<sub>0</sub> en fonction de (x, t) :<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;<b>x<sub>0</sub> = (x + t + 1)e<sup>-t</sup> - 1</b>.", st['body']))

    story.append(Paragraph("• <b>Étape 3 : Évolution de u le long de la caractéristique</b><br/>"
                           "du/ds = t(s)<sup>2</sup> = s<sup>2</sup> &rArr; u(s) = u(0) + &int;<sub>0</sub><sup>s</sup> &tau;<sup>2</sup> d&tau; = u(x<sub>0</sub>, 0) + s<sup>3</sup>/3.<br/>"
                           "Avec la condition initiale u(x, 0) = x, on a u(x<sub>0</sub>, 0) = x<sub>0</sub>.<br/>"
                           "Donc u(s) = x<sub>0</sub> + s<sup>3</sup>/3.<br/>"
                           "En substituant x<sub>0</sub> et s = t, on obtient la solution analytique exacte :", st['body']))
    story.append(Spacer(1, 2))
    story.append(boxed_res("u(x, t) = (x + t + 1) e<sup>-t</sup> - 1 + t<sup>3</sup> / 3<br/>"
                           "<i>Vérification : u(x, 0) = (x + 1) - 1 = x (Vérifié).<br/>"
                           "&part;<sub>t</sub> u + (x+t)&part;<sub>x</sub> u = -(x+t)e<sup>-t</sup> + t<sup>2</sup> + (x+t)e<sup>-t</sup> = t<sup>2</sup> (Vérifié).</i>", st))
    story.append(Spacer(1, 8))

    # Question 2
    story.append(Paragraph("<b>Question 2 : Résolution de &part;<sub>t</sub> u + [x / (1 + t<sup>2</sup>)]&part;<sub>x</sub> u = x / (1 + t<sup>2</sup>) avec u(x, 0) = cos(x)</b>", st['h2']))
    story.append(Paragraph("• Caractéristiques : dt/ds = 1 &rArr; t = s.<br/>"
                           "dx/ds = x / (1 + s<sup>2</sup>) &rArr; dx/x = ds / (1 + s<sup>2</sup>) &rArr; ln|x| = arctan(s) + C.<br/>"
                           "En s = 0, x(0) = x<sub>0</sub>, d'où <b>x(s) = x<sub>0</sub> e<sup>arctan(s)</sup> &rArr; x<sub>0</sub> = x e<sup>-arctan(t)</sup></b>.<br/>"
                           "• Évolution de u : du/ds = x(s) / (1 + s<sup>2</sup>) = x<sub>0</sub> e<sup>arctan(s)</sup> / (1 + s<sup>2</sup>).<br/>"
                           "Par intégration directe : &int;<sub>0</sub><sup>s</sup> e<sup>arctan(&tau;)</sup> / (1 + &tau;<sup>2</sup>) d&tau; = [e<sup>arctan(&tau;)</sup>]<sub>0</sub><sup>s</sup> = e<sup>arctan(s)</sup> - 1.<br/>"
                           "Donc u(s) = u<sub>0</sub>(x<sub>0</sub>) + x<sub>0</sub>(e<sup>arctan(s)</sup> - 1) = cos(x<sub>0</sub>) + x - x<sub>0</sub>.", st['body']))
    story.append(Spacer(1, 2))
    story.append(boxed_res("u(x, t) = cos( x e<sup>-arctan(t)</sup> ) + x - x e<sup>-arctan(t)</sup>", st))
    story.append(Spacer(1, 8))

    # Question 3
    story.append(Paragraph("<b>Question 3 : Résolution de &part;<sub>t</sub> u + (x + t)&part;<sub>x</sub> u = t avec u(x, 0) = 2x</b>", st['h2']))
    story.append(Paragraph("Mêmes caractéristiques qu'à la question 1 : x<sub>0</sub> = (x + t + 1)e<sup>-t</sup> - 1.<br/>"
                           "du/ds = s &rArr; u(s) = u<sub>0</sub>(x<sub>0</sub>) + s<sup>2</sup>/2 = 2 x<sub>0</sub> + s<sup>2</sup>/2.", st['body']))
    story.append(Spacer(1, 2))
    story.append(boxed_res("u(x, t) = 2 [ (x + t + 1) e<sup>-t</sup> - 1 ] + t<sup>2</sup> / 2", st))
    story.append(Spacer(1, 10))

    # Page Break for Exercices 2.7 & 3.2
    story.append(PageBreak())

    # --- Exercice 2.7 ---
    story.append(Paragraph("Exercice 2.7 : Problèmes de Raccordement de Solutions sur &reals;", st['h1']))
    story.append(Paragraph("<b>1. Résolution sur &reals; de t y' - 2y = t<sup>3</sup> :</b><br/>"
                           "• Pour t &ne; 0 : y' - (2/t)y = t<sup>2</sup>.<br/>"
                           "Solution homogène : y<sub>h</sub>(t) = C t<sup>2</sup>.<br/>"
                           "Variation de la constante : C'(t) t<sup>2</sup> = t<sup>2</sup> &rArr; C'(t) = 1 &rArr; C(t) = t.<br/>"
                           "D'où y(t) = C<sub>1</sub> t<sup>2</sup> + t<sup>3</sup> sur ]0, +&infin;[ et y(t) = C<sub>2</sub> t<sup>2</sup> + t<sup>3</sup> sur ]-&infin;, 0[.<br/>"
                           "• <b>Raccordement en t = 0 :</b><br/>"
                           "lim<sub>t&rarr;0</sub> y(t) = 0, donc y(0) = 0.<br/>"
                           "Dérivabilité en 0 : [y(t) - y(0)] / t = C t + t<sup>2</sup> &rarr; 0 quand t &rarr; 0.<br/>"
                           "Donc y'(0) = 0. En réinjectant dans l'EDO : 0 &middot; y'(0) - 2y(0) = 0 = 0<sup>3</sup>, ce qui est toujours vérifié !<br/>"
                           "Les constantes C<sub>1</sub> et C<sub>2</sub> peuvent être arbitraires et différentes.", st['body']))
    story.append(Spacer(1, 2))
    story.append(boxed_res("Les solutions sur &reals; sont y(t) = C<sub>1</sub> t<sup>2</sup> + t<sup>3</sup> pour t &ge; 0, et y(t) = C<sub>2</sub> t<sup>2</sup> + t<sup>3</sup> pour t &lt; 0 (C<sub>1</sub>, C<sub>2</sub> &isin; &reals;).", st))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>2. Résolution sur &reals; de t<sup>2</sup> y' - y = 0 :</b><br/>"
                           "• Pour t &ne; 0 : y'/y = 1/t<sup>2</sup> &rArr; y(t) = C e<sup>-1/t</sup>.<br/>"
                           "Sur ]0, +&infin;[ : quand t &rarr; 0<sup>+</sup>, -1/t &rarr; -&infin;, donc e<sup>-1/t</sup> &rarr; 0.<br/>"
                           "Sur ]-&infin;, 0[ : quand t &rarr; 0<sup>-</sup>, -1/t &rarr; +&infin;, donc e<sup>-1/t</sup> &rarr; +&infin; !<br/>"
                           "Pour assurer la continuité en t = 0, il est impératif que C = 0 sur ]-&infin;, 0[.<br/>"
                           "Par ailleurs, en 0<sup>+</sup> : lim [e<sup>-1/t</sup> - 0]/t = 0 par croissances comparées, la fonction est de classe C<sup>&infin;</sup> en 0.", st['body']))
    story.append(Spacer(1, 2))
    story.append(boxed_res("Solutions sur &reals; : y(t) = C e<sup>-1/t</sup> pour t &gt; 0, et y(t) = 0 pour t &le; 0 (C &isin; &reals;).", st))
    story.append(Spacer(1, 10))

    # --- Exercice 3.2 ---
    story.append(Paragraph("Exercice 3.2 : Problème de Cauchy non-linéaire", st['h1']))
    story.append(Paragraph("<b>Énoncé :</b> Résoudre le problème de Cauchy y' = t e<sup>t<sup>2</sup></sup> / cos<sup>2</sup>(y) avec y(0) = 0.<br/>"
                           "• <b>Application du théorème de Cauchy-Lipschitz :</b><br/>"
                           "La fonction f(t, y) = t e<sup>t<sup>2</sup></sup> / cos<sup>2</sup>(y) est définie et de classe C<sup>&infin;</sup> sur &reals; &times; ]-&pi;/2, &pi;/2[.<br/>"
                           "D'après le théorème de Cauchy-Lipschitz, il existe une unique solution maximale y(t) passant par (0, 0).<br/>"
                           "• <b>Séparation des variables et intégration :</b><br/>"
                           "cos<sup>2</sup>(y) dy = t e<sup>t<sup>2</sup></sup> dt.<br/>"
                           "En intégrant entre 0 et y(t) :<br/>"
                           "&int;<sub>0</sub><sup>y</sup> cos<sup>2</sup>(u) du = &int;<sub>0</sub><sup>y</sup> [ (1 + cos(2u)) / 2 ] du = y/2 + sin(2y)/4.<br/>"
                           "&int;<sub>0</sub><sup>t</sup> s e<sup>s<sup>2</sup></sup> ds = [ (1/2) e<sup>s<sup>2</sup></sup> ]<sub>0</sub><sup>t</sup> = (e<sup>t<sup>2</sup></sup> - 1) / 2.<br/>"
                           "En multipliant par 4 :", st['body']))
    story.append(Spacer(1, 2))
    story.append(boxed_res("Relation implicite exacte : 2 y(t) + sin( 2 y(t) ) = 2 ( e<sup>t<sup>2</sup></sup> - 1 )<br/>"
                           "<i>Valable sur l'intervalle maximal où |y(t)| &lt; &pi;/2. En t = 0 : 0 + sin(0) = 0 = 2(1-1) (Vérifié).</i>", st))

    doc.build(story)
    print(f"✔ Solution Outils Maths générée : {pdf_out}")

def main():
    sol_out = TEMP_DIR / "Solution_Equations_Diff_Transports.pdf"
    build_pdf(sol_out)
    
    target_pdf = BASE_DIR / "courses_data" / "OUTILSMATH3" / "Cours_26-27_Outils_mathmatiqu..._.79258" / "Fichier_Equations_diffrentiel..._.79270" / "content" / "Equations différentielles_Problèmes de transports.pdf"
    
    if target_pdf.exists():
        # Append solution
        writer = pypdf.PdfWriter()
        with open(target_pdf, "rb") as f_s, open(sol_out, "rb") as f_sol:
            r = pypdf.PdfReader(f_s)
            for p in r.pages:
                writer.add_page(p)
            r_sol = pypdf.PdfReader(f_sol)
            for p in r_sol.pages:
                writer.add_page(p)
                
            temp_out = target_pdf.parent / "temp_merged.pdf"
            with open(temp_out, "wb") as f_o:
                writer.write(f_o)
        temp_out.replace(target_pdf)
        print(f"✔ Corrigé fusionné avec succès à la suite de : {target_pdf.name} (Total: {len(writer.pages)} pages)")
    else:
        print(f"Fichier cible introuvable : {target_pdf}")

if __name__ == "__main__":
    main()
