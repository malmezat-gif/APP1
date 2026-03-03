"""Version console du morpion."""

import ia
import regles
import outils


def afficher(plateau):
    print(outils.plateau_vers_texte(plateau))


def lire_mode():
    print("Mode de jeu :")
    print("1 - Joueur vs IA")
    print("2 - Joueur vs Joueur")
    print("3 - IA vs IA")
    choix = input("Choix (1-3) : ").strip()
    if choix == "2":
        return "jvj"
    if choix == "3":
        return "iavia"
    return "jvia"


def lire_niveau():
    try:
        niveau = int(input("Difficulte IA (1-9) : ").strip())
    except ValueError:
        return 4
    return max(1, min(9, niveau))


def role_joueur(mode, joueur):
    if mode == "jvj":
        return "humain"
    if mode == "iavia":
        return "ia"
    return "humain" if joueur == "X" else "ia"


def jouer_tour_humain(plateau, joueur):
    entree = input(f"Tour {joueur} - Choisis une case (0-8) ou q pour quitter : ").strip().lower()
    if entree == "q":
        return False, plateau

    try:
        case = int(entree)
    except ValueError:
        print("Entree invalide.")
        return True, plateau

    if case < 0 or case > 8:
        print("Case hors limites.")
        return True, plateau
    if plateau[case] != outils.VIDE:
        print("Case deja occupee.")
        return True, plateau

    nouveau = outils.copier_plateau(plateau)
    nouveau[case] = joueur
    return True, nouveau


def jouer_tour_ia(plateau, joueur, niveau):
    meilleur_coup, meilleure_note, notes = ia.choisir_meilleur_coup(plateau, joueur, niveau)
    print(f"IA {joueur} - notes: {notes}")
    if meilleur_coup is None:
        return plateau
    print(f"IA {joueur} joue avec une note {meilleure_note}")
    return meilleur_coup


def main():
    print("JEU DU MORPION")
    mode = lire_mode()
    niveau = lire_niveau()
    plateau = outils.plateau_vide()
    joueur_courant = "X"

    while True:
        afficher(plateau)
        resultat = regles.verifier_gagnant(plateau)
        if resultat is not None:
            if resultat == "Nul":
                print("Match nul")
            else:
                print(f"Le joueur {resultat} a gagne")
            break

        role = role_joueur(mode, joueur_courant)
        if role == "ia":
            plateau = jouer_tour_ia(plateau, joueur_courant, niveau)
            joueur_courant = outils.joueur_suivant(joueur_courant)
            continue

        continuer, nouveau = jouer_tour_humain(plateau, joueur_courant)
        if not continuer:
            print("Partie arretee.")
            break
        if nouveau == plateau:
            continue

        plateau = nouveau
        joueur_courant = outils.joueur_suivant(joueur_courant)


if __name__ == "__main__":
    main()
