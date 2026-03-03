# Ce module contient l'intelligence artificielle du morpion.
# L'algorithme utilise Minimax avec elagage alpha-beta pour accelerer.

# On importe les regles pour evaluer les positions.
import regles
# On importe les utilitaires pour manipuler le plateau.
import outils


# Cette fonction Minimax retourne la meilleure note atteignable depuis un plateau donne.
def minimax(plateau, joueur_courant, pion_ia, profondeur, alpha=-10_000, beta=10_000):
    # Si on a atteint la profondeur max ou une fin de partie, on evalue directement.
    if profondeur == 0 or regles.verifier_gagnant(plateau) is not None:
        # On retourne la note de la position du point de vue de l'IA.
        return regles.calcul_score(plateau, pion_ia)

    # On recupere la liste de tous les coups possibles a partir de ce plateau.
    coups = outils.coups_possibles(plateau)

    # Si c'est le tour de l'IA, on cherche a maximiser le score.
    if joueur_courant == pion_ia:
        # Valeur de depart tres basse pour pouvoir monter.
        meilleur = -10_000
        # On teste chaque case disponible.
        for case in coups:
            # On copie le plateau pour ne pas modifier l'original.
            prochain = outils.copier_plateau(plateau)
            # On place le pion du joueur courant sur la case testee.
            prochain[case] = joueur_courant
            # On evalue recursivement la suite en passant au joueur suivant.
            note = minimax(
                # Nouveau plateau apres le coup.
                prochain,
                # On alterne au joueur suivant.
                outils.joueur_suivant(joueur_courant),
                # Le pion de reference de l'IA ne change pas.
                pion_ia,
                # On descend d'un niveau dans l'arbre.
                profondeur - 1,
                # Alpha courant.
                alpha,
                # Beta courant.
                beta,
            )
            # On garde la meilleure note rencontree.
            meilleur = max(meilleur, note)
            # On met a jour alpha avec la meilleure valeur connue cote MAX.
            alpha = max(alpha, note)
            # Si beta <= alpha, on peut couper cette branche (elagage).
            if beta <= alpha:
                # On arrete la boucle car les autres coups n'apporteront rien.
                break
        # On retourne la meilleure note trouvee pour ce noeud MAX.
        return meilleur

    # Sinon c'est le tour de l'adversaire: on cherche a minimiser le score de l'IA.
    pire = 10_000
    # On teste chaque case disponible.
    for case in coups:
        # On copie le plateau pour simuler un coup sans toucher a l'etat actuel.
        prochain = outils.copier_plateau(plateau)
        # On applique le coup adverse.
        prochain[case] = joueur_courant
        # On evalue recursivement la suite.
        note = minimax(
            # Plateau apres le coup.
            prochain,
            # On passe au joueur suivant.
            outils.joueur_suivant(joueur_courant),
            # Pion de reference de l'IA.
            pion_ia,
            # On descend d'un niveau.
            profondeur - 1,
            # Alpha courant.
            alpha,
            # Beta courant.
            beta,
        )
        # On garde cette fois la plus petite note (adversaire optimal).
        pire = min(pire, note)
        # On met a jour beta avec la meilleure borne cote MIN.
        beta = min(beta, note)
        # Si beta <= alpha, la branche est inutile, on coupe.
        if beta <= alpha:
            # On stoppe les calculs de cette branche.
            break
    # On retourne la pire note trouvee pour ce noeud MIN.
    return pire


# Cette fonction choisit concretement le meilleur coup a jouer.
def choisir_meilleur_coup(plateau, pion_joueur, profondeur):
    # Si la partie est deja terminee, aucun coup n'est possible.
    if regles.verifier_gagnant(plateau) is not None:
        # On retourne un resultat vide coherent.
        return None, 0, []

    # On recupere toutes les cases encore jouables.
    coups = outils.coups_possibles(plateau)
    # On memorisera ici le meilleur plateau trouve.
    meilleur_coup = None
    # Note initiale tres basse pour chercher un maximum.
    meilleure_note = -10_000
    # Cette liste stocke les notes de chaque case testee.
    notes = []

    # On teste chaque coup disponible.
    for case in coups:
        # On copie le plateau courant.
        prochain = outils.copier_plateau(plateau)
        # On applique le coup candidat.
        prochain[case] = pion_joueur
        # On evalue la suite avec Minimax.
        note = minimax(
            # Plateau apres le coup.
            prochain,
            # Au niveau suivant, ce sera le tour de l'autre joueur.
            outils.joueur_suivant(pion_joueur),
            # Le pion de l'IA de reference est le joueur qui choisit ici.
            pion_joueur,
            # On retire 1 car on vient de jouer un coup.
            max(0, profondeur - 1),
        )
        # On enregistre la note pour affichage/debug.
        notes.append((case, note))

        # Si la note est meilleure que la meilleure connue, on met a jour.
        if note > meilleure_note:
            # Nouvelle meilleure note.
            meilleure_note = note
            # Nouveau meilleur plateau.
            meilleur_coup = prochain

    # On retourne le plateau choisi, sa note et toutes les notes candidates.
    return meilleur_coup, meilleure_note, notes
