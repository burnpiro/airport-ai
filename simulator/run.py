import networkx as nx
import random
import math
import numpy as np
import pygame
from Simulator import Simulation
from skimage.transform import resize
from imageio import imsave
pygame.init()

# g = Grid()
# mask = g.mask


# class Agent:
#     def __init__(self, grid, pos=None) -> None:
#         self.target = None
#         self.path = None
#         self.speed = 1
#         self.grid = grid
#         if pos:
#             self.pos = pos
#         else:
#             self.pos = self.grid.random()

#     def step(self):
#         while self.target is None:
#             self.target = random.choice(self.grid.goals)
#             self.path = self.grid.paths[tuple(self.target)]
#             # print(self.path)
#             if len(self.path)==0:
#                 self.target = None
#         # try:
#         grid_pos = self.grid.pos_to_grid(self.pos)
#         next_pos = self.path[tuple(grid_pos)]
#         vec = np.array([next_pos[0]-self.pos[0], next_pos[1]-self.pos[1]])*self.speed
#         self.pos += vec
#         if grid_pos==self.target:
#             self.target = None
    
#     def  get_pos(self):
#         return (self.pos[0]/self.grid.grid_size[0], self.pos[1]/self.grid.grid_size[1])


# agents = [Agent(g) for _ in range(1000)]
# for a in agents:
#     print(a.get_pos())
sim = Simulation()
mask = sim.mask
scale = 3
screen_size = tuple(x*scale for x in mask.shape)
screen = pygame.display.set_mode(screen_size)
imsave('mask.png', mask*1.0)
# map = pygame.image.load('assets/layout_small.png')
map = pygame.surfarray.make_surface(resize(mask, screen_size)*255)

clock = pygame.time.Clock()
fps = []
running = True
while running:
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(map, (0, 0))
    
    for agent in sim.agents:
        # print(tuple([int(x) for x in agent.pos]))
        pygame.draw.circle(screen, (0, 0, 255), tuple([int(x*scale) for x in agent.pos]), 2)
        # if agent.target:
        #     pygame.draw.circle(screen, (255, 0, 0), tuple([int(x) for x in agent.target]), 2)

    sim.step()
    # mouse_pos = pygame.mouse.get_pos()
    # print(sim.grid.direction_torwards_grid(mouse_pos))
    # direction = sim.grid.direction_torwards_grid(mouse_pos)

    # pygame.draw.circle(screen, (255, 0, 0), (mouse_pos[0]+direction[0], mouse_pos[1]+direction[1]), 2)

    clock.tick(300)
    pygame.display.flip()

    # print(clock.get_fps())
    fps.append(clock.get_fps())
    if len(fps)>40:
        print(np.mean(fps))
        fps.clear()


pygame.quit()
