import ia
import regles


def afficher(plateau):
    print("\n")
    print(f"  {plateau[0]} | {plateau[1]} | {plateau[2]} ")
    print(" ---+---+---")
    print(f"  {plateau[3]} | {plateau[4]} | {plateau[5]} ")
    print(" ---+---+---")
    print(f"  {plateau[6]} | {plateau[7]} | {plateau[8]} ")
    print("\n")


def joueur_suivant(joueur):
    if joueur == "X":
        return "O"
    return "X"


def type_joueur(mode, joueur):
    if mode == "jvj":
        return "humain"
    if mode == "iavia":
        return "ia"
    if joueur == "X":
        return "ia"
    return "humain"


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
        niveau = int(input("Difficulte (1-9) : ").strip())
    except Exception:
        niveau = 4
    if niveau < 1:
        return 1
    if niveau > 9:
        return 9
    return niveau


def afficher_scores_generation(plateau, joueur_courant, niveau):
    try:
        generation = int(input(f"Generation a afficher (0-{niveau}) : ").strip())
    except Exception:
        generation = 1

    arbre = ia.generer_arbre(plateau, joueur_courant, niveau)
    scores = ia.evaluer_generation(arbre, generation, niveau, joueur_courant, joueur_courant)
    if not scores:
        print("Generation invalide ou vide.")
        return
    print(f"Scores generation {generation} : {scores}")
    print(f"Min = {min(scores)} | Max = {max(scores)}")


def afficher_ligne_ideale(plateau, joueur_courant, niveau, cible):
    arbre = ia.generer_arbre(plateau, joueur_courant, niveau)
    suite, score, gagnant = ia.ligne_ideale(arbre, niveau, joueur_courant, cible)
    if cible == "X":
        print("Suite ideale pour l'IA (X) :")
    else:
        print("Suite ideale pour l'adversaire (O) :")

    for index, etat in enumerate(suite):
        print(f"Etape {index}:")
        afficher(etat)

    print(f"Score final estime : {score}")
    if gagnant is None:
        print("Aucun gagnant sur la profondeur analysee.")
    else:
        print(f"Gagnant sur la ligne ideale : {gagnant}")


def jouer_coup_ia(plateau, joueur, niveau):
    meilleur_coup, meilleure_note, scores_options = ia.choisir_meilleur_coup(plateau, joueur, niveau)
    print(f"Scores des options pour {joueur} : {scores_options}")
    if meilleur_coup is not None:
        print(f"L'IA ({joueur}) choisit score : {meilleure_note}")
        return meilleur_coup
    return plateau


def jouer_coup_humain(plateau, joueur, niveau):
    commande = input(
        f"A {joueur} - Case (0-8) ou commande [s=score, wi=ligne IA, wa=ligne ADV, q=quitter] : "
    ).strip().lower()

    if commande == "q":
        return False, plateau
    if commande == "s":
        afficher_scores_generation(plateau, joueur, niveau)
        return True, plateau
    if commande == "wi":
        afficher_ligne_ideale(plateau, joueur, niveau, "X")
        return True, plateau
    if commande == "wa":
        afficher_ligne_ideale(plateau, joueur, niveau, "O")
        return True, plateau

    try:
        case = int(commande)
    except Exception:
        print("Entree invalide.")
        return True, plateau

    if case < 0 or case > 8:
        print("Case hors limites.")
        return True, plateau
    if plateau[case] != " ":
        print("Case deja occupee.")
        return True, plateau

    nouveau = list(plateau)
    nouveau[case] = joueur
    return True, nouveau


def main():
    print("JEU DU MORPION")

    mode = lire_mode()
    niveau = lire_niveau()

    plateau = [" "] * 9
    if mode == "jvia":
        joueur_courant = "O"
    else:
        joueur_courant = "X"

    while True:
        afficher(plateau)
        resultat = regles.verifier_gagnant(plateau)
        if resultat is not None:
            if resultat == "Nul":
                print("MATCH NUL")
            else:
                print(f"Le joueur {resultat} a gagne")
            break

        role = type_joueur(mode, joueur_courant)
        if role == "ia":
            print(f"Tour IA ({joueur_courant})...")
            plateau = jouer_coup_ia(plateau, joueur_courant, niveau)
            joueur_courant = joueur_suivant(joueur_courant)
            continue

        continuer, nouveau_plateau = jouer_coup_humain(plateau, joueur_courant, niveau)
        if not continuer:
            print("Partie arretee.")
            break
        if nouveau_plateau == plateau:
            continue
        plateau = nouveau_plateau
        joueur_courant = joueur_suivant(joueur_courant)


if __name__ == "__main__":
    main()
