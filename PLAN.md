# PLAN — APP1 Morpion IA

## 1) Compréhension du problème
- Définir le périmètre : morpion 3x3 avec IA Minimax.
- Identifier les sorties attendues (scores, suites idéales, modes de jeu, niveaux).
- Clarifier les contraintes de complexité (profondeur de recherche).

## 2) Découpage technique
- Représentation du plateau : liste de 9 cases.
- Génération d’arbre : expansion des coups possibles.
- Évaluation : score terminal + heuristique intermédiaire.
- Minimax : propagation des scores.
- Interfaces : console + GUI (Tkinter).

## 3) Plan d’action (phases)
### A. Séance “aller”
- Répartition des rôles.
- Lecture du sujet et identification des objectifs.
- Liste des questions/risques.
- Plan de livrables.

### B. Travail individuel
- Implémenter fonctions clés (règles, minimax, évaluation).
- Préparer exemples/explications.
- Tests simples et cas limites.

### C. Séance “retour”
- Mise en commun des résultats.
- Validation des fonctionnalités.
- Finalisation des livrables (README, PLAN, KANBAN).

## 4) Backlog priorisé
1. IA Minimax fonctionnelle + évaluation.
2. Modes de jeu (JvJ, JvIA, IAvIA).
3. Affichage scores d’une génération + min/max.
4. Suite idéale de coups (IA gagne / adversaire gagne).
5. Niveaux de difficulté (profondeur).
6. Bonus : aligner 4.

## 5) Tests à prévoir
- Victoire IA / victoire joueur / match nul.
- Profondeur faible vs élevée.
- Cas limites : plateau plein, coup illégal, entrée invalide.
