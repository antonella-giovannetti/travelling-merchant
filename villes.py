import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcule la distance de Haversine entre deux points spécifiés par leur latitude et longitude.

    :param lat1: Latitude du premier point.
    :param lon1: Longitude du premier point.
    :param lat2: Latitude du deuxième point.
    :param lon2: Longitude du deuxième point.
    :return: Distance entre les deux points en kilomètres.
    """
    R = 6371.0  # Rayon de la Terre en kilomètres
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

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

# Création du graphe des villes
G = nx.Graph()

for ville in villes:
    G.add_node(ville, pos=villes[ville])

for ville1 in villes:
    for ville2 in villes:
        if ville1 != ville2:
            lat1, lon1 = villes[ville1]
            lat2, lon2 = villes[ville2]
            distance = haversine(lat1, lon1, lat2, lon2)
            G.add_edge(ville1, ville2, weight=distance)

# Initialisation de la carte avec Cartopy
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-5, 10, 41, 52])  # Limites géographiques pour la France

ax.add_feature(cfeature.BORDERS, linestyle=':', alpha=0.7)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

# Positions des villes pour Cartopy (projection PlateCarree)
pos = {ville: (lon, lat) for ville, (lat, lon) in villes.items()}

# Tracé des villes sur la carte
for ville, (lon, lat) in pos.items():
    plt.plot(lon, lat, marker='o', color='red', markersize=5, transform=ccrs.PlateCarree())
    plt.text(lon + 0.1, lat, ville, fontsize=9, transform=ccrs.PlateCarree())

# Tracé des routes entre les villes
for ville1, ville2 in G.edges():
    lat1, lon1 = villes[ville1]
    lat2, lon2 = villes[ville2]
    plt.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.5, transform=ccrs.PlateCarree())

plt.title('Réseau de villes et routes en France (Cartopy)')
plt.show()