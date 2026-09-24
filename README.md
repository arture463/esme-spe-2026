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

## 👥 TRAVAIL COLLABORATIF À PLUSIEURS (RÈGLES IMPORTANTES)

Ce projet est conçu pour que **plusieurs étudiants travaillent et révisent ensemble** sur le même dépôt.

### ⚠️ Règle d'or absolue :
> **Toujours exécuter `git pull` avant de commencer à travailler** pour récupérer immédiatement les cours, TD ou corrections déposés par les camarades et éviter tout conflit.

### 📥 1. Installation pour un nouveau collaborateur
Le camarade clone le dépôt sur sa machine :
```bash
git clone https://github.com/arture463/esme-spe-2026.git
cd esme-spe-2026
```

### 🔄 2. Workflow à suivre pour chaque collaborateur
Chaque fois qu'un étudiant souhaite ajouter un document ou apporter des modifications :

1. **Synchroniser la version locale (OBLIGATOIRE) :**
   ```bash
   git pull origin main
   ```
2. **Déposer les nouveaux fichiers :**
   - Glisser les PDF dans le dossier de la matière (ex : `courses_data/MECAFLU/`).
3. **Mettre à jour l'index :**
   - Double-cliquer sur `Mettre_A_Jour.bat` (ce script effectue automatiquement un `git pull` puis réindexe tous les cours avec `build_master_index.py`).
4. **Envoyer le travail à tout le monde :**
   ```bash
   git add .
   git commit -m "Ajout du TD 3 de Maths (par [Votre Nom])"
   git push origin main
   ```

⚡ **Mise à jour instantanée :** Dès qu'un commit est poussé, le site public [**https://arture463.github.io/esme-spe-2026/**](https://arture463.github.io/esme-spe-2026/) est réactualisé en moins d'une minute pour toute la promotion !
