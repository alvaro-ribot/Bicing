# Moduls pel tractament de dades.
import pandas as pd
from pandas import DataFrame

# Modul per treballar amb grafs.
import networkx as nx

# Moduls per mapes i distancies reals.
from staticmap import StaticMap, Line, CircleMarker
from haversine import haversine
from geopy.geocoders import Nominatim


# Retorna les dades d'estacions de bicing de Barcelona
def dades_bicing():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    return bicing


# Funcio per construir el graf geometric donada la distancia d maxima entre dos nodos. 
# L'algorisme funciona partint el grafo en zones quadrades d*d i examinant-les amb les seves 
# zones adjacents en temps constant, suposant una distribucio uniforme de nodes en la ciutat.
def geometric_graph(distance, bicing):
    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node(st)  # Nodes del graf.

    # Trobem les latituds i longituds minimes para saber les dimensiones de la zona de bicis.
    min_lat = bicing.loc[1].lat
    max_lat = bicing.loc[1].lat
    min_lon = bicing.loc[1].lon
    max_lon = bicing.loc[1].lon
    for st in G:
        if st.lat < min_lat: min_lat = st.lat
        if st.lat > max_lat: max_lat = st.lat
        if st.lon < min_lon: min_lon = st.lon
        if st.lat > min_lat: max_lon = st.lon

    corner1 = (min_lat, min_lon)
    corner2 = (min_lat, max_lon)
    corner3 = (max_lat, min_lon)
    width = haversine(corner1, corner2)*1000   # amplada
    height = haversine(corner1, corner3)*1000  # alcada
    w_shells = int(width/distance)+1  # dividim l'amplada segons la distnacia
    h_shells = int(height/distance)+1 # dividim l'alcada segons la distancia

    # Graella de zones de la ciutat que contindran les estacions, en funcio de distance.
    grid = [[[] for j in range(w_shells)] for i in range(h_shells)]

    # Afegim cada node a la zona corresponent 
    for st in G:
        lon_st = int((st.lon - min_lon)/w_shells)
        lat_st = int((st.lat - min_lat)/h_shells)
        grid[lon_st][lat_st].append(st)

    # Afegeix arestes al graf G visitant nomes els nodes que pertanyen a zones i, j
    # de la graella (grid) adjacents a la zona a qui pertany st1.
    def neighbour(G, st1, i, j, grid):
        for st2 in grid[i][j]:
            if st1.Index != st2.Index:
                coord1 = (st1.lat, st1.lon)
                coord2 = (st2.lat, st2.lon)
                if haversine(coord1, coord2)*1000 <= distance: # Condicio graf geometric
                    G.add_edge(st1, st2)

    # Afegim les arestes del graf geometric.
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
            grid[i][j].clear() # es guanya eficiencia no tornant a visitar aquesta zona
    
    return G



# Retorna el nombre de nodes que del graf G.
def get_nodes(G):
    return G.number_of_nodes()



# Retorna el nombre d'arestes que del graf G.
def get_edges(G):
    return G.number_of_edges()



# Retorna el nobre de components connexes que del graf G.
def connex_components(G):
    return len(list(nx.connected_components(G)))



# Retorna una imatge del graf G.
def plot_graph(G):
    m_bcn = StaticMap(1000, 1000)
    for st in G:
        marker = CircleMarker((st.lon, st.lat), 'red', 2)
        m_bcn.add_marker(marker)
    for e in G.edges():
        st1 = e[0];
        st2 = e[1];
        line = Line(((st1.lon, st1.lat), (st2.lon, st2.lat)), 'blue', 1)
        m_bcn.add_line(line)

    return m_bcn.render()



# Retorna les dues coordenades de duess direccions (addresses) de Barcelona en 
# una sola string seperant-les amb una coma. Si no les troba, retorna None.
def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None



# Calcula la ruta mes rapida entre dues direccions (adresseses) al graf G,
# retorna None si no troba les direccions.
def route(G, addresses):
    coords = addressesTOcoordinates(addresses)
    if coords is None: return None
    else:
        coord_origen, coord_desti = coords
        origen = ('source', coord_origen[0], coord_origen[1])
        desti = ('target', coord_desti[0], coord_desti[1])

        W = nx.Graph() # creem un nou graf amb pesos a les arestes

        W.add_node(origen)
        W.add_node(desti)
        for st in G: W.add_node(st)

        # El pes de cada aresta es la distancia entre els nodes dividit entre la
        # velocitat (10 km/h en bici i 4 km/h caminant)
        for e in G.edges():
            time = haversine((e[0].lat, e[0].lon), (e[1].lat, e[1].lon))/10
            W.add_edge(e[0], e[1], weight = time)

        for st in G:
            t1 = haversine((st.lat, st.lon), (origen[1], origen[2]))/4
            t2 = haversine((st.lat, st.lon), (desti[1], desti[2]))/4
            W.add_edge(origen, st, weight = t1)
            W.add_edge(desti, st, weight = t2)

        caminant = haversine((desti[1], desti[2]), (origen[1], origen[2]))/4
        W.add_edge(origen, desti, weight = caminant)
        
        # Cami mes curt utilitzant l'algorisme de dijkstra
        path = nx.dijkstra_path(W, source=origen, target=desti)

        # Dibuixem la ruta en un mapa
        m_route = StaticMap(1000, 1000)
        m_route.add_marker(CircleMarker((origen[2], origen[1]), 'red', 6))
        m_route.add_marker(CircleMarker((desti[2], desti[1]), 'red', 6))
        for st in path:
            if st != origen and st != desti:
                marker = CircleMarker((st.lon, st.lat), 'red', 6)
                m_route.add_marker(marker)

        n = len(path)
        for i in range(n-1):
            st1 = path[i]
            st2 = path[i+1]
            if st1 == origen:
                lon1 = st1[2]
                lat1 = st1[1]
            else:
                lon1 = st1.lon
                lat1 = st1.lat
            if st2 == desti:
                lon2 = st2[2]
                lat2 = st2[1]
            else:
                lon2 = st2.lon
                lat2 = st2.lat
            m_route.add_line(Line(((lon1, lat1), (lon2, lat2)), 'green', 4))

        return m_route.render()

        W.clear()


