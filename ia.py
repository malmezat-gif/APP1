# Ce module contient l'intelligence artificielle du morpion.
# L'IA utilise Minimax (avec elagage alpha-beta) et un profil par niveau.

# random sert a introduire des erreurs volontaires aux niveaux faibles.
import random
# On importe les regles pour evaluer les positions.
import regles
# On importe les utilitaires pour manipuler le plateau.
import outils


# Cette fonction retourne un nom lisible pour le niveau choisi.
def nom_niveau(niveau):
    # On force le niveau entre 1 et 9.
    niveau = max(1, min(9, int(niveau)))
    # Les niveaux 1 a 3 correspondent au mode simple.
    if niveau <= 3:
        return "Simple"
    # Le niveau 9 est le mode impossible.
    if niveau == 9:
        return "Impossible"
    # Les niveaux 4 a 8 sont intermediaires.
    return "Intermediaire"


# Cette fonction transforme un niveau utilisateur en profil IA concret.
def _profil_niveau(niveau, nb_cases_libres):
    # On borne la valeur pour eviter les erreurs.
    niveau = max(1, min(9, int(niveau)))

    # S'il reste 0 ou 1 coup, inutile de complexifier.
    if nb_cases_libres <= 1:
        return {
            # Nom du profil.
            "nom": "Fin de partie",
            # Profondeur minimale utile.
            "profondeur": 1,
            # Aucune erreur volontaire.
            "chance_erreur": 0.0,
            # Fenetre de choix en cas d'erreur.
            "fenetre_erreur": 1,
        }

    # Profil simple: recherche faible + erreurs frequentes.
    if niveau <= 3:
        return {
            # Nom du profil.
            "nom": "Simple",
            # Faible profondeur pour rendre l'IA moins precise.
            "profondeur": min(nb_cases_libres, 1 + (niveau // 2)),
            # Plus le niveau est bas, plus il y a d'erreurs.
            "chance_erreur": {1: 0.60, 2: 0.45, 3: 0.30}[niveau],
            # L'IA peut choisir parmi plusieurs coups imparfaits.
            "fenetre_erreur": 4,
        }

    # Profil intermediaire: IA correcte, erreurs rares.
    if niveau <= 8:
        return {
            # Nom du profil.
            "nom": "Intermediaire",
            # Profondeur progressive selon le niveau.
            "profondeur": min(nb_cases_libres, niveau - 1),
            # A 4: quelques erreurs, a 8: presque aucune.
            "chance_erreur": max(0.0, (8 - niveau) * 0.05),
            # En cas d'erreur, la deviation reste limitee.
            "fenetre_erreur": 3,
        }

    # Profil impossible: recherche complete, sans erreur.
    return {
        # Nom du profil.
        "nom": "Impossible",
        # Recherche totale jusqu'a la fin de partie.
        "profondeur": nb_cases_libres,
        # Aucune etourderie.
        "chance_erreur": 0.0,
        # Pas de fenetre d'erreur.
        "fenetre_erreur": 1,
    }


# Cette fonction choisit un coup a partir des analyses notees.
def _selectionner_coup(analyses, chance_erreur, fenetre_erreur):
    # On trie les coups du meilleur score vers le moins bon.
    analyses_triees = sorted(analyses, key=lambda element: element[1], reverse=True)

    # Si le profil autorise des erreurs, on peut parfois eviter le meilleur coup.
    if chance_erreur > 0.0 and len(analyses_triees) > 1 and random.random() < chance_erreur:
        # On choisit une zone de coups non optimaux pour simuler une etourderie.
        limite = min(len(analyses_triees), fenetre_erreur + 1)
        candidats_erreur = analyses_triees[1:limite]
        # Si la fenetre est valide, on tire un coup dedans.
        if candidats_erreur:
            return random.choice(candidats_erreur)

    # Sinon, on joue au mieux.
    meilleure_note = analyses_triees[0][1]
    # On prend tous les coups ex aequo avec la meilleure note.
    meilleurs_coups = [element for element in analyses_triees if element[1] == meilleure_note]
    # On choisit aleatoirement parmi les meilleurs pour varier les parties.
    return random.choice(meilleurs_coups)


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
def choisir_meilleur_coup(plateau, pion_joueur, niveau):
    # Si la partie est deja terminee, aucun coup n'est possible.
    if regles.verifier_gagnant(plateau) is not None:
        # On retourne un resultat vide coherent.
        return None, 0, []

    # On recupere toutes les cases encore jouables.
    coups = outils.coups_possibles(plateau)
    # On construit un profil de difficulte a partir du niveau.
    profil = _profil_niveau(niveau, len(coups))
    # On lit la profondeur de recherche associee au profil.
    profondeur = profil["profondeur"]
    # Cette liste stocke les analyses de chaque coup possible.
    analyses = []

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
        # On enregistre case, note et plateau resultant.
        analyses.append((case, note, prochain))

    # On selectionne un coup selon le profil (optimale ou etourderie possible).
    case_choisie, note_choisie, plateau_choisi = _selectionner_coup(
        # Toutes les analyses disponibles.
        analyses,
        # Probabilite de faire une erreur a ce niveau.
        profil["chance_erreur"],
        # Amplitude de deviation en cas d'erreur.
        profil["fenetre_erreur"],
    )

    # On garde une version legere (case, note) pour affichage/debug interface.
    notes = [(case, note) for case, note, _ in analyses]
    # On retourne le plateau choisi, la note associee et les details des notes.
    return plateau_choisi, note_choisie, notes
