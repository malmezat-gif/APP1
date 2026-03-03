# PLAN - APP1 Morpion IA

## 1) Perimetre actuel
- Jeu de morpion 3x3 avec interface graphique Tkinter uniquement.
- IA basee sur Minimax avec elagage alpha-beta.
- Modes de jeu: Joueur vs IA, Joueur vs Joueur, IA vs IA.
- Difficulte IA de 1 a 9 avec profils:
  - `Simple` (1-3): erreurs volontaires.
  - `Intermediaire` (4-8): jeu de plus en plus solide.
  - `Impossible` (9): recherche complete, tres fort.

## 2) Decoupage technique
- `interface.py`: gestion UI, tours, statuts, scores et fin de partie.
- `ia.py`: evaluation des coups et selection selon le profil de niveau.
- `regles.py`: detection victoire/nul + calcul de score heuristique.
- `outils.py`: utilitaires (plateau vide, copie, joueur suivant, coups possibles).

## 3) Plan d'action
1. Stabiliser les regles de jeu et les transitions de tours.
2. Renforcer le comportement IA par niveau de difficulte.
3. Assurer une UX fluide (blocages evites, relance auto apres nul).
4. Maintenir une documentation simple et coherente (README + PLAN).

## 4) Verifications cibles
- Le jeu se lance avec `python3 interface.py`.
- Aucun mode terminal n'est present dans le depot.
- Niveau `Simple`: l'IA commet des erreurs regulieres.
- Niveau `Impossible`: l'IA ne laisse pas de victoire facile.
- En cas de match nul: nouvelle partie automatique.
