# Ce module contient les regles du morpion et la fonction de score pour l'IA.

# On importe les utilitaires (constantes et fonctions communes).
import outils

# Cette constante liste toutes les lignes gagnantes possibles sur un plateau 3x3.
COMBINAISONS_GAGNANTES = (
    # Premiere ligne horizontale.
    (0, 1, 2),
    # Deuxieme ligne horizontale.
    (3, 4, 5),
    # Troisieme ligne horizontale.
    (6, 7, 8),
    # Premiere colonne verticale.
    (0, 3, 6),
    # Deuxieme colonne verticale.
    (1, 4, 7),
    # Troisieme colonne verticale.
    (2, 5, 8),
    # Diagonale principale.
    (0, 4, 8),
    # Diagonale secondaire.
    (2, 4, 6),
)


# Cette fonction verifie s'il existe un gagnant direct sur le plateau.
def gagnant(plateau):
    # On parcourt chaque combinaison gagnante possible.
    for a, b, c in COMBINAISONS_GAGNANTES:
        # On lit le pion de la premiere case de la combinaison.
        pion = plateau[a]
        # On verifie que la case n'est pas vide et que les 3 cases sont identiques.
        if pion != outils.VIDE and pion == plateau[b] == plateau[c]:
            # Si la condition est vraie, le joueur de ce pion a gagne.
            return pion
    # Si aucune combinaison n'est gagnante, on retourne None.
    return None


# Cette fonction donne l'etat global de la partie.
def verifier_gagnant(plateau):
    # On cherche d'abord un gagnant (X ou O).
    pion_gagnant = gagnant(plateau)
    # Si un gagnant existe, on le retourne.
    if pion_gagnant is not None:
        return pion_gagnant
    # S'il n'y a plus de case vide, la partie est un match nul.
    if outils.VIDE not in plateau:
        return "Nul"
    # Sinon la partie continue.
    return None


# Cette fonction calcule un score pour Minimax en se placant du point de vue de l'IA.
def calcul_score(plateau, pion_ia):
    # On verifie d'abord si la partie est deja terminee.
    resultat = verifier_gagnant(plateau)
    # Si l'IA gagne, on retourne un tres grand score positif.
    if resultat == pion_ia:
        return 1000
    # Si la partie est nulle, le score est neutre.
    if resultat == "Nul":
        return 0
    # Si l'adversaire gagne, on retourne un tres grand score negatif.
    if resultat is not None:
        return -1000

    # On determine le pion de l'adversaire (X <-> O).
    pion_adverse = outils.joueur_suivant(pion_ia)
    # On initialise le score heuristique.
    score = 0

    # On evalue chaque ligne gagnante potentielle.
    for a, b, c in COMBINAISONS_GAGNANTES:
        # On recupere les 3 valeurs de la ligne.
        ligne = (plateau[a], plateau[b], plateau[c])
        # On compte le nombre de pions IA sur cette ligne.
        nb_ia = ligne.count(pion_ia)
        # On compte le nombre de pions adverses sur cette ligne.
        nb_adverse = ligne.count(pion_adverse)

        # Si les deux joueurs sont presents sur la ligne, elle est bloquee.
        if nb_ia and nb_adverse:
            # On ignore cette ligne car elle n'aide personne.
            continue

        # Si l'IA a 2 pions alignes et pas d'adversaire, c'est tres favorable.
        if nb_ia == 2:
            # On ajoute un bonus important.
            score += 30
        # Si l'IA a 1 pion seul sur la ligne, c'est un petit avantage.
        elif nb_ia == 1:
            # On ajoute un petit bonus.
            score += 10

        # Si l'adversaire a 2 pions alignes, c'est dangereux pour l'IA.
        if nb_adverse == 2:
            # On retire des points pour pousser l'IA a bloquer.
            score -= 30
        # Si l'adversaire a 1 pion seul, c'est un petit risque.
        elif nb_adverse == 1:
            # On retire un petit malus.
            score -= 10

    # On retourne le score final de cette position.
    return score
