#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/25 10:18
@Description:
@Reference: https://github.com/csiesheep/hin2vec/blob/master/ds/network.py

"""
from collections import defaultdict
from network import Network


class HeterogeneousInformationNetwork(object):
    '''
    Heterogeneous information network.
    '''
    def __init__(self, is_directed=True):
        '''
        Initialization
        --------------------------------------------------

        '''
        self.is_directed = is_directed

        # Nodes
        self.nodes = defaultdict()    # {node: node_id, ....}
        self.class_nodes = defaultdict(set)        # {node_class: set([node_id, ...]), ....}

        # Edges
        self.edges = defaultdict()          # {edge: edge_id, ....}
        self.class_edges = defaultdict(set)        # {edge_class: set(edge_id, ....), ....}

        # Graph
        self.graph = dict()          # {from_id: {edge_class: {to_id: weight, ...}, ... }, ... }


    def __eq__(self, other):
        '''
        Decide whether self is equal to other.
        ---------------------------------------------------
        Parameters:
            other: HeteregeneousInformationNetwork class
        Returns:
            flag: True or False
        '''
        pass

    def add_edge(self, from_node, from_class, to_node, to_class, weight=1):
        '''
        Add edges.
        -------------------------------------------------------
        Parameters:
            from_node:
            from_class:
            to_node:
            to_class:
            weight:
        Returns:

        '''
        # Add node
        from_node_id = self.nodes.get(from_node, len(self.nodes))
        self.nodes[from_node] = from_node_id
        self.class_nodes[from_class].add(from_node_id)

        to_node_id = self.nodes.get(to_node, len(self.nodes))
        self.nodes[to_node] = to_node_id
        self.class_nodes[to_class].add(to_node_id)

        # Add edge class
        self.edges[(from_node_id, to_node_id)] = self.edges.get((from_node_id, to_node_id), len(self.edges))
        class_edge = "{}-{}".format(from_class, to_class)
        self.class_edges[class_edge].add(self.edges[(from_node_id, to_node_id)])

        # Add graph
        self.graph.setdefault(from_node_id, dict())
        self.graph[from_node_id].setdefault(class_edge, dict())
        self.graph[from_node_id][class_edge].setdefault(to_node_id, dict())
        self.graph[from_node_id][class_edge][to_node_id] = weight

    def to_undirected_network(self):
        '''
        Transerfer directed network to undirected one.
        ---------------------------------------------------------------
        '''
        nodeid_class = {node_id: class_node for class_node, node_id in self.class_nodes.items()}
        for from_node_id, to_node_id in self.edges.keys():
            self.edges[(to_node_id, from_node_id)] = self.edges[(from_node_id, to_node_id)]
            class_edge = "{}-{}".format(nodeid_class[from_node_id], nodeid_class[to_node_id])
            t_class_edge = "{}-{}".format(nodeid_class[to_node_id], nodeid_class[from_node_id])
            self.class_edges[t_class_edge].add(self.edges[(to_node_id, from_node_id)])
            self.graph[to_node_id][t_class_edge].setdefault(from_node_id, defaultdict(0))
            self.graph[to_node_id][t_class_edge][from_node_id] = self.graph[from_node_id][class_edge][to_node_id]

    def add_data(self, data, from_class, to_class):
        assert (len(data) > 0)
        if isinstance(data, list):
            assert (len(data[0]) > 1)
            if len(data[0]) == 2:
                for i, j in data:
                    self.add_edge(from_node=i, from_class=from_class, to_node=j, to_class=to_class)
            else:
                for i, j, w in data:
                    self.add_edge(from_node=i, from_class=from_class, to_node=j, to_class=to_class, weight=w)
        elif isinstance(data, dict):
            for i in data:
                for j, w in data[i].iteritems():
                    self.add_edge(from_node=i, from_class=from_class, to_node=j, to_class=to_class, weight=w)

    def process(self):
        if self.is_directed:
            self.to_undirected_network()

    def to_homogeneous_network(self):
        '''
        Transfer graph into homogeneous network.
        -------------------------------------------------------------
        '''
        network = Network()

        id_nodes = {index:node for node, index in self.nodes.items()}
        for from_node_id in self.graph:
            for class_edge in self.graph[from_node_id]:
                for to_node_id in self.graph[from_node_id][class_edge]:
                    network.add_edge(from_node=id_nodes[from_node_id], from_node_id=from_node_id,
                                     to_node=id_nodes[to_node_id], to_node_id=to_node_id,
                                     weight=self.graph[from_node_id][class_edge][to_node_id])
        return network


if __name__ == '__main__':
    from movie_reader import MovieReader
    reader = MovieReader()
    reader.load_data()

    hin = HeterogeneousInformationNetwork()
    hin.add_data(reader.movie_actors, from_class='M', to_class='A')
    hin.add_data(reader.movie_directors, from_class='M', to_class='D')
    hin.add_data(reader.movie_genres, from_class='M', to_class='G')
    hin.add_data(reader.ratings, from_class='U', to_class='M')

    from sampler.random_walk import RandomWalk
    network = hin.to_homogeneous_network()
    network.to_undirected()
    random_walk = RandomWalk(num_paths=5, path_length=5, alpha=0.0)
    walks = list(random_walk.generate(network))
    for walk in walks:
        path = [str(i) for i in walk]
        print ' - '.join(path)