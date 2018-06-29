import networkx as nx




def read_edgelist(path, comments="#", delimiter=None, create_using=None,
                  nodetype=None, data=True, encoding='utf-8'):
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
            sign = int(rest[0])
            if abs(sign) != 1:
                raise ValueError(f'{sign} is not a valid value for edge sign - should be either -1 or 1')
            data_dict = {'u': u, 'v': v, 'attr': {'sign': sign}}
            if data is not None:
                if len(rest) <= 1:
                    raise ValueError(f'data argument was not None, but there is no extra data on line #{i}')
                else:
                    for j, (name, typing) in enumerate(data):
                        data_dict['attr'][name] = typing(rest[j + 1])
            G.add_edge(**data_dict)
    return G





