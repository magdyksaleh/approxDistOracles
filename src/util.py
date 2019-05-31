import networkx as nx

@profile
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
