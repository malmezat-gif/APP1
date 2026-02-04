def verifier_gagnant(plateau):
    combinaisons = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for ligne in combinaisons:
        c1 = plateau[ligne[0]]
        c2 = plateau[ligne[1]]
        c3 = plateau[ligne[2]]
        
        if c1 == c2 == c3 and c1 != " ":
            return c1

    if " " not in plateau:
        return "Nul"
    
    return None

def calcul_score(plateau, pion_ia):
    gagnant = verifier_gagnant(plateau)
    
    if gagnant == pion_ia:
        return 1000
    elif gagnant == "Nul":
        return 0
    elif gagnant is not None:
        return -1000

    score = 0
    pion_adversaire = "O" if pion_ia == "X" else "X"
    
    combinaisons = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for ligne in combinaisons:
        valeurs = [plateau[i] for i in ligne]
        nb_ia = valeurs.count(pion_ia)
        nb_adv = valeurs.count(pion_adversaire)
        
        if nb_ia > 0 and nb_adv > 0:
            continue
            
        if nb_ia == 2:
            score += 30
        elif nb_ia == 1:
            score += 10
            
        if nb_adv == 2:
            score -= 30
        elif nb_adv == 1:
            score -= 10
            
    return score
