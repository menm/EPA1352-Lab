from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from components import Source, Sink, SourceSink, Bridge, Link, Intersection
import pandas as pd
from collections import defaultdict
import networkx as nx

# ---------------------------------------------------------------


def driving_time(model):
    """
    Function to collect the average driving time
    Driving times are collected in ticks which represent minutes
    """
    # If the list of driving times is not empty,
    # then take the driving time.
    # Otherwise this value will be 0.
    if len(model.driving_times) > 0:
        driving_times = sum(model.driving_times) / len(model.driving_times)
        return driving_times
    else:
        return 0

def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    """
    Set the HTML continuous space canvas bounding box (for visualization)
    give the min and max latitudes and Longitudes in Decimal Degrees (DD)

    Add white borders at edges (default 2%) of the bounding box
    """

    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio

    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# ---------------------------------------------------------------
class BangladeshModel(Model):
    """
    The main (top-level) simulation model

    One tick represents one minute; this can be changed
    but the distance calculation need to be adapted accordingly

    Class Attributes:
    -----------------
    step_time: int
        step_time = 1 # 1 step is 1 min

    path_ids_dict: defaultdict
        Key: (origin, destination)
        Value: the shortest path (Infra component IDs) from an origin to a destination

        Only straight paths in the Demo are added into the dict;
        when there is a more complex network layout, the paths need to be managed differently

    sources: list
        all sources in the network

    sinks: list
        all sinks in the network

    """

    step_time = 1

    #file_name = '../data/demo-4.csv'
    file_name = '../data/roads_data_processed_1503.csv'

    def __init__(self, scenario = 0, seed=None, x_max=500, y_max=500, x_min=0, y_min=0):

        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series())
        self.space = None
        self.sources = []
        self.sinks = []

        # Add driving times as a model variable to store
        # the driving times of the vehicles
        self.driving_times = []
        # Add scenarios as a model variable to store
        self.scenario = scenario

        self.generate_model()


    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv(self.file_name)

        # Read in the scenario csv
        self.scenarios = pd.read_csv( '../data/A3_scenarios.csv', sep = ";")

        # A list of names of roads to be generated
        # This list contains all the roads
        roads = df.road.unique()

        # A list of names of national roads N1 and N2, and its N-sideroads
        # roads = ["N1", "N2", "N102", "N104", "N105", "N204", "N207", "N208"]

        df_objects_all = []
        for road in roads:
            # Select all the objects on a particular road in the original order as in the cvs
            df_objects_on_road = df[df['road'] == road]

            if not df_objects_on_road.empty:
                df_objects_all.append(df_objects_on_road)

                """
                Set the path 
                1. get the serie of object IDs on a given road in the cvs in the original order
                2. add the (straight) path to the path_ids_dict
                3. put the path in reversed order and reindex
                4. add the path to the path_ids_dict so that the vehicles can drive backwards too
                """
                path_ids = df_objects_on_road['id']
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids
                path_ids = path_ids[::-1]
                path_ids.reset_index(inplace=True, drop=True)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids


        # put back to df with selected roads so that min and max and be easily calculated
        df = pd.concat(df_objects_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        # ContinuousSpace from the Mesa package;
        # not to be confused with the SimpleContinuousModule visualization
        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        for i in df_objects_all:
            for _, row in i.iterrows():  # index, row in ...

                # create agents according to model_type
                model_type = row['model_type'].strip()
                agent = None

                name = row['name']
                if pd.isna(name):
                    name = ""
                else:
                    name = name.strip()

                if model_type == 'Source':
                    agent = Source(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                elif model_type == 'Sink':
                    agent = Sink(row['id'], self, row['length'], name, row['road'])
                    self.sinks.append(agent.unique_id)
                elif model_type == 'SourceSink':
                    agent = SourceSink(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                    self.sinks.append(agent.unique_id)
                elif model_type == 'Bridge':
                    agent = Bridge(row['id'], self, row['length'], name, row['road'], row['condition'])
                elif model_type == 'Link':
                    agent = Link(row['id'], self, row['length'], name, row['road'])
                elif model_type == 'Intersection':
                    if not row['id'] in self.schedule._agents:
                        agent = Intersection(row['id'], self, row['length'], name, row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)

        # Define nodes and edges
        all_id_pairs_and_weights = []
        # The nodes are a set, since there are intersections,
        # which have the same ID
        all_nodes = set()

        # For every row, add the ID to the list containing the nodes
        # If the index is within the bound
        # Then add the current node, next node and the length inbetween them
        # as a tuple. Subsequently, add the tuple to the list containing
        # all the nodes and weights.
        for index, row in df.iterrows():
            all_nodes.add(row["id"])
            if index < df.shape[0] - 1:
                if df.road.iloc[index] == df.road.iloc[index + 1]:
                    id_pair = (df.id.iloc[index], df.id.iloc[index + 1], int(row['length']))
                    # weigh edges
                    all_id_pairs_and_weights.append(id_pair)

        # Build network in networkx
        # Global G to access the graph later on
        # for calculating the shortest path
        global G
        G = nx.Graph()
        G.add_nodes_from(all_nodes)
        G.add_weighted_edges_from(all_id_pairs_and_weights)
        # print("Number of nodes in network:", G.number_of_nodes())
        # print("Number of edges in network:",G.number_of_edges())
        # print("Network is connected:  ", nx.is_connected(G))

    def get_random_route(self, source):
        """
        pick up a random route given an origin
        """
        while True:
            # different source and sink
            sink = self.random.choice(self.sinks)
            if sink is not source:
                break
        return self.path_ids_dict[source, sink]

    def get_route(self, source):
        #return self.get_straight_route(source)
        return self.get_shortest_route(source)
        #return self.get_random_route(source)

    def get_straight_route(self, source):
        """
        pick up a straight route given an origin
        """
        return self.path_ids_dict[source, None]

    # Get the shortest route
    def get_shortest_route(self, source):
        # Every vehicle gets a random sink upon generation
        while True:
            # different source and sink
            sink = self.random.choice(self.sinks)
            if sink is not source:
                break

        # Check if route between source and sink already exists in path_id_dict
        if (source, sink) not in self.path_ids_dict.keys():
            # Calculate and assign shortest path to path_id_dict as pandas series
            shortest = nx.shortest_path(G, source=source, target=sink, weight='weight')
            self.path_ids_dict[source, sink] = pd.Series(shortest)

        return self.path_ids_dict[source, sink]

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()

# EOF -----------------------------------------------------------
