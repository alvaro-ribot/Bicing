import pandas as pd
import networkx as nx
from pandas import DataFrame
from staticmap import StaticMap, Line, CircleMarker
from haversine import haversine
from geopy.geocoders import Nominatim


G = nx.Graph()


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


def geometric_graph(distance):
    G.clear()

    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')

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



def get_nodes():
    return G.number_of_nodes()

def get_edges():
    return G.number_of_edges()

def connex_components():
    return len(list(nx.connected_components(G)))

def plot_graph():
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
    G = nx.Graph()
    for st in bicing.itertuples():
        stop = (st.Index, st.lat, st.lon)
        G.add_node(stop)

    print(G.number_of_nodes())
    print(G.number_of_edges())

    d = 100 

    for st1 in G:
        for st2 in G:
            if st1[0] != st2[0]:
                coord1 = (st1[1], st1[2])
                coord2 = (st2[1], st2[2])
                if haversine(coord1, coord2)*1000 <= d:
                    G.add_edge(st1, st2)

    print(G.number_of_nodes())
    print(G.number_of_edges())

    l = list(nx.connected_components(G))
    '''
    for m in l :
        print(m)
        print('...')
        print('...')
    '''
    print(len(l))
    '''
    m = StaticMap(300, 400, 10)
    m.add_line(Line(((13.4, 52.5), (2.3, 48.9)), 'blue', 3))
    image = m.render()
    image.save('map.png')
    '''

    route(G, 'Pau Gargallo 1, PL. Lesseps', d)

    m_bcn = StaticMap(600, 600)
    for st in G:
        marker = CircleMarker((st[2], st[1]), 'red', 2)
        m_bcn.add_marker(marker)

    #l = list(G.edges())
    for e in G.edges():
        st1 = e[0];
        st2 = e[1];
        line = Line(((st1[2], st1[1]), (st2[2], st2[1])), 'blue', 2)
        m_bcn.add_line(line)


    image = m_bcn.render()
    image.save('bicing.png')


geometric_graph(1000)


route(G, 'Pau Gargallo 1, PL. Lesseps', 1000)
geometric_graph(500)
plot_graph()


