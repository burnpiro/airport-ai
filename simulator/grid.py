import pickle
# import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import polygon2mask
import json
import networkx as nx
from scipy.spatial import Delaunay
from collections import deque


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
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 1 and j == 1:
                    continue

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


class Grid:
    def __init__(self) -> None:
        with open('layout.json') as f:
            data = json.loads(f.read())

        contour = (np.asarray(data['contour'])).astype('int')
        size = (np.asarray(data['image-size'])).astype('int')

        self.grid_size = (400, 300)
        contour = contour/size * self.grid_size

        self.mask = polygon2mask(self.grid_size, contour)
        self.goals = self.get_goals(data)
        self.paths = {}

        # for i in range(self.mask.shape[0]):
        #     for j in range(self.mask.shape[1]):
        #         if self.mask[i, j]==1:


        pf = PathFinding(self.mask)

        for goal in self.goals:
            self.paths[goal] = pf.bfs(goal)

    def inside_grid(self, n):
        return n[0] >= 0 and n[0] < self.grid_size[0] and n[1] >= 0 and n[1] < self.grid_size[1]

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
        gridPos = int(pos[0]), int(pos[1])
        if not self.inside_grid(gridPos) or self.mask[gridPos] == 0:
            queue = deque([gridPos])
            visited = set([gridPos])

            while len(queue) > 0:
                v = queue[0]
                queue.popleft()

                for n in neighbors(v):
                    if self.inside_grid(n) and self.mask[tuple(n)] == 1:
                        return n, False

                    if tuple(n) not in visited:
                        queue.append(n)
                        visited.add(tuple(n))

        return gridPos, True

    def random(self):
        while True:
            x, y = np.random.uniform([0, 0], self.grid_size).astype(np.int)
            if self.mask[x, y] == 1:
                return x, y

    def get_goals(self, data):
        size = (np.asarray(data['image-size'])).astype('int')
        gates = data['gates']['points']

        goals = []

        for gate in gates:
            goals.append(
                tuple(
                    (np.array(gate).mean(axis=0)/size*self.grid_size).astype('int')
                )
            )

        return goals
