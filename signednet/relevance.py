import signednet.graph as graph

## Adapted from https://arxiv.org/abs/1710.07236

def signed_common_neighbors(G, u, v):
    pos_u = set(graph.positive_neighbors(G, u))
    neg_u = set(graph.negative_neighbors(G, u))

    pos_v = set(graph.positive_neighbors(G, v))
    neg_v = set(graph.negative_neighbors(G, v))

    agree = len(pos_u & pos_v) + len(neg_u & neg_v)
    disagree = len(pos_u & neg_v) + len(pos_v & neg_u)
    return agree - disagree

def signed_jaccard_index(G, u, v):

    # prevent repeated computation of neighborhood sets
    pos_u = set(graph.positive_neighbors(G, u))
    neg_u = set(graph.negative_neighbors(G, u))

    pos_v = set(graph.positive_neighbors(G, v))
    neg_v = set(graph.negative_neighbors(G, v))

    agree = len(pos_u & pos_v) + len(neg_u & neg_v)
    disagree = len(pos_u & neg_v) + len(pos_v & neg_u)
    scn = agree - disagree

    total = len(pos_u | pos_v | neg_u | neg_v)
    return scn / total
