#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:04
@Description: 
"""
from multiprocessing import cpu_count
import psutil
import os


class NetworkEmbedding(object):
    def __init__(self, graph, random_walk, is_directed=True):
        '''
        Initialization
        --------------------------------------
        Parameters:
            graph: 图
                type: graph
            is_directed: 图是否为有向图
                type: bool
        '''
        self.graph = graph
        self.random_walk = random_walk
        self.is_directed = is_directed
        self.set_environment()

    def set_environment(self):
        # Set the parallel opt
        p = psutil.Process(os.getpid())
        try:
            self.workers = cpu_count()
            p.set_cpu_affinity(list(range(cpu_count())))
        except AttributeError:
            try:
                self.workers = cpu_count()
                p.cpu_affinity(list(range(cpu_count())))
            except AttributeError:
                pass

    def run(self, args):
        '''
        Training
        ----------------------------------------------
        Parameters:

        '''
        pass



if __name__ == '__main__':
    pass