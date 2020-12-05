from grid import get_grid
import networkx as nx
import random
import math
import pygame
pygame.init()
import pickle

image_size = [1770, 1440]
screen = pygame.display.set_mode(image_size)
map = pygame.image.load('assets/mask_big.png')

try:
    with open('points.pickle', 'rb') as f:
        positions = pickle.loads(f.read())
        positions = [(int(p[0]*image_size[0]), int(p[1]*image_size[1])) for p in positions]
except:
    positions = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            with open('points.pickle', 'wb') as f:
                positions = [(x/image_size[0], y/image_size[1]) for x, y in positions]
                f.write(pickle.dumps(positions))
                positions = []

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            positions.append(pos)
            print(f'Adding {pos}')
        
        if event.type == pygame.KEYUP and event.key==113:
            if positions:
                positions.pop()    

    screen.fill((255, 255, 255))
    screen.blit(map, (0, 0))

    for pos in positions:
        pygame.draw.circle(screen, (0, 0, 255), pos, 2)

    pygame.display.flip()


pygame.quit()
