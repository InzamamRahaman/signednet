import networkx as nx



def signed_in_neighbors(G, n):
    pos = []
    neg = []

    nbrs = None
    if nx.is_directed(G):
        nbrs = G.preds[n]
    else:
        nbrs = G[n]

    for v in nbrs:
        sign = G[v][n]['sign']
        if sign == 1:
            pos.append(v)
        else:
            neg.append(v)
    return pos, neg

def signed_out_neighbors(G, n):
    pos = []
    neg = []
    nbrs = None

    if nx.is_directed(G):
        nbrs = G.succ[n]
    else:
        nbrs = G[n]

    for v in nbrs:
        sign = G[v][n]['sign']
        if sign == 1:
            pos.append(v)
        else:
            neg.append(v)
    return pos, neg

def signed_neighbors(G, n):
    in_pos, in_neg = signed_in_neighbors(G, n)
    pos = in_pos
    neg = in_neg

    if nx.is_directed(G):
        out_pos, out_neg = signed_out_neighbors(G, n)

        pos.extend(out_pos)
        neg.extend(out_neg)

    return pos, neg

def negative_neighbors(G, n):
    pos, neg = signed_neighbors(G, n)
    return neg

def positive_neighbors(G, n):
    pos, neg = signed_neighbors(G, n)
    return pos

def signed_in_degrees(G, n):
    pos = 0
    neg = 0
    nbrs = None

    if nx.is_directed(G):
        nbrs = G.preds[n]
    else:
        nbrs = G[n]

    for v in nbrs:
        sign = G[v][n]['sign']
        if sign == 1:
            pos += 1
        else:
            neg += 1
    return pos, neg

def signed_out_degrees(G, n):
    pos = 0
    neg = 0
    nbrs = None

    if nx.is_directed(G):
        nbrs = G.succ[n]
    else:
        nbrs = G[n]

    for v in nbrs:
        sign = G[v][n]['sign']
        if sign == 1:
            pos += 1
        else:
            neg += 1
    return pos, neg

def signed_degrees(G, n):
    in_pos, in_neg = signed_in_degrees(G, n)
    pos = in_pos
    neg = in_neg
    if nx.is_directed(G):
        out_pos, out_neg = signed_out_degrees(G, n)
        pos += out_pos
        neg += out_neg
    return pos, neg


def signed_modularity(G, partition):
    pass

def frustration(G, partition):
    pass