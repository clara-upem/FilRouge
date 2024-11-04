# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:40:57 2024

@author: Clara Correia
Projet PPMD POO -Rummikub-
Classe Main
Qui represente la Main d'un joueur'
"""
from jetons import Jetons
from Pioche import Pioche
import random
# Classe Main pour gérer les mains de 14 jetons
class Main:
    def __init__(self, jeu_de_jetons, fixe=False, fixe2=False):

        if fixe:
            # Si la première main fixe est demandée, on crée cette main prédéfinie
            self.jetons = [
                Jetons(10, 1),  # 10 R
                Jetons(10, 2),  # 10 V
                Jetons(10, 3),  # 10 B
                Jetons(1, 1),   # 1 R
                Jetons(2, 1),   # 2 R
                Jetons(3, 1),   # 3 R
                Jetons(4, 2),   # 4 V
                Jetons(5, 2),   # 5 V
                Jetons(6, 3),   # 6 B
                Jetons(7, 4),   # 7 J
                Jetons(8, 2),   # 8 V
                Jetons(9, 3),   # 9 B
                Jetons(11, 4),  # 11 J
                Jetons(12, 2)   # 12 V
            ]
            # Ajouter ces jetons à la main et les retirer de la pioche
            for jeton in self.jetons:
                if jeton in jeu_de_jetons.jetons:
                    jeu_de_jetons.jetons.remove(jeton)

        elif fixe2:
            # Si la deuxième main fixe est demandée, on crée cette main prédéfinie
            self.jetons = [
                Jetons(1, 1),   # 1 R
                Jetons(2, 2),   # 2 V
                Jetons(2, 4),   # 2 J
                Jetons(3, 4),   # 3 J
                Jetons(4, 1),   # 4 R                
                Jetons(5, 3),   # 5 B
                Jetons(5, 2),   # 5 R
                Jetons(5, 4),   # 5 J
                Jetons(7, 3),   # 7 B
                Jetons(9, 1),   # 9 R
                Jetons(9, 2),   # 9 V
                Jetons(11, 1),  # 11 R
                Jetons(13, 2),  # 13 V
                Jetons(13, 1)   # 13 R
            ]
            # Ajouter ces jetons à la main et les retirer de la pioche
            for jeton in self.jetons:
                if jeton in jeu_de_jetons.jetons:
                    jeu_de_jetons.jetons.remove(jeton)
        else:
            # Sinon, on génère une main aléatoire de 14 jetons
            self.jetons = []
            for _ in range(14):
                jeton = random.choice(jeu_de_jetons.jetons)  # Sélectionner un jeton au hasard
                self.jetons.append(jeton)  # Ajouter le jeton à la main
                jeu_de_jetons.jetons.remove(jeton)  # Retirer le jeton de la pioche

    def suppr_jeton(self, jeton):
        if jeton in self.jetons:
            self.jetons.remove(jeton)
            print(f"Jeton {jeton} supprimé de la main.")
        else:
            print(f"Jeton {jeton} n'est pas dans la main.")
    
    def pass_turn(self):
        # Demande au joueur s'il veut passer son tour
        reponse = input("Voulez-vous passer votre tour ? (o/n) : ").lower()
        return reponse == 'o'
    
    def remettre_jetons_posés(self, jetons_posés):
        """Remettre les jetons posés dans la main."""
        for jeton in jetons_posés:
            self.add_jeton(jeton)  # Ajoute les jetons posés de retour à la main
        jetons_posés.clear()  # Vider la liste des jetons posés
        print("Tous les jetons posés ont été remis dans la main.")
    
    def poser_jetons(self, joueur_actuel, joueurs, plateau, total_points, pioche, premier_tour):
        jetons_posés = []  # Liste pour garder les jetons posés durant le tour
        points_set_total = 0  # Total des points des sets posés durant le tour
    
        while True:
            # Demander au joueur de sélectionner un set
            print("\nSélectionnez les indices des jetons à placer comme un set (séparés par des virgules) ou 'fin' pour terminer le tour:")
            selection = input("Entrez les indices (ex: 0,1,2) ou 'fin': ").strip()
            
            if selection.lower() == 'fin':
                if premier_tour and total_points[joueur_actuel] < 30:
                    print("Vous devez avoir au moins 30 points pour terminer ce tour. Vous devez piocher un jeton.")
                    pioche.piocher_jeton(joueur_actuel, joueurs, total_points)  # Piocher un jeton
                    self.remettre_jetons_posés(jetons_posés)  # Remettre les jetons posés
                return (joueur_actuel + 1) % 2  # Passer au joueur suivant
    
            try:
                indices = [int(idx.strip()) for idx in selection.split(',')]
            except ValueError:
                print("Entrée invalide. Veuillez entrer des indices séparés par des virgules.")
                continue
    
            # Vérifier que les indices sont valides pour la main du joueur
            if not all(0 <= idx < len(joueurs[joueur_actuel].jetons) for idx in indices):
                print("Un ou plusieurs indices sont invalides.")
                continue
    
            # Récupérer les jetons sélectionnés à partir des indices
            set_jetons = [joueurs[joueur_actuel].jetons[idx] for idx in indices]
    
            # Vérifier si le set de jetons est valide
            if not plateau.verifier_set(set_jetons):
                print("Set non valide selon les règles de Rummikub.")
                continue  # Redemander un set valide
    
            # Calculer les points pour le set de jetons
            points_set = plateau.calculer_points(set_jetons)
            print(f"Points pour ce set : {points_set}")
    
            # Demander à l'utilisateur sur quelle ligne il veut placer les jetons
            try:
                ligne = int(input(f"Entrez la ligne de placement (0 à {plateau.lignes - 1}): "))
            except ValueError:
                print("Coordonnée de ligne non valide.")
                continue
    
            # Vérifier si la ligne est valide
            if ligne < 0 or ligne >= plateau.lignes:
                print("Ligne invalide. Veuillez entrer une ligne correcte.")
                continue
    
            # Vérifier l'espace pour placer les jetons
            col_start = 0
            while col_start < plateau.colonnes and plateau.plateau[ligne][col_start] is not None:
                col_start += 1
            
            if col_start + len(set_jetons) > plateau.colonnes:
                print("Pas assez d'espace pour placer tous les jetons sur la ligne choisie.")
                continue
    
            # Essayer de placer le set de jetons sur le plateau
            if plateau.placer_set(set_jetons, ligne, col_start):
                total_points[joueur_actuel] += points_set  # Ajouter les points au total du joueur
                points_set_total += points_set  # Accumuler les points du set
                jetons_posés.extend(set_jetons)  # Conserver les jetons posés
                for jeton in set_jetons:
                    joueurs[joueur_actuel].suppr_jeton(jeton)
    
                plateau.afficher_plateau_ascii()
    
                # Vérifier si le joueur a atteint ou dépassé 30 points
                if premier_tour and points_set_total >= 30:
                    print(f"Vous avez atteint {points_set_total} points avec ce set ! Vous pouvez maintenant passer au joueur suivant.")
                    return (joueur_actuel + 1) % 2  # Passer au joueur suivant
                
                # Demander si le joueur veut continuer à poser des jetons
                continuer = input("Voulez-vous poser un autre set ? (o/n): ").strip().lower()
                if continuer != 'o':
                    return (joueur_actuel + 1) % 2  # Passer au joueur suivant
    
            else:
                print("Placement échoué. Essayez un autre emplacement.")
    
        


    # Affichage des jetons sous forme de tableau ASCII
    def afficher_main_ascii(self):
        print("+-------+-------+-------+")
        print("| Index | Numéro|Couleur|")
        print("+-------+-------+-------+")
        for idx, jeton in enumerate(self.jetons):
            print(f"|  {idx:^3} | {jeton.numero:^5} | {jeton.couleur:^6} |")
        print("+-------+-------+-------+")
    
    def __repr__(self):
        return f"Main: {self.jetons}"
