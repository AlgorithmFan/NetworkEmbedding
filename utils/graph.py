#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:29
@Description: 
"""
from collections import defaultdict
from scipy.sparse import issparse


class Graph(defaultdict):
    """ Efficient basic implementation of nx 'graph' undirected graphs with self loops. """
    def __init__(self, data, is_directed=True):
        defaultdict.__init__(self, list)
        self.is_directed = is_directed
        self.from_numpy(data, is_directed)

    def from_numpy(self, data, is_directed=True):
        ''' transfer data into graph. '''
        if issparse(data):
            c_data = data.tocoo()
            for i,j, w in zip(c_data.row, c_data.col, c_data.data):
                self[i].append((j, w))
        else:
            raise Exception("Dense matrices not yet supported.")

        if not is_directed:
            self.make_undirected()

    def make_undirected(self):
        ''' transfer directed graph into undirected one. '''
        # remove weights
        for out_node in self.keys():
            in_nodes = [node for node, weight in self[out_node]]
            self[out_node] = in_nodes

        # add undirected edges
        for out_node in self.keys():
            for in_node in self[out_node]:
                self[in_node].append(out_node)

        # remove duplication and loops
        for out_node in self.keys():
            in_nodes = set(self[out_node])
            if out_node in in_nodes:
                in_nodes.remove(out_node)
            self[out_node] = list(in_nodes)



if __name__ == '__main__':
    from data_reader import DataReader
    from Sampler.random_walk import RandomWalk

    data = DataReader.load_matfile('../data/blogcatalog.mat', is_directed=True)
    graph = Graph(data, is_directed=False)

    random_walk = RandomWalk(num_paths=5, path_length=5, alpha=0.0)
    walks = list(random_walk.generate(graph))
    for walk in walks:
        path = [str(i) for i in walk]
        print ' - '.join(path)
