# APP1 - Morpion IA et Puissance 4

Projet Python avec interface graphique `CustomTkinter` autour de deux jeux de plateau :
- un morpion avec IA Minimax et outils d'analyse
- un module Puissance 4 avec IA simple a profondeur limitee

## Fonctionnalites

### Morpion
- mode `Joueur vs IA`
- mode `Joueur vs Joueur`
- mode `IA vs IA`
- difficulte liee a la profondeur de recherche
- panneau d'analyse integre dans l'interface :
  - affichage des scores d'une generation donnee
  - affichage du score minimum et du score maximum
  - affichage d'une suite ideale pour l'ordinateur ou pour l'adversaire

### Puissance 4
- ouverture depuis la fenetre principale du morpion
- mode `Joueur vs IA`
- mode `Joueur vs Joueur`
- mode `IA vs IA`
- difficulte liee a la profondeur de recherche

## Fichiers principaux
- `interface.py` : fenetre principale du morpion et acces au Puissance 4
- `ia.py` : IA du morpion + fonctions d'analyse
- `regles.py` : regles et evaluation du morpion
- `outils.py` : constantes et utilitaires communs
- `puissance4_interface.py` : interface du Puissance 4
- `puissance4_ia.py` : IA du Puissance 4
- `puissance4_regles.py` : regles et evaluation du Puissance 4

## Installation

Le projet utilise `CustomTkinter`.

Si besoin, installe la dependance avec :

```bash
python3 -m pip install customtkinter
```

## Lancer le projet

Depuis le dossier du projet :

```bash
python3 interface.py
```

## Utilisation

### Morpion
- choisis un mode de jeu
- regle la difficulte avec le curseur
- clique sur une case pour jouer
- utilise le panneau de droite pour :
  - afficher les scores d'une generation
  - voir le minimum et le maximum
  - afficher une suite ideale de coups

### Puissance 4
- clique sur `Ouvrir Puissance 4`
- choisis le mode et le niveau
- clique sur une colonne pour jouer

## Notes
- l'interface du morpion permet une analyse de generation de profondeur `1` a `9`
- l'IA du morpion reste la plus forte au niveau `9`
- l'IA du Puissance 4 reste volontairement simple et pedagogique pour convenir a un projet etudiant
- la fenetre du Puissance 4 peut se faire defiler si l'ecran est petit
