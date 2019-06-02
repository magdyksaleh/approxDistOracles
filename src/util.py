import networkx as nx
import numpy as np
from collections import defaultdict
import tqdm
from heapq import *

def singleSourceSP(G: nx.Graph, A_i: list):
    """Return node: (dist, p(node)) for A_i

    Arguments:
        G {nx.Graph} -- [description]
        A_i {list} -- [description]
    """

    virtNodeId = len(G.nodes())
    G.add_node(virtNodeId)
    G.add_weighted_edges_from([(i, virtNodeId, 0) for i in A_i])
    distances, paths = nx.single_source_dijkstra(G, virtNodeId)
    G.remove_node(virtNodeId)


    path = {
            node: paths[node][1]
                    for node in paths if node != virtNodeId
    }

    return distances, path

def build_Gs(G, n, k, i=9.2) :

    np.random.seed(42)
    # Sample vertex set S
    prob = n**(-1/k)
    while True:
        S = [node for node in G.nodes() if np.random.rand() <= prob]

        if len(S) > n**(1-i/k):
            break

    d, p = singleSourceSP(G, S)
    # Construct E_S and then build G_S
    E_S = []
    for edge in tqdm.tqdm(G.edges()):
        weight = 1 if (G.get_edge_data(*edge) == {}) else G.get_edge_data(*edge)['weight']
        a, b = edge
        if weight <= d[a] or weight <= d[b] :
            E_S.append(edge)
    GS = nx.Graph()
    GS.add_nodes_from(G.nodes())
    GS.add_edges_from(E_S)
    return GS, S, d, p


def modifiedDijkstra(G: nx.Graph, sourceNode, distances):
    """
    Based on: https://gist.github.com/kachayev/5990802
    """
    seen  = set()
    frontier  = [(0,sourceNode,[])] # COST, NODE, PATH
    mins = {sourceNode: 0}
    distance = {}
    paths = {}

    while frontier:
        (cost,v1,path) = heappop(frontier)
        if v1 not in seen:
            seen.add(v1)
            path = [v1] + path
            for v2 in G.neighbors(v1):
                if v2 in seen: continue
                c = 1 if (G.get_edge_data(v1, v2) == {}) else G.get_edge_data(v1, v2)['weight']
                next = cost + c
                prev = mins.get(v2, None)

                if prev is None or next < distances[v2]:
                    mins[v2] = next
                    paths[v2] = path
                    heappush(frontier, (next, v2, path))

    return mins, paths
