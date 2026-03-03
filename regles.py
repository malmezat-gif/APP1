"""Regles et evaluation du morpion."""

import outils

COMBINAISONS_GAGNANTES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def gagnant(plateau):
    """Retourne X ou O si une ligne gagnante existe, sinon None."""
    for a, b, c in COMBINAISONS_GAGNANTES:
        pion = plateau[a]
        if pion != outils.VIDE and pion == plateau[b] == plateau[c]:
            return pion
    return None


def verifier_gagnant(plateau):
    """Retourne X, O, 'Nul' ou None."""
    pion_gagnant = gagnant(plateau)
    if pion_gagnant is not None:
        return pion_gagnant
    if outils.VIDE not in plateau:
        return "Nul"
    return None


def calcul_score(plateau, pion_ia):
    """Score Minimax: fort aux positions gagnantes, heuristique sinon."""
    resultat = verifier_gagnant(plateau)
    if resultat == pion_ia:
        return 1000
    if resultat == "Nul":
        return 0
    if resultat is not None:
        return -1000

    pion_adverse = outils.joueur_suivant(pion_ia)
    score = 0

    for a, b, c in COMBINAISONS_GAGNANTES:
        ligne = (plateau[a], plateau[b], plateau[c])
        nb_ia = ligne.count(pion_ia)
        nb_adverse = ligne.count(pion_adverse)

        if nb_ia and nb_adverse:
            continue

        if nb_ia == 2:
            score += 30
        elif nb_ia == 1:
            score += 10

        if nb_adverse == 2:
            score -= 30
        elif nb_adverse == 1:
            score -= 10

    return score
