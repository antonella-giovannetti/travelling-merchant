import networkx as nx
from itertools import combinations
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Fonction pour calculer la distance de Haversine entre deux points géographiques
def haversine(coord1, coord2):
    R = 6371.0  # Rayon de la Terre en kilomètres

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Fonction pour créer un graphe complet avec des distances comme poids
def create_complete_graph(cities):
    G = nx.Graph()
    for (city1, pos1), (city2, pos2) in combinations(cities.items(), 2):
        distance = haversine(pos1, pos2)
        G.add_edge(city1, city2, weight=distance)
    return G

# Fonction principale pour implémenter l'algorithme de Christofides
def christofides_algorithm(cities):
    G = create_complete_graph(cities)
    
    # Étape 1 : Calculer l'arbre couvrant minimal (MST)
    mst = nx.minimum_spanning_tree(G)

    # Étape 2 : Trouver les sommets avec un degré impair dans le MST
    odd_nodes = [node for node in mst.nodes() if mst.degree(node) % 2 == 1]

    # Étape 3 : Trouver un couplage parfait minimum sur les sommets impairs
    odd_subgraph = G.subgraph(odd_nodes)
    min_matching = nx.algorithms.matching.min_weight_matching(odd_subgraph)

    # Étape 4 : Ajouter les arêtes du couplage parfait au MST
    multigraph = nx.MultiGraph(mst)
    multigraph.add_edges_from(min_matching)

    # Étape 5 : Trouver un circuit eulérien
    eulerian_circuit = list(nx.eulerian_circuit(multigraph))

    # Étape 6 : Convertir le circuit eulérien en un chemin Hamiltonien
    hamiltonian_path = []
    visited = set()
    for u, v in eulerian_circuit:
        if u not in visited:
            visited.add(u)
            hamiltonian_path.append(u)
    # Assurer que le chemin retourne au point de départ
    if hamiltonian_path and hamiltonian_path[0] != list(cities.keys())[0]:
        hamiltonian_path.append(list(cities.keys())[0])

    return hamiltonian_path

# Fonction pour calculer la distance totale du chemin
def calculate_total_distance(path, graph):
    total_distance = 0
    path = path + [path[0]]  # Ajouter la ville de départ pour fermer le circuit
    for i in range(len(path) - 1):
        total_distance += graph[path[i]][path[i+1]]['weight']
    return total_distance

# Fonction pour visualiser le chemin et afficher les distances
def plot_route_with_distances(cities, route, graph):
    fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-10, 15, 40, 55])  # Limites de la carte (Europe de l'Ouest)

    ax.add_feature(cfeature.BORDERS, linestyle='--')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAKES, edgecolor='black')
    
    # Tracer les villes
    for city, coord in cities.items():
        ax.plot(coord[1], coord[0], marker='o', color='red', markersize=7, transform=ccrs.PlateCarree())
        ax.text(coord[1] + 0.2, coord[0], city, transform=ccrs.PlateCarree(), fontsize=10, color='black')

    # Tracer le chemin et afficher les distances
    for i in range(len(route) - 1):
        city1 = route[i]
        city2 = route[i + 1]
        distance = graph[city1][city2]['weight']
        ax.plot([cities[city1][1], cities[city2][1]], [cities[city1][0], cities[city2][0]], color='blue', linewidth=2, transform=ccrs.Geodetic())
        
        # Afficher la distance entre les villes
        midpoint_lon = (cities[city1][1] + cities[city2][1]) / 2
        midpoint_lat = (cities[city1][0] + cities[city2][0]) / 2
        ax.text(midpoint_lon, midpoint_lat, f"{distance:.1f} km", transform=ccrs.PlateCarree(), fontsize=10, color='blue')

    # Retour à la ville de départ
    city1 = route[-1]
    city2 = route[0]
    distance = graph[city1][city2]['weight']
    ax.plot([cities[city1][1], cities[city2][1]], [cities[city1][0], cities[city2][0]], color='blue', linewidth=2, transform=ccrs.Geodetic())
    
    # Afficher la distance de retour
    midpoint_lon = (cities[city1][1] + cities[city2][1]) / 2
    midpoint_lat = (cities[city1][0] + cities[city2][0]) / 2
    ax.text(midpoint_lon, midpoint_lat, f"{distance:.1f} km", transform=ccrs.PlateCarree(), fontsize=10, color='blue')

    plt.title('Itinéraire et distances entre les villes', fontsize=14)
    plt.show()

# Exemple de données pour les villes
cities = {
    "Paris": (48.8566, 2.3522),
    "Marseille": (43.2965, 5.3698),
    "Lyon": (45.764, 4.8357),
    "Toulouse": (43.6047, 1.4442),
    "Nice": (43.7102, 7.262),
    "Nantes": (47.2184, -1.5536),
    "Strasbourg": (48.5734, 7.7521),
    "Montpellier": (43.6119, 3.8772),
    "Bordeaux": (44.8378, -0.5792),
    "Lille": (50.6292, 3.0573),
    "Rennes": (48.1173, -1.6778),
    "Reims": (49.2583, 4.0317),
    "Le Havre": (49.4944, 0.1079),
    "Saint-Étienne": (45.4397, 4.3872),
    "Toulon": (43.1242, 5.928),
    "Grenoble": (45.1885, 5.7245),
    "Dijon": (47.322, 5.0415),
    "Angers": (47.4784, -0.5632),
    "Nîmes": (43.8367, 4.3601),
    "Clermont-Ferrand": (45.7772, 3.087)
}

# Exécution de l'algorithme de Christofides
path = christofides_algorithm(cities)
print("Chemin trouvé par l'algorithme de Christofides :", path)

# Création du graphe complet avec les distances comme poids
graph = create_complete_graph(cities)

# Calcul de la distance totale
total_distance = calculate_total_distance(path, graph)
print(f"Distance totale du chemin : {total_distance:.2f} km")

# Visualisation du chemin avec les distances
plot_route_with_distances(cities, path, graph)
