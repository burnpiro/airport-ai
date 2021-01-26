from os import close
import pickle
# import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import polygon2mask
import json
import networkx as nx
from scipy.spatial import Delaunay
from collections import deque
from math import sqrt


def getTargetSize():
    with open('layout.json') as f:
        data = json.loads(f.read())
    return data['image-size']


class PathFinding:
    def __init__(self, mask) -> None:
        self.mask = mask

    def neighbors(self, node):
        ret = []
        n = node
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            new_node = n[0]+i, n[1]+j
            if self.mask[new_node] == 1:
                ret.append(new_node)
        return ret

    def bfs(self, dest):
        queue = deque([dest])
        visited = set([dest])
        paths = {dest: dest}

        while len(queue) > 0:
            v = queue[0]
            queue.popleft()

            for n in self.neighbors(v):
                if tuple(n) not in visited:
                    queue.append(n)
                    visited.add(n)
                    paths[n] = v

        return paths

    def dijkstra(self, dest, distances):
        max_distance_from_walls = max(distances.values())
        distance = {dest: 0}
        queue = set([dest])

        paths = {dest: dest}
        # visited = set([init_pos])

        while len(queue) > 0:
            v = min(queue, key=lambda x: distance[x])
            queue.discard(v)

            for n in self.neighbors(v):
                n = tuple(n)
                new_distance = distance[v] + sqrt((n[0]-v[0])**2+(n[1]-v[1])**2) - 0.01*(
                    distances[v] + max_distance_from_walls)
                if n not in distance or distance[n] > new_distance:
                    queue.add(n)
                    distance[n] = new_distance
                    paths[n] = v

        return paths


class Grid:
    def __init__(self) -> None:
        with open('layout.json') as f:
            data = json.loads(f.read())

        self.grid_size = (400, 300)

        contour = (np.asarray(data['contour'])).astype('int')
        size = (np.asarray(data['image-size'])).astype('int')

        self.entrance = (np.asarray((12482, 6260))/size * self.grid_size).astype('int')
        self.exit = (np.asarray((12006, 6260))/size * self.grid_size).astype('int')

        
        contour = contour/size * self.grid_size

        # self.mask = polygon2mask(self.grid_size, contour)
        self.mask = self.get_mask(data)
        self.goals = self.get_goals(data)
        self.goals['entrance'] = tuple(self.entrance)
        self.goals['exit'] = tuple(self.exit)
        self.gates = self.get_goals(data)

        self.paths = {}

        distances = self.get_distance_from_walls()

        # for i in range(self.mask.shape[0]):
        #     for j in range(self.mask.shape[1]):
        #         if self.mask[i, j]==1:

        pf = PathFinding(self.mask)

        for goal, point in self.goals.items():
            self.paths[goal] = pf.dijkstra(point, distances)

        path = self.paths['exit']
        self.mask = np.zeros_like(self.mask)
        for point in path:
            self.mask[point] = 1

        self.closest_cells = self.get_closest_cells()

        

    def get_mask(self, data):
        contour = (np.asarray(data['contour'])).astype('int')
        size = (np.asarray(data['image-size'])).astype('int')
        contour = contour/size * self.grid_size
        mask = polygon2mask(self.grid_size, contour)
        objects_mask = np.zeros_like(mask)
        objects = data['objects']
        objects_to_ignore = ['route']
        for name, object in objects.items():
            if name in objects_to_ignore:
                continue
            points = object['points']
            for polygon in points:
                polygon = polygon/size*self.grid_size
                m = polygon2mask(self.grid_size, polygon)
                objects_mask = np.logical_or(objects_mask, m)

        mask = np.logical_and(mask, np.logical_not(objects_mask))
        return mask

    def get_closest_cells(self):
        # closest_cells = {}
        init_pos = 0, 0
        for x in range(self.mask.shape[0]):
            for y in range(self.mask.shape[1]):
                if self.mask[x, y] == 1:
                    init_pos = x, y
                    break

        # closest_cells = {init_pos: {"cell": init_pos, "distance": 0}}

        def neighbors(node):
            ret = []
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 1 and j == 1:
                        continue

                    offset = [i, j]

                    ret.append((node[0]+offset[0], node[1]+offset[1]))
            return ret

        distance = {init_pos: 0}
        queue = set([init_pos])

        closest_cells = {init_pos: init_pos}
        # visited = set([init_pos])

        while len(queue) > 0:
            v = min(queue, key=lambda x: distance[x])
            queue.discard(v)

            for n in neighbors(v):
                if not self.inside_grid(n):
                    continue
                n = tuple(n)
                if n not in distance or distance[n] > distance[v] + sqrt((n[0]-v[0])**2+(n[1]-v[1])**2):
                    queue.add(n)
                    if self.mask[n] == 1:
                        distance[n] = 0
                        closest_cells[n] = n
                    else:
                        distance[n] = distance[v] + \
                            sqrt((n[0]-v[0])**2+(n[1]-v[1])**2)
                        closest_cells[n] = v if self.mask[v] == 1 else closest_cells[v]

        return closest_cells

    def get_distance_from_walls(self):
        # closest_cells = {}
        init_pos = 0, 0

        def neighbors(node):
            ret = []
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 1 and j == 1:
                        continue

                    offset = [i, j]

                    ret.append((node[0]+offset[0], node[1]+offset[1]))
            return ret

        distance = {init_pos: 0}
        queue = set([init_pos])

        while len(queue) > 0:
            v = min(queue, key=lambda x: distance[x])
            queue.discard(v)

            for n in neighbors(v):
                if not self.inside_grid(n):
                    continue
                n = tuple(n)
                if n not in distance or distance[n] > distance[v] + sqrt((n[0]-v[0])**2+(n[1]-v[1])**2):
                    queue.add(n)
                    if self.mask[n] == 0:
                        distance[n] = 0
                    else:
                        distance[n] = distance[v] + \
                            sqrt((n[0]-v[0])**2+(n[1]-v[1])**2)

        return distance

    def inside_grid(self, n):
        return n[0] >= 0 and n[0] < self.grid_size[0] and n[1] >= 0 and n[1] < self.grid_size[1]

    def direction_torwards_grid(self, pos):
        gridPos = self.grid_pos(pos)

        closest = self.closest_cells[gridPos]
        return closest-np.array(gridPos)

    def grid_pos(self, pos):
        return int(pos[0]+0.5), int(pos[1]+0.5)

    def pos_to_grid(self, pos):
        def neighbors(node):
            ret = []
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 1 and j == 1:
                        continue

                    offset = [i, j]

                    ret.append((node[0]+offset[0], node[1]+offset[1]))
            return ret

        # gridPos = np.round(pos).astype(np.int)
        gridPos = self.grid_pos(pos)
        if not self.inside_grid(gridPos):
            print(gridPos)
            queue = deque([gridPos])
            visited = set([gridPos])

            while len(queue) > 0:
                v = queue[0]
                queue.popleft()

                for n in neighbors(v):
                    if self.inside_grid(n):
                        return self.closest_cells[n], False

                    if tuple(n) not in visited:
                        queue.append(n)
                        visited.add(tuple(n))

        if self.mask[gridPos] == 0:
            return self.closest_cells[gridPos], False

        return gridPos, True

    def random(self):
        while True:
            x, y = np.random.uniform([0, 0], self.grid_size).astype(np.int)
            if self.mask[x, y] == 1:
                return x, y

    def get_goals(self, data):
        size = (np.asarray(data['image-size'])).astype('int')
        gates = data['gates']['points']
        ids = data['gates']['ids']

        goals = {}

        for gate, id in zip(gates, ids):
            goals[id]=(
                tuple(
                    (np.array(gate).mean(axis=0)/size*self.grid_size).astype('int')
                )
            )

        return goals
