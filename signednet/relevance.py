import signednet.graph as graph
import networkx as nx

## Adapted from https://arxiv.org/abs/1710.07236


def relevance_over_graph(method, **kwargs):
    ebunch = kwargs.get('ebunch', None)
    G = kwargs.get('G', None)
    if G is None:
        raise ValueError('G cannot be None')
    if ebunch is None:
        ebunch = nx.non_edges(G)

    arg_dict = {k:v for k,v in kwargs.items() if k != 'ebunch'}
    for u, v in ebunch:
        arg_dict['u'] = u
        arg_dict['v'] = v
        ans = method(**arg_dict)
        yield ans



def signed_common_neighbors_pair(G, u, v):
    pos_u, neg_u = graph.signed_neighbors(G, u)
    pos_u = set(pos_u)
    neg_u = set(neg_u)

    pos_v, neg_v = graph.signed_neighbors(G, v)
    pos_v = set(pos_v)
    neg_v = set(neg_v)


    agree = len(pos_u & pos_v) + len(neg_u & neg_v)
    disagree = len(pos_u & neg_v) + len(pos_v & neg_u)
    return agree - disagree

def signed_common_neighbors(G, ebunch=None):
    if ebunch is None:
        ebunch = nx.non_edges(G)
    return ((u, v, signed_common_neighbors_pair(G, u, v)) for u, v in ebunch)




def signed_jaccard_index_pair(G, u, v):

    # prevent repeated computation of neighborhood sets
    pos_u, neg_u = graph.signed_neighbors(G, u)
    pos_u = set(pos_u)
    neg_u = set(neg_u)

    pos_v, neg_v = graph.signed_neighbors(G, v)
    pos_v = set(pos_v)
    neg_v = set(neg_v)

    agree = len(pos_u & pos_v) + len(neg_u & neg_v)
    disagree = len(pos_u & neg_v) + len(pos_v & neg_u)
    scn = agree - disagree

    total = len(pos_u | pos_v | neg_u | neg_v)
    return scn / total


def signed_jaccard_index(G, ebunch=None):
    if ebunch is None:
        ebunch = nx.non_edges(G)
    return ((u, v, signed_jaccard_index_pair(G, u, v)) for u, v in ebunch)


def signed_preferential_attachment_pair(G, u, v, f=max):
    d_pos_u, d_neg_u = graph.signed_degrees(G, u)
    d_pos_v, d_neg_v = graph.signed_degrees(G, v)

    upa_pos = d_pos_u * d_pos_v
    upa_neg = d_neg_u * d_neg_v

    diff = upa_pos - upa_neg
    sign = 1 if diff >= 0 else -1
    factor = f(upa_pos, upa_neg)

    return sign * factor


def signed_preferential_attachment(G, ebunch=None, f=max):
    if ebunch is None:
        ebunch = nx.non_edges(G)
    return ((u, v, signed_preferential_attachment_pair(G, u, v, f=f)) for u, v in ebunch)