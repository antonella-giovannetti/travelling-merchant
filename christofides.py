import heapq
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from villes import haversine, villes

def create_complete_graph(cities):
    """
    Crée un graphe complet avec des distances comme poids entre les villes.

    :param cities: Dictionnaire des villes avec leurs coordonnées.
    :return: Un graphe complet avec les distances comme poids.
    """
    G = nx.Graph()
    for (city1, pos1), (city2, pos2) in combinations(cities.items(), 2):
        distance = haversine(pos1[0], pos1[1], pos2[0], pos2[1])
        G.add_edge(city1, city2, weight=distance)
    return G

def prim_mst(G):
    """
    Implémente l'algorithme de Prim pour calculer l'arbre couvrant minimum d'un graphe pondéré.

    :param G: Graphe complet avec des distances pondérées entre les villes.
    :return: Liste des arêtes de l'arbre couvrant minimum (MST).
    """
    start_node = list(G.nodes())[0]  # Choisir un noeud de départ
    mst_edges = []  # Arêtes de l'arbre couvrant minimum
    visited = set([start_node])  # Noeuds déjà visités
    edge_heap = []  # Utiliser un tas pour les arêtes (poids, u, v)

    # Ajouter toutes les arêtes sortantes du noeud de départ dans le tas
    for neighbor in G[start_node]:
        weight = G[start_node][neighbor]['weight']  # Accéder au poids
        heapq.heappush(edge_heap, (weight, start_node, neighbor))

    # Tant qu'il reste des arêtes à traiter
    while edge_heap:
        weight, u, v = heapq.heappop(edge_heap)

        # Si le noeud de destination n'a pas encore été visité
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))  # Ajouter l'arête à l'MST

            # Ajouter toutes les nouvelles arêtes sortantes du noeud v au tas
            for neighbor in G[v]:
                if neighbor not in visited:
                    weight = G[v][neighbor]['weight']  # Accéder au poids
                    heapq.heappush(edge_heap, (weight, v, neighbor))

    return mst_edges

def christofides_algorithm(cities):
    """
    Implémente l'algorithme de Christofides pour résoudre le problème du voyageur de commerce.

    :param cities: Dictionnaire des villes avec leurs coordonnées.
    :return: Chemin Hamiltonien trouvé par l'algorithme de Christofides.
    """
    G = create_complete_graph(cities)
    mst_edges = prim_mst(G)  # Utilisation de l'implémentation de Prim
    mst = nx.Graph()
    mst.add_weighted_edges_from(mst_edges)

    odd_nodes = [node for node in mst.nodes() if mst.degree(node) % 2 == 1]
    odd_subgraph = G.subgraph(odd_nodes)
    min_matching = nx.algorithms.matching.min_weight_matching(odd_subgraph)
    multigraph = nx.MultiGraph(mst)
    multigraph.add_edges_from(min_matching)
    eulerian_circuit = list(nx.eulerian_circuit(multigraph))

    hamiltonian_path = []
    visited = set()
    for u, v in eulerian_circuit:
        if u not in visited:
            visited.add(u)
            hamiltonian_path.append(u)
    if hamiltonian_path and hamiltonian_path[0] != list(cities.keys())[0]:
        hamiltonian_path.append(list(cities.keys())[0])

    return hamiltonian_path

def calculate_total_distance(path, graph):
    """
    Calcule la distance totale d'un chemin dans le graphe.

    :param path: Liste des villes constituant le chemin.
    :param graph: Graphe avec les poids des arêtes.
    :return: Distance totale du chemin.
    """
    total_distance = 0
    path = path + [path[0]]
    for i in range(len(path) - 1):
        total_distance += graph[path[i]][path[i+1]]['weight']
    return total_distance

def plot_route_with_distances(cities, route, graph):
    """
    Visualise le chemin et les distances entre les villes sur une carte.

    :param cities: Dictionnaire des villes avec leurs coordonnées.
    :param route: Liste des villes constituant le chemin.
    :param graph: Graphe avec les poids des arêtes.
    """
    fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-10, 15, 40, 55])

    ax.add_feature(cfeature.BORDERS, linestyle='--')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAKES, edgecolor='black')

    for city, coord in cities.items():
        ax.plot(coord[1], coord[0], marker='o', color='red', markersize=7, transform=ccrs.PlateCarree())
        ax.text(coord[1] + 0.2, coord[0], city, transform=ccrs.PlateCarree(), fontsize=10, color='black')

    for i in range(len(route) - 1):
        city1 = route[i]
        city2 = route[i + 1]
        distance = graph[city1][city2]['weight']
        ax.plot([cities[city1][1], cities[city2][1]], [cities[city1][0], cities[city2][0]], color='blue', linewidth=2, transform=ccrs.Geodetic())
        midpoint_lon = (cities[city1][1] + cities[city2][1]) / 2
        midpoint_lat = (cities[city1][0] + cities[city2][0]) / 2
        ax.text(midpoint_lon, midpoint_lat, f"{distance:.1f} km", transform=ccrs.PlateCarree(), fontsize=10, color='blue')

    city1 = route[-1]
    city2 = route[0]
    distance = graph[city1][city2]['weight']
    ax.plot([cities[city1][1], cities[city2][1]], [cities[city1][0], cities[city2][0]], color='blue', linewidth=2, transform=ccrs.Geodetic())
    midpoint_lon = (cities[city1][1] + cities[city2][1]) / 2
    midpoint_lat = (cities[city1][0] + cities[city2][0]) / 2
    ax.text(midpoint_lon, midpoint_lat, f"{distance:.1f} km", transform=ccrs.PlateCarree(), fontsize=10, color='blue')

    plt.title('Itinéraire et distances entre les villes', fontsize=14)
    plt.show()

path = christofides_algorithm(villes)
print("Chemin trouvé par l'algorithme de Christofides :", path)

graph = create_complete_graph(villes)
total_distance = calculate_total_distance(path, graph)
print(f"Distance totale du chemin : {total_distance:.2f} km")

# Visualisation du chemin avec les distances
plot_route_with_distances(cities, path, graph)
