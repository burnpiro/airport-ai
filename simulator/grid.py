import pickle
import matplotlib.pyplot as plt
from imageio import imread, imsave
import numpy as np
import math
from scipy.spatial import Delaunay

import networkx as nx

GRID_SIZE = 5


def build_graph(grid_matrix):
    nodes = []
    edges = []
    pos = None
    for i in range(grid_matrix.shape[0]):
        for j in range(grid_matrix.shape[1]):
            if grid_matrix[i, j] > 0.5:
                pos = (i, j)
                nodes.append(pos)
    print(len(nodes))

    visited = set()
    current_nodes = [pos]

    while current_nodes:
        current = current_nodes.pop()

        if current in visited:
            continue

        visited.add(current)

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                next = (current[0]+x, current[1]+y)
                if next[0] < 0 or next[0] >= grid_matrix.shape[0]:
                    continue

                if next[1] < 0 or next[1] >= grid_matrix.shape[1]:
                    continue

                if next not in nodes:
                    continue

                edges.append((current, next, math.sqrt(x**2+y**2)))
                current_nodes.append(next)

    G = nx.Graph()
    G.add_nodes_from([(n[1]*GRID_SIZE, n[0]*GRID_SIZE) for n in nodes])
    G.add_weighted_edges_from(
        [(*[(n[1]*GRID_SIZE, n[0]*GRID_SIZE) for n in e[:2]], e[2]) for e in edges])
    return G


def get_grid() -> nx.Graph:
    mask = imread('assets/mask.png')[:, :, 0]
    mask = mask > 127

    grid_matrix = np.empty(
        (mask.shape[0]//GRID_SIZE, mask.shape[1]//GRID_SIZE))

    for i in range(grid_matrix.shape[0]):
        for j in range(grid_matrix.shape[1]):
            grid_matrix[i, j] = 1.0 if mask[i*GRID_SIZE:i *
                                            GRID_SIZE+GRID_SIZE, j*GRID_SIZE:j*GRID_SIZE+GRID_SIZE].sum() < 25 else 0.0
    G = build_graph(grid_matrix)
    return G


def get_grid2() -> nx.Graph:
    with open('points.pickle', 'rb') as f:
        all_points = np.array(pickle.loads(f.read()))

    G = nx.Graph()

    G.add_nodes_from(tuple(point) for point in all_points)

    mask = imread('assets/mask.png')[:, :, 0]

    tri = Delaunay(np.array(all_points))
    triangles_mask = np.zeros(tri.simplices.shape[0], dtype=np.bool)

    size = np.array(mask.shape)

    for i in range(triangles_mask.shape[0]):
        # print(tri.simplices[i])
        points = all_points[tri.simplices[i]]        
        center = np.sum(points, axis=0)/3
        
        y, x = np.round(center*size[::-1]).astype('int')
        triangles_mask[i] = mask[x, y] == 0

        for j in range(3):
            y, x = np.round((points[j] + points[j-1])/2*size[::-1]).astype('int')
            if mask[x, y] != 0:
                triangles_mask[i] = 0

        if triangles_mask[i] == 1:
            G.add_edges_from([
                (tuple(points[j]), tuple(points[j-1])) for j in range(3)
            ])
    components = list(nx.algorithms.components.connected_components(G))
    biggest = max([len(x) for x in components])
    for component in components:
        if len(component)< biggest:
            G.remove_nodes_from(component)


    # plt.imshow(mask, cmap='gray_r')
    # # plt.triplot(points[:, 0], points[:, 1], tri.simplices[triangles_mask])
    # for i in range(triangles_mask.shape[0]):
    #     if triangles_mask[i]:
    #         t = plt.Polygon(all_points[tri.simplices[i]], color='green')

    #         plt.gca().add_patch(t)

    # plt.triplot(all_points[:, 0]*size[1], all_points[:, 1]*size[0], tri.simplices[triangles_mask])

    # # plt.plot(points[:,0], points[:,1], 'o', linewidth=0.1)
    # nodes = np.array(G.nodes)
    # plt.scatter(nodes[:,0]*size[1], nodes[:,1]*size[0], c='red')

    # plt.show()

    return G
