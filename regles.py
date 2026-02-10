# Ce fichier contient les regles du morpion.
# On y trouve la verification de fin de partie et le calcul de score.


# Voici toutes les lignes gagnantes possibles sur un plateau 3x3.
COMBINAISONS_GAGNANTES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
]


def verifier_gagnant(plateau):
    # On regarde chaque combinaison gagnante.
    for ligne in COMBINAISONS_GAGNANTES:
        case1 = plateau[ligne[0]]
        case2 = plateau[ligne[1]]
        case3 = plateau[ligne[2]]

        # Si les 3 cases sont identiques et non vides, on a un gagnant.
        if case1 == case2 == case3 and case1 != " ":
            return case1

    # Si le plateau est plein et sans gagnant, c'est un match nul.
    if " " not in plateau:
        return "Nul"

    # Sinon la partie continue.
    return None


def calcul_score(plateau, pion_ia):
    # On verifie d'abord si la partie est deja terminee.
    gagnant = verifier_gagnant(plateau)

    # Cas simple: victoire, nul ou defaite.
    if gagnant == pion_ia:
        return 1000
    if gagnant == "Nul":
        return 0
    if gagnant is not None:
        return -1000

    # Si la partie n'est pas finie, on applique une heuristique.
    score = 0

    # On deduit le pion adverse a partir du pion de l'IA.
    if pion_ia == "X":
        pion_adversaire = "O"
    else:
        pion_adversaire = "X"

    # On evalue chaque ligne/colonne/diagonale.
    for ligne in COMBINAISONS_GAGNANTES:
        valeurs = [plateau[i] for i in ligne]
        nb_ia = valeurs.count(pion_ia)
        nb_adversaire = valeurs.count(pion_adversaire)

        # Ligne bloquee (les 2 joueurs sont presents) -> aucun gain.
        if nb_ia > 0 and nb_adversaire > 0:
            continue

        # Ligne favorable a l'IA.
        if nb_ia == 2:
            score += 30
        elif nb_ia == 1:
            score += 10

        # Ligne favorable a l'adversaire.
        if nb_adversaire == 2:
            score -= 30
        elif nb_adversaire == 1:
            score -= 10

    return score
