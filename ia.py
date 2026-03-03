"""IA Minimax (avec elagage alpha-beta) pour le morpion."""

import regles
import outils


def minimax(plateau, joueur_courant, pion_ia, profondeur, alpha=-10_000, beta=10_000):
    """Calcule la meilleure note atteignable depuis un etat."""
    if profondeur == 0 or regles.verifier_gagnant(plateau) is not None:
        return regles.calcul_score(plateau, pion_ia)

    coups = outils.coups_possibles(plateau)

    if joueur_courant == pion_ia:
        meilleur = -10_000
        for case in coups:
            prochain = outils.copier_plateau(plateau)
            prochain[case] = joueur_courant
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

    pire = 10_000
    for case in coups:
        prochain = outils.copier_plateau(plateau)
        prochain[case] = joueur_courant
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


def choisir_meilleur_coup(plateau, pion_joueur, profondeur):
    """Retourne (nouveau_plateau, meilleure_note, notes_par_coup)."""
    if regles.verifier_gagnant(plateau) is not None:
        return None, 0, []

    coups = outils.coups_possibles(plateau)
    meilleur_coup = None
    meilleure_note = -10_000
    notes = []

    for case in coups:
        prochain = outils.copier_plateau(plateau)
        prochain[case] = pion_joueur
        note = minimax(
            prochain,
            outils.joueur_suivant(pion_joueur),
            pion_joueur,
            max(0, profondeur - 1),
        )
        notes.append((case, note))

        if note > meilleure_note:
            meilleure_note = note
            meilleur_coup = prochain

    return meilleur_coup, meilleure_note, notes
