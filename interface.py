"""Interface graphique simple du morpion (Tkinter, sans dependance externe)."""

import tkinter as tk
from tkinter import messagebox, ttk

import ia
import regles
import outils


class MorpionApp:
    """Fenetre principale du jeu."""

    MODES = ("Joueur vs IA", "Joueur vs Joueur", "IA vs IA")

    def __init__(self, root):
        self.root = root
        self.root.title("Morpion")
        self.root.resizable(False, False)

        self.plateau = outils.plateau_vide()
        self.joueur_courant = "X"
        self.partie_terminee = False
        self.ia_en_cours = False
        self.scores = {"X": 0, "O": 0, "Nul": 0}

        self.mode_var = tk.StringVar(value=self.MODES[0])
        self.niveau_var = tk.IntVar(value=4)
        self.statut_var = tk.StringVar(value="")
        self.niveau_label_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="")

        self.boutons = []
        self._construire_interface()
        self.nouvelle_partie()

    def _construire_interface(self):
        conteneur = ttk.Frame(self.root, padding=12)
        conteneur.grid(row=0, column=0, sticky="nsew")

        ttk.Label(conteneur, text="Mode:").grid(row=0, column=0, sticky="w")
        self.combo_mode = ttk.Combobox(
            conteneur,
            textvariable=self.mode_var,
            values=self.MODES,
            width=18,
            state="readonly",
        )
        self.combo_mode.grid(row=0, column=1, sticky="ew", padx=(8, 8))
        self.combo_mode.bind("<<ComboboxSelected>>", self._changement_mode)

        ttk.Label(conteneur, text="Difficulte:").grid(row=0, column=2, sticky="w")
        self.scale_niveau = tk.Scale(
            conteneur,
            from_=1,
            to=9,
            orient="horizontal",
            variable=self.niveau_var,
            showvalue=False,
            length=120,
            command=self._changement_niveau,
        )
        self.scale_niveau.grid(row=0, column=3, sticky="ew")

        bouton_nouvelle = ttk.Button(conteneur, text="Nouvelle partie", command=self.nouvelle_partie)
        bouton_nouvelle.grid(row=0, column=4, padx=(10, 0))

        ttk.Label(conteneur, textvariable=self.statut_var, font=("Helvetica", 12, "bold")).grid(
            row=1,
            column=0,
            columnspan=5,
            pady=(10, 0),
            sticky="ew",
        )
        ttk.Label(conteneur, textvariable=self.niveau_label_var).grid(row=2, column=0, columnspan=5, sticky="ew")
        ttk.Label(conteneur, textvariable=self.score_var).grid(row=3, column=0, columnspan=5, sticky="ew")

        grille = ttk.Frame(conteneur, padding=(0, 10, 0, 0))
        grille.grid(row=4, column=0, columnspan=5)

        for index in range(9):
            bouton = tk.Button(
                grille,
                text="",
                width=4,
                height=2,
                font=("Helvetica", 28, "bold"),
                command=lambda i=index: self.clic_case(i),
            )
            bouton.grid(row=index // 3, column=index % 3, padx=4, pady=4)
            self.boutons.append(bouton)

    def _mode_code(self):
        if self.mode_var.get() == "Joueur vs Joueur":
            return "jvj"
        if self.mode_var.get() == "IA vs IA":
            return "iavia"
        return "jvia"

    def _types_joueurs(self):
        mode = self._mode_code()
        if mode == "jvj":
            return {"X": "humain", "O": "humain"}
        if mode == "iavia":
            return {"X": "ia", "O": "ia"}
        return {"X": "humain", "O": "ia"}

    def _tour_humain_possible(self):
        if self.partie_terminee or self.ia_en_cours:
            return False
        return self._types_joueurs()[self.joueur_courant] == "humain"

    def _mettre_a_jour_labels(self, message=None):
        if message is not None:
            self.statut_var.set(message)
        elif self.partie_terminee:
            self.statut_var.set("Partie terminee")
        else:
            role = self._types_joueurs()[self.joueur_courant]
            self.statut_var.set(f"Tour de {self.joueur_courant} ({role})")

        self.niveau_label_var.set(f"Niveau IA: {self.niveau_var.get()}")
        self.score_var.set(
            f"Score X: {self.scores['X']}   Score O: {self.scores['O']}   Nuls: {self.scores['Nul']}"
        )

    def _rafraichir_plateau(self):
        for index, bouton in enumerate(self.boutons):
            pion = self.plateau[index]
            if pion == outils.VIDE:
                bouton.config(text="", state="normal" if self._tour_humain_possible() else "disabled")
                continue

            couleur = "#b91c1c" if pion == "X" else "#0e7490"
            bouton.config(text=pion, fg=couleur, state="disabled")

    def _verifier_fin(self):
        resultat = regles.verifier_gagnant(self.plateau)
        if resultat is None:
            return False

        self.partie_terminee = True
        self.scores[resultat] += 1

        if resultat == "Nul":
            message = "Match nul"
        else:
            message = f"Le joueur {resultat} a gagne"

        self._mettre_a_jour_labels(message)
        self._rafraichir_plateau()
        messagebox.showinfo("Fin de partie", message)
        return True

    def _finir_tour(self):
        if self._verifier_fin():
            return

        self.joueur_courant = outils.joueur_suivant(self.joueur_courant)
        self._mettre_a_jour_labels()
        self._rafraichir_plateau()

        if self._types_joueurs()[self.joueur_courant] == "ia":
            self.root.after(150, self._lancer_tour_ia)

    def _lancer_tour_ia(self):
        if self.partie_terminee:
            return
        if self._types_joueurs()[self.joueur_courant] != "ia":
            return

        self.ia_en_cours = True
        self._mettre_a_jour_labels(f"IA {self.joueur_courant} reflechit...")
        self._rafraichir_plateau()
        self.root.after(180, self._jouer_coup_ia)

    def _jouer_coup_ia(self):
        profondeur = self.niveau_var.get()
        meilleur_coup, meilleure_note, _ = ia.choisir_meilleur_coup(
            self.plateau,
            self.joueur_courant,
            profondeur,
        )

        self.ia_en_cours = False
        if meilleur_coup is None:
            self._finir_tour()
            return

        self.plateau = meilleur_coup
        self._mettre_a_jour_labels(f"IA {self.joueur_courant} joue (note {meilleure_note})")
        self.root.after(100, self._finir_tour)

    def clic_case(self, index):
        if not self._tour_humain_possible():
            return
        if self.plateau[index] != outils.VIDE:
            return

        self.plateau[index] = self.joueur_courant
        self._finir_tour()

    def _changement_mode(self, _event):
        self.nouvelle_partie()

    def _changement_niveau(self, _valeur):
        self._mettre_a_jour_labels()

    def nouvelle_partie(self):
        self.plateau = outils.plateau_vide()
        self.joueur_courant = "X"
        self.partie_terminee = False
        self.ia_en_cours = False

        self._mettre_a_jour_labels()
        self._rafraichir_plateau()

        if self._types_joueurs()[self.joueur_courant] == "ia":
            self.root.after(150, self._lancer_tour_ia)


def main():
    root = tk.Tk()
    MorpionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
