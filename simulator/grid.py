import pickle
import matplotlib.pyplot as plt
from imageio import imread, imsave
import numpy as np
from skimage.draw import polygon2mask
import json
import networkx as nx
import polytri


def get_grid() -> nx.Graph:
    with open('layout.json') as f:
        data = json.loads(f.read())

    contour = (np.asarray(data['contour'])/20).astype('int')
    size = (np.asarray(data['image-size'])/20).astype('int')

    points_to_triangulate = [(x/size[0], y/size[1]) for x, y in contour]

    mask = polygon2mask(size, contour)

    G = nx.Graph()

    try:
        for triangle in polytri.triangulate(points_to_triangulate):
            G.add_edges_from([
                (tuple(triangle[j]), tuple(triangle[j-1])) for j in range(3)
            ])
    except:
        pass

    components = list(nx.algorithms.components.connected_components(G))
    biggest = max([len(x) for x in components])
    for component in components:
        if len(component)< biggest:
            G.remove_nodes_from(component)

    # nodes = np.asarray(G.nodes)
    # plt.imshow(mask.T, cmap='gray')
    # plt.scatter(nodes[:, 0]*size[0], nodes[:, 1]*size[1], c='red')
    # plt.show()

    return G, mask
