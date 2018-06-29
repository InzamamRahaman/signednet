import networkx as nx


def negative_neighbors(G, n):
    nbrs = G[n]
    neg_nbrs = filter(lambda x:  nbrs[x]['sign'] == -1, nbrs)
    return neg_nbrs

def positive_neighbors(G, n):
    nbrs = G[n]
    neg_nbrs = filter(lambda x: nbrs[x]['sign'] == 1, nbrs)
    return neg_nbrs

def signed_neighbors(G, n):
    nbrs = G[n]
    pos = []
    neg = []
    for v in nbrs:
        if G[n][v]['sign'] == 1:
            pos.append(v)
        else:
            neg.append(v)
    return pos, neg

def signed_degrees(G, n):
    nbrs = G[n]
    pos = 0
    neg = 0
    for v in nbrs:
        if G[n]['sign'] == -1:
            neg += 1
        else:
            pos += 1
    return pos, neg
