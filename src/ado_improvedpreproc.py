import networkx as nx 
import numpy as np
import math
import util
import tqdm
import collections

from ado import ApproximateDistanceOracle

class ApproximateDistanceOracleImprovedPreprocess(object):
    def __init__(self, G: nx.Graph, k: int, fasterQuery=False):
        """
            G {nx.Graph} -- [description]
            k {int} -- [description]
        """
        self.G = G
        self.k = k
        self.paths = []
        self.distances = []

        self.i = 8.92 # Should work for k = 1 to k = 105
        self.kprime = math.floor( (k + 3*(math.ceil(k/(self.i + 1)) - 1))/(6*math.ceil(k/(self.i+1)) - 3)) #don't hate the player hate the paper 
        self.kappa = math.ceil(k/(self.i+1)) 
        self.fasterQuery = fasterQuery
        self.n = len(self.G.nodes())
        #Clusters span of tree from A_i node 
        self.C = {}

        # Restricted vertex set, some init parameter should specify whether we use this
        self.S = []

    def preprocess(self):
        """Implementing vanilla ADO
        
        Arguments:
            k {int} -- [description]
            G {nx.Graph} -- [description]
        """

        #Generate A's 

        self.Gs, self.S, self.distances, self.paths = util.build_Gs(self.G, self.n, self.k)
        
        H = nx.algorithms.sparsifiers.spanner(self.G, 2*self.kprime + 1,'weight')
        
        self.GSOracle = ApproximateDistanceOracle(self.Gs, self.k, fasterQuery=True)
        self.restrictedOracle = ApproximateDistanceOracle(H, self.kappa, restricted=True, S=self.S)
        
        self.GSOracle.preprocess()
        self.restrictedOracle.preprocess()

    def query(self, u: int, v: int):
        d1 = self.GSOracle.query(u, v)
        d2 = self.distances[u] + \
             self.restrictedOracle.query(self.paths[u], self.paths[v]) + \
             self.distances[v]
        
        return min(d1, d2)

######################################################



# ado_approx_10 = ApproximateDistanceOracleImprovedPreprocess(G, 10)
# ado_approx_10.preprocess()


G = nx.fast_gnp_random_graph(200, 0.3)
for (u, v) in G.edges():
    G.edges[u,v]['weight'] = 1 #np.random.randint(0,10)


k = int(np.floor(np.log(len(G))))
ado_approx_k = ApproximateDistanceOracleImprovedPreprocess(G, 16)
# ado_approx_k = ApproximateDistanceOracleImprovedPreprocess(G, 1)
ado_approx_k.preprocess()

r_k = []
for i in tqdm.tqdm(range(30)):
    u = np.random.randint(0, len(G.nodes())-1)
    v = np.random.randint(0, len(G.nodes())-1)
    if (u == v): continue
    print("node1: ", u, "node2: ", v,  "dist: ", ado_approx_k.query(u, v))
