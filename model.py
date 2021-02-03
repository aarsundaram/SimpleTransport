import sys
import mesa 
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
import networkx as nx
import matplotlib.pyplot as plt
from Bridge import Bridge
from Link import Link
from Source import Source
from Sink import Sink
from Vehicles import Truck
import os
import pandas as pd

path = os.getcwd()

# ---------------------------------------------------------------
# input: latitude and Longitude in Decimal Degrees (DD)
def set_lat_lon_bound(lat_min, lat_max, lon_min, lon_max, edge_ratio=0.02):
    # add edges (margins) to the bounding box
    lat_edge = (lat_max - lat_min) * edge_ratio
    lon_edge = (lon_max - lon_min) * edge_ratio
    x_max = lon_max + lon_edge
    y_max = lat_min - lat_edge
    x_min = lon_min - lon_edge
    y_min = lat_max + lat_edge
    return y_min, y_max, x_min, x_max


# 1 tick 1 min
class BangladeshModel(Model):

    def __init__(self, x_max=500, y_max=500, x_min=0, y_min=0):

        #global shortest 
        self.schedule = BaseScheduler(self)
        self.running = True

        df = pd.read_csv(path+'/data/simpleTransport.csv')
        self.G= nx.DiGraph()
        self.pos={}
        self.shortest = []
        self.truck_counter = 0 
        self.trucks_exited = 0 

        #roads = [
        #    'N1',
        #    'N2',
        #    'N3',
        #    'N4',
        #    'N5',
        #    'N6',
        #    'N7',
        #    'N8'
        #]

        #df_bridges_all = []
        #self.num_bridges = 0

        #for road in roads:
        #    df_bridges_on_road = df[df['road'] == road].sort_values(by=['km'])

        #    if not df_bridges_on_road.empty:
        #        df_bridges_all.append(df_bridges_on_road)
        #        self.num_bridges += len(df_bridges_on_road.index)

        # self.num_agents = len(df.index)

        #df = pd.concat(df_bridges_all)
        y_min, y_max, x_min, x_max = set_lat_lon_bound(
            df['lat'].min(),
            df['lat'].max(),
            df['lon'].min(),
            df['lon'].max(),
            0.05
        )

        self.space = ContinuousSpace(x_max, y_max, True, x_min, y_min)

        # def __init__(self, unique_id, model, LRP_m, LRP_name, length,
        #              condition, name='Unknown', road_name='Unknown')

        #for df in df_bridges_all:
        for index, row in df.iterrows():

            model_type = row['model_type']

            agent = None

            if model_type == 'source':
                agent = Source(index, self, row['km'] * 1000, row['length'],
                                row['name'], row['road'])
            elif model_type == 'sink':
                agent = Sink(index, self, row['km'] * 1000, row['length'],
                                row['name'], row['road'])
            elif model_type == 'bridge':
                agent = Bridge(index, self, row['km'] * 1000, row['length'],
                                row['name'], row['road'])
            elif model_type == 'link':
                agent = Link(index, self, row['km'] * 1000, row['length'] * 1000,
                                row['name'], row['road'])

            if agent:
                self.schedule.add(agent)
                #print(agent.name + 'has been added at model.py')
                y = row['lat']
                x = row['lon']
                self.space.place_agent(agent, (x, y))
                agent.pos = (x, y)

        
        agent_list=self.schedule.agents
        for agent in agent_list:
            self.G.add_node(agent.name, label=agent.name) #adding them as nodes in the order of creation
            self.pos[agent.name]= agent.pos 
            #print(agent.name)
            #adding edges: 

        for i in range(len(agent_list)):
            if i < len(agent_list)-1:
                self.G.add_edge(agent_list[i].name,agent_list[i+1].name)
                #print('adding edge between'+ agent_list[i].name + 'and' + agent_list[i+1].name)

        

 



    def step(self):
        #nx.draw(self.G,pos=self.pos, with_labels=True)
        #plt.show()
        self.shortest = nx.shortest_path(self.G, source='source', target='sink')
        print(self.shortest)
        print(self) 
        self.schedule.step()
        
     
samplemodel = BangladeshModel()
samplemodel.step()