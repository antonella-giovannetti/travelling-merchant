import networkx as nx
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2
import numpy as np

# Fonction pour calculer la distance de Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Rayon de la Terre en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Liste des villes avec leurs coordonnées
villes = {
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

# Création du graphe
G = nx.Graph()

# Ajout des sommets (villes)
for ville in villes:
    G.add_node(ville, pos=villes[ville])

# Ajout des arêtes avec la distance de Haversine comme poids
for ville1 in villes:
    for ville2 in villes:
        if ville1 != ville2:
            lat1, lon1 = villes[ville1]
            lat2, lon2 = villes[ville2]
            distance = haversine(lat1, lon1, lat2, lon2)
            G.add_edge(ville1, ville2, weight=distance)

# Récupération des positions pour l'affichage
pos = nx.get_node_attributes(G, 'pos')

# Affichage du graphe
plt.figure(figsize=(12, 12))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')

# Ajouter les étiquettes des poids (distances)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{w:.1f} km' for u, v, w in G.edges(data='weight')})

plt.title('Réseau de villes et routes (Distance Haversine)')
plt.show()
