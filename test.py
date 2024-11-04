# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:40:57 2024

@author: Clara Correia
Projet PPMD POO -Rummikub-
Classe Main
Qui represente la Main d'un joueur
"""
from jetons import Jetons, EnsembleDeJetons
from Pioche import Pioche
from plateau import Plateau
from main import Main
import random

def main():
    # Initialisation du jeu de jetons, plateau, et mains des joueurs
    jeu_de_jetons = EnsembleDeJetons()
    jeu_de_jetons.melanger()
    plateau = Plateau()

    # Initialisation des mains des joueurs (main fixe pour le joueur 1 et joueur 2)
    main_joueur_1 = Main(jeu_de_jetons, fixe=True)
    main_joueur_2 = Main(jeu_de_jetons, fixe2=True)

    # Initialisation de la pioche
    pioche = Pioche(jeu_de_jetons, main_joueur_1, main_joueur_2)

    joueurs = [main_joueur_1, main_joueur_2]
    total_points = [0, 0]  # Liste pour stocker les points des deux joueurs
    joueur_actuel = 0  # Indice du joueur courant (0 pour joueur 1, 1 pour joueur 2)
    premier_tour = True  # Flag pour le premier tour

    while True:
        print(f"\n--- Tour du Joueur {joueur_actuel + 1} ---")
        print(f"Total des points accumulés : {total_points[joueur_actuel]}")

        # Affichage du plateau avant de poser la question
        plateau.afficher_plateau_ascii()

        # Affichage de la main du joueur
        joueurs[joueur_actuel].afficher_main_ascii()
        print(f"\n--- Tour du Joueur {joueur_actuel + 1} ---")
        action = input("Voulez-vous poser des jetons ou piocher un jeton? (poser/piocher): ").strip().lower()

        if action == "piocher":
            # Lorsque le joueur pioche, remettre les jetons posés dans sa main
            joueurs[joueur_actuel].remettre_jetons_posés()  # Remettre les jetons posés
            pioche.piocher_jeton(joueur_actuel, joueurs, total_points)
            joueur_actuel = (joueur_actuel + 1) % 2  # Passer au joueur suivant

        elif action == "poser":
            # Appeler la méthode poser_jetons en passant le joueur actuel
            joueur_actuel = joueurs[joueur_actuel].poser_jetons(joueur_actuel, joueurs, plateau, total_points, pioche, premier_tour)
            premier_tour = False  # Changer l'état du premier tour après le premier tour est passé

    print("\n--- Fin de la Partie ---")
    print(f"Total des points Joueur 1: {total_points[0]} points.")
    print(f"Total des points Joueur 2: {total_points[1]} points.")
    plateau.afficher_plateau_ascii()


if __name__ == "__main__":
    main()