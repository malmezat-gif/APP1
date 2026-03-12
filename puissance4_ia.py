# Ce module contient l'IA du Puissance 4.

# random sert a rendre les niveaux faibles moins parfaits.
import random

# On reutilise les constantes de joueurs du projet.
import outils
# Ce module contient les regles et l'evaluation du Puissance 4.
import puissance4_regles as regles


# Cette fonction retourne un nom lisible pour le niveau selectionne.
def nom_niveau(niveau):
    # On force le niveau dans l'intervalle prevu.
    niveau = max(1, min(6, int(niveau)))

    if niveau <= 2:
        return "Simple"
    if niveau == 6:
        return "Impossible"
    return "Intermediaire"


# Cette fonction transforme le niveau utilisateur en profil concret.
def _profil_niveau(niveau):
    # On borne le niveau pour eviter toute valeur incoherente.
    niveau = max(1, min(6, int(niveau)))

    profils = {
        1: {"nom": "Simple", "profondeur": 1, "chance_erreur": 0.35, "fenetre_erreur": 4},
        2: {"nom": "Simple", "profondeur": 2, "chance_erreur": 0.20, "fenetre_erreur": 3},
        3: {"nom": "Intermediaire", "profondeur": 3, "chance_erreur": 0.10, "fenetre_erreur": 3},
        4: {"nom": "Intermediaire", "profondeur": 4, "chance_erreur": 0.05, "fenetre_erreur": 2},
        5: {"nom": "Intermediaire", "profondeur": 5, "chance_erreur": 0.02, "fenetre_erreur": 2},
        6: {"nom": "Impossible", "profondeur": 5, "chance_erreur": 0.0, "fenetre_erreur": 1},
    }

    return profils[niveau]


# Cette fonction choisit un coup parmi les analyses disponibles.
def _selectionner_coup(analyses, chance_erreur, fenetre_erreur):
    # On trie du meilleur score vers le moins bon.
    analyses_triees = sorted(analyses, key=lambda element: (element[1], element[3]), reverse=True)

    # Les niveaux faibles peuvent parfois devier du meilleur choix.
    if chance_erreur > 0.0 and len(analyses_triees) > 1 and random.random() < chance_erreur:
        limite = min(len(analyses_triees), fenetre_erreur + 1)
        candidats_erreur = analyses_triees[1:limite]
        if candidats_erreur:
            return random.choice(candidats_erreur)

    # En mode normal, on choisit parmi les meilleurs coups ex aequo.
    meilleure_note = analyses_triees[0][1]
    meilleur_gain_immediat = analyses_triees[0][3]
    meilleurs_coups = [
        element
        for element in analyses_triees
        if element[1] == meilleure_note and element[3] == meilleur_gain_immediat
    ]
    return random.choice(meilleurs_coups)


# Cette fonction Minimax retourne la meilleure note atteignable.
def minimax(plateau, joueur_courant, pion_ia, profondeur, alpha=-1_000_000, beta=1_000_000):
    # On arrete la recherche en feuille ou en fin de partie.
    if profondeur == 0 or regles.verifier_gagnant(plateau) is not None:
        return regles.calcul_score(plateau, pion_ia)

    # On recupere toutes les colonnes jouables.
    coups = regles.coups_possibles(plateau)

    # Cote MAX: le joueur de reference cherche a maximiser sa note.
    if joueur_courant == pion_ia:
        meilleur = -1_000_000
        for colonne in coups:
            prochain = regles.copier_plateau(plateau)
            regles.jouer_coup(prochain, colonne, joueur_courant)
            note = minimax(
                prochain,
                outils.joueur_suivant(joueur_courant),
                pion_ia,
                profondeur - 1,
                alpha,
                beta,
            )
            meilleur = max(meilleur, note)
            alpha = max(alpha, note)
            if beta <= alpha:
                break
        return meilleur

    # Cote MIN: l'adversaire cherche a reduire la note de l'IA.
    pire = 1_000_000
    for colonne in coups:
        prochain = regles.copier_plateau(plateau)
        regles.jouer_coup(prochain, colonne, joueur_courant)
        note = minimax(
            prochain,
            outils.joueur_suivant(joueur_courant),
            pion_ia,
            profondeur - 1,
            alpha,
            beta,
        )
        pire = min(pire, note)
        beta = min(beta, note)
        if beta <= alpha:
            break
    return pire


# Cette fonction choisit concretement une colonne a jouer.
def choisir_meilleur_coup(plateau, pion_joueur, niveau):
    # Si la partie est deja terminee, aucun coup n'est possible.
    if regles.verifier_gagnant(plateau) is not None:
        return None, None, 0, []

    # On lit le profil correspondant au niveau choisi.
    profil = _profil_niveau(niveau)
    profondeur = profil["profondeur"]
    analyses = []

    # On teste chaque colonne jouable.
    for colonne in regles.coups_possibles(plateau):
        prochain = regles.copier_plateau(plateau)
        regles.jouer_coup(prochain, colonne, pion_joueur)
        note = minimax(
            prochain,
            outils.joueur_suivant(pion_joueur),
            pion_joueur,
            max(0, profondeur - 1),
        )
        gain_immediat = regles.verifier_gagnant(prochain) == pion_joueur
        analyses.append((colonne, note, prochain, gain_immediat))

    # On choisit le coup final selon le profil.
    colonne_choisie, note_choisie, plateau_choisi, _ = _selectionner_coup(
        analyses,
        profil["chance_erreur"],
        profil["fenetre_erreur"],
    )

    # On conserve une version legere pour un affichage eventuel.
    notes = [(colonne, note) for colonne, note, _, _ in analyses]
    return plateau_choisi, colonne_choisie, note_choisie, notes
