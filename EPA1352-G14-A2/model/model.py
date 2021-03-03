from mesa import Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from components import Source, Sink, SourceSink, Bridge, Link, Vehicle
import pandas as pd
from collections import defaultdict


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


# function used for DataCollector during testing
def calculate_avg_driving_time(model):
    """
    Calculate average driving time of a single vehicle in ticks (=minutes)
    Averaged over all vehicles
    Only takes vehicles into account which have completed the
    full drive cycle (Source until Sink)

    """

    # start when cars have reached sink
    if model.total_removed_vehicles != 0:
        print(model.total_driving_time, model.total_removed_vehicles)
        # divide all cars driven minutes of cars which have completed full drive cyle
        # by total cars which have been removed
        average_total_driving_time = model.total_driving_time / model.total_removed_vehicles
        return average_total_driving_time
    else:
        return 0

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

        Since there is only one road in the Demo, the paths are added with the road info;
        when there is a more complex network layout, the paths need to be managed differently

    sources: list
        all sources in the network

    sinks: list
        all sinks in the network

    break_down_prob: list
        all break down probabilities in ints (0-100) in order [A,B,C,D]

    total_removed_vehicles: int
        counter of removed vehicles in system which have reached the sink

    total_driving_time: int
        number of ticks driven from source to sink added for all vehicles

    """

    step_time = 1
    def __init__(self, seed=None, x_max=500, y_max=500, x_min=0, y_min=0, break_down_prob = [0, 0, 0, 0]):
        self.schedule = BaseScheduler(self) #calls agent step by step in same order
        self.running = True
        self.path_ids_dict = defaultdict(lambda: pd.Series())
        self.space = None
        self.sources = []
        self.sinks = []
        self.generate_model()

        # new attributes
        self.break_down_prob = break_down_prob
        self.total_removed_vehicles = 0
        self.total_driving_time = 0

        # save average driving time in datacollector
        self.datacollector = DataCollector(model_reporters=({'average_total_driving_time': calculate_avg_driving_time}))


    def generate_model(self):
        """
        generate the simulation model according to the csv file component information

        Warning: the labels are the same as the csv column labels
        """

        df = pd.read_csv('../data/N1_infrastructure.csv') # reads in file and creates very basic simulation

        # a list of names of roads to be generated
        roads = ['N1']


        df_objects_all = []
        for road in roads:

            # Select all the objects on a particular road
            # following code was not needed, because road links are already ordered
            #   df_objects_on_road = df[df['road'] == road].sort_values(by=['id'])
            df_objects_on_road = df[df['road'] == road]

            if not df_objects_on_road.empty:
                df_objects_all.append(df_objects_on_road)

                # the object IDs on a given road
                path_ids = df_objects_on_road['id']
                # add the path to the path_ids_dict
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids
                # put the path in reversed order and reindex
                path_ids = path_ids[::-1]
                path_ids.reset_index(inplace=True, drop=True)
                # add the path to the path_ids_dict so that the vehicles can drive backwards too
                self.path_ids_dict[path_ids[0], path_ids.iloc[-1]] = path_ids

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

        for df in df_objects_all:
            for _, row in df.iterrows():    # index, row in ...
                # create agents according to model_type
                model_type = row['model_type']
                agent = None

                if model_type == 'source':
                    agent = Source(row['id'], self, row['length'], row['name'], row['road'])
                    self.sources.append(agent.unique_id)
                elif model_type == 'sink':
                    agent = Sink(row['id'], self, row['length'], row['name'], row['road'])
                    self.sinks.append(agent.unique_id)
                elif model_type == 'sourcesink':
                    agent = SourceSink(row['id'], self, row['length'], row['name'], row['road'])
                    self.sources.append(agent.unique_id)
                    self.sinks.append(agent.unique_id)
                elif model_type == 'bridge':
                    # parse break down probability for all bridges
                    agent = Bridge(row['id'], self, row['length'], row['name'], row['road'], row['condition'], self.break_down_prob)
                elif model_type == 'link':
                    agent = Link(row['id'], self, row['length'], row['name'], row['road'])

                if agent:
                    self.schedule.add(agent)
                    y = row['lat']
                    x = row['lon']
                    self.space.place_agent(agent, (x, y))
                    agent.pos = (x, y)

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

    def step(self):
        """
        Advance the simulation by one step.
        """
        self.schedule.step()
        self.datacollector.collect(self)

# EOF -----------------------------------------------------------
