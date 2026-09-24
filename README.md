# 🎓 Portail ESME Spé (S03 - 2026/2027)

> Portail autonome et interactif regroupant les cours, TD, TP et annales d'examens corrigés pour la promotion **Ingénieur Spé (Semestre 3)** de l'**ESME Paris**.

🌐 **Accès au site en ligne :** [**https://arture463.github.io/esme-spe-2026/**](https://arture463.github.io/esme-spe-2026/)

---

## 🚀 Lancement Local (Hors-ligne)

- **Windows :** Double-cliquez sur `Lancer_Portail.bat` (accessible sur `http://localhost:8000`).
- **Mac / Linux :** Double-cliquez sur `Lancer_Portail_Mac.command`.

---

## 🗂️ Les 12 Matières Réparties par UE

- **UE1 : Mathématiques & Signal**
  - `MATHFONDA3` : Mathématiques Fondamentales 3 (Séries numériques, espaces vectoriels normés, colles, examens corrigés)
  - `OUTILSMATH3` : Outils Mathématiques 3 (Calcul différentiel, intégrales multiples, EDP, MidTerms et examens)
  - `ANANUM` : Analyse Numérique (Norme IEEE 754, dérivation numérique, notebooks Python Jupyter)
  - `SIGNAUXSYS` : Signaux & Systèmes (Régimes transitoires, ARQS, examens et corrigés détaillés)
- **UE2 : Sciences de l'Ingénieur & Environnement**
  - `SYSTECH3` : Systèmes Technologiques 3 (Automatique, schémas-blocs, critères de Routh, TD et examens)
  - `MECAFLU` : Mécanique des Fluides (5 chapitres complets, statique, réels, parfaits, ondes, annales résolues)
  - `GESTPROJ` : Gestion de Projet (WBS, diagramme de Gantt, gestion des risques)
  - `ENJEUXENV1` : Enjeux Environnementaux 1 (GIEC, cycle du carbone, biodiversité, banque d'annales chapitres 1 à 6)
- **UE3 : Numérique, Électronique & Langues**
  - `ALGOAV2` : Algorithmique Avancée 2 (Python avancé, POO, APP1 et APP2)
  - `ELECANA1` : Électronique Analogique 1 & 2 (Diodes, transistors, AOP, TP SPICE, MidTerms et examens finaux)
  - `ANG` : Anglais Professionnel (Syllabus officiels, communication technique)
- **UE4 : Entreprise & Management**
  - `GESTENT1` : Gestion d'Entreprise 1 (Chaîne de valeur, bilan, initiation à la comptabilité)

---

## 🔄 Workflow de Mise à Jour & Synchronisation

Pour ajouter un nouveau cours ou actualiser le site :

1. **Synchroniser avec `git pull` :**
   ```bash
   git pull
   ```
2. **Ajouter le fichier :** Déposez le nouveau document dans `courses_data/<MATIERE>/`.
3. **Mettre à jour l'index :** Double-cliquez sur `Mettre_A_Jour.bat` (ou exécutez `python build_master_index.py`).
4. **Publier en ligne :**
   ```bash
   git add .
   git commit -m "Ajout de nouveaux cours"
   git push
   ```
   *Le site en ligne GitHub Pages est actualisé automatiquement en direct.*
