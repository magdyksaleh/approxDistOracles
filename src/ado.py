import networkx as nx 
import numpy as np
import util
import collections



class approximateDistanceOracle(object):
    def __init__(self, G: nx.Graph, k: int):
        """
            G {nx.Graph} -- [description]
            k {int} -- [description]
        """
        self.G = G
        self.k = k
        self.paths = []
        self.distances = []
        self.n = len(self.G.nodes())
        #Clusters span of tree from A_i node 
        self.C = {}
        #bunches
        self.B = collections.defaultdict(list)

    def preprocess(self):
        """Implementing vanilla ADO
        
        Arguments:
            k {int} -- [description]
            G {nx.Graph} -- [description]
        """
        #Generate A's 
        A = [[] for i in range(self.k)]
        prob = self.n**(-1/self.k) 
        print("retention prob: %.2f" % prob)
        for i in range(self.k):
            if i == 0: 
                A[i] = self.G.nodes()
            else: 
                A[i] = [j for j in A[i-1] if np.random.rand() <= prob]
        
        #for each A_i 
        # add new source node s with weight 0 from 
        # each node in A_i to s. Run shorted path from 
        # s to all v in O(m) to get distances

        for i, A_i in enumerate(reversed(A)):
            d, p = util.singleSourceSP(self.G, A_i)
            self.paths.append(p)
            self.distances.append(d)
            if i == 0: prev = A_i
            else:
                # update path args
                print(p)
                for node in p: 
                    if self.distances[i][node] == self.distances[i-1][node]:
                        self.paths[i][node] = self.paths[i-1][node]
                
                #all elements in A_i - A_(i+1)
                diff_As = [x for x in A_i if x not in prev]
                for node in diff_As:
                    d, p = nx.single_source_dijkstra(self.G, node)
                    self.C[node] = [
                        x for x in d
                            if d[x] < self.distances[i-1][x]
                    ]
                    for elem in self.C[node]:
                        self.B[elem].append(node)
                
    def query(self, u: int, v: int):
        w = u
        i = 0
        while (w not in self.B[u]):
            i += 1
            (u, v) = (v, u)
            w = self.paths[i][u]

        return self.distances[i][u] + self.distances[i][v]


######################################################
G = nx.Graph()
numNodes = 16
G.add_nodes_from([0, numNodes])
G.add_weighted_edges_from([(i-1, i, 1.0) for i in range(1, numNodes+1)])
ado = approximateDistanceOracle(G, 2)
ado.preprocess()
print(ado.query(1, 2))