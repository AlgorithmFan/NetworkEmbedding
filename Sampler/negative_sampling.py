#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:22
@Description: 
"""
import random


class NegativeSampling:
    def __init__(self):
        pass

    def generate(self, graph, path_length, alpha, start=None):
        '''
        Generate random walks path.
        -------------------------------------------------
        Parameters:
            graph:
            path_length: the length of walks.
                type: int
            alpha: threshold
                type: double
            start: the start node of random walk path.
                type: graph[i].
        Returns:
            path: random walk path.
                type: list
        '''
        if start:
           path = [start]
        else:
            path = [random.choice(list(graph.keys()))]

        while len(path) < path_length:
            cur = path[-1]
            if len(graph[cur]) > 0:
                if random.random() >= alpha:
                    path.append(random.choice(graph[cur]))
                else:
                    path.append(path[0])
            else:
                break
        return [str(p) for p in path]
