# Ce fichier contient des fonctions utilitaires tres simples.
# Le but est d'eviter de re-ecrire les memes petites operations.


def get_racine(arbre):
    # La racine est la premiere case de la liste.
    if arbre == []:
        return None
    return arbre[0]


def get_sous_arbres(arbre):
    # Les sous-arbres sont tous les elements apres la racine.
    if arbre == []:
        return []
    return arbre[1:]


def est_une_feuille(arbre):
    # Un noeud feuille n'a pas d'enfants.
    return len(arbre) == 1


def joueur_suivant(joueur):
    # Cette fonction alterne entre X et O.
    if joueur == "X":
        return "O"
    return "X"


def copier_plateau(plateau):
    # On cree une copie pour ne pas modifier l'original.
    return list(plateau)


def plateau_vers_texte(plateau):
    # Cette fonction transforme le plateau en texte lisible.
    ligne1 = f" {plateau[0]} | {plateau[1]} | {plateau[2]} "
    ligne2 = f" {plateau[3]} | {plateau[4]} | {plateau[5]} "
    ligne3 = f" {plateau[6]} | {plateau[7]} | {plateau[8]} "
    separateur = "---+---+---"
    return "\n" + ligne1 + "\n" + separateur + "\n" + ligne2 + "\n" + separateur + "\n" + ligne3 + "\n"
