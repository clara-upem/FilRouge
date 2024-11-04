# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:32:02 2024

@author: Formation
"""

class Pioche:
    def __init__(self, jeu_de_jetons, main_joueur_1, main_joueur_2):
        self.jetons = [jeton for jeton in jeu_de_jetons.jetons if jeton not in main_joueur_1.jetons and jeton not in main_joueur_2.jetons]
        
    
    def piocher_jeton(self, joueur_actuel, joueurs, total_points):
        # Piocher un jeton
        if self.jetons:
            jeton_pioche = self.jetons.pop()  # Prend un jeton de la pioche
            joueurs[joueur_actuel].jetons.append(jeton_pioche)  # Ajoute le jeton à la main du joueur
            print(f"Joueur {joueur_actuel + 1} a pioché : {jeton_pioche}.")
        else:
            print("Il n'y a plus de jetons à piocher.")
