# APP1 — Morpion IA (Minimax)

## Contexte
Projet APP (Algorithmique avancée 2) : concevoir un jeu de morpion doté d’une IA de décision basée sur un arbre de jeu et l’algorithme Minimax.

## Objectifs fonctionnels
- Jouer au morpion contre l’ordinateur.
- Afficher les scores d’évaluation d’une génération (min/max inclus).
- Afficher une suite idéale de coups pour que l’IA gagne.
- Afficher une suite idéale de coups pour que l’adversaire gagne.
- Ajuster la difficulté via la profondeur de recherche (plus profond = plus lent).
- Simuler joueur vs joueur et ordinateur vs ordinateur.
- Bonus : généraliser à un jeu d’alignement de 4 (type puissance 4).

## Principes algorithmiques
- Générer l’arbre des configurations possibles depuis un état courant.
- Évaluer les feuilles (victoire/égalité/défaite + heuristique).
- Propager les scores :
  - Noeud MAX (tour de l’IA) : max des scores enfants.
  - Noeud MIN (tour de l’adversaire) : min des scores enfants.

## Évaluation (exemple)
- +1000 si l’IA gagne
- 0 si égalité
- -1000 si l’IA perd
- Heuristique : bonus/malus selon lignes/colonnes/diagonales (2 pions alignés, etc.).

## Structure du dépôt
- `principal.py` : version console
- `interface.py` : interface Tkinter
- `ia.py` : génération d’arbre + minimax
- `regles.py` : règles du jeu + fonction d’évaluation
- `outils.py` : utilitaires (racine, enfants, feuille)

## Exécuter
- Console : `python3 principal.py`
- GUI : `python3 interface.py`

## Équipe & rôles
Groupe APP :
- Maxime Maury
- Thibault Malmezat
- Ilyass Boukkad
- Titouan Vernier

Rôles :
- Porte‑parole : Thibault Malmezat
- Barreur : Ilyass Boukkad
- Activateur : Titouan Vernier
- Gardien du temps : Maxime Maury
- Faiseur de point : Thibault Malmezat
- Circulateur de parole : Maxime Maury
- Secrétaire : tout le monde
- Scribe : Titouan Vernier
- Intégrateur Git : Thibault Malmezat
- Testeur : tout le monde
- Architecte : tout le monde

## Livrables attendus
- Code fonctionnel du morpion + IA Minimax.
- Documentation (README, PLAN, KANBAN).
- Démonstration des fonctionnalités demandées.
