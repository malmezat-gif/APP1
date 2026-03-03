# Ce module regroupe des petites fonctions utiles dans tout le projet.

# Cette constante represente une case vide du plateau.
VIDE = " "
# Cette constante represente le pion du joueur X.
JOUEUR_X = "X"
# Cette constante represente le pion du joueur O.
JOUEUR_O = "O"


# Cette fonction cree un nouveau plateau vide de 9 cases.
def plateau_vide():
    # On retourne une liste de 9 cases vides.
    return [VIDE] * 9


# Cette fonction copie un plateau existant.
def copier_plateau(plateau):
    # list(plateau) cree une nouvelle liste pour eviter de modifier l'original.
    return list(plateau)


# Cette fonction donne le joueur qui doit jouer apres le joueur courant.
def joueur_suivant(joueur):
    # Si le joueur courant est X, le suivant est O, sinon c'est X.
    return JOUEUR_O if joueur == JOUEUR_X else JOUEUR_X


# Cette fonction renvoie les indices des cases encore disponibles.
def coups_possibles(plateau):
    # On parcourt toutes les cases et on garde celles qui sont vides.
    return [index for index, valeur in enumerate(plateau) if valeur == VIDE]
