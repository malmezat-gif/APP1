# Interface graphique principale du projet.

# Tkinter fournit les variables d'interface et les boites de dialogue.
import tkinter as tk
from tkinter import messagebox

# CustomTkinter modernise l'interface sans changer la logique du jeu.
import customtkinter as ctk

# Ces modules contiennent la logique metier du morpion.
import ia
import regles
import outils


# On conserve un theme moderne et coherent pour toute l'application.
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Palette commune de l'interface.
WINDOW_BG = "#09101D"
CARD_BG = "#101826"
CARD_ALT = "#172235"
BORDER = "#243247"
TEXT_MAIN = "#F8FAFC"
TEXT_MUTED = "#94A3B8"
ACCENT = "#14B8A6"
ACCENT_HOVER = "#0F766E"
EMPTY_BG = "#1E293B"
EMPTY_HOVER = "#334155"
X_COLOR = "#FB7185"
O_COLOR = "#38BDF8"
ANALYSIS_BG = "#0B1220"


class MorpionApp:
    """Fenetre principale du morpion."""

    # Les modes de jeu existants sont conserves.
    MODES = ("Joueur vs IA", "Joueur vs Joueur", "IA vs IA")
    # Le morpion permet d'aller jusqu'a 9 coups d'avance.
    GENERATIONS = tuple(str(numero) for numero in range(1, 10))

    def __init__(self, root):
        # On memorise la fenetre racine.
        self.root = root
        # Titre visible dans la barre de fenetre.
        self.root.title("Morpion")
        # Taille par defaut un peu plus large pour accueillir l'analyse.
        self.root.geometry("1280x860")
        # Taille minimale pour garder une interface lisible.
        self.root.minsize(1100, 760)
        # Couleur de fond generale.
        self.root.configure(fg_color=WINDOW_BG)
        # La fenetre principale utilise toute la place disponible.
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Etat courant de la partie de morpion.
        self.plateau = outils.plateau_vide()
        self.joueur_courant = outils.JOUEUR_X
        self.partie_terminee = False
        self.ia_en_cours = False
        self.scores = {"X": 0, "O": 0, "Nul": 0}

        # Variables d'interface.
        self.mode_var = tk.StringVar(value=self.MODES[0])
        self.niveau_var = tk.IntVar(value=4)
        self.generation_var = tk.StringVar(value=self.GENERATIONS[1])
        self.statut_var = tk.StringVar(value="")
        self.niveau_label_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="")
        self.analyse_resume_var = tk.StringVar(value="")

        # Les references graphiques utiles sont initialisees ici.
        self.boutons = []
        self.fenetre_puissance4 = None

        # Construction de toute la fenetre.
        self._construire_interface()
        # Demarrage sur une partie propre.
        self.nouvelle_partie()

    def _construire_interface(self):
        # Le conteneur principal structure la page.
        self.conteneur = ctk.CTkFrame(self.root, fg_color="transparent")
        self.conteneur.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)
        self.conteneur.grid_columnconfigure(0, weight=3)
        self.conteneur.grid_columnconfigure(1, weight=2)
        self.conteneur.grid_rowconfigure(1, weight=1)

        # Carte d'entete avec le titre et les controles principaux.
        self.hero = ctk.CTkFrame(
            self.conteneur,
            fg_color=CARD_BG,
            corner_radius=28,
            border_width=1,
            border_color=BORDER,
        )
        self.hero.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.hero.grid_columnconfigure(0, weight=1)

        # Titre du jeu.
        self.titre = ctk.CTkLabel(
            self.hero,
            text="Morpion",
            font=ctk.CTkFont(family="Avenir Next", size=34, weight="bold"),
            text_color=TEXT_MAIN,
        )
        self.titre.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 4))

        # Sous-titre explicatif.
        self.sous_titre = ctk.CTkLabel(
            self.hero,
            text="Jeu principal, analyse Minimax et acces direct au module Puissance 4",
            font=ctk.CTkFont(family="Avenir Next", size=14),
            text_color=TEXT_MUTED,
        )
        self.sous_titre.grid(row=1, column=0, sticky="ew", padx=24)

        # Zone des controles du haut.
        self.controles = ctk.CTkFrame(self.hero, fg_color="transparent")
        self.controles.grid(row=2, column=0, sticky="ew", padx=24, pady=(20, 16))
        self.controles.grid_columnconfigure((0, 1, 2), weight=1)

        # Carte du mode de jeu.
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
            height=40,
        )
        self.combo_mode.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))

        # Carte du niveau d'IA.
        self.carte_niveau = ctk.CTkFrame(
            self.controles,
            fg_color=CARD_ALT,
            corner_radius=20,
            border_width=1,
            border_color=BORDER,
        )
        self.carte_niveau.grid(row=0, column=1, sticky="ew", padx=8)
        self.carte_niveau.grid_columnconfigure(0, weight=1)

        self.label_niveau_titre = ctk.CTkLabel(
            self.carte_niveau,
            text="Difficulte",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            text_color=TEXT_MUTED,
        )
        self.label_niveau_titre.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))

        self.scale_niveau = ctk.CTkSlider(
            self.carte_niveau,
            from_=1,
            to=9,
            number_of_steps=8,
            variable=self.niveau_var,
            command=self._changement_niveau,
            progress_color=ACCENT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            fg_color="#273449",
            height=18,
        )
        self.scale_niveau.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))

        # Carte des actions principales.
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
            text="Actions",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            text_color=TEXT_MUTED,
        )
        self.label_action.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))

        self.bouton_nouvelle = ctk.CTkButton(
            self.carte_action,
            text="Nouvelle partie",
            command=self.nouvelle_partie,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#06131E",
            font=ctk.CTkFont(family="Avenir Next", size=14, weight="bold"),
            corner_radius=14,
            height=40,
        )
        self.bouton_nouvelle.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))

        self.bouton_puissance4 = ctk.CTkButton(
            self.carte_action,
            text="Ouvrir Puissance 4",
            command=self._ouvrir_puissance4,
            fg_color="#22314A",
            hover_color="#31425E",
            text_color=TEXT_MAIN,
            font=ctk.CTkFont(family="Avenir Next", size=14, weight="bold"),
            corner_radius=14,
            height=40,
        )
        self.bouton_puissance4.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))

        # Informations de statut en dessous des controles.
        self.label_tour = ctk.CTkLabel(
            self.hero,
            textvariable=self.statut_var,
            wraplength=960,
            justify="center",
            font=ctk.CTkFont(family="Avenir Next", size=24, weight="bold"),
            text_color=TEXT_MAIN,
        )
        self.label_tour.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 8))

        self.label_niveau = ctk.CTkLabel(
            self.hero,
            textvariable=self.niveau_label_var,
            font=ctk.CTkFont(family="Avenir Next", size=14),
            text_color=TEXT_MUTED,
        )
        self.label_niveau.grid(row=4, column=0, sticky="ew", padx=24)

        self.label_score = ctk.CTkLabel(
            self.hero,
            textvariable=self.score_var,
            font=ctk.CTkFont(family="Avenir Next", size=15),
            text_color=TEXT_MAIN,
        )
        self.label_score.grid(row=5, column=0, sticky="ew", padx=24, pady=(6, 22))

        # Carte du plateau de morpion.
        self.carte_plateau = ctk.CTkFrame(
            self.conteneur,
            fg_color=CARD_BG,
            corner_radius=28,
            border_width=1,
            border_color=BORDER,
        )
        self.carte_plateau.grid(row=1, column=0, sticky="nsew", pady=(18, 0), padx=(0, 10))
        self.carte_plateau.grid_columnconfigure(0, weight=1)
        self.carte_plateau.grid_rowconfigure(1, weight=1)

        self.titre_plateau = ctk.CTkLabel(
            self.carte_plateau,
            text="Plateau de jeu",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=18, weight="bold"),
            text_color=TEXT_MAIN,
        )
        self.titre_plateau.grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 0))

        self.grille = ctk.CTkFrame(self.carte_plateau, fg_color="transparent")
        self.grille.grid(row=1, column=0, padx=22, pady=22, sticky="nsew")
        self.grille.grid_columnconfigure((0, 1, 2), weight=1)
        self.grille.grid_rowconfigure((0, 1, 2), weight=1)

        for index in range(9):
            bouton = ctk.CTkButton(
                self.grille,
                text="",
                command=lambda i=index: self.clic_case(i),
                width=170,
                height=150,
                corner_radius=24,
                fg_color=EMPTY_BG,
                hover_color=EMPTY_HOVER,
                border_width=1,
                border_color=BORDER,
                text_color=TEXT_MAIN,
                font=ctk.CTkFont(family="Avenir Next", size=52, weight="bold"),
            )
            bouton.grid(row=index // 3, column=index % 3, padx=10, pady=10, sticky="nsew")
            self.boutons.append(bouton)

        # Carte laterale d'analyse du morpion.
        self.carte_analyse = ctk.CTkFrame(
            self.conteneur,
            fg_color=CARD_BG,
            corner_radius=28,
            border_width=1,
            border_color=BORDER,
        )
        self.carte_analyse.grid(row=1, column=1, sticky="nsew", pady=(18, 0), padx=(10, 0))
        self.carte_analyse.grid_columnconfigure(0, weight=1)
        self.carte_analyse.grid_rowconfigure(4, weight=1)

        self.titre_analyse = ctk.CTkLabel(
            self.carte_analyse,
            text="Outils d'analyse",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=18, weight="bold"),
            text_color=TEXT_MAIN,
        )
        self.titre_analyse.grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 4))

        self.resume_analyse = ctk.CTkLabel(
            self.carte_analyse,
            textvariable=self.analyse_resume_var,
            wraplength=420,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=13),
            text_color=TEXT_MUTED,
        )
        self.resume_analyse.grid(row=1, column=0, sticky="ew", padx=22)

        # Bloc des controles d'analyse.
        self.outils_analyse = ctk.CTkFrame(
            self.carte_analyse,
            fg_color=CARD_ALT,
            corner_radius=20,
            border_width=1,
            border_color=BORDER,
        )
        self.outils_analyse.grid(row=2, column=0, sticky="ew", padx=22, pady=(16, 14))
        self.outils_analyse.grid_columnconfigure((0, 1), weight=1)

        self.label_generation = ctk.CTkLabel(
            self.outils_analyse,
            text="Generation a analyser",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            text_color=TEXT_MUTED,
        )
        self.label_generation.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))

        self.combo_generation = ctk.CTkOptionMenu(
            self.outils_analyse,
            variable=self.generation_var,
            values=list(self.GENERATIONS),
            command=self._changement_generation,
            fg_color="#213149",
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color="#152033",
            dropdown_hover_color="#22314A",
            text_color=TEXT_MAIN,
            font=ctk.CTkFont(family="Avenir Next", size=13),
            dropdown_font=ctk.CTkFont(family="Avenir Next", size=13),
            corner_radius=14,
            dynamic_resizing=False,
            height=38,
        )
        self.combo_generation.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))

        self.bouton_generation = ctk.CTkButton(
            self.outils_analyse,
            text="Afficher les scores",
            command=self._afficher_scores_generation,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#06131E",
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            corner_radius=14,
            height=38,
        )
        self.bouton_generation.grid(row=1, column=1, sticky="ew", padx=(0, 16), pady=(0, 14))

        self.bouton_suite_ia = ctk.CTkButton(
            self.outils_analyse,
            text="Suite ideale principale",
            command=self._afficher_suite_principale,
            fg_color="#22314A",
            hover_color="#31425E",
            text_color=TEXT_MAIN,
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            corner_radius=14,
            height=38,
        )
        self.bouton_suite_ia.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 10))

        self.bouton_suite_adversaire = ctk.CTkButton(
            self.outils_analyse,
            text="Suite ideale secondaire",
            command=self._afficher_suite_secondaire,
            fg_color="#22314A",
            hover_color="#31425E",
            text_color=TEXT_MAIN,
            font=ctk.CTkFont(family="Avenir Next", size=13, weight="bold"),
            corner_radius=14,
            height=38,
        )
        self.bouton_suite_adversaire.grid(row=2, column=1, sticky="ew", padx=(0, 16), pady=(0, 10))

        self.texte_aide_analyse = ctk.CTkLabel(
            self.outils_analyse,
            text="La generation explore toutes les positions atteintes apres 1 a 9 coups.",
            wraplength=390,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(family="Avenir Next", size=12),
            text_color=TEXT_MUTED,
        )
        self.texte_aide_analyse.grid(row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 14))

        # Zone scrollable qui affiche les resultats de l'analyse.
        self.zone_analyse = ctk.CTkTextbox(
            self.carte_analyse,
            fg_color=ANALYSIS_BG,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT_MAIN,
            font=ctk.CTkFont(family="Menlo", size=12),
            wrap="word",
        )
        self.zone_analyse.grid(row=4, column=0, sticky="nsew", padx=22, pady=(0, 22))

        # Texte d'aide sous les cartes.
        self.aide = ctk.CTkLabel(
            self.conteneur,
            text="Joue sur le plateau, puis utilise le panneau d'analyse pour observer les scores d'une generation et les suites gagnantes depuis la position courante.",
            font=ctk.CTkFont(family="Avenir Next", size=13),
            text_color=TEXT_MUTED,
        )
        self.aide.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(16, 0))

    def _mode_code(self):
        # On convertit le libelle lisible en code interne.
        if self.mode_var.get() == "Joueur vs Joueur":
            return "jvj"
        if self.mode_var.get() == "IA vs IA":
            return "iavia"
        return "jvia"

    def _types_joueurs(self):
        # On determine si chaque joueur est humain ou IA selon le mode choisi.
        mode = self._mode_code()
        if mode == "jvj":
            return {"X": "humain", "O": "humain"}
        if mode == "iavia":
            return {"X": "ia", "O": "ia"}
        return {"X": "humain", "O": "ia"}

    def _tour_humain_possible(self):
        # Un clic humain n'est possible que si la partie continue et qu'aucune IA n'est en cours.
        if self.partie_terminee or self.ia_en_cours:
            return False
        return self._types_joueurs()[self.joueur_courant] == "humain"

    def _libelles_suites(self):
        # Les libelles s'adaptent au mode pour rester pedagogiques.
        mode = self._mode_code()
        if mode == "jvia":
            return {
                "principal": ("ordinateur", outils.JOUEUR_O),
                "secondaire": ("adversaire", outils.JOUEUR_X),
            }
        if mode == "iavia":
            return {
                "principal": ("IA X", outils.JOUEUR_X),
                "secondaire": ("IA O", outils.JOUEUR_O),
            }
        return {
            "principal": ("joueur X", outils.JOUEUR_X),
            "secondaire": ("joueur O", outils.JOUEUR_O),
        }

    def _reference_scores(self):
        # En Joueur vs IA, l'analyse est naturellement faite du point de vue de l'ordinateur.
        if self._mode_code() == "jvia":
            return outils.JOUEUR_O, "ordinateur (O)"
        # Dans les autres modes, on regarde la position du point de vue du joueur courant.
        return self.joueur_courant, f"joueur courant ({self.joueur_courant})"

    def _mettre_a_jour_labels(self, message=None):
        # Le statut principal reste identique a la version precedente.
        if message is not None:
            self.statut_var.set(message)
        elif self.partie_terminee:
            self.statut_var.set("Partie terminee")
        else:
            role = self._types_joueurs()[self.joueur_courant]
            self.statut_var.set(f"Tour de {self.joueur_courant} ({role})")

        # Le niveau reste affiche avec son nom pedagogique.
        niveau = int(round(float(self.niveau_var.get())))
        nom_niveau = ia.nom_niveau(niveau)
        self.niveau_label_var.set(f"Niveau IA: {niveau} ({nom_niveau})")
        self.score_var.set(
            f"Score X: {self.scores['X']}   Score O: {self.scores['O']}   Nuls: {self.scores['Nul']}"
        )

        # Le panneau d'analyse s'adapte au mode courant.
        reference, libelle_reference = self._reference_scores()
        self.analyse_resume_var.set(
            f"Les scores de generation sont evalues du point de vue de {libelle_reference}. "
            f"La position actuelle commence avec le joueur {self.joueur_courant}."
        )

        libelles = self._libelles_suites()
        self.bouton_suite_ia.configure(
            text=f"Suite ideale {libelles['principal'][0]} ({libelles['principal'][1]})"
        )
        self.bouton_suite_adversaire.configure(
            text=f"Suite ideale {libelles['secondaire'][0]} ({libelles['secondaire'][1]})"
        )

    def _rafraichir_plateau(self):
        # Chaque bouton du plateau est recolorie selon son contenu.
        for index, bouton in enumerate(self.boutons):
            pion = self.plateau[index]
            if pion == outils.VIDE:
                actif = self._tour_humain_possible()
                bouton.configure(
                    text="",
                    state="normal" if actif else "disabled",
                    fg_color=EMPTY_BG,
                    hover_color=EMPTY_HOVER,
                    border_width=1,
                    border_color=BORDER,
                    text_color=TEXT_MAIN,
                    text_color_disabled=TEXT_MUTED,
                    hover=actif,
                )
                continue

            couleur = X_COLOR if pion == outils.JOUEUR_X else O_COLOR
            contour = "#BE123C" if pion == outils.JOUEUR_X else "#0369A1"
            bouton.configure(
                text=pion,
                state="disabled",
                fg_color=CARD_ALT,
                hover=False,
                border_width=2,
                border_color=contour,
                text_color=couleur,
                text_color_disabled=couleur,
            )

    def _case_vers_coordonnees(self, case):
        # Les coordonnees humaines sont numerotees a partir de 1.
        ligne = (case // 3) + 1
        colonne = (case % 3) + 1
        return f"L{ligne} C{colonne}"

    def _chemin_vers_texte(self, chemin):
        # On transforme une liste de coups en phrase lisible.
        if not chemin:
            return "Position courante"
        return " -> ".join(
            f"{joueur} {self._case_vers_coordonnees(case)}" for joueur, case in chemin
        )

    def _ecrire_analyse(self, lignes):
        # On remplace le contenu de la zone d'analyse par le nouveau resultat.
        self.zone_analyse.delete("1.0", "end")
        self.zone_analyse.insert("1.0", "\n".join(lignes))

    def _initialiser_zone_analyse(self):
        # Ce message apparait tant qu'aucune analyse n'a encore ete lancee.
        _, libelle_reference = self._reference_scores()
        libelles = self._libelles_suites()
        self._ecrire_analyse(
            [
                "Analyse de la position courante",
                "",
                f"- Tour actuel : {self.joueur_courant}",
                f"- Evaluation de generation : point de vue de {libelle_reference}",
                f"- Suite 1 : {libelles['principal'][0]} ({libelles['principal'][1]})",
                f"- Suite 2 : {libelles['secondaire'][0]} ({libelles['secondaire'][1]})",
                "",
                "Utilise les boutons ci-dessus pour lancer l'analyse.",
            ]
        )

    def _afficher_scores_generation(self):
        # On lit la generation voulue dans le controle de l'interface.
        profondeur = int(self.generation_var.get())
        # On choisit le point de vue d'evaluation adapte au mode.
        reference, libelle_reference = self._reference_scores()
        # On delegue le calcul au module IA.
        analyse = ia.analyser_generation(
            self.plateau,
            self.joueur_courant,
            profondeur,
            reference,
        )

        # On construit un texte clair pour l'utilisateur.
        lignes = [
            "Scores d'evaluation d'une generation",
            "",
            f"Generation demandee : {analyse['profondeur']}",
            f"Joueur qui doit jouer : {self.joueur_courant}",
            f"Point de vue des scores : {libelle_reference}",
            f"Nombre de positions atteintes : {len(analyse['positions'])}",
            f"Minimum : {analyse['minimum']}",
            f"Maximum : {analyse['maximum']}",
            "",
            "Liste complete des scores de cette generation :",
        ]

        # On affiche tous les scores, regroupes par lignes pour rester lisibles.
        notes = analyse["notes"]
        for debut in range(0, len(notes), 24):
            bloc = notes[debut : debut + 24]
            lignes.append(" ".join(f"{note:>5}" for note in bloc))

        # Si la generation est raisonnable, on affiche aussi le detail complet des chemins.
        if len(analyse["positions"]) <= 120:
            lignes.append("")
            lignes.append("Details des positions atteintes :")
            for numero, position in enumerate(analyse["positions"], start=1):
                resultat = position["resultat"] if position["resultat"] is not None else "En cours"
                lignes.append(
                    f"{numero:>2}. score {position['score']:>4} | "
                    f"{self._chemin_vers_texte(position['chemin'])} | {resultat}"
                )
        else:
            lignes.append("")
            lignes.append(
                "Details des chemins : apercu des 40 premiers pour garder une interface lisible."
            )
            for numero, position in enumerate(analyse["positions"][:40], start=1):
                resultat = position["resultat"] if position["resultat"] is not None else "En cours"
                lignes.append(
                    f"{numero:>2}. score {position['score']:>4} | "
                    f"{self._chemin_vers_texte(position['chemin'])} | {resultat}"
                )

        self._ecrire_analyse(lignes)

    def _afficher_suite_ideale(self, joueur_cible, libelle_cible):
        # On demande a l'IA si une victoire forcee existe pour ce joueur.
        resultat = ia.trouver_suite_gagnante(self.plateau, self.joueur_courant, joueur_cible)

        # Si la position de depart est deja terminee, on l'indique simplement.
        if resultat["resultat"] == joueur_cible and not resultat["suite"]:
            self._ecrire_analyse(
                [
                    f"Suite ideale pour {libelle_cible}",
                    "",
                    f"La position courante est deja gagnante pour {joueur_cible}.",
                ]
            )
            return

        # Si aucune suite gagnante n'existe, on renvoie un message clair.
        if not resultat["trouvee"]:
            self._ecrire_analyse(
                [
                    f"Suite ideale pour {libelle_cible}",
                    "",
                    f"Aucune suite gagnante trouvee pour {libelle_cible} depuis cette position.",
                    f"Score optimal obtenu par Minimax : {resultat['score']}",
                ]
            )
            return

        # Sinon on detaille la suite optimale trouvee.
        lignes = [
            f"Suite ideale pour {libelle_cible}",
            "",
            f"Joueur qui doit jouer maintenant : {self.joueur_courant}",
            "Sequence optimale :",
        ]

        for numero, (joueur, case) in enumerate(resultat["suite"], start=1):
            lignes.append(f"{numero}. {joueur} joue en {self._case_vers_coordonnees(case)}")

        lignes.append("")
        lignes.append(f"Conclusion : {joueur_cible} peut forcer la victoire depuis cette position.")
        self._ecrire_analyse(lignes)

    def _afficher_suite_principale(self):
        # Ce bouton affiche la premiere suite demandee dans l'interface.
        libelles = self._libelles_suites()
        libelle, joueur = libelles["principal"]
        self._afficher_suite_ideale(joueur, libelle)

    def _afficher_suite_secondaire(self):
        # Ce bouton affiche la seconde suite demandee dans l'interface.
        libelles = self._libelles_suites()
        libelle, joueur = libelles["secondaire"]
        self._afficher_suite_ideale(joueur, libelle)

    def _verifier_fin(self):
        # On controle si la partie vient de se terminer.
        resultat = regles.verifier_gagnant(self.plateau)
        if resultat is None:
            return False

        # On memorise l'etat de fin et on incremente le score.
        self.partie_terminee = True
        self.scores[resultat] += 1

        # Le texte d'information depend du resultat.
        if resultat == "Nul":
            message = "Match nul"
        else:
            message = f"Le joueur {resultat} a gagne"

        self._mettre_a_jour_labels(message)
        self._rafraichir_plateau()

        # En cas de nul, on relance automatiquement la partie comme demande precedemment.
        if resultat == "Nul":
            self._mettre_a_jour_labels("Match nul - nouvelle partie...")
            self.root.after(500, self.nouvelle_partie)
            return True

        # Pour une victoire, on garde une boite de dialogue simple.
        messagebox.showinfo("Fin de partie", message)
        return True

    def _finir_tour(self):
        # Si la partie est terminee, rien d'autre n'est a faire.
        if self._verifier_fin():
            return

        # Sinon on passe au joueur suivant.
        self.joueur_courant = outils.joueur_suivant(self.joueur_courant)
        self._mettre_a_jour_labels()
        self._rafraichir_plateau()
        self._initialiser_zone_analyse()

        # Si le nouveau joueur est une IA, on programme son tour.
        if self._types_joueurs()[self.joueur_courant] == "ia":
            self.root.after(150, self._lancer_tour_ia)

    def _lancer_tour_ia(self):
        # On securise le lancement pour eviter un double calcul.
        if self.partie_terminee:
            return
        if self._types_joueurs()[self.joueur_courant] != "ia":
            return

        self.ia_en_cours = True
        self._mettre_a_jour_labels(f"IA {self.joueur_courant} reflechit...")
        self._rafraichir_plateau()
        self.root.after(180, self._jouer_coup_ia)

    def _jouer_coup_ia(self):
        # La profondeur de recherche du morpion est directement liee au slider actuel.
        profondeur = int(round(float(self.niveau_var.get())))
        meilleur_coup, meilleure_note, _ = ia.choisir_meilleur_coup(
            self.plateau,
            self.joueur_courant,
            profondeur,
        )

        self.ia_en_cours = False
        if meilleur_coup is None:
            self._finir_tour()
            return

        # Le plateau est remplace par la meilleure position retournee par l'IA.
        self.plateau = meilleur_coup
        self._mettre_a_jour_labels(
            f"IA {self.joueur_courant} joue (note {meilleure_note}, {ia.nom_niveau(profondeur)})"
        )
        self.root.after(100, self._finir_tour)

    def clic_case(self, index):
        # Les clics ne sont acceptes que si le coup est legal.
        if not self._tour_humain_possible():
            return
        if self.plateau[index] != outils.VIDE:
            return

        # On pose le pion du joueur humain.
        self.plateau[index] = self.joueur_courant
        self._finir_tour()

    def _changement_mode(self, _event):
        # Un changement de mode relance une partie propre.
        self.nouvelle_partie()

    def _changement_niveau(self, _valeur):
        # Le changement de niveau ne modifie pas la partie, seulement l'affichage.
        self._mettre_a_jour_labels()

    def _changement_generation(self, _valeur):
        # L'information du panneau d'analyse est simplement reinitialisee.
        self._mettre_a_jour_labels()
        self._initialiser_zone_analyse()

    def _ouvrir_puissance4(self):
        # On importe ici pour garder `interface.py` independant du module secondaire.
        import puissance4_interface

        # Si la fenetre existe deja, on la remet juste au premier plan.
        if self.fenetre_puissance4 is not None and self.fenetre_puissance4.winfo_exists():
            self.fenetre_puissance4.lift()
            self.fenetre_puissance4.focus()
            return

        # Sinon on cree une nouvelle fenetre Puissance 4.
        self.fenetre_puissance4 = puissance4_interface.Puissance4App(self.root)

    def nouvelle_partie(self):
        # La grille revient a l'etat initial.
        self.plateau = outils.plateau_vide()
        self.joueur_courant = outils.JOUEUR_X
        self.partie_terminee = False
        self.ia_en_cours = False

        # On remet l'affichage a jour.
        self._mettre_a_jour_labels()
        self._rafraichir_plateau()
        self._initialiser_zone_analyse()

        # En mode IA vs IA, l'IA X commence automatiquement.
        if self._types_joueurs()[self.joueur_courant] == "ia":
            self.root.after(150, self._lancer_tour_ia)


def main():
    # Point d'entree de l'application.
    root = ctk.CTk()
    MorpionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
