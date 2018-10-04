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
        #print(G[v][n]['attr'])
        sign = G[v][n]['attr']['sign']
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
        sign = G[n][v]['attr']['sign']
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
        sign = G[v][n]['attr']['sign']
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
        sign = G[n][v]['attr']['sign']
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
    raise NotImplementedError('Modularity needs to be implemented')

def adj_entry(G, i, j):
    return G[i][j]['attr']['sign']

def abs_adj_entry(G, i, j):
    return abs(adj_entry(G, i, j))

def reverse_partition(partition):
    d = {}
    for c, nodes in partition.items():
        for node in nodes:
            d[node] = c
    return d

def dirac_delta(i, j):
    return (1 if i == j else 0)

def _community_dirac_delta(G, i, j, reveresed_part):
    ci = reveresed_part[i]
    cj = reveresed_part[j]
    return dirac_delta(ci, cj)

def frustration(G, partition):
    # taken from  https://www.researchgate.net/publication/318591280
    reversed_part = reverse_partition(partition)
    p1 = 0
    p2 = 0

    for i in G.nodes():
        for j in G.nodes():
            if i != j:
                a = abs_adj_entry(G, i, j)
                b = adj_entry(G, i, j)
                numer1 = a - b
                numer2 = a + b
                denom = 2
                frac1 = (numer1 / denom) * _community_dirac_delta(G, i, j, reversed_part)
                frac2 = (numer2 / denom) * (1 - _community_dirac_delta(G, i, j, reversed_part))
                p1 += frac1
                p2 += frac2
    return (p1 + p2)