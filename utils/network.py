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


class Network(object):
    def __init__(self, is_directed=True):
        self.is_directed = is_directed
        self.graph = defaultdict(defaultdict)
        self.nodes = defaultdict()

    def add_data(self, data):
        '''

        '''
        assert(len(data) > 0)
        assert(len(data[0]) > 1)
        if len(data[0]) == 2:
            for i, j in data:
                self.add_edge(from_node=i, to_node=j)
        else:
            for i, j, w in data:
                self.add_edge(from_node=i, to_node=j, weight=w)

    def add_edge(self, from_node, from_node_id=None, to_node=None, to_node_id=None, weight=1):
        '''
        Add edges.
        ---------------------------------------------------
        Parameters:
            from_node:
            from_node_id:
            to_node:
            to_node_id:
            weight:
        '''
        assert(to_node is not None)
        if from_node_id is None:
            from_node_id = self.nodes.get(from_node, len(self.nodes))
        self.nodes[from_node] = from_node_id

        if to_node_id is None:
            to_node_id = self.nodes.get(to_node, len(self.nodes))
        self.nodes[to_node] = to_node_id

        self.graph[from_node_id][to_node_id] = weight

    def to_undirected(self):
        '''
        Transfer directed network to undirected one.
        '''
        for out_node in self.graph.keys():
            for in_node in self.graph[out_node].keys():
                self.graph[in_node][out_node] = self.graph[out_node][in_node]

        # remove duplication and loops
        for out_node in self.graph.keys():
            if out_node in self.graph[out_node]:
                self.graph[out_node].pop(out_node)

    def process(self):
        if not self.is_directed:
            self.to_undirected()


if __name__ == '__main__':
    from data_reader import DataReader
    from sampler.random_walk import RandomWalk

    data = DataReader.load_matfile('../data/blogcatalog.mat')
    network = Network(is_directed=False)
    network.add_data(data)
    network.process()

    random_walk = RandomWalk(num_paths=5, path_length=5, alpha=0.0)
    walks = list(random_walk.generate(network))
    for walk in walks:
        path = [str(i) for i in walk]
        print ' - '.join(path)
