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


def choisir_meilleur_coup(plateau, pion_joueur, profondeur):
    arbre = generer_arbre(plateau, pion_joueur, profondeur)
    options = outils.get_sous_arbres(arbre)
    meilleur_coup = None
    meilleure_note = -99999
    scores_options = []

    for option in options:
        note = minimax(option, profondeur - 1, False, pion_joueur)
        scores_options.append(note)
        if note > meilleure_note:
            meilleure_note = note
            meilleur_coup = outils.get_racine(option)

    return meilleur_coup, meilleure_note, scores_options


def _joueur_suivant(joueur):
    if joueur == "X":
        return "O"
    return "X"


def _noeuds_a_profondeur(arbre, generation):
    if generation == 0:
        return [arbre]
    noeuds = []
    for enfant in outils.get_sous_arbres(arbre):
        noeuds.extend(_noeuds_a_profondeur(enfant, generation - 1))
    return noeuds


def evaluer_generation(arbre, generation, profondeur_totale, joueur_courant, pion_ia):
    if generation < 0 or generation > profondeur_totale:
        return []

    noeuds = _noeuds_a_profondeur(arbre, generation)
    profondeur_restante = profondeur_totale - generation
    joueur_au_noeud = joueur_courant if generation % 2 == 0 else _joueur_suivant(joueur_courant)
    c_est_max = joueur_au_noeud == pion_ia

    scores = []
    for noeud in noeuds:
        score = minimax(noeud, profondeur_restante, c_est_max, pion_ia)
        scores.append(score)
    return scores


def ligne_ideale(arbre, profondeur, joueur_courant, cible):
    plateau = outils.get_racine(arbre)
    fin = regles.verifier_gagnant(plateau)
    if fin is not None or profondeur == 0 or outils.est_une_feuille(arbre):
        return [plateau], regles.calcul_score(plateau, cible), fin

    enfants = outils.get_sous_arbres(arbre)
    c_est_max = joueur_courant == cible

    meilleur_enfant = None
    meilleure_valeur = None

    for enfant in enfants:
        valeur = minimax(enfant, profondeur - 1, not c_est_max, cible)
        if meilleur_enfant is None:
            meilleur_enfant = enfant
            meilleure_valeur = valeur
            continue
        if c_est_max and valeur > meilleure_valeur:
            meilleur_enfant = enfant
            meilleure_valeur = valeur
        if (not c_est_max) and valeur < meilleure_valeur:
            meilleur_enfant = enfant
            meilleure_valeur = valeur

    suite, score_final, gagnant_final = ligne_ideale(
        meilleur_enfant,
        profondeur - 1,
        _joueur_suivant(joueur_courant),
        cible,
    )
    return [plateau] + suite, score_final, gagnant_final
