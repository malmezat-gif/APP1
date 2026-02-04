import regles
import outils

def generer_arbre(plateau, joueur_courant, profondeur):
    if profondeur == 0 or regles.verifier_gagnant(plateau) is not None:
        return [plateau]

    arbre = [plateau]
    prochain_joueur = "O" if joueur_courant == "X" else "X"

    for i in range(9):
        if plateau[i] == " ":
            nouveau_plateau = list(plateau)
            nouveau_plateau[i] = joueur_courant
            sous_arbre = generer_arbre(nouveau_plateau, prochain_joueur, profondeur - 1)
            arbre.append(sous_arbre)
            
    return arbre

def minimax(arbre, profondeur, c_est_max, pion_ia):
    plateau = outils.get_racine(arbre)
    
    if outils.est_une_feuille(arbre) or profondeur == 0:
        return regles.calcul_score(plateau, pion_ia)

    enfants = outils.get_sous_arbres(arbre)
    liste_scores = []
    
    for enfant in enfants:
        note = minimax(enfant, profondeur - 1, not c_est_max, pion_ia)
        liste_scores.append(note)

    if c_est_max:
        return max(liste_scores)
    else:
        return min(liste_scores)
