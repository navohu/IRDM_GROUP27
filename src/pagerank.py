import networkx as nx
import json
import pandas as pd
from scipy.sparse import csc_matrix
import numpy as np

def create_graph():
    with open("graph.json") as data_file:    
        data = json.load(data_file)

    graph = {}
    for obj in data:
        key = obj.keys()[0]
        values = obj.values()[0]
        values = []
        for value in obj.values()[0]:
            if "cs.ucl.ac.uk" in value:
                values.append(value)
        graph[key] = values
    return graph

def getAdjacencyMatrix(g):
    g = {k: [v.strip() for v in vs] for k, vs in g.items()}
    print "Producing adjacency matrix..."

    edges = [(a, b) for a, bs in g.items() for b in bs]

    df = pd.DataFrame(edges)

    adj_matrix = pd.crosstab(df[0], df[1])
    return adj_matrix

def pageRank(G, s = .85, maxerr = .001):
    """
    Computes the pagerank for each of the n states.
    Used in webpage ranking and text summarization using unweighted
    or weighted transitions respectively.
    Args
    ----------
    G: matrix representing state transitions
       Gij can be a boolean or non negative real number representing the
       transition weight from state i to j.
    Kwargs
    ----------
    s: probability of following a transition. 1-s probability of teleporting
       to another state. Defaults to 0.85
    maxerr: if the sum of pageranks between iterations is bellow this we will
            have converged. Defaults to 0.001

    https://gist.github.com/diogojc/1338222
    """
    print "Calculating PageRank..."
    n = G.shape[0]

    # transform G into markov matrix M
    M = csc_matrix(G,dtype=np.float)
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    M.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    while np.sum(np.abs(r-ro)) > maxerr:
        print "Convergence: " + str(np.sum(np.abs(r-ro)))
        ro = r.copy()
        # calculate each pagerank at a time
        for i in xrange(0,n):
            # inlinks of state i
            Ii = np.array(M[:,i].todense())[:,0]
            # account for sink states
            Si = sink / float(n)
            # account for teleportation to state i
            Ti = np.ones(n) / float(n)

            r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )

    # return normalized pagerank
    return r/sum(r)

def main():
    # graph = create_graph()
    print graph
# adj_matrix = getAdjacencyMatrix(graph)
# page_rank = pageRank(adj_matrix, s=0.86)

if __name__ == '__main__':
    main()