from grid import get_grid2
import networkx as nx
import random
import math
import pygame
pygame.init()

g = get_grid2()


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


agents = [Agent(g) for _ in range(1000)]
for a in agents:
    print(a.get_pos())
screen_size = [820, 667]
screen = pygame.display.set_mode(screen_size)

map = pygame.image.load('assets/layout_small.png')
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(map, (0, 0))
    for agent in agents:
        # print(agent.pos)
        agent_pos = agent.get_pos()
        pos = int(agent_pos[0]*screen_size[0]), int(agent_pos[1]*screen_size[1])
        pygame.draw.circle(screen, (0, 0, 255), pos, 2)
        agent.step()

    clock.tick(30)
    pygame.display.flip()
    # print(clock.get_fps())


pygame.quit()
