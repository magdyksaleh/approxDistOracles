import networkx as nx
from collections import defaultdict
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



def modifiedDijkstra(G: nx.Graph, A_i: list, A_i_next: list):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf")