# Módulo para el tratamiento de datos.
import pandas as pd
from pandas import DataFrame

# Módulo para grafos.
import networkx as nx

# Módulos para mapas y distancias reales.
from staticmap import StaticMap, Line, CircleMarker
from haversine import haversine
from geopy.geocoders import Nominatim



def addressesTOcoordinates(addresses):
    '''
    Returns the two coordinates of two addresses of Barcelona
    in a single string separated by a comma. In case of failure, returns None.
    '''
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None

'''
coords = addressesTOcoordinates('Passeig de Gràcia 92, La Rambla 51')
if coords is None: print("Adreça no trobada")
else:
    coord_origen, coord_desti = coords
    print('Passeig de Gràcia 92:', coord_origen)
    print('La Rambla 51:', coord_desti)

coords = addressesTOcoordinates('Avinguda de Jordi Cortadella, Carrer de Jordi Petit')
if coords is None: print("Adreça no trobada")
else: print(coords)  
'''


# Función que calcula la ruta más rápida entre dos direcciones, retornando -1 si la ruta no es posible.
def route(G, addresses, d):
    coords = addressesTOcoordinates(addresses)
    if coords is None: return None
    else:
        coord_origen, coord_desti = coords
        st1 = ('source', coord_origen[0], coord_origen[1])
        st2 = ('target', coord_desti[0], coord_origen[1])

        G.add_node(st1)
        G.add_node(st2)

        for st in G:

            if st[0] != st2[0] and haversine((st[1], st[2]), (st1[1], st1[2]))*1000 <= d:
                G.add_edge(st1, st)
            if st[0] != st1[0] and haversine((st[1], st[2]), (st2[1], st2[2]))*1000 <= d:
                G.add_edge(st2, st)
        
        path = nx.shortest_path(G, source=st1, target=st2)
        print(path)


        m_route = StaticMap(1000, 1000)
        for st in path:
            marker = CircleMarker((st[2], st[1]), 'red', 6)
            m_route.add_marker(marker)

        #l = list(G.edges())
        '''
        for e in path.edges():
            st1 = e[0];
            st2 = e[1];
            line = Line(((st1[2], st1[1]), (st2[2], st2[1])), 'blue', 1)
            m_route.add_line(line)

        '''


        image = m_route.render()
        image.save('route.png')


        G.remove_node(st1)
        G.remove_node(st2)


'''
def geometric_graph(distance, bicing):
    G = nx.Graph()

    for st in bicing.itertuples():
        stop = (st.Index, st.lat, st.lon)
        G.add_node(stop)

    for st1 in G:
        for st2 in G:
            if st1[0] != st2[0]:
                coord1 = (st1[1], st1[2])
                coord2 = (st2[1], st2[2])
                if haversine(coord1, coord2)*1000 <= distance:
                    G.add_edge(st1, st2)

    return G
'''


def geometric_graph(distance, bicing):
    G = nx.Graph()

    for st in bicing.itertuples():
        G.add_node(st.Index)

    for idx1 in G:
        for idx2 in G:
            if idx1 != idx2:

                coord1 = (bicing.at[idx1, 'lat'], bicing.at[idx1, 'lon'])
                coord2 = (bicing.at[idx2, 'lat'], bicing.at[idx2, 'lon'])
                if haversine(coord1, coord2)*1000 <= distance:
                    G.add_edge(idx1, idx2)

    return G


# Función para construir el grafo geométrico dada la distancia d máxima entre dos nodos. 
# El algoritmo funciona partiendo el grafo en zonas cuadradas d*d y examinándolas con sus zonas adyacentes
# en tiempo constante, suponiendo una distribución uniforme de nodos en la ciudad.
def geo_graph(distance, bicing):

    # Nodos del grafo.
    G = nx.Graph()

    # Encontramos las latitudes y longitudes mínimas para saber las dimensiones de la zona de bicis.
    min_lat = bicing.loc[1].lat
    max_lat = bicing.loc[1].lat
    min_lon = bicing.loc[1].lon
    max_lon = bicing.loc[1].lon

    for st in bicing.itertuples():
        if st.lat < min_lat: min_lat = st.lat
        if st.lat > max_lat: max_lat = st.lat
        if st.lon < min_lon: min_lon = st.lon
        if st.lat > min_lat: max_lon = st.lon

    print(min_lat)
    print(max_lat)
    print(min_lon)
    print(max_lon)

    print('**********************')

    coord1 = (min_lat, min_lon)
    coord2 = (min_lat, max_lon)
    coord3 = (max_lat, max_lon)
    coord4 = (max_lat, min_lon)

    width = haversine(coord1, coord2)*1000
    height = haversine(coord2, coord3)*1000

    # Matriz de zonas de la ciudad que contendrán las estaciones, en función de la distancia d.
    grid = [[[] for j in range(int(width/d) + 1)] for i in range(int(height/d) + 1)]

    '''
    for stop in bicing:
        grid[][].append(stop)
        
    '''

    '''
    min_lat = 41.357067
    max_lat = 41.450634
    min_lon = 2.111615
    max_lon = 2.17482

    dist_lon = 5.275325461106297
    dist_lat = 10.4041900722105
    '''


def get_nodes(G):
    return G.number_of_nodes()

def get_edges(G):
    return G.number_of_edges()

def connex_components(G):
    return len(list(nx.connected_components(G)))

def plot_graph(G):
    m_bcn = StaticMap(1000, 1000)
    for st in G:
        marker = CircleMarker((st[2], st[1]), 'red', 2)
        m_bcn.add_marker(marker)

    #l = list(G.edges())
    for e in G.edges():
        st1 = e[0];
        st2 = e[1];
        line = Line(((st1[2], st1[1]), (st2[2], st2[1])), 'blue', 1)
        m_bcn.add_line(line)


    image = m_bcn.render()
    image.save('bicing_plot.png')
    return 'bicing_plot.png'

def main ():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')


    G = geo_graph(1000, bicing)


    '''
    print(bicing.loc[1].lat)
    print(bicing.at[1, 'lat'], bicing.at[1, 'lon'])
    '''

    #print(G.number_of_nodes())
    #print(G.number_of_edges())
    #plot_graph(G)

    #geo_graph(1)
    #route(G, 'Pau Gargallo 1, PL. Lesseps', d)

#main()

url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')


d = 5000


min_lat = bicing.loc[1].lat
max_lat = bicing.loc[1].lat
min_lon = bicing.loc[1].lon
max_lon = bicing.loc[1].lon

for st in bicing.itertuples():
    if st.lat < min_lat: min_lat = st.lat
    if st.lat > max_lat: max_lat = st.lat
    if st.lon < min_lon: min_lon = st.lon
    if st.lat > min_lat: max_lon = st.lon

print(min_lat)
print(max_lat)
print(min_lon)
print(max_lon)

print('**********************')

coord1 = (min_lat, min_lon)
coord2 = (min_lat, max_lon)
coord3 = (max_lat, max_lon)
coord4 = (max_lat, min_lon)

width = haversine(coord1, coord2)*1000
height = haversine(coord2, coord3)*1000


print(width)
print(height)

grid = [[[] for j in range(int(width/d)+1)] for i in range(int(height/d)+1)]


G = nx.Graph()
for st in bicing.itertuples():
        G.add_node(st.Index)

print(grid)
grid[0][0].append(1)
print(grid)
'''
for idx1 in G:
        for idx2 in G:
            if idx1 != idx2:
                coord1 = (bicing.at[idx1, 'lat'], bicing.at[idx1, 'lon'])
                coord2 = (bicing.at[idx2, 'lat'], bicing.at[idx2, 'lon'])
                if haversine(coord1, coord2)*1000 <= distance:
                    G.add_edge(idx1, idx2)

'''










'''
route(G, 'Avinguda Meridiana 1, Plaza Lesseps', 1000)
geometric_graph(500)
plot_graph()
'''


