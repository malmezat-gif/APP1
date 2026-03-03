# APP1 - Morpion IA (Minimax)

Projet de morpion avec:
- un mode console
- une interface graphique Tkinter
- une IA basee sur Minimax (avec elagage alpha-beta)

## Fichiers
- `interface.py`: interface graphique (a lancer en priorite)
- `principal.py`: version console
- `ia.py`: choix du meilleur coup
- `regles.py`: victoire, nul, score heuristique
- `outils.py`: fonctions utilitaires

## Lancer le jeu
Depuis le dossier du projet:

```bash
python3 interface.py
```

Si tu veux la version console:

```bash
python3 principal.py
```

## Comment ca marche
- Le plateau est une liste de 9 cases (`" "`, `"X"`, `"O"`).
- L'IA teste tous les coups possibles jusqu'a une profondeur choisie.
- Le score est calcule avec:
  - `+1000` si l'IA gagne
  - `-1000` si l'IA perd
  - `0` si match nul
  - sinon une heuristique simple sur les lignes ouvertes

## Modes de jeu
- `Joueur vs IA`
- `Joueur vs Joueur`
- `IA vs IA`

## Niveau de difficulte
Le curseur va de 1 a 9.
- Niveau faible: plus rapide, moins precis
- Niveau eleve: plus fort, mais peut ralentir

## Notes
Tkinter est inclus avec Python standard sur macOS/Linux/Windows, donc aucune dependance externe n'est necessaire pour l'interface.
