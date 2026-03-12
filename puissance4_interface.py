# Interface graphique du Puissance 4.

# Tkinter fournit les variables et les boites de dialogue.
import tkinter as tk
from tkinter import messagebox

# CustomTkinter apporte le rendu moderne.
import customtkinter as ctk

# Ces modules contiennent la logique du Puissance 4.
import outils
import puissance4_ia as ia
import puissance4_regles as regles


# On reutilise une palette proche du morpion pour garder une identite coherente.
WINDOW_BG = "#09101D"
CARD_BG = "#101826"
CARD_ALT = "#172235"
BORDER = "#243247"
TEXT_MAIN = "#F8FAFC"
TEXT_MUTED = "#94A3B8"
ACCENT = "#14B8A6"
ACCENT_HOVER = "#0F766E"
BOARD_BG = "#10233C"
BOARD_SLOT = "#20324B"
X_COLOR = "#FBBF24"
O_COLOR = "#38BDF8"
EMPTY_COLOR = "#334155"


class Puissance4App(ctk.CTkToplevel):
    """Fenetre secondaire dediee au Puissance 4."""

    MODES = ("Joueur vs IA", "Joueur vs Joueur", "IA vs IA")

    def __init__(self, parent):
        # On cree une vraie fenetre secondaire CustomTkinter.
        super().__init__(parent)
        # Titre de la fenetre.
        self.title("Puissance 4")
        # Taille par defaut de la fenetre.
        self.geometry("1040x780")
        # Taille minimale pour rester lisible.
        self.minsize(900, 700)
        # Couleur generale.
        self.configure(fg_color=WINDOW_BG)
        # La grille principale occupe toute la fenetre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Etat courant de la partie.
        self.plateau = regles.plateau_vide()
        self.joueur_courant = outils.JOUEUR_X
        self.partie_terminee = False
        self.ia_en_cours = False
        self.scores = {"X": 0, "O": 0, "Nul": 0}

        # Variables d'interface.
        self.mode_var = tk.StringVar(value=self.MODES[0])
        self.niveau_var = tk.IntVar(value=3)
        self.statut_var = tk.StringVar(value="")
        self.niveau_label_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="")

        # References graphiques utiles.
        self.boutons_colonnes = []
        self.cases = []

        # Construction de la fenetre.
        self._construire_interface()
        self.nouvelle_partie()

    def _construire_interface(self):
        # Conteneur principal de la fenetre.
        self.conteneur = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.conteneur.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self.conteneur.grid_columnconfigure(0, weight=1)

        # Carte d'entete.
        self.hero = ctk.CTkFrame(
            self.conteneur,
            fg_color=CARD_BG,
            corner_radius=28,
            border_width=1,
            border_color=BORDER,
        )
        self.hero.grid(row=0, column=0, sticky="ew")
        self.hero.grid_columnconfigure(0, weight=1)

        self.titre = ctk.CTkLabel(
            self.hero,
            text="Puissance 4",
            font=ctk.CTkFont(family="Avenir Next", size=28, weight="bold"),
            text_color=TEXT_MAIN,
        )
        self.titre.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 4))

        self.sous_titre = ctk.CTkLabel(
            self.hero,
            text="Modes Joueur vs IA, Joueur vs Joueur et IA vs IA avec profondeur limitee",
            font=ctk.CTkFont(family="Avenir Next", size=13),
            text_color=TEXT_MUTED,
        )
        self.sous_titre.grid(row=1, column=0, sticky="ew", padx=20)

        # Ligne de controles.
        self.controles = ctk.CTkFrame(self.hero, fg_color="transparent")
        self.controles.grid(row=2, column=0, sticky="ew", padx=20, pady=(16, 12))
        self.controles.grid_columnconfigure((0, 1, 2), weight=1)

        self.carte_mode = ctk.CTkFrame(
            self.controles,
            fg_color=CARD_ALT,
            corner_radius=20,
            border_width=1,
            border_color=BORDER,
        )
        self.carte_mode.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.carte_mode.grid_columnconfigure(0, weight=1)

        self.label_mode = ctk.CTkLabel(
            self.carte_mode,
            text="Mode de jeu",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            text_color=TEXT_MUTED,
        )
        self.label_mode.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))

        self.combo_mode = ctk.CTkOptionMenu(
            self.carte_mode,
            variable=self.mode_var,
            values=list(self.MODES),
            command=self._changement_mode,
            fg_color="#213149",
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color="#152033",
            dropdown_hover_color="#22314A",
            text_color=TEXT_MAIN,
            font=ctk.CTkFont(family="Avenir Next", size=14),
            dropdown_font=ctk.CTkFont(family="Avenir Next", size=13),
            corner_radius=14,
            dynamic_resizing=False,
            height=36,
        )
        self.combo_mode.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))

        self.carte_niveau = ctk.CTkFrame(
            self.controles,
            fg_color=CARD_ALT,
            corner_radius=20,
            border_width=1,
            border_color=BORDER,
        )
        self.carte_niveau.grid(row=0, column=1, sticky="ew", padx=8)
        self.carte_niveau.grid_columnconfigure(0, weight=1)

        self.label_niveau = ctk.CTkLabel(
            self.carte_niveau,
            text="Difficulte",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            text_color=TEXT_MUTED,
        )
        self.label_niveau.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))

        self.scale_niveau = ctk.CTkSlider(
            self.carte_niveau,
            from_=1,
            to=6,
            number_of_steps=5,
            variable=self.niveau_var,
            command=self._changement_niveau,
            progress_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            fg_color="#273449",
            height=16,
        )
        self.scale_niveau.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))

        self.carte_action = ctk.CTkFrame(
            self.controles,
            fg_color=CARD_ALT,
            corner_radius=20,
            border_width=1,
            border_color=BORDER,
        )
        self.carte_action.grid(row=0, column=2, sticky="ew", padx=(8, 0))
        self.carte_action.grid_columnconfigure(0, weight=1)

        self.label_action = ctk.CTkLabel(
            self.carte_action,
            text="Controle",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            text_color=TEXT_MUTED,
        )
        self.label_action.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))

        self.bouton_nouvelle = ctk.CTkButton(
            self.carte_action,
            text="Nouvelle partie",
            command=self.nouvelle_partie,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#06131E",
            font=ctk.CTkFont(family="Avenir Next", size=14, weight="bold"),
            corner_radius=14,
            height=36,
        )
        self.bouton_nouvelle.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))

        self.label_tour = ctk.CTkLabel(
            self.hero,
            textvariable=self.statut_var,
            wraplength=820,
            justify="center",
            font=ctk.CTkFont(family="Avenir Next", size=20, weight="bold"),
            text_color=TEXT_MAIN,
        )
        self.label_tour.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 6))

        self.label_niveau_detail = ctk.CTkLabel(
            self.hero,
            textvariable=self.niveau_label_var,
            font=ctk.CTkFont(family="Avenir Next", size=13),
            text_color=TEXT_MUTED,
        )
        self.label_niveau_detail.grid(row=4, column=0, sticky="ew", padx=20)

        self.label_score = ctk.CTkLabel(
            self.hero,
            textvariable=self.score_var,
            font=ctk.CTkFont(family="Avenir Next", size=14),
            text_color=TEXT_MAIN,
        )
        self.label_score.grid(row=5, column=0, sticky="ew", padx=20, pady=(4, 18))

        # Carte du plateau de jeu.
        self.carte_plateau = ctk.CTkFrame(
            self.conteneur,
            fg_color=CARD_BG,
            corner_radius=28,
            border_width=1,
            border_color=BORDER,
        )
        self.carte_plateau.grid(row=1, column=0, sticky="nsew", pady=(14, 0))
        self.carte_plateau.grid_columnconfigure(0, weight=1)
        self.carte_plateau.grid_rowconfigure(2, weight=1)

        self.titre_plateau = ctk.CTkLabel(
            self.carte_plateau,
            text="Plateau",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=17, weight="bold"),
            text_color=TEXT_MAIN,
        )
        self.titre_plateau.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 0))

        # Les boutons du haut servent a choisir une colonne.
        self.controles_colonnes = ctk.CTkFrame(self.carte_plateau, fg_color="transparent")
        self.controles_colonnes.grid(row=1, column=0, sticky="ew", padx=18, pady=(14, 0))
        self.controles_colonnes.grid_columnconfigure(tuple(range(regles.NB_COLONNES)), weight=1)

        for colonne in range(regles.NB_COLONNES):
            bouton = ctk.CTkButton(
                self.controles_colonnes,
                text=f"Col {colonne + 1}",
                command=lambda c=colonne: self.clic_colonne(c),
                fg_color=ACCENT,
                hover_color=ACCENT_HOVER,
                text_color="#06131E",
                font=ctk.CTkFont(family="Avenir Next", size=12, weight="bold"),
                corner_radius=14,
                height=34,
            )
            bouton.grid(row=0, column=colonne, padx=4, sticky="ew")
            self.boutons_colonnes.append(bouton)

        # Le plateau est dessine comme une grille de pastilles.
        self.grille = ctk.CTkFrame(
            self.carte_plateau,
            fg_color=BOARD_BG,
            corner_radius=24,
            border_width=1,
            border_color=BORDER,
        )
        self.grille.grid(row=2, column=0, sticky="nsew", padx=18, pady=18)
        self.grille.grid_columnconfigure(tuple(range(regles.NB_COLONNES)), weight=1)
        self.grille.grid_rowconfigure(tuple(range(regles.NB_LIGNES)), weight=1)

        for ligne in range(regles.NB_LIGNES):
            ligne_cases = []
            for colonne in range(regles.NB_COLONNES):
                case = ctk.CTkFrame(
                    self.grille,
                    width=70,
                    height=70,
                    corner_radius=18,
                    fg_color=BOARD_SLOT,
                )
                case.grid(row=ligne, column=colonne, padx=5, pady=5, sticky="nsew")
                case.grid_propagate(False)
                case.grid_columnconfigure(0, weight=1)
                case.grid_rowconfigure(0, weight=1)

                # Le jeton est un disque colore a l'interieur du logement.
                jeton = ctk.CTkFrame(
                    case,
                    width=50,
                    height=50,
                    corner_radius=25,
                    fg_color=EMPTY_COLOR,
                    border_width=1,
                    border_color="#41566F",
                )
                jeton.grid(row=0, column=0, padx=8, pady=8, sticky="")
                ligne_cases.append(jeton)
            self.cases.append(ligne_cases)

        self.aide = ctk.CTkLabel(
            self.conteneur,
            text="Clique sur une colonne pour laisser tomber ton pion. L'IA utilise Minimax avec une profondeur limitee et une evaluation simple du plateau.",
            font=ctk.CTkFont(family="Avenir Next", size=12),
            text_color=TEXT_MUTED,
        )
        self.aide.grid(row=2, column=0, sticky="ew", pady=(12, 0))

    def _mode_code(self):
        # Cette fonction convertit le libelle visible en code interne.
        if self.mode_var.get() == "Joueur vs Joueur":
            return "jvj"
        if self.mode_var.get() == "IA vs IA":
            return "iavia"
        return "jvia"

    def _types_joueurs(self):
        # On indique pour chaque pion s'il s'agit d'un humain ou d'une IA.
        mode = self._mode_code()
        if mode == "jvj":
            return {"X": "humain", "O": "humain"}
        if mode == "iavia":
            return {"X": "ia", "O": "ia"}
        return {"X": "humain", "O": "ia"}

    def _tour_humain_possible(self):
        # Un humain ne peut jouer que si la partie continue et qu'aucune IA n'est en train de calculer.
        if self.partie_terminee or self.ia_en_cours:
            return False
        return self._types_joueurs()[self.joueur_courant] == "humain"

    def _mettre_a_jour_labels(self, message=None):
        # Le statut principal explique toujours qui doit jouer.
        if message is not None:
            self.statut_var.set(message)
        elif self.partie_terminee:
            self.statut_var.set("Partie terminee")
        else:
            role = self._types_joueurs()[self.joueur_courant]
            self.statut_var.set(f"Tour de {self.joueur_courant} ({role})")

        # Le nom du niveau reste lisible pour l'utilisateur.
        niveau = int(round(float(self.niveau_var.get())))
        self.niveau_label_var.set(f"Niveau IA: {niveau} ({ia.nom_niveau(niveau)})")
        self.score_var.set(
            f"Score X: {self.scores['X']}   Score O: {self.scores['O']}   Nuls: {self.scores['Nul']}"
        )

    def _rafraichir_plateau(self):
        # On active ou desactive les boutons de colonnes selon la situation actuelle.
        humain_actif = self._tour_humain_possible()
        for colonne, bouton in enumerate(self.boutons_colonnes):
            jouable = regles.colonne_jouable(self.plateau, colonne)
            bouton.configure(
                state="normal" if humain_actif and jouable else "disabled",
                hover=humain_actif and jouable,
            )

        # On recolorie chaque pastille du plateau.
        for ligne in range(regles.NB_LIGNES):
            for colonne in range(regles.NB_COLONNES):
                pion = self.plateau[ligne][colonne]
                if pion == outils.JOUEUR_X:
                    couleur = X_COLOR
                    contour = "#F59E0B"
                elif pion == outils.JOUEUR_O:
                    couleur = O_COLOR
                    contour = "#0284C7"
                else:
                    couleur = EMPTY_COLOR
                    contour = "#41566F"
                self.cases[ligne][colonne].configure(fg_color=couleur, border_color=contour)

    def _verifier_fin(self):
        # On verifie si la partie vient de se terminer.
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
        messagebox.showinfo("Fin de partie - Puissance 4", message)
        return True

    def _finir_tour(self):
        # Si une fin de partie est detectee, on s'arrete.
        if self._verifier_fin():
            return

        # Sinon on alterne avec le joueur suivant.
        self.joueur_courant = outils.joueur_suivant(self.joueur_courant)
        self._mettre_a_jour_labels()
        self._rafraichir_plateau()

        # Si le nouveau joueur est une IA, on programme son coup.
        if self._types_joueurs()[self.joueur_courant] == "ia":
            self.after(200, self._lancer_tour_ia)

    def _lancer_tour_ia(self):
        # Ces gardes evitent les appels inutiles.
        if self.partie_terminee:
            return
        if self._types_joueurs()[self.joueur_courant] != "ia":
            return

        self.ia_en_cours = True
        self._mettre_a_jour_labels(f"IA {self.joueur_courant} reflechit...")
        self._rafraichir_plateau()
        self.after(220, self._jouer_coup_ia)

    def _jouer_coup_ia(self):
        # Le niveau pilote la profondeur du Minimax simplifie.
        niveau = int(round(float(self.niveau_var.get())))
        meilleur_plateau, colonne, note, _ = ia.choisir_meilleur_coup(
            self.plateau,
            self.joueur_courant,
            niveau,
        )

        self.ia_en_cours = False
        if meilleur_plateau is None:
            self._finir_tour()
            return

        self.plateau = meilleur_plateau
        self._mettre_a_jour_labels(
            f"IA {self.joueur_courant} joue en colonne {colonne + 1} (note {note})"
        )
        self.after(140, self._finir_tour)

    def clic_colonne(self, colonne):
        # Les clics sont ignores si le tour n'appartient pas a un humain.
        if not self._tour_humain_possible():
            return
        if not regles.colonne_jouable(self.plateau, colonne):
            return

        # On laisse tomber le pion dans la colonne choisie.
        regles.jouer_coup(self.plateau, colonne, self.joueur_courant)
        self._finir_tour()

    def _changement_mode(self, _event):
        # Un changement de mode relance une partie propre.
        self.nouvelle_partie()

    def _changement_niveau(self, _valeur):
        # Seul l'affichage du niveau change immediatement.
        self._mettre_a_jour_labels()

    def nouvelle_partie(self):
        # On remet le plateau a zero.
        self.plateau = regles.plateau_vide()
        self.joueur_courant = outils.JOUEUR_X
        self.partie_terminee = False
        self.ia_en_cours = False

        self._mettre_a_jour_labels()
        self._rafraichir_plateau()

        # En mode IA vs IA, X demarre automatiquement.
        if self._types_joueurs()[self.joueur_courant] == "ia":
            self.after(200, self._lancer_tour_ia)
