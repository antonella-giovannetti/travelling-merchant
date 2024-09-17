import csv
import math
import random
import numpy as np

# Lecture des villes à partir du fichier CSV
def lire_villes(fichier_csv):
    villes = {}
    with open(fichier_csv, mode='r') as fichier:
        lecteur_csv = csv.reader(fichier)
        next(lecteur_csv)  # Sauter l'en-tête
        for ligne in lecteur_csv:
            ville = ligne[0]
            latitude = float(ligne[1])
            longitude = float(ligne[2])
            villes[ville] = (latitude, longitude)
    return villes

# Calcul de la distance de Haversine
def haversine(coord1, coord2):
    R = 6371  # Rayon de la Terre en km
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convertir les degrés en radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c  # Résultat en km

# Calcul de la distance totale pour un itinéraire donné
def total_distance(route, villes):
    distance = 0
    for i in range(len(route) - 1):
        ville1 = villes[route[i]]
        ville2 = villes[route[i + 1]]
        distance += haversine(ville1, ville2)
    # Retour à la ville de départ
    distance += haversine(villes[route[-1]], villes[route[0]])
    return distance

# Algorithme de recuit simulé
def simulated_annealing(villes, T_init, alpha, T_min):
    # Initialisation de la solution (un ordre aléatoire des villes)
    current_solution = list(villes.keys())
    random.shuffle(current_solution)
    
    # Calcul de la distance pour la solution initiale
    current_distance = total_distance(current_solution, villes)
    
    # Solution optimale
    best_solution = current_solution[:]
    best_distance = current_distance
    
    # Température initiale
    T = T_init
    
    while T > T_min:
        # Générer une solution voisine (échanger deux villes)
        new_solution = current_solution[:]
        i, j = random.sample(range(len(villes)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        # Calculer la distance de la nouvelle solution
        new_distance = total_distance(new_solution, villes)
        
        # Calculer la différence de distance
        delta = new_distance - current_distance
        
        # Si la nouvelle solution est meilleure ou acceptée avec une probabilité
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
            current_solution = new_solution
            current_distance = new_distance
        
        # Mettre à jour la meilleure solution trouvée
        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance
        
        # Refroidir la température
        T *= alpha
    
    return best_solution, best_distance

# Lecture des données
villes = lire_villes('villes_france_lat_long.csv')

# Paramètres du recuit simulé
T_init = 1000  # Température initiale
alpha = 0.999  # Facteur de refroidissement
T_min = 1e-8   # Température minimale

# Exécution de l'algorithme de recuit simulé
best_route, best_distance = simulated_annealing(villes, T_init, alpha, T_min)

# Affichage du meilleur itinéraire et de la distance minimale
print("Meilleur itinéraire trouvé :", best_route)
print("Distance totale minimale :", best_distance, "km")