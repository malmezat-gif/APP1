# Interface graphique moderne et minimaliste du morpion.
# Le code reste volontairement simple pour rester lisible par des eleves.

import tkinter as tk
from tkinter import messagebox

import ia
import regles
import outils


# -----------------------------
# Etat global du jeu
# -----------------------------

# Plateau 3x3 (9 cases)
plateau = [" "] * 9

# Joueur courant: "X" ou "O"
joueur_courant = "X"

# Niveau de difficulte (profondeur Minimax)
niveau = 4

# Mode actuel: jvia / jvj / iavia
mode_jeu = "jvia"

# Type de chaque joueur selon le mode
# Ex: {"X": "humain", "O": "ia"}
types_joueurs = {"X": "humain", "O": "ia"}

# Drapeaux de controle
partie_terminee = False
ia_en_cours = False


# -----------------------------
# Widgets Tkinter
# -----------------------------

fenetre = None
label_tour = None
label_niveau = None
var_mode = None
scale_niveau = None
boutons_cases = []


# -----------------------------
# Couleurs (style moderne)
# -----------------------------

COULEUR_BG = "#0b1220"
COULEUR_CARTE = "#111827"
COULEUR_CELLULE = "#1f2937"
COULEUR_SURVOL = "#334155"
COULEUR_TEXTE = "#e5e7eb"
COULEUR_X = "#ef4444"
COULEUR_O = "#22d3ee"
COULEUR_ACCENT = "#10b981"
COULEUR_ACCENT_HOVER = "#059669"


# -----------------------------
# Fonctions utilitaires
# -----------------------------

def mode_depuis_texte(texte):
    # Convertit le texte affiche en code mode interne.
    if texte == "Joueur vs Joueur":
        return "jvj"
    if texte == "IA vs IA":
        return "iavia"
    return "jvia"


def appliquer_mode():
    # Met a jour le mode et le type des joueurs.
    global mode_jeu, types_joueurs

    mode_jeu = mode_depuis_texte(var_mode.get())

    if mode_jeu == "jvj":
        types_joueurs = {"X": "humain", "O": "humain"}
    elif mode_jeu == "iavia":
        types_joueurs = {"X": "ia", "O": "ia"}
    else:
        # En Joueur vs IA: X humain, O IA
        types_joueurs = {"X": "humain", "O": "ia"}


def couleur_pion(pion):
    # Donne la couleur d'affichage selon le pion.
    if pion == "X":
        return COULEUR_X
    if pion == "O":
        return COULEUR_O
    return COULEUR_TEXTE


def texte_mode(mode):
    # Texte lisible pour l'etat du mode.
    if mode == "jvj":
        return "Joueur vs Joueur"
    if mode == "iavia":
        return "IA vs IA"
    return "Joueur vs IA"


def tour_humain_possible():
    # Le clic est possible seulement pendant un tour humain.
    if partie_terminee:
        return False
    if ia_en_cours:
        return False
    return types_joueurs[joueur_courant] == "humain"


# -----------------------------
# Mise a jour de l'affichage
# -----------------------------

def mettre_a_jour_label_tour(message=""):
    # Met a jour le message principal (tour courant).
    if message != "":
        label_tour.config(text=message)
        return

    if partie_terminee:
        label_tour.config(text="Partie terminee")
        return

    type_joueur = types_joueurs[joueur_courant]
    label_tour.config(text=f"Tour de {joueur_courant} ({type_joueur})")


def mettre_a_jour_label_niveau():
    # Affiche le niveau courant sous le slider.
    label_niveau.config(text=f"Difficulte: {int(scale_niveau.get())}")


def rafraichir_plateau():
    # Met a jour les 9 cases visuellement.
    for index in range(9):
        bouton = boutons_cases[index]
        pion = plateau[index]

        # Texte et couleur du pion.
        if pion == " ":
            bouton.config(text="", fg=COULEUR_TEXTE)
        else:
            bouton.config(text=pion, fg=couleur_pion(pion))

        # Gestion de l'activation des boutons.
        if pion != " ":
            bouton.config(state="disabled")
            continue

        if tour_humain_possible():
            bouton.config(state="normal")
        else:
            bouton.config(state="disabled")


def survol_case_entree(event):
    # Effet de survol pour une sensation plus fluide.
    bouton = event.widget
    if str(bouton["state"]) == "normal":
        bouton.config(bg=COULEUR_SURVOL)


def survol_case_sortie(event):
    # Revient a la couleur normale quand la souris sort.
    bouton = event.widget
    if str(bouton["state"]) == "normal":
        bouton.config(bg=COULEUR_CELLULE)


# -----------------------------
# Logique de partie
# -----------------------------

def verifier_fin_partie():
    # Verifie victoire ou match nul.
    global partie_terminee

    resultat = regles.verifier_gagnant(plateau)
    if resultat is None:
        return False

    partie_terminee = True
    rafraichir_plateau()

    if resultat == "Nul":
        message = "Match nul"
    else:
        message = f"Le joueur {resultat} a gagne"

    mettre_a_jour_label_tour(message)
    messagebox.showinfo("Fin de partie", message)
    return True


def passer_joueur_suivant():
    # Alterne X/O.
    global joueur_courant
    joueur_courant = outils.joueur_suivant(joueur_courant)


def finir_tour():
    # Etapes executees apres un coup (humain ou IA).
    rafraichir_plateau()

    # Si la partie est finie, on arrete ici.
    if verifier_fin_partie():
        return

    # Sinon on passe au joueur suivant.
    passer_joueur_suivant()
    rafraichir_plateau()
    mettre_a_jour_label_tour("")

    # Si le prochain joueur est une IA, on la lance automatiquement.
    if types_joueurs[joueur_courant] == "ia":
        fenetre.after(180, lancer_tour_ia)


def lancer_tour_ia():
    # Lance un tour IA avec un petit delai pour fluidifier l'interface.
    global ia_en_cours

    if partie_terminee:
        return

    if types_joueurs[joueur_courant] != "ia":
        return

    ia_en_cours = True
    mettre_a_jour_label_tour(f"IA {joueur_courant} reflechit...")
    rafraichir_plateau()

    # Petit delai avant calcul pour laisser voir l'etat "reflechit".
    fenetre.after(220, jouer_coup_ia)


def jouer_coup_ia():
    # Fait jouer l'IA pour le joueur courant.
    global plateau, ia_en_cours

    profondeur = int(scale_niveau.get())

    meilleur_coup, meilleure_note, _ = ia.choisir_meilleur_coup(
        plateau,
        joueur_courant,
        profondeur,
    )

    # Si aucun coup n'est trouve, on termine proprement.
    if meilleur_coup is None:
        ia_en_cours = False
        verifier_fin_partie()
        return

    plateau = meilleur_coup

    ia_en_cours = False
    mettre_a_jour_label_tour(f"IA {joueur_courant} joue (score {meilleure_note})")

    # On continue la partie.
    fenetre.after(120, finir_tour)


def clic_case(index):
    # Gere le clic d'un joueur humain sur une case.
    if not tour_humain_possible():
        return

    if plateau[index] != " ":
        return

    plateau[index] = joueur_courant
    finir_tour()


def nouvelle_partie():
    # Reinitialise tout l'etat de la partie.
    global plateau, joueur_courant, partie_terminee, ia_en_cours, niveau

    appliquer_mode()

    plateau = [" "] * 9
    joueur_courant = "X"
    partie_terminee = False
    ia_en_cours = False

    niveau = int(scale_niveau.get())

    rafraichir_plateau()
    mettre_a_jour_label_tour("")
    mettre_a_jour_label_niveau()

    # En mode IA vs IA, ou si X est IA, on demarre automatiquement.
    if types_joueurs[joueur_courant] == "ia":
        fenetre.after(220, lancer_tour_ia)


def changement_mode(_=None):
    # Quand le mode change, on relance une partie propre.
    nouvelle_partie()


def changement_niveau(_=None):
    # Quand le slider bouge, on met juste a jour le label.
    mettre_a_jour_label_niveau()


# -----------------------------
# Construction de la fenetre
# -----------------------------

def creer_interface():
    # Initialise la fenetre principale.
    global fenetre, label_tour, label_niveau, var_mode, scale_niveau

    fenetre = tk.Tk()
    fenetre.title("Morpion - Interface moderne")
    fenetre.geometry("560x720")
    fenetre.minsize(520, 680)
    fenetre.configure(bg=COULEUR_BG)

    # Bloc principal centrer sur la fenetre.
    cadre_principal = tk.Frame(fenetre, bg=COULEUR_CARTE, padx=18, pady=18)
    cadre_principal.pack(fill="both", expand=True, padx=18, pady=18)

    # Titre sobre.
    label_titre = tk.Label(
        cadre_principal,
        text="MORPION",
        font=("Avenir", 30, "bold"),
        bg=COULEUR_CARTE,
        fg=COULEUR_TEXTE,
    )
    label_titre.pack(pady=(4, 2))

    label_sous_titre = tk.Label(
        cadre_principal,
        text="Interface minimaliste et cliquable",
        font=("Avenir", 11),
        bg=COULEUR_CARTE,
        fg="#9ca3af",
    )
    label_sous_titre.pack(pady=(0, 12))

    # Ligne de controles: mode + niveau.
    cadre_controles = tk.Frame(cadre_principal, bg=COULEUR_CARTE)
    cadre_controles.pack(fill="x", pady=(0, 10))

    tk.Label(
        cadre_controles,
        text="Mode",
        font=("Avenir", 11, "bold"),
        bg=COULEUR_CARTE,
        fg=COULEUR_TEXTE,
    ).grid(row=0, column=0, sticky="w")

    var_mode = tk.StringVar(value=texte_mode(mode_jeu))
    menu_mode = tk.OptionMenu(
        cadre_controles,
        var_mode,
        "Joueur vs IA",
        "Joueur vs Joueur",
        "IA vs IA",
        command=changement_mode,
    )
    menu_mode.config(
        bg=COULEUR_CELLULE,
        fg=COULEUR_TEXTE,
        activebackground=COULEUR_SURVOL,
        highlightthickness=0,
        relief="flat",
        width=16,
    )
    menu_mode["menu"].config(bg=COULEUR_CELLULE, fg=COULEUR_TEXTE)
    menu_mode.grid(row=0, column=1, sticky="w", padx=(8, 20))

    tk.Label(
        cadre_controles,
        text="Niveau",
        font=("Avenir", 11, "bold"),
        bg=COULEUR_CARTE,
        fg=COULEUR_TEXTE,
    ).grid(row=0, column=2, sticky="w")

    scale_niveau = tk.Scale(
        cadre_controles,
        from_=1,
        to=9,
        orient="horizontal",
        command=changement_niveau,
        bg=COULEUR_CARTE,
        fg=COULEUR_TEXTE,
        troughcolor=COULEUR_CELLULE,
        highlightthickness=0,
        length=140,
    )
    scale_niveau.set(niveau)
    scale_niveau.grid(row=0, column=3, sticky="w", padx=(8, 0))

    # Bouton unique pour reset (minimal).
    bouton_reset = tk.Button(
        cadre_principal,
        text="Nouvelle partie",
        command=nouvelle_partie,
        font=("Avenir", 11, "bold"),
        bg=COULEUR_ACCENT,
        fg="#042f2e",
        activebackground=COULEUR_ACCENT_HOVER,
        activeforeground="#042f2e",
        relief="flat",
        padx=12,
        pady=8,
        bd=0,
        cursor="hand2",
    )
    bouton_reset.pack(pady=(2, 14))

    # Label de statut.
    label_tour = tk.Label(
        cadre_principal,
        text="",
        font=("Avenir", 14, "bold"),
        bg=COULEUR_CARTE,
        fg=COULEUR_TEXTE,
    )
    label_tour.pack(pady=(0, 8))

    label_niveau = tk.Label(
        cadre_principal,
        text="",
        font=("Avenir", 10),
        bg=COULEUR_CARTE,
        fg="#9ca3af",
    )
    label_niveau.pack(pady=(0, 12))

    # Plateau 3x3 en boutons larges.
    cadre_plateau = tk.Frame(cadre_principal, bg=COULEUR_CARTE)
    cadre_plateau.pack(pady=(6, 6))

    boutons_cases.clear()

    for index in range(9):
        bouton = tk.Button(
            cadre_plateau,
            text="",
            command=lambda i=index: clic_case(i),
            font=("Avenir", 36, "bold"),
            width=4,
            height=2,
            bg=COULEUR_CELLULE,
            fg=COULEUR_TEXTE,
            activebackground=COULEUR_SURVOL,
            activeforeground=COULEUR_TEXTE,
            relief="flat",
            bd=0,
            cursor="hand2",
            disabledforeground="#6b7280",
        )

        ligne = index // 3
        colonne = index % 3
        bouton.grid(row=ligne, column=colonne, padx=6, pady=6)

        bouton.bind("<Enter>", survol_case_entree)
        bouton.bind("<Leave>", survol_case_sortie)

        boutons_cases.append(bouton)

    # Note d'aide courte, sans boutons supplementaires.
    label_aide = tk.Label(
        cadre_principal,
        text="Clique sur une case pour jouer. Change mode/niveau puis relance une partie.",
        font=("Avenir", 10),
        bg=COULEUR_CARTE,
        fg="#9ca3af",
        wraplength=500,
        justify="center",
    )
    label_aide.pack(pady=(12, 2))

    # Lancement de la premiere partie.
    nouvelle_partie()

    fenetre.mainloop()


if __name__ == "__main__":
    creer_interface()
