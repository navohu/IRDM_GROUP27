import networkx as nx
import json
import pandas as pd
from scipy.sparse import csc_matrix
import numpy as np
import os

from index.post_indexing_step import PostIndexing

def create_graph():
    with open("index/pagerank/graph.json") as data_file:    
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
    col_names = [str(col) for col in adj_matrix]
    pages = list(adj_matrix) + list(adj_matrix.index)
    # Remove duplicates
    pages = list(set(pages))
    pages.sort()
    print 'Shape before padding:', adj_matrix.shape 

    for p in range(len(pages)):
        if p % 200 == 0:
            print 'Checking page', p, '/', len(pages)
        page = pages[p]
        if page not in adj_matrix.index:
            #print page, 'missing from rows'
            adj_matrix.loc[page] = np.zeros(len(list(adj_matrix)), dtype=np.uint8)

        if page not in adj_matrix:
            #print page, 'missing from cols'
            adj_matrix.insert(p, page, np.zeros(len(adj_matrix), dtype=np.int8))
    
    adj_matrix = adj_matrix.sort_index(axis=0)
    adj_matrix = adj_matrix.sort_index(axis=1)
    print 'Shape after padding:', adj_matrix.shape 
    print adj_matrix.head(3)
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
    M = csc_matrix(G, dtype=np.float)
    rsums = np.array(M.sum(1))[:,0]
    ri, ci = M.nonzero()
    M.data /= rsums[ri]

    # bool array of sink states
    sink = rsums==0
    # bool array of non-sink states
    non_sink = rsums!=0
    print sink

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)
    while np.sum(np.abs(r-ro)) > maxerr:
        print "Convergence: " + str(np.sum(np.abs(r-ro)))
        ro = r.copy()
        # calculate each pagerank at a time
        for i in xrange(0, n):
            # transition probabilities from incoming links
            incoming_links = np.array(M[:,i].todense())[:,0]
            #print 'page', i, 'has', sum(incoming_links), 'incoming links'
            # teleporting from sink states - do these get counted twice?
            sink_links = sink / float(n)
            #print 'page', i, 'has', sum(sink_links), 'sink links'
            # teleporting from elsewhere
            teleportation_links = non_sink / float(n)
            #print 'page', i, 'has', sum(teleportation_links), 'teleportation links'

            r[i] = ro.dot( incoming_links*s + sink_links*s + teleportation_links*(1-s) )

    # return normalized pagerank
    return r/sum(r)

def main():
    graph = create_graph()
    matrix_filename = 'index/pagerank/adj_matrix.csv'
    if os.path.isfile(matrix_filename):
        adj_matrix = pd.read_csv(matrix_filename, index_col=0)
    else:
        adj_matrix = getAdjacencyMatrix(graph)
        adj_matrix.to_csv(matrix_filename)



    '''adj_matrix_contents = adj_matrix.ix[1:]
                adj_matrix_contents.drop(adj_matrix.columns[[0]], axis=1, inplace=True)
                print adj_matrix.head(2)
                print adj_matrix_contents.head(2)'''
    #page_rank = pageRank(adj_matrix, s=0.80)
    pagerank = np.ones(adj_matrix.shape[0])
    pagerank /= adj_matrix.shape[0]
    PostIndexing().add_pageranks(zip(adj_matrix.index, pagerank))

    print pagerank

if __name__ == '__main__':
    main()
