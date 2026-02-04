import tkinter as tk
from tkinter import messagebox
import regles
import ia
import outils

plateau = [" "] * 9
joueur_humain = "O"
joueur_ia = "X"
niveau = 4
tour_humain = True
fenetre = None
canvas = None

def dessiner_grille():
    canvas.delete("all")
    
    canvas.create_line(100, 0, 100, 300, width=5)
    canvas.create_line(200, 0, 200, 300, width=5)
    canvas.create_line(0, 100, 300, 100, width=5)
    canvas.create_line(0, 200, 300, 200, width=5)

    for i in range(9):
        x = (i % 3) * 100 + 50
        y = (i // 3) * 100 + 50
        
        pion = plateau[i]
        
        if pion == "X":
            canvas.create_line(x-30, y-30, x+30, y+30, width=4, fill="red")
            canvas.create_line(x+30, y-30, x-30, y+30, width=4, fill="red")
        elif pion == "O":
            canvas.create_oval(x-30, y-30, x+30, y+30, width=4, outline="blue")

def verifier_fin():
    gagnant = regles.verifier_gagnant(plateau)
    
    if gagnant:
        dessiner_grille()
        if gagnant == "Nul":
            messagebox.showinfo("Fin", "Match Nul")
        else:
            messagebox.showinfo("Fin", f"Vainqueur : {gagnant}")
        fenetre.quit()
        return True
    return False

def jouer_ia():
    global plateau, tour_humain
    
    arbre = ia.generer_arbre(plateau, joueur_ia, niveau)
    
    meilleur_coup = None
    meilleure_note = -99999
    
    options = outils.get_sous_arbres(arbre)
    
    for option in options:
        note = ia.minimax(option, niveau - 1, False, joueur_ia)
        
        if note > meilleure_note:
            meilleure_note = note
            meilleur_coup = outils.get_racine(option)
            
    if meilleur_coup:
        plateau = meilleur_coup
    
    dessiner_grille()
    if not verifier_fin():
        tour_humain = True

def clic(event):
    global plateau, tour_humain
    
    if not tour_humain:
        return

    col = event.x // 100
    lig = event.y // 100
    case = lig * 3 + col
    
    if plateau[case] == " ":
        plateau[case] = joueur_humain
        dessiner_grille()
        
        if not verifier_fin():
            tour_humain = False
            fenetre.after(100, jouer_ia)

def lancer():
    global fenetre, canvas, niveau
    
    try:
        niveau = int(input("Niveau (1-9) : "))
    except:
        niveau = 4

    fenetre = tk.Tk()
    fenetre.title("Morpion")
    
    canvas = tk.Canvas(fenetre, width=300, height=300, bg="white")
    canvas.pack()
    
    canvas.bind("<Button-1>", clic)
    
    dessiner_grille()
    fenetre.mainloop()

if __name__ == "__main__":
    lancer()
