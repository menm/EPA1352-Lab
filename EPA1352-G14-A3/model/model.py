from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from networkx import Graph

from components import Source, Sink, SourceSink, Bridge, Link, Intersection
import pandas as pd
from collections import defaultdict
import networkx as nx


# ---------------------------------------------------------------
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

    # test with dummy data
    # file_name = '../data/dummy_data.csv'

    # roads data
    file_name = '../data/roads_data_processed_1503.csv'

    def __init__(self, seed=None, x_max=500, y_max=500, x_min=0, y_min=0):

        self.schedule = BaseScheduler(self)
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series())
        self.space = None
        self.sources = []
        self.sinks = []
        self.bridges = []

        self.generate_model()

    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv(self.file_name)

        # a list of names of roads to be generated
        roads = df.road.unique()

        # df for mesa
        df_objects_all = []
        for road in roads:
            # Select all the objects on a particular road in the original order as in the cvs
            df_objects_on_road = df[df['road'] == road]

            if not df_objects_on_road.empty:
                #print("not empty")
                df_objects_all.append(df_objects_on_road)

                """
                Set the path 
                1. get the series of object IDs on a given road in the cvs in the original order
                2. add the (straight) path to the path_ids_dict
                3. put the path in reversed order and reindex
                4. add the path to the path_ids_dict so that the vehicles can drive backwards too
                """
                path_ids = df_objects_on_road['id']
                path_ids.reset_index(inplace=True, drop=True)
                # print(path_ids)
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                self.path_ids_dict[path_ids[0], None] = path_ids

                # creates the reversed
                path_ids = path_ids[::-1]
                # print(path_ids)
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
        print(roads, "YO")
        #print(self.path_ids_dict)

        #print(df_objects_all)

        # ContinuousSpace from the Mesa package;
        # not to be confused with the SimpleContinuousModule visualization
        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        for i in df_objects_all:
            #print(type(i))
            for _, row in i.iterrows():  # index, row in ...

                # create agents according to model_type
                model_type = row['model_type'].strip()
                agent = None

                name = row['name']
                if pd.isna(name):
                    name = ""
                else:
                    name = name.strip()

                if model_type == 'source':
                    agent = Source(row['id'], self, row['length'], name, row['road'])
                    self.sources.append(agent.unique_id)
                elif model_type == 'sink':
                    agent = Sink(row['id'], self, row['length'], name, row['road'])
                    self.sinks.append(agent.unique_id)
                elif model_type == 'sourcesink':
                    agent = SourceSink(row['id'], self, row['length'], name, row['road'])
                elif model_type == 'bridge':
                    agent = Bridge(row['id'], self, row['length'], name, row['road'], row['condition'])
                    self.bridges.append(agent.unique_id)
                elif model_type == 'link':
                    agent = Link(row['id'], self, row['length'], name, row['road'])
                elif model_type == 'intersection':
                    if not row['id'] in self.schedule._agents:
                        agent = Intersection(row['id'], self, row['length'], name, row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)
        print("YAY", type(df_objects_all))
        print("WHAT", type(df))

        # The problem: changed name df in the previous part of code, otherwise df would be the last one in that whole df
        # and turned on the df_objects on road, because it is in the loop, otherwise it is set to the previous one, where it
        # only registers the last one, so you have to actually set it to df[df['road'] == road]

        roads = df.road.unique()
        print("?", roads)

        # df for mesa
        df_objects_all = []
        # df for network x
        all_id_pairs_and_weights = []
        all_nodes = set()

        for road in roads:
            #print("HELLO", road)

            # already exists
            df_objects_on_road = df[df['road'] == road]
            #print(df_objects_on_road)
            df_objects_on_road.reset_index(inplace=True, drop=True)
            # print(df_objects_on_road)
            path_length_list = []
            id_list = []
            road_pair_list = []
            startindex = 0
            partial_path_length = 0

            # all except the last are empty!!!??
            print("HELLO ELIAS", df_objects_on_road)

            # something goes wrong here, only takes last road not all roads, becasue only the last one is not empty!!
            for index, row in df_objects_on_road.iterrows():
                # select all sourcesinks and intersections
                # it now only selects the last road Z013
                #print(df_objects_on_road)
                #print("rows: ", index)

                # select all sourcesinks and intersections
                if (row['model_type'] == "SourceSink") or (row['model_type'] == "Intersection"):
                    print("ja")
                # now only prints the first and last item?
                    # add ids to nodes list
                    id_list.append(row['id'])
                    #print(row['id'])
                    all_nodes.add(row['id'])
                    if startindex > 0:
                        path_length_list.append(partial_path_length)
                        partial_path_length = 0
                    startindex += 1

                # sum up the partial lengths
                partial_path_length += int(round(row['length']))

            for i in range(len(id_list) - 1):
                id_pair = (id_list[i], id_list[i + 1], path_length_list[i])
                #print(id_pair)
                road_pair_list.append(id_pair)
                all_id_pairs_and_weights.append(id_pair)

        all_nodes = list(all_nodes)
        #print(id_list)
        print("all nodes:", all_nodes)



        # generate networkX model here
        G = nx.Graph()
        G.add_nodes_from(all_nodes)
        print("num nodes: ",G.number_of_nodes())
        G.add_weighted_edges_from(all_id_pairs_and_weights)
        print("num edges: ",G.number_of_edges())


        # pos = nx.spring_layout(G)
        #
        # plt.figure(figsize=(15, 15))
        #
        # # version 2
        # nx.draw(G, pos, node_size=60, font_size=8)

        # specify edge labels explicitly
        # edge_labels = dict([((u, v,), d['weight'])
        #                     for u, v, d in G.edges(data=True)])

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

    # TODO
    def get_route(self, source):
        return self.get_straight_route(source)
        #return self.get_random_route(source)
        #return self.get_shortest_route(source)

    def get_straight_route(self, source):
        """
        pick up a straight route given an origin
        """
        return self.path_ids_dict[source, None]

    def get_shortest_route(self, source):
        """
        pick up the shortest route route given an origin and destination
        """
        shortest_route = []
        full_path_ids = []
        full_list = []

        # return dict of route
        while True:
            sink = self.random.choice(self.sinks)
            if sink is not source:
                break
            # if path does not exist yet, calculate shortest route
            if self.path_ids_dict.get([source, sink]) is None:
                # calc shortest route
                shortest_route = nx.shortest_path(G, source=source, target=sink, weight='weight')
                # find full mesa csv path_id_list
                # select all node pairs
                for previous, current in zip(shortest_route, shortest_route[1:]):
                    # if id of previous node is lower, step down els step up
                    if previous > current:
                        step = -1
                    else:
                        step = 1
                    # add ranges of id's between nodes (links)
                    full_list.append(list(range(previous, current, step)))

                # add last item - #Lidh changed something here
                full_list.append([shortest_route[-1]])
                # flatten list
                full_path_ids = [j for sub in full_list for j in sub]

                # write to mesa path_id_dict
                self.path_ids_dict[source, sink] = full_path_ids

        print("path ids's: ", self.path_ids_dict[source, sink])
        # if it already exists or is calculated, return path
        return self.path_ids_dict[source, sink]

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()

# EOF -----------------------------------------------------------
