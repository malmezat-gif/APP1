"""Fonctions utilitaires partagees par le mode console et l'interface."""

VIDE = " "
JOUEUR_X = "X"
JOUEUR_O = "O"


def plateau_vide():
    """Cree un plateau de morpion vide (9 cases)."""
    return [VIDE] * 9


def copier_plateau(plateau):
    """Retourne une copie du plateau pour eviter les effets de bord."""
    return list(plateau)


def joueur_suivant(joueur):
    """Alterne entre X et O."""
    return JOUEUR_O if joueur == JOUEUR_X else JOUEUR_X


def coups_possibles(plateau):
    """Liste les indices de cases encore libres."""
    return [index for index, valeur in enumerate(plateau) if valeur == VIDE]


def plateau_vers_texte(plateau):
    """Convertit un plateau en rendu texte 3x3 pour la console."""
    lignes = []
    for depart in (0, 3, 6):
        lignes.append(f" {plateau[depart]} | {plateau[depart + 1]} | {plateau[depart + 2]} ")
    return "\n" + "\n---+---+---\n".join(lignes) + "\n"
