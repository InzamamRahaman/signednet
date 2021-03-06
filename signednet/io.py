import networkx as nx
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold
import copy
import random


def write_edgelist(G, path, delimiter=',', write_extra=False, shuffle=True):
    lines = []
    fp = path 
    if type(path) == type('str'):
        fp = open(path, 'w')
    for (u, v, d) in G.edges(data=True):
        s = d['attr']['sign']
        arr = [u, v, s]
        if write_extra:
            attr = d['attr']
            for k, v in attr.items():
                if k != 'sign':
                    arr.append(v)
        arr = map(str, arr)
        # arr = np.array(list(map(str, arr)))
        # per_idx = np.arange(0, len(arr))
        # per_idx = np.random.permutation(per_idx)
        # print(len(arr))
        # print(arr.shape)
        # arr = arr[per_idx, :]
        line = delimiter.join(arr)
        lines.append(line)
    if shuffle:
        lines = np.array(lines)
        lines = np.random.permutation(lines)
    fp.write('\n'.join(lines))
    fp.close()



def from_adj_matrix(adj_matrix, start_with=1, 
    create_using=nx.DiGraph(), ignore_neutrals=False):
    G = create_using
    n = len(adj_matrix) #+ start_with
    for i in range(n):
        for j in range(n):
            score = adj_matrix[i][j] 
            sign = 0
            if score < 0.0:
                sign = -1
            elif score > 0.0:
                sign = 1 
            if (not ignore_neutrals and sign != 0) or ignore_neutrals:
                u = start_with + i
                v = start_with + j
                data_dict = {'sign': sign, 'attr':{'sign': sign, 'sweight':score}}
                G.add_edge(u, v, **data_dict)
    return G



def read_edgelist(path, comments="#", delimiter=',', create_using=None,
                  nodetype=None, data=None, encoding='utf-8'):
    if type(path) == str:
        with open(path, 'rb') as fp:
            lines = [line.decode(encoding) for line in fp]
            G = parse_edgelist(lines, comments=comments, nodetype=nodetype,
                               create_using=create_using, data=data, delimiter=delimiter)
    else:
        fp = path
        lines = [line.decode(encoding) for line in fp]
        G = parse_edgelist(lines, comments=comments, nodetype=nodetype,
                           create_using=create_using, data=data)
    return G


def process_k_fold_edgelist(path, comments='#', delimiter=',', create_using=None,
                    nodetype=None, data=None, encoding='utf-8', k=10):
    if type(path) == str:
        with open(path, 'rb') as fp:
            lines = []
            signs = []
            for line in fp:
                line = line.decode(encoding)
                d = line.strip().split(delimiter)
                sign = float(d[2])
                if sign != 0.0:
                    sign = -1 if sign < 0 else 1
                    lines.append(line)
                    signs.append(sign)
            #lines = [line.decode(encoding) for line in fp]
            lines = np.array(lines)
            signs = np.array(signs)
            kfold = StratifiedKFold(n_splits=k, shuffle=True)
            kfold.get_n_splits(lines, signs)
            for train_idx, test_idx in kfold.split(lines, signs):
                create_using_copy = copy.deepcopy(create_using)
                G_train = parse_edgelist(lines[train_idx], comments, nodetype, create_using,
                                         data, delimiter)
                G_test = parse_edgelist(lines[test_idx], comments, nodetype, create_using_copy,
                                         data, delimiter)
                yield G_train, G_test
    else:
        fp = path
        lines = []
        signs = []
        for line in fp:
            line = line.decode(encoding)
            d = line.strip().split(delimiter)
            sign = float(data[2])
            if sign != 0.0:
                sign = -1 if sign < 0 else 1
                lines.append(line)
                signs.append(sign)
        # lines = [line.decode(encoding) for line in fp]
        lines = np.array(lines)
        signs = np.array(signs)
        kfold = StratifiedKFold(n_splits=k, shuffle=True)
        kfold.get_n_splits(lines, signs)
        for train_idx, test_idx in kfold.split(lines, signs):
            create_using_copy = copy.deepcopy(create_using)
            #print('D',data)
            G_train = parse_edgelist(lines[train_idx], comments, nodetype, create_using,
                                     data, delimiter)
            #print('E',data)
            G_test = parse_edgelist(lines[test_idx], comments, nodetype, create_using_copy,
                                    data, delimiter)
            yield G_train, G_test
        # lines = [line.decode(encoding) for line in fp]
        # lines = np.array(lines)
        # kfold = KFold(n_splits=k, shuffle=True)
        # kfold.get_n_splits(lines)
        # for train_idx, test_idx in kfold.split(lines):
        #     G_train = parse_edgelist(lines[train_idx], comments, nodetype, create_using,
        #                              data, delimiter)
        #     G_test = parse_edgelist(lines[test_idx], comments, nodetype, create_using,
        #                             data, delimiter)
        #     yield G_train, G_test



def parse_edgelist(lines, comments='#', nodetype=int, create_using=None, data=None, delimiter=','):
    G = nx.Graph() if create_using is None else create_using
    for i, line in enumerate(lines):
        if line[0] != comments:
            u, v, *rest = line.split(delimiter)
            u = nodetype(u)
            v = nodetype(v)
            rest_len = len(rest)
            if rest_len == 0:
                raise ValueError('No sign found on line #{i}. Suggestion: Use NetworkX graph')
            weight = float(rest[0].strip())
            sign = -1 if weight < 0.0 else (1 if weight > 0.0 else 0)
            if sign != 0:
                if abs(sign) != 1:
                    raise ValueError(f'{sign} is not a valid value for edge sign - should be either -1 or 1')
                data_dict = {'u_of_edge': u, 'v_of_edge': v, 'sign': sign, 'attr': {'sign': sign, 'sweight': weight}}
                #print(data)
                if data is not None:
                    if len(rest) <= 1:
                        raise ValueError(f'data argument was not None, but there is no extra data on line #{i}')
                    else:
                        for j, (name, typing) in enumerate(data):
                            data_dict['attr'][name] = typing(rest[j + 1])
            G.add_edge(**data_dict)
    return G





