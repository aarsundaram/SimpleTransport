import sys

from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import ContinuousSpace
from Vehicles import Truck
import pandas as pd


class Source(Agent):
    """A simple bridge agent"""
    truck_generated_flag = False
    truck_counter = 0

    def __init__(self, unique_id, model, LRP_m, length,
                 name='Unknown', road_name='Unknown'):
        super().__init__(unique_id, model)
        self.name = name
        self.LRP_m = LRP_m  # in meters
        self.length = length  # in meters
        self.road_name = road_name

        #get the next component in line:


    def generate_truck(self):
        #try:
                                                                          # changed from self.location to self.pos
        agent = Truck('Truck' + str(self.model.truck_counter), self, self.pos, componentlocation=self.name)
                                                                                                    #giving the name of the current component.
        if agent:
            #self.model.schedule.add(agent)  #is this necessary? 
            self.model.truck_counter += 1
            self.truck_generated_flag = True
            self.model.space.place_agent(agent, self.pos) #self.model , because source has no "space" functionality
            agent.pos = self.pos #location of the source. 
                                # this is what i need to update, in move() of vehicles 

            #agent.location=self.location   # giving current location to location of source 
            #agent.location_offset= self.location_offset #giving a static location of origin so that 
                                                        # we are able to track how far it is from start
            agent.step()
            print("moving a truck")

            agent.go_to_next_flag = True   #if this is true for the truck, the next source will check
                                            # for all the vehicles in source 1 which have go_to_next_flag = True 
                                            # and increase its counter by that number 
                                            # And the counter of trucks for Source 1 reduces by that number. 



    #except Exception as e:
    #    print("Oops!", e.__class__, "occurred in source.")

    def step(self):
    
        if self.model.schedule.steps % 2 == 0:
            self.generate_truck()
        else:
            self.truck_generated_flag = False