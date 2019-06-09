import pandas as pd
import networkx as nx
from pandas import Dataframe
import staticmap
from haversine import haversine
from geopy.geocoders import Nominatim

url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')

def main ():

	G = nx.graph()







main ()