import pandas as pd
import networkx as nx
from pandas import DataFrame
import staticmap
from haversine import haversine
from geopy.geocoders import Nominatim

url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
#for st in bicing.itertuples(): print(st.Index, st.lat, st.lon)

coord4 = (41.393480, 2.181555)
coord5 = (41.391075, 2.180223)
print (haversine(coord4, coord5))

def addressesTOcoordinates(addresses):
    '''
    Returns the two coordinates of two addresses of Barcelona
    in a single string separated by a comma. In case of failure, returns None.

    Examples:

    >>> addressesTOcoordinates('Jordi Girona, Plaça de Sant Jaume')
    ((41.3875495, 2.113918), (41.38264975, 2.17699121912479))
    >>> addressesTOcoordinates('Passeig de Gràcia 92, La Rambla 51')
    ((41.3952564, 2.1615724), (41.38082045, 2.17357087674997))
    >>> addressesTOcoordinates('Avinguda de Jordi Cortadella, Carrer de Jordi Petit')
    None
    >>> addressesTOcoordinates('foo')
    None
    >>> addressesTOcoordinates('foo, bar, lol')
    None
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

G = nx.Graph()
for st in bicing.itertuples():
    stop = (st.Index, st.lat, st.lon)
    G.add_node(stop)

print(G.number_of_nodes())
print(G.number_of_edges())

d = int(input("Distance: "))

for st1 in G:
    for st2 in G:
        if st1[0] != st2[0]:
            coord1 = (st1[1], st1[2])
            coord2 = (st2[1], st2[2])
            if haversine(coord1, coord2) <= d:
                G.add_edge(st1, st2)

print(G.number_of_nodes())
print(G.number_of_edges())


def main ():
    G = nx.graph()
    for st in bicing.itertuples():
        G.addNode(st.Index, st.lat, st.lon)
    print(G.number_of_nodes())
    print(G.number_of_edges())


main

