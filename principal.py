# Version console du jeu.
# Ce fichier est utile pour tester rapidement la logique sans interface graphique.

import ia
import regles
import outils


def afficher(plateau):
    # Affichage simple du plateau en console.
    print(outils.plateau_vers_texte(plateau))


def type_joueur(mode, joueur):
    # Cette fonction dit si le joueur actuel est humain ou IA.
    if mode == "jvj":
        return "humain"
    if mode == "iavia":
        return "ia"

    # En mode JvIA, X est l'IA et O est l'humain.
    if joueur == "X":
        return "ia"
    return "humain"


def lire_mode():
    # Menu principal des modes de jeu.
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
    # Niveau = profondeur de recherche Minimax.
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
    # Outil de debug: affiche les scores d'une generation de l'arbre.
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
    # Outil de debug: affiche une suite "ideale" de coups.
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
    # L'IA calcule son meilleur coup avec Minimax.
    meilleur_coup, meilleure_note, scores_options = ia.choisir_meilleur_coup(plateau, joueur, niveau)

    print(f"Scores des options pour {joueur} : {scores_options}")

    if meilleur_coup is not None:
        print(f"L'IA ({joueur}) choisit score : {meilleure_note}")
        return meilleur_coup

    return plateau


def jouer_coup_humain(plateau, joueur, niveau):
    # Sur un tour humain, on peut jouer une case ou une commande.
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

    # Sinon on essaye d'interpreter la commande comme un numero de case.
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

    # Coup valide: on place le pion.
    nouveau_plateau = outils.copier_plateau(plateau)
    nouveau_plateau[case] = joueur
    return True, nouveau_plateau


def main():
    # Point d'entree du jeu console.
    print("JEU DU MORPION")

    mode = lire_mode()
    niveau = lire_niveau()

    plateau = [" "] * 9

    # En mode JvIA, on garde O pour l'humain (comme ton ancienne version).
    if mode == "jvia":
        joueur_courant = "O"
    else:
        joueur_courant = "X"

    while True:
        afficher(plateau)

        # Verifier si la partie est terminee.
        resultat = regles.verifier_gagnant(plateau)
        if resultat is not None:
            if resultat == "Nul":
                print("MATCH NUL")
            else:
                print(f"Le joueur {resultat} a gagne")
            break

        # Selon le mode, on joue humain ou IA.
        role = type_joueur(mode, joueur_courant)

        if role == "ia":
            print(f"Tour IA ({joueur_courant})...")
            plateau = jouer_coup_ia(plateau, joueur_courant, niveau)
            joueur_courant = outils.joueur_suivant(joueur_courant)
            continue

        continuer, nouveau_plateau = jouer_coup_humain(plateau, joueur_courant, niveau)

        if not continuer:
            print("Partie arretee.")
            break

        # Si rien n'a change, on reste sur le meme joueur.
        if nouveau_plateau == plateau:
            continue

        plateau = nouveau_plateau
        joueur_courant = outils.joueur_suivant(joueur_courant)


if __name__ == "__main__":
    main()
