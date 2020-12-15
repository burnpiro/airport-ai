import networkx as nx
import random
import math
import numpy as np

class Agent:
    def __init__(self, graph, pos=None) -> None:
        self.target = None
        self.graph = graph
        self.path = None
        self.speed = 0.001
        if pos:
            self.pos = pos
        else:
            self.pos = random.choice(list(graph.nodes))

    def step(self):
        while self.target is None:
            self.target = random.choice(list(self.graph.nodes))
            self.path = nx.algorithms.shortest_paths.generic.shortest_path(
                self.graph, source=self.pos, target=self.target)[1:]
            if len(self.path)==0:
                self.target = None

        next_pos = self.path[0]
        vec = (next_pos[0]-self.pos[0], next_pos[1]-self.pos[1])
        l = math.sqrt(vec[0]**2+vec[1]**2)
        if l <= self.speed:
            self.pos = next_pos
            self.path = self.path[1:]
            if len(self.path) == 0:
                self.target = None
        else:
            self.pos = (self.pos[0]+vec[0]/l*self.speed,
                        self.pos[1]+vec[1]/l*self.speed)
    
    def  get_pos(self):
        return tuple(x for x in self.pos)