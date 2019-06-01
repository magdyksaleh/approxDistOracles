import networkx as nx
import numpy as np

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

def build_Gs(G, n, k) :

    # Sample vertex set S
    S = []
    prob = n**(-1/k) 
    for node in G.nodes() :
        if np.random.rand() <= prob :
            S.append(node)

    d, p = singleSourceSP(G, S)
    
    # Construct E_S and then build G_S
    E_S = []
    for edge in G.edges() :
        weight = 1 if (G.get_edge_data(*edge) == {}) else G.get_edge_data(*edge)['weight']
        a, b = edge
        if weight < d[a] and weight < d[b] :
            E_S.append(edge)
    GS = nx.Graph()
    GS.add_nodes_from(G.nodes())
    GS.add_edges_from(E_S)
    return GS, S, distances, paths