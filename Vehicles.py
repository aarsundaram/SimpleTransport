import sys

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace

import pandas as pd


class Truck(Agent):
    """A simple truck agent"""
    #truck_flag = False
    go_to_next_flag = False
    print("printing the shortest path list inside vehicles.py")
    #print(shortest)
     
    def __init__(self, unique_id, model, location=(0,0), location_offset=0, componentlocation=None):
        super().__init__(unique_id, model)
        self.componentlocation = componentlocation  #this is the name of the Component on which it is on. 
        #self.next_location = next_location   
        self.location_offset = 0
        self.pos = location
        self.name = ''
        self.length = 1

    def move(self):
        #make the vehicle move every step from its current location to the one next in shortest path 
        print(self)
        print("at the move() of vehicles.py ")
        #current location:
        current_location = self.pos #the source should have given its position to the agent upon creation
        next_location= (0,0)
        next_location_object = self.model
        print("current location of" + str(self.unique_id) + "is" + str(current_location))
        print("self.model in move() of vehicles.py", str(self.model.model))
        shortestpath = self.model.model.shortest
        #next_location should be what comes next, in the shorttest path. 
        for i in range(len(shortestpath)):
            if i < len(shortestpath)-1:
                if current_location== shortestpath[i]:
                    next_location= shortestpath[i+1]
            else:
                self.model.model.trucks_exited+=1 
        for agents in self.model.model.schedule.agents:
            if next_location == agents.name:
                next_location_object = agents
        
        self.pos = next_location_object.pos
        print("new location of" + self.name + "is" + str(self.pos))
        self.model.space.place_agent(self,self.pos) 

    def step(self):
        print("step function triggered in Truck() ")
        self.move()