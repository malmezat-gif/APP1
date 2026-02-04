def get_racine(arbre):
    if arbre == []:
        return None
    return arbre[0]

def get_sous_arbres(arbre):
    if arbre == []:
        return []
    return arbre[1:]

def est_une_feuille(arbre):
    return len(arbre) == 1
