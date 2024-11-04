# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:42:25 2024

@author: Clara Correia
Projet PPMD POO -Rummikub-
Classe Jetons
Qui represente les jetons et leurs fonction
"""

import random
from Pioche import Pioche

# Classe Jetons pour créer et gérer l'ensemble des 108 jetons
class Jetons:
    def __init__(self, numero, couleur):
        self.numero = numero
        self.couleur = couleur
    
    def afficher_ascii(self):
        return f"| {self.numero:^3} _ {self.couleur:^3} |"
    
    
    
    def poser_jetons(joueur_actuel, joueurs, plateau, total_points, pioche):
        jetons_posés = []  # Liste pour garder les jetons posés durant le tour
    
        while True:  # Boucle pour permettre plusieurs tentatives de placement
            # Demander au joueur de sélectionner un set
            print("\nSélectionnez les indices des jetons à placer comme un set (séparés par des virgules) ou 'fin' pour terminer le tour:")
            selection = input("Entrez les indices (ex: 0,1,2) ou 'fin': ").strip()
    
            if selection.lower() == 'fin':
                if total_points[joueur_actuel] < 30:  # Vérifier si les points sont insuffisants
                    print("Total des points insuffisant. Vous devez retourner vos jetons et piocher un nouveau jeton.")
                    for jeton in jetons_posés:
                        joueurs[joueur_actuel].jetons.append(jeton)  # Rendre les jetons à la main
                        plateau.retirer_jeton(jeton)  # Retirer du plateau
                    jetons_posés.clear()  # Effacer la liste des jetons posés
    
                    Pioche.piocher_jeton(joueur_actuel, joueurs, pioche, total_points)
    
                return (joueur_actuel + 1) % 2  # Passer au joueur suivant
    
            try:
                indices = [int(idx.strip()) for idx in selection.split(',')]
            except ValueError:
                print("Entrée invalide. Veuillez entrer des indices séparés par des virgules.")
                continue
    
            if not all(0 <= idx < len(joueurs[joueur_actuel].jetons) for idx in indices):
                print("Un ou plusieurs indices sont invalides.")
                continue
    
            set_jetons = [joueurs[joueur_actuel].jetons[idx] for idx in indices]
    
            if not plateau.verifier_set(set_jetons):
                print("Set non valide selon les règles de Rummikub.")
                choix = input("Souhaitez-vous passer votre tour? (o/n): ").strip().lower()
                if choix == 'o':
                    # Rendre les jetons posés
                    for jeton in jetons_posés:
                        joueurs[joueur_actuel].jetons.append(jeton)
                        plateau.retirer_jeton(jeton)
                    jetons_posés.clear()
                    if total_points[joueur_actuel] < 30:
                        Pioche.piocher_jeton(joueur_actuel, joueurs, pioche, total_points)
                    return (joueur_actuel + 1) % 2  # Passer au joueur suivant
                else:
                    continue  # Demander à nouveau un set
    
            points_set = plateau.calculer_points(set_jetons)
            print(f"Points pour ce set : {points_set}")
    
            try:
                x = int(input(f"Entrez la ligne de départ (0 à {plateau.lignes - 1}): "))
                y = int(input(f"Entrez la colonne de départ (0 à {plateau.colonnes - 1}): "))
            except ValueError:
                print("Coordonnées non valides.")
                continue
    
            if plateau.placer_set(set_jetons, x, y):
                total_points[joueur_actuel] += points_set
                jetons_posés.extend(set_jetons)  # Ajouter les jetons posés à la liste
                for jeton in set_jetons:
                    joueurs[joueur_actuel].suppr_jeton(jeton)
    
                plateau.afficher_plateau_ascii()
    
                # Vérifier le total des points après placement
                if total_points[joueur_actuel] < 30:
                    joueurs[joueur_actuel].afficher_main_ascii()
                    choix = input("Vous avez moins de 30 points. Voulez-vous proposer un autre set ou piocher un jeton? (proposer/piocher): ").strip().lower()
                    if choix == "piocher":
                        Pioche.piocher_jeton(joueur_actuel, joueurs, pioche, total_points)
                    return (joueur_actuel + 1) % 2  # Passer au joueur suivant
                return joueur_actuel  # Rester sur le même joueur
    
            else:
                print("Placement échoué. Essayez un autre emplacement ou passez votre tour.")
    
        
    def __repr__(self):
        couleurs_nom = {1: 'Rouge', 2: 'Vert', 3: 'Bleu', 4: 'Jaune', 0: 'Joker'}
        return f"Jeton(numéro: {self.numero}, couleur: {couleurs_nom.get(self.couleur, 'Inconnue')})"


# Classe Joker qui hérite de Jetons
class Joker(Jetons):
    def __init__(self):
        # Un Joker a un numéro et une couleur de 0
        super().__init__(numero=0, couleur=0)

    # Fonction spécifique au Joker appelée "metamorphose"
    def metamorphose(self, numero, couleur):
        # Permet au Joker de prendre la forme d'un autre jeton
        self.numero = numero
        self.couleur = couleur
    
    def afficher_ascii(self):
        return f"| {'J':^3} _ {'J':^3} |"  # Pour afficher un Joker sous forme de 'J'

    def __repr__(self):
        return f"Joker(métamorphosé en numéro: {self.numero}, couleur: {self.couleur})" if self.numero != 0 else "Joker"

# Classe qui gère l'ensemble des jetons (108 jetons)
class EnsembleDeJetons:
    def __init__(self):
        self.jetons = []
        self.couleurs = [1, 2, 3, 4]  # Couleurs représentées par des nombres de 1 à 4

        # Création des jetons normaux (numéros de 1 à 13, 4 couleurs, 2 exemplaires chacun)
        for _ in range(2):  # On fait tout deux fois
            for couleur in self.couleurs:
                for numero in range(1, 14):
                    self.jetons.append(Jetons(numero, couleur))
        
        # Ajout des deux jokers
        self.jetons.append(Joker())  # Joker 1
        self.jetons.append(Joker())  # Joker 2

    # Mélange des jetons
    def melanger(self):
        random.shuffle(self.jetons)
        
    def piocher(self):
        if self.jetons:
            return self.jetons.pop()
        return None

    def __repr__(self):
        return f"EnsembleDeJetons({len(self.jetons)} jetons)"
    
