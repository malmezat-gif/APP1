# Ce fichier contient l'interface graphique du morpion.
# Le jeu est 100% pilotable a la souris depuis cette fenetre.

# On importe Tkinter (bibliotheque graphique standard de Python).
import tkinter as tk
# On importe un popup (messagebox) et les widgets modernes (ttk).
from tkinter import messagebox, ttk

# On importe le module IA pour calculer les coups automatiques.
import ia
# On importe les regles du jeu (victoire, nul, etc.).
import regles
# On importe les utilitaires (plateau vide, joueur suivant, ...).
import outils


# Cette classe represente toute l'application graphique.
class MorpionApp:
    # Cette docstring explique le role global de la classe.
    """Fenetre principale du jeu."""

    # Cette constante contient les modes affiches dans la liste deroulante.
    MODES = ("Joueur vs IA", "Joueur vs Joueur", "IA vs IA")

    # Le constructeur initialise la fenetre, l'etat du jeu et l'interface.
    def __init__(self, root):
        # On garde une reference vers la fenetre principale Tkinter.
        self.root = root
        # On definit le titre de la fenetre.
        self.root.title("Morpion")
        # On empeche le redimensionnement pour garder un layout simple.
        self.root.resizable(False, False)

        # On cree un plateau vide (9 cases).
        self.plateau = outils.plateau_vide()
        # X commence toujours au debut d'une partie.
        self.joueur_courant = "X"
        # Ce drapeau passe a True quand la partie est terminee.
        self.partie_terminee = False
        # Ce drapeau passe a True pendant le calcul du coup IA.
        self.ia_en_cours = False
        # Ce dictionnaire garde les scores cumules des manches.
        self.scores = {"X": 0, "O": 0, "Nul": 0}

        # Variable Tkinter qui stocke le texte du mode courant.
        self.mode_var = tk.StringVar(value=self.MODES[0])
        # Variable Tkinter qui stocke la difficulte (profondeur IA).
        self.niveau_var = tk.IntVar(value=4)
        # Variable Tkinter pour le texte du statut en haut.
        self.statut_var = tk.StringVar(value="")
        # Variable Tkinter pour afficher le niveau courant.
        self.niveau_label_var = tk.StringVar(value="")
        # Variable Tkinter pour afficher les scores.
        self.score_var = tk.StringVar(value="")

        # Liste qui contiendra les 9 boutons de la grille.
        self.boutons = []
        # On construit tous les widgets de la fenetre.
        self._construire_interface()
        # On lance une partie propre au demarrage.
        self.nouvelle_partie()

    # Cette methode construit visuellement la fenetre.
    def _construire_interface(self):
        # On cree un cadre principal avec un peu de marge interne.
        conteneur = ttk.Frame(self.root, padding=12)
        # On place ce cadre dans la fenetre avec grid.
        conteneur.grid(row=0, column=0, sticky="nsew")

        # Etiquette "Mode:" a gauche.
        ttk.Label(conteneur, text="Mode:").grid(row=0, column=0, sticky="w")
        # Combobox pour choisir le mode de jeu.
        self.combo_mode = ttk.Combobox(
            # Parent de la combobox.
            conteneur,
            # Variable liee au texte selectionne.
            textvariable=self.mode_var,
            # Liste des options possibles.
            values=self.MODES,
            # Largeur visuelle en caracteres.
            width=18,
            # readonly interdit de taper du texte libre.
            state="readonly",
        )
        # Placement de la combobox.
        self.combo_mode.grid(row=0, column=1, sticky="ew", padx=(8, 8))
        # Quand l'utilisateur change le mode, on declenche une nouvelle partie.
        self.combo_mode.bind("<<ComboboxSelected>>", self._changement_mode)

        # Etiquette "Difficulte:" a cote du slider.
        ttk.Label(conteneur, text="Difficulte:").grid(row=0, column=2, sticky="w")
        # Slider horizontal pour regler la profondeur de l'IA.
        self.scale_niveau = tk.Scale(
            # Parent du slider.
            conteneur,
            # Valeur minimale.
            from_=1,
            # Valeur maximale.
            to=9,
            # Orientation horizontale.
            orient="horizontal",
            # Variable liee a la valeur du slider.
            variable=self.niveau_var,
            # On cache la valeur numerique standard du widget.
            showvalue=False,
            # Longueur visuelle du slider.
            length=120,
            # Callback appele a chaque changement.
            command=self._changement_niveau,
        )
        # Placement du slider.
        self.scale_niveau.grid(row=0, column=3, sticky="ew")

        # Bouton pour relancer une nouvelle manche.
        bouton_nouvelle = ttk.Button(conteneur, text="Nouvelle partie", command=self.nouvelle_partie)
        # Placement du bouton.
        bouton_nouvelle.grid(row=0, column=4, padx=(10, 0))

        # Label du statut (tour courant / message de fin).
        ttk.Label(conteneur, textvariable=self.statut_var, font=("Helvetica", 12, "bold")).grid(
            # Ligne du label.
            row=1,
            # Colonne de depart.
            column=0,
            # Le label prend la largeur des 5 colonnes.
            columnspan=5,
            # Petite marge verticale.
            pady=(10, 0),
            # Etirement horizontal.
            sticky="ew",
        )
        # Label d'information du niveau IA courant.
        ttk.Label(conteneur, textvariable=self.niveau_label_var).grid(row=2, column=0, columnspan=5, sticky="ew")
        # Label des scores cumules.
        ttk.Label(conteneur, textvariable=self.score_var).grid(row=3, column=0, columnspan=5, sticky="ew")

        # Cadre qui contient la grille 3x3 des boutons du plateau.
        grille = ttk.Frame(conteneur, padding=(0, 10, 0, 0))
        # Placement du cadre grille.
        grille.grid(row=4, column=0, columnspan=5)

        # Boucle pour creer exactement 9 boutons (3 lignes x 3 colonnes).
        for index in range(9):
            # Creation d'un bouton de case.
            bouton = tk.Button(
                # Parent du bouton.
                grille,
                # Texte initial vide.
                text="",
                # Largeur visuelle.
                width=4,
                # Hauteur visuelle.
                height=2,
                # Police du pion affiche.
                font=("Helvetica", 28, "bold"),
                # Callback clic: on passe l'index de la case.
                command=lambda i=index: self.clic_case(i),
            )
            # Placement du bouton selon son index (ligne/colonne).
            bouton.grid(row=index // 3, column=index % 3, padx=4, pady=4)
            # On memorise le bouton pour le mettre a jour plus tard.
            self.boutons.append(bouton)

    # Cette methode convertit le texte de la combobox en code interne.
    def _mode_code(self):
        # Si le mode choisi est Joueur vs Joueur.
        if self.mode_var.get() == "Joueur vs Joueur":
            # Code interne du mode humain contre humain.
            return "jvj"
        # Si le mode choisi est IA vs IA.
        if self.mode_var.get() == "IA vs IA":
            # Code interne du mode automatique.
            return "iavia"
        # Par defaut, on est en Joueur vs IA.
        return "jvia"

    # Cette methode indique pour X et O s'ils sont humains ou IA.
    def _types_joueurs(self):
        # On lit le code du mode actuel.
        mode = self._mode_code()
        # Cas joueur contre joueur.
        if mode == "jvj":
            # Les deux joueurs sont humains.
            return {"X": "humain", "O": "humain"}
        # Cas IA contre IA.
        if mode == "iavia":
            # Les deux joueurs sont des IA.
            return {"X": "ia", "O": "ia"}
        # Cas Joueur vs IA: X humain, O IA.
        return {"X": "humain", "O": "ia"}

    # Cette methode dit si un clic humain est autorise maintenant.
    def _tour_humain_possible(self):
        # Si la partie est finie, aucun clic n'est autorise.
        if self.partie_terminee or self.ia_en_cours:
            # False bloque les clics.
            return False
        # Sinon, clic autorise seulement si le joueur courant est humain.
        return self._types_joueurs()[self.joueur_courant] == "humain"

    # Cette methode met a jour tous les textes d'information de l'interface.
    def _mettre_a_jour_labels(self, message=None):
        # Si un message explicite est fourni, on l'affiche directement.
        if message is not None:
            self.statut_var.set(message)
        # Sinon, si la partie est finie, on l'indique.
        elif self.partie_terminee:
            self.statut_var.set("Partie terminee")
        # Sinon on affiche le tour de jeu courant.
        else:
            # On recupere si le joueur courant est humain ou IA.
            role = self._types_joueurs()[self.joueur_courant]
            # On met a jour le texte du statut.
            self.statut_var.set(f"Tour de {self.joueur_courant} ({role})")

        # On affiche la profondeur IA choisie avec le slider.
        self.niveau_label_var.set(f"Niveau IA: {self.niveau_var.get()}")
        # On affiche les scores cumules X, O et Nuls.
        self.score_var.set(
            # Texte formate des scores.
            f"Score X: {self.scores['X']}   Score O: {self.scores['O']}   Nuls: {self.scores['Nul']}"
        )

    # Cette methode met a jour visuellement les 9 boutons de la grille.
    def _rafraichir_plateau(self):
        # On parcourt chaque bouton avec son index.
        for index, bouton in enumerate(self.boutons):
            # On lit le contenu de la case correspondante du plateau.
            pion = self.plateau[index]
            # Si la case est vide.
            if pion == outils.VIDE:
                # On efface le texte et on active/desactive selon le tour humain.
                bouton.config(text="", state="normal" if self._tour_humain_possible() else "disabled")
                # On passe a la case suivante.
                continue

            # Si la case contient un pion, on choisit sa couleur.
            couleur = "#b91c1c" if pion == "X" else "#0e7490"
            # On affiche le pion et on bloque le bouton.
            bouton.config(text=pion, fg=couleur, state="disabled")

    # Cette methode verifie si la partie vient de se terminer.
    def _verifier_fin(self):
        # On demande aux regles l'etat de la partie.
        resultat = regles.verifier_gagnant(self.plateau)
        # Si pas de resultat final, on retourne False.
        if resultat is None:
            return False

        # On marque la partie comme terminee.
        self.partie_terminee = True
        # On incremente le score correspondant au resultat.
        self.scores[resultat] += 1

        # Si resultat nul, message adapte.
        if resultat == "Nul":
            message = "Match nul"
        # Sinon message de victoire.
        else:
            message = f"Le joueur {resultat} a gagne"

        # On met a jour les labels avec le message final.
        self._mettre_a_jour_labels(message)
        # On rafraichit l'etat des boutons.
        self._rafraichir_plateau()
        # On affiche une popup de fin de partie.
        messagebox.showinfo("Fin de partie", message)
        # On indique a l'appelant que la partie est finie.
        return True

    # Cette methode finalise un tour (humain ou IA) et enchaine si besoin.
    def _finir_tour(self):
        # Si la partie est terminee apres le coup, on arrete ici.
        if self._verifier_fin():
            return

        # Sinon on passe au joueur suivant.
        self.joueur_courant = outils.joueur_suivant(self.joueur_courant)
        # On met a jour les textes.
        self._mettre_a_jour_labels()
        # On met a jour les boutons.
        self._rafraichir_plateau()

        # Si le prochain joueur est une IA, on lance son tour automatiquement.
        if self._types_joueurs()[self.joueur_courant] == "ia":
            # Petit delai pour rendre l'animation plus naturelle.
            self.root.after(150, self._lancer_tour_ia)

    # Cette methode prepare un tour IA.
    def _lancer_tour_ia(self):
        # Si la partie est terminee, on ne fait rien.
        if self.partie_terminee:
            return
        # Securite: si le joueur courant n'est pas une IA, on ne fait rien.
        if self._types_joueurs()[self.joueur_courant] != "ia":
            return

        # On indique qu'un calcul IA est en cours (bloque les clics humains).
        self.ia_en_cours = True
        # On affiche un message d'attente.
        self._mettre_a_jour_labels(f"IA {self.joueur_courant} reflechit...")
        # On met a jour les boutons en mode bloque.
        self._rafraichir_plateau()
        # On programme l'execution du calcul IA apres un court delai.
        self.root.after(180, self._jouer_coup_ia)

    # Cette methode calcule et applique le coup IA.
    def _jouer_coup_ia(self):
        # On lit la profondeur choisie par l'utilisateur.
        profondeur = self.niveau_var.get()
        # On demande au moteur IA le meilleur coup.
        meilleur_coup, meilleure_note, _ = ia.choisir_meilleur_coup(
            # Plateau actuel.
            self.plateau,
            # Joueur qui doit jouer maintenant.
            self.joueur_courant,
            # Profondeur de recherche.
            profondeur,
        )

        # Le calcul IA est termine.
        self.ia_en_cours = False
        # Si aucun coup n'est possible, on continue la logique de fin de tour.
        if meilleur_coup is None:
            self._finir_tour()
            return

        # On applique le plateau retourne par l'IA.
        self.plateau = meilleur_coup
        # On affiche la note du coup choisi.
        self._mettre_a_jour_labels(f"IA {self.joueur_courant} joue (note {meilleure_note})")
        # On termine le tour apres un petit delai.
        self.root.after(100, self._finir_tour)

    # Cette methode est appelee quand un humain clique une case.
    def clic_case(self, index):
        # Si le clic n'est pas autorise maintenant, on ignore.
        if not self._tour_humain_possible():
            return
        # Si la case est deja occupee, on ignore.
        if self.plateau[index] != outils.VIDE:
            return

        # On place le pion du joueur courant sur la case cliquee.
        self.plateau[index] = self.joueur_courant
        # On termine le tour.
        self._finir_tour()

    # Cette methode est appelee lors d'un changement de mode.
    def _changement_mode(self, _event):
        # On relance une nouvelle partie avec les nouvelles regles de mode.
        self.nouvelle_partie()

    # Cette methode est appelee quand le slider de niveau change.
    def _changement_niveau(self, _valeur):
        # On met juste a jour les labels (pas besoin de reset la partie).
        self._mettre_a_jour_labels()

    # Cette methode reinitialise totalement l'etat d'une manche.
    def nouvelle_partie(self):
        # On recree un plateau vide.
        self.plateau = outils.plateau_vide()
        # X recommence au debut de chaque manche.
        self.joueur_courant = "X"
        # On remet le drapeau de fin a False.
        self.partie_terminee = False
        # On remet le drapeau IA en cours a False.
        self.ia_en_cours = False

        # On met a jour les textes d'information.
        self._mettre_a_jour_labels()
        # On met a jour les boutons du plateau.
        self._rafraichir_plateau()

        # Si le mode fait commencer une IA, on lance son tour automatiquement.
        if self._types_joueurs()[self.joueur_courant] == "ia":
            self.root.after(150, self._lancer_tour_ia)


# Cette fonction sert de point d'entree du programme.
def main():
    # On cree la fenetre principale Tkinter.
    root = tk.Tk()
    # On instancie l'application dans cette fenetre.
    MorpionApp(root)
    # On demarre la boucle d'evenements Tkinter.
    root.mainloop()


# Ce bloc execute main() seulement si ce fichier est lance directement.
if __name__ == "__main__":
    # On lance l'application.
    main()
