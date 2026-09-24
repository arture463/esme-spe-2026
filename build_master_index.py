import os
import sys
import json
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = Path(__file__).parent.resolve()
COURSES_DATA_DIR = PROJECT_DIR / "courses_data"
JSON_INDEX_PATH = PROJECT_DIR / "courses_index.json"
JS_DATA_PATH = PROJECT_DIR / "courses_data.js"

UE_MAPPING = {
    "MATHFONDA3": {
        "code": "MATHFONDA3", "ue": "UE1",
        "name": "Mathématiques Fondamentales 3",
        "desc": "Séries numériques, espaces vectoriels normés, suites et séries de fonctions, développements asymptotiques",
        "icon": "calculator", "color": "indigo"
    },
    "OUTILSMATH3": {
        "code": "OUTILSMATH3", "ue": "UE1",
        "name": "Outils Mathématiques 3",
        "desc": "Calcul différentiel, équations différentielles, intégrales multiples, analyse vectorielle, EDP de transport",
        "icon": "sigma", "color": "blue"
    },
    "ANANUM": {
        "code": "ANANUM", "ue": "UE1",
        "name": "Analyse Numérique",
        "desc": "Représentation binaire, IEEE 754, recherche de zéros, dérivation/intégration numérique, équations différentielles (Euler, Runge-Kutta), inversion matricielle (Jacobi)",
        "icon": "binary", "color": "cyan"
    },
    "SIGNAUXSYS": {
        "code": "SIGNAUXSYS", "ue": "UE1",
        "name": "Signaux et Systèmes",
        "desc": "Électrocinétique, régimes transitoires des circuits du 1er et 2nd ordre, transformée de Laplace, filtrage linéaire",
        "icon": "activity", "color": "sky"
    },
    "SYSTECH3": {
        "code": "SYSTECH3", "ue": "UE2",
        "name": "Systèmes Technologiques 3",
        "desc": "Automatique linéaire continue et invariante (SLCI), modélisation des signaux, schémas-blocs, identification (Strejc, Broida), stabilité (Routh, Bode), MATLAB & Simulink",
        "icon": "cpu", "color": "amber"
    },
    "MECAFLU": {
        "code": "MECAFLU", "ue": "UE2",
        "name": "Mécanique des Fluides",
        "desc": "Statique des fluides (Archimède, baromètre, barrages, forces pressantes, oscillations), dynamique des fluides parfaits et réels",
        "icon": "droplets", "color": "teal"
    },
    "GESTPROJ": {
        "code": "GESTPROJ", "ue": "UE2",
        "name": "Gestion de Projet",
        "desc": "Management de projet, cadrage, planification WBS/Gantt, exécution, pilotage des risques, clôture et templates officiels",
        "icon": "kanban", "color": "emerald"
    },
    "ENJEUXENV1": {
        "code": "ENJEUXENV1", "ue": "UE2",
        "name": "Enjeux Environnementaux 1",
        "desc": "Changement climatique (GIEC), cycle du carbone, érosion de la biodiversité, extraction minière et transition écologique",
        "icon": "leaf", "color": "green"
    },
    "ALGOAV2": {
        "code": "ALGOAV2", "ue": "UE3",
        "name": "Algorithmique Avancée 2",
        "desc": "Programmation Python avancée, listes en compréhension, fonctions lambda, récursivité, complexité O(n), POO (classes, héritage), cryptographie (RSA)",
        "icon": "code-2", "color": "violet"
    },
    "ELECANA1": {
        "code": "ELECANA1", "ue": "UE3",
        "name": "Électronique Analogique 1",
        "desc": "Diodes de redressement et Zener, transistors bipolaires et MOS, amplificateurs opérationnels (AOP)",
        "icon": "zap", "color": "orange"
    },
    "ANG": {
        "code": "ANG", "ue": "UE3",
        "name": "Anglais Professionnel",
        "desc": "Communication technique en anglais d'ingénieur, préparation aux certifications internationales",
        "icon": "languages", "color": "rose"
    },
    "GESTENT1": {
        "code": "GESTENT1", "ue": "UE4",
        "name": "Gestion d'Entreprise 1",
        "desc": "Comptabilité générale, bilan, compte de résultat, analyse fonctionnelle (FRNG, BFR, Trésorerie), soldes intermédiaires de gestion (SIG)",
        "icon": "briefcase", "color": "fuchsia"
    }
}

EXCLUDED_EXT = {
    'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'bmp', 'webp',
    'css', 'js', 'map', 'html', 'htm', 'url', 'ini'
}

def format_size(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.1f} MB"

def normalize_text(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8').lower()

def get_clean_doc_info(subj_code, fname, rel_path):
    fn_lower = fname.lower()
    fn_norm = normalize_text(fname)
    
    doc_type = "Cours"
    section = "Supports de Cours"
    clean_title = fname.rsplit('.', 1)[0]
    origin = "Tous campus / Tronc Commun"
    order = 50

    # ==================== MECAFLU ====================
    if subj_code == "MECAFLU":
        if "partie 1" in fn_norm or "chapitre 1" in fn_norm and "etud" in fn_norm:
            clean_title = "Chapitre 1 : Statique des Fluides (Support Complet Étudiant)"
            doc_type = "Cours"; section = "Cours Magistral"; order = 1
        elif "chapitre 2" in fn_norm or "parfaits" in fn_norm:
            clean_title = "Chapitre 2 : Mécanique des Fluides Parfaits (Bernoulli & Débits)"
            doc_type = "Cours"; section = "Cours Magistral"; order = 2
        elif "chapitre 3" in fn_norm or "reels" in fn_norm:
            clean_title = "Chapitre 3 : Mécanique des Fluides Réels (Viscosité & Navier-Stokes)"
            doc_type = "Cours"; section = "Cours Magistral"; order = 3
        elif "chapitre 4" in fn_norm or "acoustiques" in fn_norm:
            clean_title = "Chapitre 4 : Perturbations & Ondes Acoustiques dans les Fluides"
            doc_type = "Cours"; section = "Cours Magistral"; order = 4
        elif "chapitre 5" in fn_norm or "electromagnetique" in fn_norm:
            clean_title = "Chapitre 5 : Ondes Électromagnétiques & Fonctions d'Onde"
            doc_type = "Cours"; section = "Cours Magistral"; order = 5
        elif "mf1ch1" in fn_norm:
            clean_title = "Fiche Synthèse Chapitre 1 : Hydrostatique & Poussée d'Archimède"
            doc_type = "Cours"; section = "Fiches Synthétiques"; order = 10
        elif "mf1ch2" in fn_norm:
            clean_title = "Fiche Synthèse Chapitre 2 : Fluides Parfaits & Théorème de Bernoulli"
            doc_type = "Cours"; section = "Fiches Synthétiques"; order = 11
        elif "mf1ch3" in fn_norm:
            clean_title = "Fiche Synthèse Chapitre 3 : Équations de Navier-Stokes & Pertes de Charge"
            doc_type = "Cours"; section = "Fiches Synthétiques"; order = 12
        elif "corrige_merged" in fn_norm:
            clean_title = "Recueil Complet des Corrigés Fusionnés de Mécanique des Fluides"
            doc_type = "TD & Corrigé"; section = "Travaux Dirigés"; order = 15
        elif "spe_midterms" in fn_norm:
            clean_title = "MidTerm 2024-2025 : Épreuve Mécanique des Fluides Spé S03 (avec Corrigé)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 20
        elif "meca des fluides 2024-2025" in fn_norm:
            clean_title = "Examen Final 2024-2025 : Mécanique des Fluides (Correction Détaillée)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 21
        elif "meca_fluide_midterms_correctionv1" in fn_norm or "correction midterm 2024_2025" in fn_norm:
            clean_title = "MidTerm 2024-2025 : Mécanique des Fluides (Correction Officielle V1)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 22
        elif "enonce midterm 2024" in fn_norm:
            clean_title = "MidTerm 2024-2025 : Mécanique des Fluides (Énoncé Officiel)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 23
        elif "td1" in fn_norm:
            clean_title = "TD 1 : Statique des Fluides (12 Exercices Résolus Pas-à-Pas)"
            doc_type = "TD & Corrigé"; section = "Travaux Dirigés"; order = 14

    # ==================== ELECANA1 ====================
    elif subj_code == "ELECANA1":
        if "ea1-midterm-2025-2026-fr-bonnes-reponses" in fn_norm:
            clean_title = "MidTerm 2025-2026 : Électronique Analogique 1 (Corrigé & Bonnes Réponses)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 1
        elif "ea1-midterm-2025-2026-fr" in fn_norm:
            clean_title = "MidTerm 2025-2026 : Électronique Analogique 1 (Énoncé Sujet)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 2
        elif "ea1-midterm1-2023-2024" in fn_norm:
            clean_title = "MidTerm 2023-2024 : Électronique Analogique 1 (Corrigé Intégral)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 3
        elif "ea2-examen-final-questions-2025-2026" in fn_norm:
            clean_title = "Examen Final 2025-2026 : Électronique Analogique (Énoncé des Questions)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 4
        elif "ea2-examen-final-questions-2024-2025" in fn_norm:
            clean_title = "Examen Final 2024-2025 : Électronique Analogique (Énoncé des Questions)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 5
        elif "ea2-examen-final-reponses-2024-2025" in fn_norm:
            clean_title = "Examen Final 2024-2025 : Corrigé Officiel & Réponses Détaillées"
            doc_type = "Examen"; section = "Examens & Annales"; order = 6
        elif "ea2-examen-final-bis" in fn_norm:
            clean_title = "Examen Final Bis (Rattrapage) 2024-2025 : Électronique Analogique"
            doc_type = "Examen"; section = "Examens & Annales"; order = 7
        elif "ea2-corriges-td" in fn_norm:
            clean_title = "TD 1 à 5 : Diodes, Transistors Bipolaires et MOS (Corrigé Complet)"
            doc_type = "TD & Corrigé"; section = "Travaux Dirigés"; order = 10
        elif "ea2-td9" in fn_norm:
            clean_title = "TD 9 : Amplificateurs Opérationnels & Rétroaction"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 14
        elif "ea2-td10" in fn_norm:
            clean_title = "TD 10 : Filtres Actifs & Stabilité des Montages AOP"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 15
        elif "ea2-tp3-examen-simulation" in fn_norm:
            clean_title = "TP 3 : Simulation SPICE & Examen Pratique Blanc"
            doc_type = "TP"; section = "Travaux Pratiques"; order = 20
        elif "ea1-cr-devoir-tp-diodes-legas" in fn_norm:
            clean_title = "Compte-Rendu Devoir TP Diodes (Rapport Spé D Arthur Legas)"
            doc_type = "TP"; section = "Travaux Pratiques"; order = 21
        elif "ea1-cr-devoir-tp-diodes" in fn_norm:
            clean_title = "Compte-Rendu Devoir TP Diodes (Exemple Validé Enseignant)"
            doc_type = "TP"; section = "Travaux Pratiques"; order = 22
        elif "tp 3 elec ana" in fn_norm:
            clean_title = "TP 3 Électronique Analogique : Document de Préparation"
            doc_type = "TP"; section = "Travaux Pratiques"; order = 23
        elif "fiche_revision_diodes_arthur_complete" in fn_norm:
            clean_title = "Fiche Mémo Complète : Théorie des Diodes et Régimes de Polarisation"
            doc_type = "Cours"; section = "Fiches Mémo & Révisions"; order = 30
        elif "fiche_revision_diodes_arthur" in fn_norm:
            clean_title = "Fiche Mémo Rapide : Caractéristiques I-V et Formules Clés"
            doc_type = "Cours"; section = "Fiches Mémo & Révisions"; order = 31

    # ==================== MATHFONDA3 ====================
    elif subj_code == "MATHFONDA3":
        if "td1" in fn_norm:
            clean_title = "TD 1 : Séries Numériques, Critères de Convergence (Énoncé & Exercices)"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 1
        elif "td2" in fn_norm:
            clean_title = "TD 2 : Séries Alternées, Règle de d'Alembert et Cauchy"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 2
        elif "questions de cours" in fn_norm or "colle 1" in fn_norm:
            clean_title = "Colle 1 : Questions de Cours & Démonstrations Théorème de Riemann"
            doc_type = "TD"; section = "Interrogations & Colles"; order = 5
        elif "interro sped" in fn_norm:
            clean_title = "Interrogation Spé D : Séries Entières R=2 et Développements Asymptotiques (Corrigé)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 10
        elif "interro spe" in fn_norm:
            clean_title = "Interrogation Spé A-B : Suites et Séries Numériques"
            doc_type = "Examen"; section = "Examens & Annales"; order = 11
        elif "corr_examen_math_fond" in fn_norm:
            clean_title = "Examen Final 2024-2025 : Maths Fondamentales Spé (Corrigé Détaillé)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 12
        elif "corr_examen_final" in fn_norm:
            clean_title = "Examen Final 2024-2025 : Correction Validée de l'Épreuve"
            doc_type = "Examen"; section = "Examens & Annales"; order = 13

    # ==================== OUTILSMATH3 ====================
    elif subj_code == "OUTILSMATH3":
        if "2024-2025 midterms outils maths" in fn_norm:
            clean_title = "MidTerm 2024-2025 : Outils Mathématiques Spé S03 (Énoncé & Sujet)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 1
        elif "correction midterms outils maths" in fn_norm:
            clean_title = "MidTerm 2024-2025 : Corrigé Officiel Complet Outils Maths Spé"
            doc_type = "Examen"; section = "Examens & Annales"; order = 2
        elif "correction outils maths" in fn_norm:
            clean_title = "Examen 2024-2025 : Corrigé Officiel Outils Mathématiques"
            doc_type = "Examen"; section = "Examens & Annales"; order = 3
        elif "cc4_om4" in fn_norm:
            clean_title = "Contrôle Continu CC4 : Équations Différentielles & Séries de Fourier (Corrigé)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 4
        elif "2023-2024 examen outils" in fn_norm:
            clean_title = "Examen 2023-2024 : Épreuve Complète Outils Maths Spé"
            doc_type = "Examen"; section = "Examens & Annales"; order = 5
        elif "2023-2024 cor examen" in fn_norm:
            clean_title = "Examen 2023-2024 : Corrigé Détaillé de l'Épreuve"
            doc_type = "Examen"; section = "Examens & Annales"; order = 6
        elif "mt_1_2025_2026" in fn_norm:
            clean_title = "MidTerm 1 2025-2026 : Solutions Analytiques Détaillées"
            doc_type = "Examen"; section = "Examens & Annales"; order = 7
        elif "probleme de synthese complexe" in fn_norm or "2025-2026 probleme de synthese" in fn_norm:
            clean_title = "Problème de Synthèse Complexe 2025-2026 (Intégration Multiple & EDP)"
            doc_type = "TD"; section = "Problèmes de Synthèse"; order = 10
        elif "problemes_de_synthese" in fn_norm or "problemes de synthese" in fn_norm:
            clean_title = "Recueil de Problèmes de Synthèse : Analyse Vectorielle & Théorème de Stokes"
            doc_type = "TD"; section = "Problèmes de Synthèse"; order = 11
        elif "cauchy-lipschitz" in fn_norm:
            clean_title = "TD-TG Approfondi : Fonctions Lipschitziennes & Théorème de Cauchy-Lipschitz"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 15
        elif "om1ch2" in fn_norm:
            clean_title = "Fiche Mémo Chapitre 2 : Calcul Différentiel et Intégrales Doubles"
            doc_type = "Cours"; section = "Supports de Cours"; order = 20

    # ==================== SIGNAUXSYS ====================
    elif subj_code == "SIGNAUXSYS":
        if "2025-2026-examen-reponses" in fn_norm:
            clean_title = "Examen 2025-2026 : Corrigé Officiel et Barème des Réponses"
            doc_type = "Examen"; section = "Examens & Annales"; order = 1
        elif "2025-2026-examen" in fn_norm:
            clean_title = "Examen 2025-2026 : Signaux et Systèmes (Épreuve Complète)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 2
        elif "examen-signaux-2024-2025" in fn_norm:
            clean_title = "Examen 2024-2025 : Corrigé & Réponses Détaillées avec Barème"
            doc_type = "Examen"; section = "Examens & Annales"; order = 3
        elif "chapitre - 5 - arqs" in fn_norm or "chapitre 5 - arqs" in fn_norm:
            clean_title = "Chapitre 5 : Approximation des Régimes Quasi-Stationnaires (ARQS)"
            doc_type = "Cours"; section = "Supports de Cours"; order = 10
        elif "td5 - arqs" in fn_norm:
            clean_title = "TD 5 : Applications de l'ARQS et Circuits Électrocinétiques"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 11

    # ==================== SYSTECH3 ====================
    elif subj_code == "SYSTECH3":
        if "spe st4 final exam" in fn_norm:
            clean_title = "Final Exam 2026 : Systèmes Technologiques Spé (Épreuve Complète)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 1
        elif "sup_systemes techniques" in fn_norm:
            clean_title = "MidTerms Spé / Sup : Systèmes Techniques avec Grille d'Évaluation"
            doc_type = "Examen"; section = "Examens & Annales"; order = 2
        elif "midterm des systemes" in fn_norm:
            clean_title = "MidTerm Systèmes Techniques : Automatique Continue & Stabilité"
            doc_type = "Examen"; section = "Examens & Annales"; order = 3
        elif "midtermes 2023-2024" in fn_norm:
            clean_title = "MidTerms 2023-2024 : Systèmes Techniques (Corrigé Intégral)"
            doc_type = "Examen"; section = "Examens & Annales"; order = 4
        elif "fe st2 2024" in fn_norm:
            clean_title = "Final Exam ST2 2024 : Épreuve d'Automatique et Modélisation"
            doc_type = "Examen"; section = "Examens & Annales"; order = 5
        elif "z-fonction de transfert" in fn_norm:
            clean_title = "Cours & Formulaire : Fonctions de Transfert & Transformée de Laplace"
            doc_type = "Cours"; section = "Supports de Cours"; order = 10
        elif "methode des blocs" in fn_norm:
            clean_title = "Guide Méthodologique : Réduction des Schémas-Blocs (Formule de Black)"
            doc_type = "Cours"; section = "Supports de Cours"; order = 11
        elif "torseur_action_mecanique" in fn_norm:
            clean_title = "Formulaire Mécanique : Torseurs des Actions Mécaniques et Liaisons"
            doc_type = "Cours"; section = "Supports de Cours"; order = 12
        elif "sequence 1" in fn_norm:
            clean_title = "Séquence 1 : Introduction aux Systèmes Asservis et Boucle Fermée"
            doc_type = "Cours"; section = "Supports de Cours"; order = 13
        elif "td_04_corrige_en" in fn_norm:
            clean_title = "TD 04 : Corrigé Officiel Critère de Routh-Hurwitz (Version Anglaise)"
            doc_type = "TD & Corrigé"; section = "Travaux Dirigés"; order = 21
        elif "td_04" in fn_norm:
            clean_title = "TD 04 : Stabilité des Systèmes SLCI (Critère de Routh-Hurwitz)"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 20
        elif "td_06" in fn_norm:
            clean_title = "TD 06 : Analyse Harmonique & Lieux de Transfert (Bode, Nyquist)"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 22
        elif "td3" in fn_norm:
            clean_title = "TD 03 : Réduction des Schémas Fonctionnels & Identification Indicielle"
            doc_type = "TD"; section = "Travaux Dirigés"; order = 23
        elif "fe_01_grille" in fn_norm:
            clean_title = "Fiche d'Évaluation FE01 : Modélisation des Systèmes Dynamiques"
            doc_type = "TD"; section = "Fiches d'Évaluation"; order = 30
        elif "fe_03_francais_grille" in fn_norm:
            clean_title = "Fiche d'Évaluation FE03 : Précision et Rapidité des Systèmes Asservis"
            doc_type = "TD"; section = "Fiches d'Évaluation"; order = 31

    # ==================== ANANUM ====================
    elif subj_code == "ANANUM":
        if "seance_02_repr_nombres_negatifs" in fn_norm:
            clean_title = "Séance 02 : Représentation Binaire (Complément à 2, Addition, Soustraction)"
            doc_type = "Cours"; section = "Arithmétique Binaire"; order = 2
        elif "seance_03_repr_nombres_reels" in fn_norm:
            clean_title = "Séance 03 : Norme IEEE 754 (Simple & Double Précision, Flottants)"
            doc_type = "Cours"; section = "Norme IEEE 754"; order = 3
        elif "td_03_repr_nombres_reels" in fn_norm:
            clean_title = "TD 03 : Exercices Python sur la Norme IEEE 754 (Notebook Jupyter)"
            doc_type = "TP"; section = "Norme IEEE 754"; order = 4
        elif "seance_05_derivation_numerique" in fn_norm:
            clean_title = "Séance 05 : Dérivation Numérique (Schémas Différences Finies)"
            doc_type = "Cours"; section = "Dérivation & Intégration"; order = 5
        elif "td_05_derivation_numerique" in fn_norm:
            clean_title = "TD 05 : TP Python Dérivation Numérique & Estimation d'Erreur"
            doc_type = "TP"; section = "Dérivation & Intégration"; order = 6

    # ==================== ENJEUXENV1 ====================
    elif subj_code == "ENJEUXENV1":
        if "chapitre 1" in fn_norm:
            clean_title = "Banque d'Examen Chapitre 1 : Introduction & Bilan Planétaire"
            doc_type = "Examen"; section = "Banque de Questions d'Examen"; order = 1
        elif "chapitre 2" in fn_norm:
            clean_title = "Banque d'Examen Chapitre 2 : Causes du Réchauffement Climatique & CO2"
            doc_type = "Examen"; section = "Banque de Questions d'Examen"; order = 2
        elif "chapitre 3" in fn_norm:
            clean_title = "Banque d'Examen Chapitre 3 : Érosion de la Biodiversité & Écosystèmes"
            doc_type = "Examen"; section = "Banque de Questions d'Examen"; order = 3
        elif "chapitre 4" in fn_norm:
            clean_title = "Banque d'Examen Chapitre 4 : Extraction Minière & Métaux de la Transition"
            doc_type = "Examen"; section = "Banque de Questions d'Examen"; order = 4
        elif "chapitre 5" in fn_norm:
            clean_title = "Banque d'Examen Chapitre 5 : Scénarios GIEC & Leviers d'Atténuation"
            doc_type = "Examen"; section = "Banque de Questions d'Examen"; order = 5
        elif "chapitre 6" in fn_norm:
            clean_title = "Banque d'Examen Chapitre 6 : Synthèse Globale & QCM de Révision"
            doc_type = "Examen"; section = "Banque de Questions d'Examen"; order = 6

    # ==================== GESTENT1 ====================
    elif subj_code == "GESTENT1":
        if "03_entrprise-agro-chaine-valeur" in fn_norm:
            clean_title = "Séance 03 : Analyse Stratégique & Chaîne de Valeur de l'Entreprise"
            doc_type = "Cours"; section = "Gestion Stratégique"; order = 1
        elif "ini a l'ent" in fn_norm:
            clean_title = "Support de Cours : Initiation à la Gestion et à la Comptabilité d'Entreprise"
            doc_type = "Cours"; section = "Comptabilité & Gestion"; order = 2
        elif "ini a lent bis" in fn_norm:
            clean_title = "Dossier d'Étude de Cas : Initiation à l'Entreprise (Synthèse)"
            doc_type = "TD"; section = "Études de Cas"; order = 3
        elif "oral initiation" in fn_norm:
            clean_title = "Soutenance Orale : Guide & Grille d'Évaluation Initiation à l'Entreprise"
            doc_type = "TD"; section = "Études de Cas"; order = 4

    # ==================== ANG ====================
    elif subj_code == "ANG":
        if "6230_20250616" in fn_norm:
            clean_title = "Syllabus Officiel Anglais Spé (S03 - 2025/2026)"
            doc_type = "Syllabus"; section = "Programme & Modalités"; order = 1
        elif "6230_20250617" in fn_norm:
            clean_title = "Syllabus Anglais Professionnel & Préparation Certifications"
            doc_type = "Syllabus"; section = "Programme & Modalités"; order = 2
        elif "6233" in fn_norm:
            clean_title = "Syllabus Anglais Ingénieur : Communication Technique & Débats"
            doc_type = "Syllabus"; section = "Programme & Modalités"; order = 3
        elif "6235" in fn_norm:
            clean_title = "Modalités d'Évaluation & Barèmes Anglais Semestre 3"
            doc_type = "Syllabus"; section = "Programme & Modalités"; order = 4

    # ==================== ALGOAV2 ====================
    elif subj_code == "ALGOAV2":
        if "app1" in fn_norm:
            clean_title = "APP 1 : Algorithmique Avancée & Structures de Données (Énoncé & Directives)"
            doc_type = "TP"; section = "Apprentissage Par Problème (APP)"; order = 1
        elif "app2_aa3" in fn_norm:
            clean_title = "APP 2 : Conception Orientée Objet & Algorithmes d'Optimisation"
            doc_type = "TP"; section = "Apprentissage Par Problème (APP)"; order = 2

    # ==================== GESTPROJ ====================
    elif subj_code == "GESTPROJ":
        if "quiz_master_projet" in fn_norm:
            clean_title = "Quiz Master Projet : Pilotage WBS, Diagramme de Gantt et Gestion des Risques"
            doc_type = "TD"; section = "Outils & Quiz de Gestion"; order = 1

    return clean_title, doc_type, section, origin, order

def main():
    print("=== GÉNÉRATION DU NOUVEAU CATALOGUE DE COURS STRUCTURÉ ===")
    
    indexed_subjects = {}
    for code, meta in UE_MAPPING.items():
        indexed_subjects[code] = {
            "code": code,
            "ue": meta["ue"],
            "name": meta["name"],
            "description": meta["desc"],
            "icon": meta["icon"],
            "color": meta["color"],
            "document_count": 0,
            "documents": []
        }

    all_docs = []
    seen_hashes = {}
    
    # Process courses_data
    for subj_code in UE_MAPPING.keys():
        s_dir = COURSES_DATA_DIR / subj_code
        if not s_dir.exists():
            continue
            
        for f in sorted(s_dir.rglob("*"), key=lambda x: x.name):
            if f.is_dir():
                continue
            ext = f.suffix.lstrip('.').lower()
            if ext in EXCLUDED_EXT or f.name.startswith('.'):
                continue
            if f.name in ["moodle.css", "icon.svg", "favicon.ico", "cours.png", "desktop.ini"]:
                continue
            if f.stat().st_size == 0:
                continue

            # Deduplicate identical files
            try:
                file_sig = f"{f.name.lower()}_{f.stat().st_size}"
                if file_sig in seen_hashes:
                    continue
                seen_hashes[file_sig] = True
            except:
                continue

            rel_path = f.relative_to(PROJECT_DIR).as_posix()
            title, dtype, section, origin, order = get_clean_doc_info(subj_code, f.name, rel_path)

            doc_entry = {
                "id": f"{subj_code}_{len(all_docs) + 1}",
                "title": title,
                "filename": f.name,
                "extension": ext,
                "size_bytes": f.stat().st_size,
                "size_formatted": format_size(f.stat().st_size),
                "subject_code": subj_code,
                "subject_name": UE_MAPPING[subj_code]["name"],
                "ue": UE_MAPPING[subj_code]["ue"],
                "section": section,
                "doc_type": dtype,
                "origin": origin,
                "order_priority": order,
                "relative_path": rel_path
            }

            all_docs.append(doc_entry)
            indexed_subjects[subj_code]["documents"].append(doc_entry)

    # Process EXAMENS_ANNALES explicitly into their real target subject
    exam_dir = COURSES_DATA_DIR / "EXAMENS_ANNALES"
    if exam_dir.exists():
        for ef in sorted(exam_dir.iterdir(), key=lambda x: x.name):
            if ef.is_dir() or ef.suffix.lstrip('.').lower() in EXCLUDED_EXT:
                continue
            fname = ef.name
            fn_l = fname.lower()
            
            # Match target subject
            if "outils maths" in fn_l:
                target_subj = "OUTILSMATH3"
                clean_title = "MidTerm 2024-2025 : Outils Mathématiques 3 Spé (avec Corrigé Officiel)"
            elif "ea1" in fn_l or "electronique" in fn_l:
                target_subj = "ELECANA1"
                clean_title = "MidTerm 2025-2026 : Électronique Analogique (avec Corrigé Officiel)"
            elif "interro" in fn_l:
                target_subj = "MATHFONDA3"
                clean_title = "Interrogation Spé D : Séries & Développements Asymptotiques (avec Corrigé)"
            elif "spe_midterms" in fn_l:
                target_subj = "MECAFLU"
                clean_title = "MidTerm 2024-2025 : Mécanique des Fluides Spé (avec Corrigé Officiel V1)"
            else:
                target_subj = "OUTILSMATH3"
                clean_title = fname.rsplit('.', 1)[0]

            rel_path = ef.relative_to(PROJECT_DIR).as_posix()
            doc_entry = {
                "id": f"{target_subj}_EXAM_{len(all_docs) + 1}",
                "title": clean_title,
                "filename": ef.name,
                "extension": ef.suffix.lstrip('.').lower(),
                "size_bytes": ef.stat().st_size,
                "size_formatted": format_size(ef.stat().st_size),
                "subject_code": target_subj,
                "subject_name": UE_MAPPING[target_subj]["name"],
                "ue": UE_MAPPING[target_subj]["ue"],
                "section": "Examens & Annales",
                "doc_type": "Examen",
                "origin": "Paris & National",
                "order_priority": 99,
                "relative_path": rel_path
            }

            all_docs.append(doc_entry)
            indexed_subjects[target_subj]["documents"].append(doc_entry)

    # Sort documents within each subject by order_priority then title
    for subj_code, subj in indexed_subjects.items():
        subj["documents"].sort(key=lambda d: (d.get("order_priority", 50), d["title"].lower()))
        subj["document_count"] = len(subj["documents"])

    # Global documents sorted by UE, subject, order_priority
    all_docs.sort(key=lambda d: (d["ue"], d["subject_code"], d.get("order_priority", 50), d["title"].lower()))

    total_size = sum(d["size_bytes"] for d in all_docs)

    index_data = {
        "school": "ESME",
        "promotion": "Ingénieur Spé (2ème année)",
        "semester": "Semestre 3 (S03)",
        "campus_user": "Paris",
        "total_documents": len(all_docs),
        "total_size_formatted": format_size(total_size),
        "total_subjects": len(indexed_subjects),
        "subjects": indexed_subjects,
        "all_documents": all_docs
    }

    # Write courses_index.json
    json_str = json.dumps(index_data, ensure_ascii=False, indent=2)
    JSON_INDEX_PATH.write_text(json_str, encoding="utf-8")
    print(f"✔ Fichier généré : {JSON_INDEX_PATH} ({len(all_docs)} documents)")

    # Write courses_data.js
    js_str = "window.COURSES_DATA = " + json_str + ";"
    JS_DATA_PATH.write_text(js_str, encoding="utf-8")
    print(f"✔ Fichier généré : {JS_DATA_PATH}")

if __name__ == "__main__":
    main()
