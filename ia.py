# Ce fichier contient l'IA du morpion.
# L'idee est d'explorer un arbre de coups avec l'algorithme Minimax.

import regles
import outils


def generer_arbre(plateau, joueur_courant, profondeur):
    # Condition d'arret:
    # - profondeur atteinte
    # - ou partie deja terminee
    if profondeur == 0 or regles.verifier_gagnant(plateau) is not None:
        return [plateau]

    # Le premier element est toujours la configuration courante.
    arbre = [plateau]

    # On prepare le prochain joueur.
    prochain_joueur = outils.joueur_suivant(joueur_courant)

    # On essaye tous les coups possibles.
    for i in range(9):
        if plateau[i] == " ":
            nouveau_plateau = outils.copier_plateau(plateau)
            nouveau_plateau[i] = joueur_courant

            # Appel recursif sur le coup suivant.
            sous_arbre = generer_arbre(nouveau_plateau, prochain_joueur, profondeur - 1)
            arbre.append(sous_arbre)

    return arbre


def minimax(arbre, profondeur, c_est_max, pion_ia):
    # On recupere la configuration associee au noeud courant.
    plateau = outils.get_racine(arbre)

    # Si on est sur une feuille (ou profondeur 0), on evalue directement.
    if outils.est_une_feuille(arbre) or profondeur == 0:
        return regles.calcul_score(plateau, pion_ia)

    # On recupere les enfants et on calcule leur note.
    enfants = outils.get_sous_arbres(arbre)
    notes = []

    for enfant in enfants:
        # On alterne MAX et MIN a chaque niveau.
        note_enfant = minimax(enfant, profondeur - 1, not c_est_max, pion_ia)
        notes.append(note_enfant)

    # Si c'est un noeud MAX, on prend la meilleure note.
    if c_est_max:
        return max(notes)

    # Sinon c'est un noeud MIN, on prend la plus petite note.
    return min(notes)


def choisir_meilleur_coup(plateau, pion_joueur, profondeur):
    # On genere l'arbre depuis la position actuelle.
    arbre = generer_arbre(plateau, pion_joueur, profondeur)
    options = outils.get_sous_arbres(arbre)

    # Valeurs de depart pour memoriser le meilleur choix.
    meilleur_coup = None
    meilleure_note = -99999
    scores_options = []

    # On evalue chaque coup possible avec Minimax.
    for option in options:
        note = minimax(option, profondeur - 1, False, pion_joueur)
        scores_options.append(note)

        if note > meilleure_note:
            meilleure_note = note
            meilleur_coup = outils.get_racine(option)

    return meilleur_coup, meilleure_note, scores_options


def noeuds_a_profondeur(arbre, generation):
    # Cette fonction recupere tous les noeuds a une generation donnee.
    if generation == 0:
        return [arbre]

    noeuds = []
    for enfant in outils.get_sous_arbres(arbre):
        noeuds.extend(noeuds_a_profondeur(enfant, generation - 1))
    return noeuds


def evaluer_generation(arbre, generation, profondeur_totale, joueur_courant, pion_ia):
    # Si la generation demandee n'est pas valide, on renvoie une liste vide.
    if generation < 0 or generation > profondeur_totale:
        return []

    # On prend tous les noeuds de la generation choisie.
    noeuds = noeuds_a_profondeur(arbre, generation)

    # Profondeur restante depuis ce niveau.
    profondeur_restante = profondeur_totale - generation

    # On deduit quel joueur doit jouer a cette generation.
    if generation % 2 == 0:
        joueur_au_noeud = joueur_courant
    else:
        joueur_au_noeud = outils.joueur_suivant(joueur_courant)

    # MAX si le joueur du noeud est le pion de reference.
    c_est_max = joueur_au_noeud == pion_ia

    # On evalue tous les noeuds de cette generation.
    scores = []
    for noeud in noeuds:
        score = minimax(noeud, profondeur_restante, c_est_max, pion_ia)
        scores.append(score)

    return scores


def ligne_ideale(arbre, profondeur, joueur_courant, cible):
    # Cette fonction renvoie une suite de plateaux "ideale"
    # pour un joueur cible (X ou O).
    plateau = outils.get_racine(arbre)
    fin = regles.verifier_gagnant(plateau)

    # Si on est au bout, on renvoie la position actuelle.
    if fin is not None or profondeur == 0 or outils.est_une_feuille(arbre):
        score = regles.calcul_score(plateau, cible)
        return [plateau], score, fin

    enfants = outils.get_sous_arbres(arbre)

    # Si le joueur courant est la cible, il cherche MAX.
    # Sinon il cherche MIN.
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

    # On continue recursivement sur l'enfant choisi.
    suite, score_final, gagnant_final = ligne_ideale(
        meilleur_enfant,
        profondeur - 1,
        outils.joueur_suivant(joueur_courant),
        cible,
    )

    return [plateau] + suite, score_final, gagnant_final
