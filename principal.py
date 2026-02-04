import regles
import ia
import outils

def afficher(p):
    print("\n")
    print(f"  {p[0]} | {p[1]} | {p[2]} ")
    print(" ---+---+---")
    print(f"  {p[3]} | {p[4]} | {p[5]} ")
    print(" ---+---+---")
    print(f"  {p[6]} | {p[7]} | {p[8]} ")
    print("\n")

def main():
    print("JEU DU MORPION")
    
    plateau = [" "] * 9
    joueur_humain = "O"
    joueur_ia = "X"
    
    try:
        niveau = int(input("Difficulté (1-9) : "))
    except:
        niveau = 4

    tour_humain = True
    
    while True:
        afficher(plateau)
        
        res = regles.verifier_gagnant(plateau)
        if res:
            if res == "Nul":
                print("MATCH NUL")
            else:
                print(f"Le joueur {res} a gagné")
            break
            
        if tour_humain:
            print(f"A vous ({joueur_humain})")
            try:
                case = int(input("Case (0-8) : "))
                if case < 0 or case > 8 or plateau[case] != " ":
                    continue
            except:
                continue
                
            plateau[case] = joueur_humain
            tour_humain = False
            
        else:
            print(f"L'IA ({joueur_ia}) réfléchit...")
            
            arbre_possibles = ia.generer_arbre(plateau, joueur_ia, niveau)
            
            meilleur_coup = None
            meilleure_note = -99999
            
            options = outils.get_sous_arbres(arbre_possibles)
            
            for option in options:
                note = ia.minimax(option, niveau - 1, False, joueur_ia)
                plat_option = outils.get_racine(option)
                
                print(f"Option score : {note}")
                
                if note > meilleure_note:
                    meilleure_note = note
                    meilleur_coup = plat_option
            
            if meilleur_coup:
                plateau = meilleur_coup
                print(f"IA choisit score : {meilleure_note}")
            
            tour_humain = True

if __name__ == "__main__":
    main()
