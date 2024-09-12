import random
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from villes import villes, haversine

def generate_individual(villes):
    """
    Génère un individu aléatoire (un itinéraire) en créant une permutation des villes.
    
    :param villes: Dictionnaire des villes et de leurs coordonnées.
    :return: Un individu, qui est une liste de villes dans un ordre aléatoire.
    """
    return random.sample(list(villes.keys()), len(villes))

def calculate_fitness(individual, villes):
    """
    Calcule l'inverse de la distance totale d'un itinéraire pour l'utiliser comme score de fitness.
    
    :param individual: Un itinéraire (liste de villes dans un ordre spécifique).
    :param villes: Dictionnaire contenant les coordonnées des villes.
    :return: L'inverse de la distance totale de l'itinéraire.
    """
    distance_total = 0
    for i in range(len(individual) - 1):
        ville1, ville2 = individual[i], individual[i + 1]
        lat1, lon1 = villes[ville1]
        lat2, lon2 = villes[ville2]
        distance_total += haversine(lat1, lon1, lat2, lon2)
    
    # Ajouter la distance entre la dernière et la première ville pour boucler l'itinéraire
    ville1, ville2 = individual[-1], individual[0]
    lat1, lon1 = villes[ville1]
    lat2, lon2 = villes[ville2]
    distance_total += haversine(lat1, lon1, lat2, lon2)
    
    return 1 / distance_total

def crossover(parent1, parent2):
    """
    Réalise un croisement partiel entre deux parents pour générer un nouvel individu.
    
    :param parent1: Le premier parent (itinéraire).
    :param parent2: Le second parent (itinéraire).
    :return: Un nouvel individu généré à partir des deux parents.
    """
    child = [-1] * len(parent1)
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child[start:end] = parent1[start:end]
    
    for i in range(len(parent2)):
        if parent2[i] not in child:
            for j in range(len(child)):
                if child[j] == -1:
                    child[j] = parent2[i]
                    break
    return child

def mutate(individual, mutation_rate):
    """
    Applique une mutation à un individu en échangeant deux villes en fonction d'un taux de mutation.
    
    :param individual: L'individu (itinéraire) à muter.
    :param mutation_rate: Probabilité d'appliquer une mutation à chaque position.
    :return: L'individu muté.
    """
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def select(population, fitness_scores):
    """
    Sélectionne un individu de la population en fonction de son fitness (méthode de la roulette).
    
    :param population: Liste des individus (itinéraires) dans la population.
    :param fitness_scores: Liste des scores de fitness pour chaque individu.
    :return: Un individu sélectionné en fonction de la méthode de la roulette.
    """
    total_fitness = sum(fitness_scores)
    pick = random.uniform(0, total_fitness)
    current = 0
    
    for i, fitness in enumerate(fitness_scores):
        current += fitness
        if current > pick:
            return population[i]

# Paramètres pour l'algorithme génétique
population_size = 500
generations = 250
mutation_rate = 0.001

# Initialisation de la population
population = [generate_individual(villes) for _ in range(population_size)]

# Boucle de l'algorithme génétique
for generation in range(generations):
    fitness_scores = [calculate_fitness(ind, villes) for ind in population]
    new_population = []
    
    for _ in range(population_size):
        parent1 = select(population, fitness_scores)
        parent2 = select(population, fitness_scores)
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate)
        new_population.append(child)
    
    population = new_population
    best_fitness = max(fitness_scores)
    best_individual = population[fitness_scores.index(best_fitness)]
    
    print(f"Génération {generation}: Meilleure fitness = {best_fitness:.5f}")

# Affichage de l'itinéraire optimal
best_itinerary = best_individual
distance_total = 1 / max(fitness_scores)
print(f"Itinéraire presque optimal : {best_itinerary}")
print(f"Distance totale : {distance_total:.2f} km")

# Affichage de l'itinéraire sur une carte
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-5, 10, 41, 52])

ax.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.7)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

# Récupération des positions des villes pour Cartopy
pos = {ville: (lon, lat) for ville, (lat, lon) in villes.items()}

# Tracer les villes sur la carte
for ville, (lon, lat) in pos.items():
    plt.plot(lon, lat, marker='o', color='red', markersize=5, transform=ccrs.PlateCarree())
    plt.text(lon + 0.1, lat, ville, fontsize=9, transform=ccrs.PlateCarree())

# Tracer les routes de l'itinéraire
for i in range(len(best_itinerary) - 1):
    ville1, ville2 = best_itinerary[i], best_itinerary[i + 1]
    lat1, lon1 = villes[ville1]
    lat2, lon2 = villes[ville2]
    plt.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=1, transform=ccrs.PlateCarree())

plt.plot([villes[best_itinerary[-1]][1], villes[best_itinerary[0]][1]],
         [villes[best_itinerary[-1]][0], villes[best_itinerary[0]][0]],
         color='blue', linewidth=1, transform=ccrs.PlateCarree())

plt.title('Itinéraire presque optimal')
plt.show()