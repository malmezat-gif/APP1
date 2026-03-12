# Ce module contient les regles du Puissance 4 et la fonction de score de son IA.

# On reutilise les constantes de joueurs du projet.
import outils


# Dimensions classiques du Puissance 4.
NB_LIGNES = 6
NB_COLONNES = 7


# Cette fonction cree un plateau vide de 6 lignes sur 7 colonnes.
def plateau_vide():
    # Chaque case vide contient un espace.
    return [[outils.VIDE for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]


# Cette fonction copie profondement un plateau existant.
def copier_plateau(plateau):
    # On duplique chaque ligne pour pouvoir simuler des coups sans effet de bord.
    return [list(ligne) for ligne in plateau]


# Cette fonction verifie si une colonne accepte encore un pion.
def colonne_jouable(plateau, colonne):
    # Une colonne est jouable si son indice est valide et si sa case du haut est vide.
    return 0 <= colonne < NB_COLONNES and plateau[0][colonne] == outils.VIDE


# Cette fonction retourne les colonnes jouables, en privilegiant le centre.
def coups_possibles(plateau):
    # L'ordre centré aide l'IA a trouver plus vite de bons coups.
    ordre = (3, 2, 4, 1, 5, 0, 6)
    # On ne conserve que les colonnes encore jouables.
    return [colonne for colonne in ordre if colonne_jouable(plateau, colonne)]


# Cette fonction place un pion dans la colonne voulue.
def jouer_coup(plateau, colonne, joueur):
    # Si la colonne n'est pas jouable, aucun coup n'est realise.
    if not colonne_jouable(plateau, colonne):
        return None

    # On descend de bas en haut pour trouver la premiere case libre.
    for ligne in range(NB_LIGNES - 1, -1, -1):
        # Si la case est vide, le pion s'y pose.
        if plateau[ligne][colonne] == outils.VIDE:
            plateau[ligne][colonne] = joueur
            return ligne

    # Ce retour de secours ne devrait pas arriver.
    return None


# Cette fonction verifie si 4 cases consecutives appartiennent au meme joueur.
def _quatre_alignes(plateau, ligne, colonne, delta_ligne, delta_colonne):
    # On lit le pion de depart.
    pion = plateau[ligne][colonne]
    # Une case vide ne peut pas lancer une combinaison gagnante.
    if pion == outils.VIDE:
        return None

    # On teste les 4 cases de la direction choisie.
    for pas in range(1, 4):
        # On calcule la prochaine case a verifier.
        nouvelle_ligne = ligne + delta_ligne * pas
        nouvelle_colonne = colonne + delta_colonne * pas

        # Si la case sort du plateau, la combinaison est impossible.
        if not (0 <= nouvelle_ligne < NB_LIGNES and 0 <= nouvelle_colonne < NB_COLONNES):
            return None

        # Si une case differe, la suite n'est pas gagnante.
        if plateau[nouvelle_ligne][nouvelle_colonne] != pion:
            return None

    # Si les 4 cases sont valides et identiques, on retourne le gagnant.
    return pion


# Cette fonction retourne le joueur gagnant si une ligne de 4 existe.
def gagnant(plateau):
    # On parcourt tout le plateau.
    for ligne in range(NB_LIGNES):
        for colonne in range(NB_COLONNES):
            # On teste les 4 directions utiles.
            for delta_ligne, delta_colonne in ((0, 1), (1, 0), (1, 1), (1, -1)):
                resultat = _quatre_alignes(plateau, ligne, colonne, delta_ligne, delta_colonne)
                if resultat is not None:
                    return resultat

    # Si rien n'est trouve, il n'y a pas encore de gagnant.
    return None


# Cette fonction retourne l'etat global de la partie.
def verifier_gagnant(plateau):
    # On cherche un gagnant direct.
    pion_gagnant = gagnant(plateau)
    if pion_gagnant is not None:
        return pion_gagnant

    # Si le haut de toutes les colonnes est occupe, la partie est nulle.
    if all(plateau[0][colonne] != outils.VIDE for colonne in range(NB_COLONNES)):
        return "Nul"

    # Sinon la partie continue.
    return None


# Cette fonction calcule le score d'une fenetre de 4 cases.
def _score_fenetre(fenetre, pion_ia):
    # On determine l'adversaire de l'IA.
    pion_adverse = outils.joueur_suivant(pion_ia)
    # On compte les symboles dans cette fenetre.
    nb_ia = fenetre.count(pion_ia)
    nb_adverse = fenetre.count(pion_adverse)
    nb_vides = fenetre.count(outils.VIDE)

    # Les gains/pertes directs sont traites au plus fort.
    if nb_ia == 4:
        return 100_000
    if nb_adverse == 4:
        return -100_000

    # Sinon on construit une evaluation simple et pedagogique.
    score = 0

    if nb_ia == 3 and nb_vides == 1:
        score += 80
    elif nb_ia == 2 and nb_vides == 2:
        score += 14
    elif nb_ia == 1 and nb_vides == 3:
        score += 3

    if nb_adverse == 3 and nb_vides == 1:
        score -= 70
    elif nb_adverse == 2 and nb_vides == 2:
        score -= 12

    return score


# Cette fonction evalue un plateau du point de vue de l'IA.
def calcul_score(plateau, pion_ia):
    # On commence par tester les fins de partie.
    resultat = verifier_gagnant(plateau)
    if resultat == pion_ia:
        return 100_000
    if resultat == "Nul":
        return 0
    if resultat is not None:
        return -100_000

    # On initialise un score neutre.
    score = 0
    pion_adverse = outils.joueur_suivant(pion_ia)

    # Le centre est strategiquement important au Puissance 4.
    colonne_centrale = [plateau[ligne][NB_COLONNES // 2] for ligne in range(NB_LIGNES)]
    score += colonne_centrale.count(pion_ia) * 6
    score -= colonne_centrale.count(pion_adverse) * 4

    # Fenetres horizontales.
    for ligne in range(NB_LIGNES):
        for colonne in range(NB_COLONNES - 3):
            fenetre = [plateau[ligne][colonne + decalage] for decalage in range(4)]
            score += _score_fenetre(fenetre, pion_ia)

    # Fenetres verticales.
    for ligne in range(NB_LIGNES - 3):
        for colonne in range(NB_COLONNES):
            fenetre = [plateau[ligne + decalage][colonne] for decalage in range(4)]
            score += _score_fenetre(fenetre, pion_ia)

    # Fenetres diagonales descendantes.
    for ligne in range(NB_LIGNES - 3):
        for colonne in range(NB_COLONNES - 3):
            fenetre = [plateau[ligne + decalage][colonne + decalage] for decalage in range(4)]
            score += _score_fenetre(fenetre, pion_ia)

    # Fenetres diagonales montantes.
    for ligne in range(3, NB_LIGNES):
        for colonne in range(NB_COLONNES - 3):
            fenetre = [plateau[ligne - decalage][colonne + decalage] for decalage in range(4)]
            score += _score_fenetre(fenetre, pion_ia)

    return score
