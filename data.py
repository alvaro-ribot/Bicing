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




def nasty_geometric_graph(distance, bicing):
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
def geometric_graph(distance, bicing):

    # Nodos del grafo.
    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node(st)

    # Encontramos las latitudes y longitudes mínimas para saber las dimensiones de la zona de bicis.
    min_lat = bicing.loc[1].lat
    max_lat = bicing.loc[1].lat
    min_lon = bicing.loc[1].lon
    max_lon = bicing.loc[1].lon
    for st in list(G.nodes()):
        if st.lat < min_lat: min_lat = st.lat
        if st.lat > max_lat: max_lat = st.lat
        if st.lon < min_lon: min_lon = st.lon
        if st.lat > min_lat: max_lon = st.lon


    corner1 = (min_lat, min_lon)
    corner2 = (min_lat, max_lon)
    corner3 = (max_lat, min_lon)

    width = haversine(corner1, corner2)*1000 # = 5.275325461106297
    height = haversine(corner1, corner3)*1000 # = 10.4041900722105

    w_shells = int(width/distance)+1
    h_shells = int(height/distance)+1

    # Matriz de zonas de la ciudad que contendrán las estaciones, en función de la distancia d.
    grid = [[[] for j in range(w_shells)] for i in range(h_shells)]

    for st in list(G.nodes()):
        lon_st = int((st.lon - min_lon)/w_shells)
        lat_st = int((st.lat - min_lat)/h_shells)
        grid[lon_st][lat_st].append(st)

    def neighbour(G, st1, i, j, grid):
        for st2 in grid[i][j]:
            if st1.Index != st2.Index:
                coord1 = (st1.lat, st1.lon)
                coord2 = (st2.lat, st2.lon)
                if haversine(coord1, coord2)*1000 <= distance:
                    G.add_edge(st1, st2)

    for i in range(h_shells):
        for j in range(w_shells):
            for st1 in grid[i][j]:
                neighbour(G, st1, i, j, grid)
                try: neighbour(G, st1, i-1, j, grid)
                except KeyError: pass
                try: neighbour(G, st1, i-1, j-1, grid)
                except KeyError: pass
                try: neighbour(G, st1, i-1, j+1, grid)
                except KeyError: pass
                try: neighbour(G, st1, i, j-1, grid)
                except KeyError: pass
                try: neighbour(G, st1, i, j+1, grid)
                except KeyError: pass
                try: neighbour(G, st1, i+1, j-1, grid)
                except KeyError: pass
                try: neighbour(G, st1, i+1, j, grid)
                except KeyError: pass
                try: neighbour(G, st1, i+1, j+1, grid)
                except KeyError: pass
            grid[i][j].clear() # es guanya eficiencia no tornant a visitar aquesta cela
    
    return G

# retorna el nombre de nodes que te el graf G
def get_nodes(G):
    return G.number_of_nodes()

# retorna el nombre d'arestes que te el graf G
def get_edges(G):
    return G.number_of_edges()

# retorna el nobre de components connexes que te el graf G
def connex_components(G):
    return len(list(nx.connected_components(G)))


def plot_graph(G):
    m_bcn = StaticMap(1000, 1000)
    for st in G:
        marker = CircleMarker((st.lon, st.lat), 'red', 2)
        m_bcn.add_marker(marker)

    #l = list(G.edges())
    for e in G.edges():
        st1 = e[0];
        st2 = e[1];
        line = Line(((st1.lon, st1.lat), (st2.lon, st2.lat)), 'blue', 1)
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


distance = 1000



G = geometric_graph(distance, bicing);
print(get_nodes(G));
print(get_edges(G));

W = nasty_geometric_graph(distance, bicing)
print(get_nodes(W));
print(get_edges(W));
plot_graph(G);          


