# PLAN - APP1 Jeux de plateau

## 1) Perimetre actuel
- Morpion avec interface `CustomTkinter`
- analyse Minimax du morpion :
  - scores d'une generation donnee
  - minimum et maximum
  - suite ideale pour une victoire cible
- Puissance 4 dans une fenetre secondaire
- modes disponibles sur les deux jeux :
  - `Joueur vs IA`
  - `Joueur vs Joueur`
  - `IA vs IA`

## 2) Decoupage technique
- `interface.py` : fenetre principale du morpion + panneau d'analyse + acces Puissance 4
- `ia.py` : IA du morpion + fonctions d'analyse
- `regles.py` : regles et evaluation du morpion
- `outils.py` : constantes et utilitaires communs
- `puissance4_interface.py` : interface du Puissance 4
- `puissance4_ia.py` : IA du Puissance 4
- `puissance4_regles.py` : regles et evaluation du Puissance 4

## 3) Verifications cibles
- Le projet se lance avec `python3 interface.py`
- Le morpion reste jouable dans les 3 modes existants
- Le panneau d'analyse du morpion affiche :
  - les scores d'une generation
  - le minimum et le maximum
  - une suite ideale pour chaque joueur cible
- Le module Puissance 4 reste accessible depuis la fenetre principale
- Les deux IA restent d'un niveau pedagogique et raisonnable
