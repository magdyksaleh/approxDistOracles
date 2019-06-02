import networkx as nx 
import numpy as np
import util
import collections
import tqdm 

class ApproximateDistanceOracle(object):
    def __init__(self, G: nx.Graph, k: int, restricted=False, S=[], fasterQuery=False):
        """
            G {nx.Graph} -- [description]
            k {int} -- [description]
            restricted -- restriced oracle or not
            S -- vertex list if needed
        """
        self.G = G
        self.k = k
        self.restricted = restricted
        self.fasterQuery=fasterQuery

        self.paths = []
        self.distances = []
        self.n = len(self.G.nodes())
        #Clusters span of tree from A_i node 
        self.C = {}
        #bunches
        self.B = collections.defaultdict(list)
        self.B_distances = {}

    def preprocess(self):
        """Implementing vanilla ADO
        
        Arguments:
            k {int} -- [description]
            G {nx.Graph} -- [description]
        """
        #Generate A's 
        print(self.k)

        A = [[] for i in range(self.k+1)]

        prob = self.n**(-1/self.k) 
        for i in range(self.k+1):
            if i == 0: 
                A[i] = self.G.nodes()
            elif i == self.k: continue
            else: 
                A[i] = [j for j in A[i-1] if np.random.rand() <= prob]
                
        #for each A_i 
        # add new source node s with weight 0 from 
        # each node in A_i to s. Run shorted path from 
        # s to all v in O(m) to get distances

        self.distances.append({
            node: float('inf') for node in self.G.nodes()
        })
        
        self.paths.append({
            node: node for node in self.G.nodes()
        })

        prev = A[-1] #start at A_k

        for i, A_i in tqdm.tqdm(enumerate(list(reversed(A)))):
            if i == 0: continue
            d, p = util.singleSourceSP(self.G, A_i)
            self.paths.append(p)
            self.distances.append(d)
            for node in p: 
                if node not in self.distances[i]:
                    print("i: ", i, " - node: ", node)
                    import pdb; pdb.set_trace()

                if self.distances[i][node] == self.distances[i-1][node]:
                    self.paths[i][node] = self.paths[i-1][node]

            #all elements in A_i - A_(i+1)
            diff_As = [x for x in A_i if x not in prev]
            for w in diff_As:
                d, p = nx.single_source_dijkstra(self.G, w)
                # print(d)
                # print(self.distances[i-1])
                # print([(x, d[x]) for x in d if d[x] < self.distances[i-1][x]])
                # break
                self.C[w] = [
                    x for x in d
                        if d[x] < self.distances[i-1][x]
                ]
                
                for v in self.C[w]:
                    if self.restricted and v not in self.S :
                        continue
                    self.B[v].append(w)
                    self.B_distances[(v, w)] = d[v]
            prev = A_i
                
        self.distances.reverse()
        self.paths.reverse()

    def query(self, u: int, v: int, fasterQuery=False):
        if self.fasterQuery :
            return self.bdistk(u, v, 0, k)
        w = u
        i = 0
        while (w not in self.B[v]):
            i += 1
            (u, v) = (v, u)
            w = self.paths[i][u]
        return self.distances[i][u] + self.B_distances[(v, w)]

    def distk(self, u: int, v: int, i: int) :
        w = u
        while (w not in self.B[v]):
            i += 1
            (u, v) = (v, u)
            w = self.paths[i][u]
        return self.distances[i][u] + self.B_distances[(v, w)]


    def bdistk(self, u: int, v: int, i1: int, i2: int) :
        if i2 - i1 <= np.log2(self.k) :
            return self.distk(u, v, i1)

        # Find middle even index
        midIndex = (i1 + i2)//2
        midIndex = midIndex + 1 if midIndex % 2 == 1 else midIndex

        bestj = -1
        closestDist = -float('inf')
        for j in range(i1, midIndex - 1) : # Won't this not work if i -2 is too small? Nope, because of base case
            deltaJu = self.distances[j+2][u] - self.distances[j][u]
            if deltaJu < closestDist :
                closestDist = deltaJu
                bestj = j

        if self.paths[bestj][u] not in self.B[v] \
            and self.paths[bestj + 1][u] not in self.B[u] :
                return self.bdistk(u, v, midIndex, i2)
        else :
            return self.bdistk(u, v, midIndex, j)

######################################################

G = nx.fast_gnp_random_graph(200, 0.3)
ado_approx_10 = ApproximateDistanceOracle(G, 10, False, []) # Ignore last two arguments
ado_approx_10.preprocess()

k = int(np.floor(np.log(len(G))))

ado_approx_k = ApproximateDistanceOracle(G, k, fasterQuery=True)
ado_approx_k.preprocess()



r_k = []
for i in tqdm.tqdm(range(30)):
    u = np.random.randint(0, len(G.nodes())-1)
    v = np.random.randint(0, len(G.nodes())-1)
    r_k.append(ado_approx_k.query(u, v))
