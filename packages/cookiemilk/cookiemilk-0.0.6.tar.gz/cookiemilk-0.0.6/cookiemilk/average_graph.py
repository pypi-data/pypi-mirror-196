#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .cmap2graph import *
import networkx as nx
from heapq import nlargest


def average_graph(
        data,
        keyterms,
        pfnet=True,
        max=1,
        min=0.1,
        r=np.inf,
        n_core=None
):

    # Step 1: obtain matrix data. For each graph, convert data into an n*n similarity matrix (n = number of the given
    # keyterms) with 1 = 'connected' and 0 = 'unconnected', and then save in 'all_m'
    all_m = []
    for x in range(0, len(data)):
        m = [[0 for i in range(len(keyterms))] for j in range(len(keyterms))]  # an n*n zero matrix

        for pair in data[x].edges:  # add edges
            i = keyterms.index(pair[0])
            j = keyterms.index(pair[1])
            m[i][j] = 1
            m[j][i] = 1

        all_m.append(m)

    # Step 2: generate an average matrix
    average_m = np.array([[0 for i in range(len(keyterms))] for j in range(len(keyterms))])  # an n*n zero matrix
    for i in range(0, len(all_m)):
        average_m = average_m + np.array(all_m[i])
    average_m = average_m/len(all_m)

    # Step 3: define a NetworkX graph, calculate PFNet if necessary
    if not pfnet:
        average_ks = nx.Graph()
        average_ks.add_nodes_from(keyterms)
        pairs = []
        for i in range(0, len(average_m)):
            for j in range(0, len(average_m)):
                if i != j:
                    pairs.append([keyterms[i], keyterms[j], average_m[i, j]])
        average_ks.add_weighted_edges_from(pairs)
    else:
        average_ks = cmap2graph(file=average_m, data_type='array', keyterms=keyterms,
                                  read_from_file=False, pfnet=True, max=max, min=min, r=r)

    # Step 4: remove non-core terms and related links if necessary
    if n_core:
        degree = dict(nx.degree_centrality(average_ks))
        core = nlargest(n_core, degree, key=degree.get)

        for pair in list(average_ks.edges):  # remove links
            if pair[0] not in core or pair[1] not in core:
                average_ks.remove_edge(pair[0], pair[1])
        for term in keyterms:
            if term not in core:
                average_ks.remove_node(term)

    print('an average graph containing {} terms is generated successfully'.format(len(average_ks.nodes)))

    return average_ks
