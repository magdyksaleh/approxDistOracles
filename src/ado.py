import networkx as nx 
import numpy as np


G = nx.Graph()
G.add_nodes_from([0, 10000])
G.add_edges_from([(0, i) for i in range(1, 10000) if i%2 == 0])

def approximateDistance(k: int, G: nx.Graph):
    """Implementing vanilla ADO
    
    Arguments:
        k {int} -- [description]
        G {nx.Graph} -- [description]
    """

    A0 = list(G.nodes())
    A = A0
    n = len(A0)

    for i in range(k):
        A = [i for i in A if np.random.rand() <= n**(-1/k)]
    
    print(A)

approximateDistance(1, G)