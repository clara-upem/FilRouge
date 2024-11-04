class Plateau:
    def __init__(self, lignes=10, colonnes=20):
        # Initialisation d'un plateau vide
        self.plateau = [[None for _ in range(colonnes)] for _ in range(lignes)]
        self.lignes = lignes
        self.colonnes = colonnes

    def afficher_plateau_ascii(self):
        print("\nPlateau:")
        # Afficher les indices de colonnes
        print("    " + "   ".join([f"{i:^5}" for i in range(self.colonnes)]))
        for i, ligne in enumerate(self.plateau):
            ligne_affiche = f"{i:^4}"  # Afficher l'indice de la ligne
            for case in ligne:
                ligne_affiche += case.afficher_ascii() if case else "|       |"
            print(ligne_affiche)
            print("-" * (self.colonnes * 9 + 4))  # Ligne de séparation

    def verifier_set(self, set_jetons):
        # Vérifie les deux règles pour un set:
        # - Tous les jetons ont le même numéro, mais des couleurs différentes
        # - Tous les jetons ont la même couleur et forment une suite

        numeros = {jeton.numero for jeton in set_jetons}
        couleurs = {jeton.couleur for jeton in set_jetons}

        # Règle 1: Même numéro, couleurs différentes
        if len(numeros) == 1 and len(couleurs) == len(set_jetons):
            return True

        # Règle 2: Même couleur, numéros consécutifs
        if len(couleurs) == 1:
            numeros_sorted = sorted(numeros)
            if numeros_sorted == list(range(numeros_sorted[0], numeros_sorted[-1] + 1)):
                return True

        return False

    def calculer_points(self, set_jetons):
        points = 0
        for jeton in set_jetons:
            points += jeton.numero  # Supposons que le numéro du jeton représente les points
        return points

    def placer_set(self, set_jetons, x, y):
        if not self.verifier_set(set_jetons):
            print("Set non valide, ne répond pas aux règles de placement.")
            return False

        # Vérifie que le set peut être placé horizontalement à partir de la colonne `y`
        if y + len(set_jetons) > self.colonnes:
            print("Pas assez de place sur la ligne pour ce set.")
            return False

        # Placer chaque jeton horizontalement à partir de la position (x, y)
        for i, jeton in enumerate(set_jetons):
            if self.plateau[x][y + i] is None:
                self.plateau[x][y + i] = jeton
            else:
                print("Impossible de placer le set (cases occupées).")
                # Réinitialiser les placements précédents du set
                for j in range(i):
                    self.plateau[x][y + j] = None
                return False  # Annuler si une position n'est pas valide

        # Calculer et afficher les points si le set est bien placé
        points = self.calculer_points(set_jetons)
        print(f"Set placé avec succès ! Points gagnés: {points}")
        return points
    
    def retirer_jeton(self, jeton):
        # Recherche le jeton sur le plateau et le retire (le remplace par None)
        for i in range(self.lignes):
            for j in range(self.colonnes):
                if self.plateau[i][j] == jeton:
                    self.plateau[i][j] = None
                    print(f"Jeton {jeton} retiré du plateau à la position ({i}, {j}).")
                    return True
        print(f"Jeton {jeton} non trouvé sur le plateau.")
        return False