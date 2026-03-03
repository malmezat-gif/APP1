# Explications du code (fichier par fichier)

Ce guide explique le fonctionnement du projet avec des references de lignes pour t'aider a lire le code.
J'ai garde les explications concretes et proches du code.

## `outils.py`
- L1: docstring du fichier, indique que ce module contient les utilitaires partages.
- L3: constante `VIDE` pour representer une case libre.
- L4: constante `JOUEUR_X`.
- L5: constante `JOUEUR_O`.
- L8: declaration de `plateau_vide()`.
- L9: docstring de la fonction.
- L10: cree et retourne une liste de 9 cases vides.
- L13: declaration de `copier_plateau(plateau)`.
- L14: docstring.
- L15: retourne une copie du plateau.
- L18: declaration de `joueur_suivant(joueur)`.
- L19: docstring.
- L20: si joueur vaut X, retourne O, sinon retourne X.
- L23: declaration de `coups_possibles(plateau)`.
- L24: docstring.
- L25: comprehension qui retourne tous les indices libres.
- L28: declaration de `plateau_vers_texte(plateau)`.
- L29: docstring.
- L30: initialise la liste des lignes texte.
- L31: boucle sur les positions de depart des 3 lignes du plateau.
- L32: construit une ligne texte de 3 cases et l'ajoute.
- L33: assemble les 3 lignes avec des separateurs et retourne le texte.

## `regles.py`
- L1: docstring du module des regles.
- L3: import de `outils` pour reutiliser la constante `VIDE`.
- L5-L14: declaration de toutes les combinaisons gagnantes possibles.
- L17: declaration de `gagnant(plateau)`.
- L18: docstring.
- L19: boucle sur chaque triplet gagnant.
- L20: lit le pion de la premiere case de la ligne.
- L21: verifie que la ligne est complete et non vide.
- L22: retourne le pion gagnant immediatement.
- L23: si aucune ligne ne gagne, retourne `None`.
- L26: declaration de `verifier_gagnant(plateau)`.
- L27: docstring, liste les valeurs de retour possibles.
- L28: calcule d'abord un gagnant strict.
- L29-L30: si gagnant trouve, le retourne.
- L31-L32: si plus de case vide, retourne `"Nul"`.
- L33: sinon la partie continue (`None`).
- L36: declaration de `calcul_score(plateau, pion_ia)`.
- L37: docstring, annonce score terminal + heuristique.
- L38: verifie si partie terminee.
- L39-L44: retourne un score final fort en cas de gain/perte/nul.
- L46: determine le pion adverse automatiquement.
- L47: initialise le score heuristique.
- L49: boucle sur les lignes gagnantes.
- L50: cree le triplet de cases correspondant a la ligne.
- L51: compte les pions IA sur la ligne.
- L52: compte les pions adverses sur la ligne.
- L54-L55: ignore les lignes bloquees (presence des 2 joueurs).
- L57-L60: ajoute un bonus pour les lignes favorables a l'IA.
- L62-L65: retire des points pour les lignes favorables a l'adversaire.
- L67: retourne le score calcule.

## `ia.py`
- L1: docstring, indique Minimax + elagage alpha-beta.
- L3-L4: imports des regles et outils.
- L7: declaration de `minimax(...)`.
- L8: docstring.
- L9: condition d'arret (profondeur 0 ou partie terminee).
- L10: dans ce cas, evalue directement le plateau.
- L12: recupere les coups encore possibles.
- L14: branche MAX: c'est au tour du pion IA.
- L15: initialise la meilleure valeur possible cote MAX.
- L16: boucle sur les coups.
- L17-L18: copie le plateau puis joue le coup.
- L19-L26: appel recursif pour evaluer la suite.
- L27: met a jour la meilleure note MAX.
- L28: met a jour `alpha`.
- L29-L30: elagage: on arrete si la branche ne peut plus battre l'existant.
- L31: retourne la meilleure valeur MAX.
- L33: branche MIN (tour adverse), initialise valeur pessimiste.
- L34-L36: boucle + application de chaque coup adverse.
- L37-L44: appel recursif pour evaluer la suite.
- L45: met a jour la pire valeur (MIN cherche le minimum).
- L46: met a jour `beta`.
- L47-L48: elagage beta/alpha.
- L49: retourne la valeur MIN.
- L52: declaration de `choisir_meilleur_coup(...)`.
- L53: docstring, format de retour.
- L54-L55: si partie deja finie, pas de coup possible.
- L57: recupere les coups libres.
- L58-L60: initialise stockage du meilleur coup.
- L62: boucle sur tous les coups candidats.
- L63-L64: copie + application du coup.
- L65-L70: evalue ce coup avec Minimax.
- L71: memorise la note associee a cette case.
- L73-L75: met a jour le meilleur coup si la note est meilleure.
- L77: retourne meilleur plateau, meilleure note et details des notes.

## `principal.py`
- L1: docstring du mode console.
- L3-L5: imports des modules du projet.
- L8: declaration de `afficher(plateau)`.
- L9: affiche le plateau formatte.
- L12: declaration de `lire_mode()`.
- L13-L16: affiche les 3 modes proposes.
- L17: lit la saisie utilisateur.
- L18-L22: convertit la saisie en code interne de mode.
- L25: declaration de `lire_niveau()`.
- L26-L27: tente de lire une difficulte numerique.
- L28-L29: en cas d'erreur, retourne un niveau par defaut (4).
- L30: borne la valeur entre 1 et 9.
- L33: declaration de `role_joueur(mode, joueur)`.
- L34-L38: determine si le joueur courant est humain ou IA selon le mode.
- L41: declaration de `jouer_tour_humain(...)`.
- L42: lit le coup utilisateur (ou `q`).
- L43-L44: si `q`, demande l'arret de partie.
- L46-L50: valide que l'entree est bien un entier.
- L52-L54: verifie borne de case (0..8).
- L55-L57: refuse si la case est deja prise.
- L59-L60: applique un coup valide sur une copie du plateau.
- L61: retourne plateau mis a jour.
- L64: declaration de `jouer_tour_ia(...)`.
- L65: demande a l'IA son meilleur coup.
- L66: affiche les notes de chaque coup teste.
- L67-L68: si aucun coup, retourne le plateau courant.
- L69: affiche la note du coup choisi.
- L70: retourne le nouveau plateau.
- L73: declaration de `main()`.
- L74: affiche le titre console.
- L75-L76: lit mode et niveau.
- L77: initialise un plateau vide.
- L78: X commence toujours.
- L80: boucle principale de la partie.
- L81: affiche le plateau.
- L82: verifie l'etat de fin.
- L83-L88: affiche resultat puis sort si partie terminee.
- L90: determine le role du joueur courant.
- L91-L94: si IA, joue coup IA puis change de joueur.
- L96: sinon lit un coup humain.
- L97-L99: si l'utilisateur quitte, arrete la partie.
- L100-L101: si coup invalide, garde le meme joueur.
- L103-L104: valide le coup et passe au joueur suivant.
- L107-L108: point d'entree Python standard.

## `interface.py`

### Import et classe
- L1: docstring de l'interface graphique.
- L3-L4: imports Tkinter (`tk`, `ttk`, `messagebox`).
- L6-L8: imports des modules de logique du jeu.
- L11: declaration de la classe `MorpionApp`.
- L12: docstring de classe.
- L14: liste des modes disponibles.

### `__init__`
- L16: declaration du constructeur.
- L17: stocke la fenetre racine.
- L18: titre de fenetre.
- L19: fenetre non redimensionnable pour garder un layout stable.
- L21: initialise le plateau vide.
- L22: X commence.
- L23: flag de fin de partie.
- L24: flag pour bloquer les clics pendant le calcul IA.
- L25: scoreboard cumule.
- L27: variable Tk pour le mode.
- L28: variable Tk pour la difficulte.
- L29: texte dynamique du statut.
- L30: texte dynamique du niveau.
- L31: texte dynamique des scores.
- L33: liste des boutons de cases.
- L34: construit tous les widgets.
- L35: lance une nouvelle partie au demarrage.

### `_construire_interface`
- L37: declaration de la methode de construction UI.
- L38-L39: frame principal + placement.
- L41: label "Mode".
- L42-L48: creation de la combobox des modes.
- L49: placement combobox.
- L50: bind evenement changement de mode.
- L52: label "Difficulte".
- L53-L62: creation du slider de niveau.
- L63: placement du slider.
- L65-L66: bouton "Nouvelle partie" et placement.
- L68-L74: label de statut (texte variable).
- L75: label de niveau.
- L76: label de score.
- L78-L79: frame contenant la grille du plateau.
- L81: boucle creation des 9 boutons.
- L82-L89: creation d'un bouton de case avec callback.
- L90: placement du bouton dans la grille 3x3.
- L91: memorise le bouton dans la liste.

### Helpers de mode et statut
- L93: declaration `_mode_code`.
- L94-L98: conversion texte interface -> code interne.
- L100: declaration `_types_joueurs`.
- L101-L106: map des roles selon le mode choisi.
- L108: declaration `_tour_humain_possible`.
- L109-L110: interdit clic si partie finie ou IA en cours.
- L111: autorise uniquement si joueur courant est humain.
- L113: declaration `_mettre_a_jour_labels`.
- L114-L120: met a jour le texte de statut selon le contexte.
- L122: met a jour texte de niveau.
- L123-L125: met a jour texte des scores.

### Gestion visuelle du plateau
- L127: declaration `_rafraichir_plateau`.
- L128: boucle sur les 9 boutons.
- L129: lit le pion de la case.
- L130-L132: case vide -> bouton vide, activable seulement au tour humain.
- L134: choisit couleur du pion.
- L135: case occupee -> affiche pion et desactive bouton.

### Fin de partie et enchainement des tours
- L137: declaration `_verifier_fin`.
- L138: recupere etat de partie via `regles`.
- L139-L140: si non termine, retourne `False`.
- L142: marque la partie comme terminee.
- L143: incremente le score du resultat (`X`, `O` ou `Nul`).
- L145-L148: construit le message de fin.
- L150: affiche ce message dans le label de statut.
- L151: rafraichit le plateau.
- L152: popup d'information.
- L153: confirme que la partie est finie.
- L155: declaration `_finir_tour`.
- L156-L157: arrete si la partie vient de se terminer.
- L159: passe au joueur suivant.
- L160-L161: met a jour labels + plateau.
- L163-L164: si prochain joueur est IA, programme son tour.

### Tour IA
- L166: declaration `_lancer_tour_ia`.
- L167-L170: verifie qu'il faut bien lancer une IA maintenant.
- L172: bloque les actions humaines pendant calcul IA.
- L173: affiche un statut "reflechit".
- L174: rafraichit UI.
- L175: programme le calcul du coup IA.
- L177: declaration `_jouer_coup_ia`.
- L178: lit le niveau de profondeur.
- L179-L183: demande le meilleur coup au module IA.
- L185: debloque le flag IA.
- L186-L188: si aucun coup, passe a la logique de fin de tour.
- L190: applique le nouveau plateau choisi par l'IA.
- L191: affiche la note du coup joue.
- L192: enchaine vers `_finir_tour`.

### Tour humain + changements UI
- L194: declaration `clic_case`.
- L195-L196: ignore les clics hors tour humain.
- L197-L198: ignore les clics sur case occupee.
- L200: ecrit le pion humain sur la case choisie.
- L201: termine le tour.
- L203-L204: changement de mode -> nouvelle partie.
- L206-L207: changement niveau -> met a jour labels.
- L209: declaration `nouvelle_partie`.
- L210: reinitialise plateau.
- L211: remet joueur courant a X.
- L212-L213: reset flags de partie.
- L215-L216: rafraichit labels et plateau.
- L218-L219: si X est IA (mode IA vs IA), lance automatiquement.

### Point d'entree
- L222: declaration `main()`.
- L223: creation de la fenetre Tk.
- L224: creation de l'application.
- L225: boucle evenementielle Tkinter.
- L228-L229: point d'entree Python standard.

## `README.md`
- L1: titre du projet.
- L3-L6: resume rapide de ce que contient le projet.
- L8-L13: role de chaque fichier.
- L15-L26: commandes de lancement (interface/console).
- L28-L36: explication courte de l'algorithme.
- L37-L40: modes de jeu disponibles.
- L42-L45: impact du niveau de difficulte.
- L47-L48: note sur l'absence de dependances externes.
