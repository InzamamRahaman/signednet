import networkx as nx


def negative_neighbors(G, n):
    nbrs = G[n]
    neg_nbrs = filter(lambda x:  nbrs[x]['sign'] == -1, nbrs)
    return neg_nbrs

def positive_neighbors(G, n):
    nbrs = G[n]
    neg_nbrs = filter(lambda x: nbrs[x]['sign'] == -1, nbrs)
    return neg_nbrs
